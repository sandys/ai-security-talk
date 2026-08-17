#!/usr/bin/env python3
"""Preflight: is this interpreter the pinned workshop environment?

Run it with the interpreter you will use for Jupyter::

    uv run python check_environment.py        # uv-managed environment
    python check_environment.py               # activated venv

Exit code 0 = ready.  1 = something is missing (the fix is printed).
"""
from __future__ import annotations

import importlib.metadata
import importlib.util
import platform
import shutil
import sys

REQUIRED = {  # distribution -> importable module
    "jupyterlab": "jupyterlab",
    "ipykernel": "ipykernel",
    "ipywidgets": "ipywidgets",
    "nbclient": "nbclient",
    "pandas": "pandas",
    "pydantic": "pydantic",
    "pytest": "pytest",
    "opentelemetry-sdk": "opentelemetry.sdk",
    "opentelemetry-exporter-otlp-proto-http": "opentelemetry.exporter.otlp.proto.http",
    "huggingface-hub": "huggingface_hub",
    "pytm": "pytm",
    "garak": "garak",
    "guardrails-ai": "guardrails",
    "presidio-analyzer": "presidio_analyzer",
    "presidio-anonymizer": "presidio_anonymizer",
    "en-core-web-sm": "en_core_web_sm",
    "inspect-ai": "inspect_ai",
    "modelscan": "modelscan",
    "fairlearn": "fairlearn",
}

print(f"Python  {sys.version.split()[0]}  ({platform.platform()})")
print(f"Prefix  {sys.prefix}")
if sys.version_info[:2] != (3, 12):
    print("WARNING: Python 3.12 is the pinned runtime (ModelScan rejects 3.13+; garak wheels target <=3.12).")

missing: list[str] = []
for dist, module in REQUIRED.items():
    found = importlib.util.find_spec(module) is not None
    try:
        version = importlib.metadata.version(dist) if found else "missing"
    except importlib.metadata.PackageNotFoundError:
        version = "present (version unknown)" if found else "missing"
    print(f"  {dist:40} {version}")
    if not found:
        missing.append(dist)

try:
    import torch  # noqa: WPS433 - optional diagnostic

    flavour = "cpu-only" if "+cpu" in torch.__version__ or not torch.cuda.is_available() else "cuda"
    print(f"  {'torch (via garak)':40} {torch.__version__} [{flavour}]")
except Exception:  # noqa: BLE001
    print(f"  {'torch (via garak)':40} not importable")

print(f"  {'graphviz dot (optional)':40} {shutil.which('dot') or 'missing - DOT text still generated'}")

if missing:
    print("\nMissing:", ", ".join(missing))
    print("Fix:     uv sync            (recommended)")
    print("   or:   python -m pip install -r requirements.txt")
    raise SystemExit(1)
print("\nEnvironment ready. Next: python verify_notebooks.py --mode full")
