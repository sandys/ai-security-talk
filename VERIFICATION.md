# Verification and Execution Status

This package separates three kinds of confidence:

1. **Static validity** — every notebook is valid JSON, every Python code cell parses, every module has a README, and every module README contains Mermaid diagrams.
2. **Offline/core execution** — notebooks that require no specialist security package execute from a clean Jupyter kernel and assert their security contracts.
3. **Specialist-tool execution** — the `pytm`, `garak`, Guardrails AI, Presidio, Inspect AI, ModelScan, and Fairlearn branches require the pinned Python 3.12 environment.

## Verification performed while packaging

| Check | Result |
|---|---|
| Notebook structure and Python syntax | **13 / 13 passed** |
| Module README present | **11 / 11 passed** |
| Mermaid diagrams in each module README | **11 / 11 passed**; two or more per module |
| Offline/core notebook execution | **6 / 6 passed** |
| Remaining notebook fallback/preflight execution | **7 / 7 passed** |
| Independent `pytest` security contract | **Passed** |
| Archive integrity | Run `unzip -t` or your platform's ZIP test after download |

The six notebooks fully executed on the packaging host were:

- `00_Start_Here/00_break_the_agent.ipynb`
- `02_Prompt_Injection_and_Red_Teaming/02A_attack_harness.ipynb`
- `03_Agent_Tool_Security/03_capability_gates.ipynb`
- `08_Observability_and_Incident_Response/08_otel_incident_trace.ipynb`
- `09_Fairness_and_Responsible_AI_Evidence/09B_model_and_system_card.ipynb`
- `10_Capstone_Secure_RAG_Agent/10_capstone.ipynb`

The other seven notebooks were executed through their dependency-aware fallback/preflight paths. Their specialist branches did **not** run on the packaging host because it used Python 3.13 and those pinned tools were intentionally not installed there. The package targets Python 3.12 because it is the shared supported runtime for the selected versions.

The machine-readable reports are:

- `verification_report.json`
- `supplemental_execution_report.json`

## Reproduce the checks

### Fast check before a session

```bash
python verify_notebooks.py --mode static
python verify_notebooks.py --mode core
python -m pytest 06_Evaluations_and_Security_Regression/test_security_contract.py -q
```

### Complete specialist-tool check

Create the Python 3.12 environment from `QUICKSTART.md`, then run:

```bash
python check_environment.py
python verify_notebooks.py --mode full
```

`--mode full` executes all 13 notebooks and fails on the first notebook whose specialist integration cannot run. This is the recommended pre-event check on the same laptops or workshop image that attendees will use.

## What the checks do not prove

Passing these labs does not certify a production AI system. The examples use synthetic records, local doubles, and deliberately small attack sets. Production teams still need system-specific threat modeling, authorization design, privacy review, representative datasets, adversarial testing, dependency scanning, incident drills, and human accountability.
