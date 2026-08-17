#!/usr/bin/env python3
"""Verify the workshop notebooks.

Modes
-----
static  : every notebook is valid JSON, every code cell parses, every module has a
          README with Mermaid diagrams.
core    : static + execute the notebooks that need no specialist package.
full    : static + preflight the specialist packages + execute **all** notebooks.

Each notebook is executed with the working directory set to *its own folder* —
exactly what JupyterLab does — so the bootstrap cell that locates the toolkit
root is exercised, not bypassed.

Usage::

    python verify_notebooks.py --mode full            # before a session
    python verify_notebooks.py --mode core            # offline fallback
    python verify_notebooks.py --mode full --inplace  # also save executed outputs

Exit code 0 means every check passed; details are in verification_report.json.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent

CORE = {
    "00_Start_Here/00_break_the_agent.ipynb",
    "02_Prompt_Injection_and_Red_Teaming/02A_attack_harness.ipynb",
    "03_Agent_Tool_Security/03_capability_gates.ipynb",
    "08_Observability_and_Incident_Response/08_otel_incident_trace.ipynb",
    "09_Fairness_and_Responsible_AI_Evidence/09B_model_and_system_card.ipynb",
    "10_Capstone_Secure_RAG_Agent/10_capstone.ipynb",
}

# distribution name -> importable module, required for --mode full
SPECIALIST = {
    "pytm": "pytm",
    "garak": "garak",
    "guardrails-ai": "guardrails",
    "presidio-analyzer": "presidio_analyzer",
    "presidio-anonymizer": "presidio_anonymizer",
    "en-core-web-sm": "en_core_web_sm",
    "inspect-ai": "inspect_ai",
    "ipywidgets": "ipywidgets",
    "modelscan": "modelscan",
    "fairlearn": "fairlearn",
}


def notebooks() -> list[Path]:
    return sorted(p for p in ROOT.glob("[0-9][0-9]_*/**/*.ipynb") if ".ipynb_checkpoints" not in p.parts)


def static_check(path: Path) -> list[str]:
    errors: list[str] = []
    nb = nbformat.read(path, as_version=4)
    if not nb.cells:
        errors.append("no cells")
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            try:
                ast.parse(cell.source)
            except SyntaxError as exc:
                errors.append(f"cell {i}: {exc}")
    readme = path.parent / "README.md"
    if not readme.exists():
        errors.append("README missing")
    elif readme.read_text(encoding="utf-8").count("```mermaid") < 2:
        errors.append("fewer than two Mermaid diagrams in README")
    return errors


def execute(path: Path, inplace: bool, timeout: int) -> tuple[str | None, float]:
    nb = nbformat.read(path, as_version=4)
    started = time.time()
    try:
        NotebookClient(
            nb,
            timeout=timeout,
            startup_timeout=120,
            kernel_name="python3",
            allow_errors=False,
        ).execute(cwd=str(path.parent))  # <- JupyterLab semantics
    except Exception as exc:  # noqa: BLE001 - we want the message, whatever it is
        message = str(exc)
        return message[-4000:], time.time() - started
    if inplace:
        nbformat.write(nb, path)
    return None, time.time() - started


def preflight() -> list[str]:
    missing = [dist for dist, module in SPECIALIST.items() if importlib.util.find_spec(module) is None]
    if sys.version_info[:2] != (3, 12):
        print(f"WARNING: Python {sys.version.split()[0]} detected; the pinned environment targets 3.12.")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mode", choices=("static", "core", "full"), default="static")
    parser.add_argument("--inplace", action="store_true", help="write executed outputs back into the notebooks")
    parser.add_argument("--timeout", type=int, default=600, help="per-cell timeout in seconds")
    args = parser.parse_args()

    if args.mode == "full":
        missing = preflight()
        if missing:
            print("FAIL preflight: missing specialist packages:", ", ".join(missing))
            print("     run `uv sync` (or `python -m pip install -r requirements.txt`) in a Python 3.12 environment")
            return 2

    failures: dict[str, list[str]] = {}
    static_validated: list[str] = []
    executed: dict[str, float] = {}
    static_only: list[str] = []
    items = notebooks()

    for path in items:
        rel = str(path.relative_to(ROOT))
        errors = static_check(path)
        if not errors:
            static_validated.append(rel)
            should_execute = args.mode == "full" or (args.mode == "core" and rel in CORE)
            if should_execute:
                err, elapsed = execute(path, args.inplace, args.timeout)
                if err:
                    errors.append(err)
                else:
                    executed[rel] = round(elapsed, 1)
            else:
                static_only.append(rel)
        if errors:
            failures[rel] = errors
            print("FAIL     ", rel)
        elif rel in executed:
            print(f"EXECUTED  {rel}  ({executed[rel]}s)")
        else:
            print("STATIC   ", rel)

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "recommended_python": "3.12",
            "cwd_semantics": "each notebook executed from its own directory (JupyterLab default)",
        },
        "notebooks_total": len(items),
        "static_validated_count": len(static_validated),
        "executed_count": len(executed),
        "executed_notebooks": executed,
        "static_only_notebooks": static_only,
        "failures": failures,
        "passed": not failures,
    }
    (ROOT / "verification_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    if failures:
        print(json.dumps(failures, indent=2), file=sys.stderr)
        return 1
    print(f"Static validated {len(static_validated)}/{len(items)}; executed {len(executed)} in {args.mode} mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
