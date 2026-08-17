from __future__ import annotations
import importlib.metadata, importlib.util, platform, shutil, sys
REQUIRED={
 "pytm":"pytm", "garak":"garak", "guardrails-ai":"guardrails",
 "presidio-analyzer":"presidio_analyzer", "presidio-anonymizer":"presidio_anonymizer",
 "inspect-ai":"inspect_ai", "modelscan":"modelscan", "fairlearn":"fairlearn",
 "opentelemetry-sdk":"opentelemetry.sdk"}
print(f"Python: {sys.version.split()[0]} ({platform.platform()})")
if sys.version_info[:2] != (3,12): print("WARNING: Python 3.12 recommended; ModelScan rejects 3.13+.")
missing=[]
for dist,module in REQUIRED.items():
 found=importlib.util.find_spec(module) is not None
 try: version=importlib.metadata.version(dist) if found else "missing"
 except importlib.metadata.PackageNotFoundError: version="present, unknown" if found else "missing"
 print(f"{dist:24} {version}")
 if not found: missing.append(dist)
print(f"{'graphviz dot':24} {shutil.which('dot') or 'missing (optional)'}")
if missing:
 print("\nInstall: python -m pip install -r requirements.txt"); raise SystemExit(1)
print("\nEnvironment ready.")
