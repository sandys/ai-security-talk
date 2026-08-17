from __future__ import annotations
import argparse, ast, json, platform, sys
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


def notebooks() -> list[Path]:
    return sorted(ROOT.glob("[0-9][0-9]_*/**/*.ipynb"))


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
    elif "```mermaid" not in readme.read_text(encoding="utf-8"):
        errors.append("Mermaid missing")
    return errors


def execute(path: Path) -> str | None:
    nb = nbformat.read(path, as_version=4)
    try:
        NotebookClient(
            nb,
            timeout=240,
            startup_timeout=90,
            kernel_name="python3",
            allow_errors=False,
        ).execute(cwd=str(ROOT))
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("static", "core", "full"), default="static")
    mode = parser.parse_args().mode

    failures: dict[str, list[str]] = {}
    static_validated: list[str] = []
    executed: list[str] = []
    static_only: list[str] = []
    items = notebooks()

    for path in items:
        rel = str(path.relative_to(ROOT))
        errors = static_check(path)
        if not errors:
            static_validated.append(rel)
            should_execute = mode == "full" or (mode == "core" and rel in CORE)
            if should_execute:
                err = execute(path)
                if err:
                    errors.append(err)
                else:
                    executed.append(rel)
            else:
                static_only.append(rel)
        if errors:
            failures[rel] = errors
            print("FAIL", rel)
        else:
            label = "EXECUTED" if rel in executed else "STATIC"
            print(label, rel)

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "recommended_python": "3.12",
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
    print(f"Static validated {len(static_validated)}/{len(items)}; executed {len(executed)} in {mode} mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
