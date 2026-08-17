# Quickstart

Everything is pinned to **Python 3.12** and an exact dependency lock. Two ways to get there; `uv` is
the recommended one because it also installs the right Python for you.

## Option A — `uv` (recommended, ~2 minutes on a normal connection)

```bash
# 1. Install uv once: https://docs.astral.sh/uv/getting-started/installation/
#    macOS/Linux:  curl -LsSf https://astral.sh/uv/install.sh | sh
#    Windows:      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. From the toolkit root: create .venv with Python 3.12 and install the exact lock (uv.lock)
uv sync

# 3. Preflight and verify every notebook actually runs on this machine
uv run python check_environment.py
uv run python verify_notebooks.py --mode full

# 4. Launch JupyterLab (the kernel "Python 3 (ipykernel)" is the project venv)
uv run jupyter lab
```

`.python-version` pins `3.12`; `uv sync` downloads a managed CPython 3.12 if none is present.

## Option B — plain `pip` with the exported lock

`requirements.txt` is generated from `uv.lock` (`uv export`) and carries `--hash` lines for every
wheel plus the extra index needed for CPU-only PyTorch. Do not edit it by hand.

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --require-hashes -r requirements.txt
python check_environment.py
python verify_notebooks.py --mode full
jupyter lab
```

## What gets installed, and why it is ~2.3 GB not ~6 GB

`garak` depends on PyTorch. The default PyPI wheel drags in ~4.5 GB of CUDA libraries that no lab
uses. `pyproject.toml` pins torch to the **CPU wheel index** on Linux/Windows (`[tool.uv.sources]`
+ `[[tool.uv.index]]`), and the exported `requirements.txt` carries the matching
`--extra-index-url https://download.pytorch.org/whl/cpu`. macOS wheels are CPU/MPS already.

The spaCy English model used by Presidio (`en_core_web_sm`, 12 MB) is a pinned wheel URL in the lock,
so there is **no `python -m spacy download` step** and no surprise network call inside a notebook.

## Offline / bad-Wi-Fi fallback

If the full install is impossible in the room, install the small core set and run only the six
notebooks that need no specialist package:

```bash
python -m pip install -r requirements-core.txt
python verify_notebooks.py --mode core
```

The core notebooks are 00, 02A, 03, 08, 09B and 10. Modules 01, 02B, 04, 05, 06, 07 and 09A stop at
their first cell with a clear `Missing dependency: …` message until the full lock is installed.

## Opening notebooks

Every notebook starts with a **bootstrap cell** that walks up from the notebook's folder to the
toolkit root, `chdir`s there and puts it on `sys.path`. JupyterLab starts each kernel *inside the
notebook's folder*, so without that cell `from demo_agent import …` would fail. Run the bootstrap
cell first (Run All does), and you can launch Jupyter from anywhere.

Regenerate a clean `_evidence/` at any time with `python verify_notebooks.py --mode full`; the folder
is git-ignored because every file in it is produced by the notebooks.

## Optional local trace UI for module 08

```bash
uv sync --extra phoenix          # or: pip install arize-phoenix arize-phoenix-otel
uv run phoenix serve             # UI on http://localhost:6006
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:6006/v1/traces
```

Module 08 works without Phoenix (in-memory exporter) and only exports over the network when that
variable is set.

## Telemetry opt-outs for the tools themselves

- **Guardrails AI** enables anonymous metrics by default. Opt out once per machine:
  `uv run guardrails configure --disable-metrics --disable-remote-inferencing`
- **garak** writes logs and reports under `~/.local/share/garak/` (the lab redirects reports to
  `_evidence/garak/` with an absolute `--report_prefix`). It does not phone home for the probes used here.
- **Inspect AI**, **ModelScan**, **Presidio**, **pytm**, **Fairlearn**: no telemetry.

No API key is required for any lab. Never put real keys in notebooks; use environment variables or a
secret manager (`.env.example` shows the shape; `.env` is git-ignored).

## Common setup problems

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: demo_agent` in a notebook | Bootstrap cell was skipped | Run the first code cell (or Run All) |
| ModelScan refuses to install | Python 3.13+ | Use Python 3.12 (`uv sync` handles it) |
| `modelscan`/`inspect` "No such file or directory" | Kernel PATH lacks the venv `bin/` | Notebooks use `workshop_utils.cli()`, which resolves the binary next to `sys.executable`; check the kernel is the project venv |
| Inspect complains about `ipywidgets` in a notebook | Package missing | It is in the lock; re-run `uv sync` |
| garak "asked for 1 got 13" / char-by-char outputs | Target function returned `str` not `list[str]` | See `vulnerable_target.py`; garak ≥ 0.16 requires a list |
| garak `--probes` deprecation warning | Old flag | Use `--spec probes.<module>.<Class>` |
| Presidio downloads a spaCy model | Wrong model name in `NlpEngineProvider` | The lab uses `en_core_web_sm`, which is in the lock |
| `dot` missing | Graphviz not installed | Optional; DOT text and a Mermaid diagram are still generated |
| Security test is flaky | Stochastic model path | Keep hard deterministic contracts separate from judge evals |
