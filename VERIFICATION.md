# Verification and execution status

This package separates three kinds of confidence:

1. **Static validity** — every notebook is valid JSON, every code cell parses, every module has a
   README with at least two Mermaid diagrams.
2. **Core execution** — the six notebooks that need no specialist package execute from a clean
   Jupyter kernel and their security assertions pass.
3. **Specialist-tool execution** — the `pytm`, `garak`, Guardrails AI, Presidio, Inspect AI, ModelScan
   and Fairlearn labs execute **for real** (no fallback branches, no silent skips) in the pinned
   Python 3.12 environment.

## Result of the last full run

| Check | Result |
|---|---|
| Notebook structure and Python syntax | **13 / 13 passed** |
| Module README present with ≥ 2 Mermaid diagrams | **11 / 11 passed** |
| Notebook execution, `--mode full`, cwd = each notebook's own folder | **13 / 13 executed** (≈ 35 s total) |
| Independent `pytest` security contract (`pytest -q` from any cwd) | **passed** |
| `inspect eval … -T agent=secure` / `-T agent=vulnerable` from the CLI | **passed** (1.0 / 0.0 accuracy) |
| garak function target contract (`list[str]`) and `--spec` selection | **passed** (vulnerable 100 % ASR, constrained 0 %) |
| ModelScan exit codes and JSON report | **passed** (0 for benign, 1 + `CRITICAL` for suspicious) |
| `pip install --dry-run --require-hashes -r requirements.txt` in a fresh 3.12 venv | **resolves** |

Environment: CPython 3.12.13 (uv-managed), Linux x86_64, `uv sync` from `uv.lock`, torch 2.13.0+cpu.
The machine-readable report is `verification_report.json` (regenerated on every run).

### Notebook-by-notebook (typical wall-clock)

| Notebook | Specialist tool exercised | Time |
|---|---|---:|
| `00_Start_Here/00_break_the_agent.ipynb` | — | 1 s |
| `01_Threat_Modeling/01_pytm_threat_model.ipynb` | pytm `resolve()`, `dfd()`, `--json` CLI | 1 s |
| `02_…/02A_attack_harness.ipynb` | — | 1 s |
| `02_…/02B_garak_scan.ipynb` | garak `--list_probes`, two function-target scans, report parsing | 4 s |
| `03_Agent_Tool_Security/03_capability_gates.ipynb` | Pydantic | 1 s |
| `04_…/04_guardrails_pydantic.ipynb` | Guardrails `Guard.for_pydantic`, custom validator, EXCEPTION/FIX | 4 s |
| `05_…/05_presidio_redaction.ipynb` | Presidio `AnalyzerEngine` (spaCy) + `AnonymizerEngine` | 5 s |
| `06_…/06_inspect_security_eval.ipynb` | pytest, Inspect `eval()` in-process + CLI, `read_eval_log` | 7 s |
| `07_Model_Supply_Chain/07_modelscan.ipynb` | ModelScan CLI (`-r json`) + Python API | 1 s |
| `08_…/08_otel_incident_trace.ipynb` | OpenTelemetry SDK `InMemorySpanExporter` | 1 s |
| `09_…/09A_fairlearn.ipynb` | Fairlearn `MetricFrame`, group metrics, parity metrics | 3 s |
| `09_…/09B_model_and_system_card.ipynb` | `huggingface_hub.ModelCard` | 1 s |
| `10_Capstone_Secure_RAG_Agent/10_capstone.ipynb` | Pydantic | 1 s |

## What "executed from its own folder" means and why it matters

JupyterLab starts a kernel with the working directory set to the **notebook's** folder, not the
repository root. The previous verifier ran every notebook with `cwd=ROOT`, which hid the fact that
`from demo_agent import …` failed for anyone who simply opened a notebook. Every notebook now starts
with a bootstrap cell that locates the root, and `verify_notebooks.py` executes with
`cwd=<notebook folder>` so that cell is exercised rather than bypassed.

## Reproduce the checks

```bash
uv sync                                          # or the pip route in QUICKSTART.md
uv run python check_environment.py               # preflight (fails if a specialist package is missing)
uv run python verify_notebooks.py --mode full    # executes all 13 notebooks
uv run pytest -q                                 # the module-06 contract, from any cwd
```

`--mode full` refuses to start if any specialist package is missing (exit code 2), so a "pass" can
never mean "the tool cells were skipped".

Add `--inplace` to write executed outputs back into the notebooks if you want to publish rendered
versions.

## What the checks do not prove

Passing these labs does not certify a production AI system. The examples use synthetic records, local
doubles, and deliberately small attack sets. Production teams still need system-specific threat
modeling, authorization design, privacy review, representative datasets, adversarial testing,
dependency scanning, incident drills, and human accountability.
