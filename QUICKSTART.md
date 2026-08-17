# Quickstart

## Use Python 3.12

Python 3.12 is the common denominator. Garak 0.16 publishes classifiers through 3.12; ModelScan 0.8.8 requires Python below 3.13.

### macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python verify_notebooks.py --mode full
jupyter lab
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python verify_notebooks.py --mode full
jupyter lab
```

### Core-only fallback

Useful when conference Wi-Fi fails, but not a substitute for the specialist labs:

```bash
python -m pip install -r requirements-core.txt
python verify_notebooks.py --mode core
```

## Preflight

```bash
python check_environment.py
python verify_notebooks.py --mode full
```

Optional local observability UI:

```bash
python -m pip install arize-phoenix
phoenix serve
```

The module 08 notebook remains useful without Phoenix because it uses an in-memory OpenTelemetry exporter.

## Common setup problems

| Symptom | Cause | Fix |
|---|---|---|
| ModelScan refuses to install | Python 3.13+ | Recreate environment with Python 3.12 |
| Garak differs from an old blog | 0.16 introduced unified selection grammar | Use module 02 commands and local `garak --help` |
| Presidio downloads a spaCy model | Full `AnalyzerEngine` defaults to NLP | The lab uses explicit local `PatternRecognizer`s |
| `dot` missing | Graphviz system package absent | Install Graphviz or inspect generated DOT text |
| Wrong helper imported | Jupyter launched outside toolkit tree | Relaunch from root and rerun first cell |
| Security test is flaky | Stochastic model path | Keep hard deterministic contracts separate from judge evals |

No API key is required for the default path. Never put real keys in notebooks; use environment variables or a secret manager.
