# Package Manifest

## Workshop structure

| Folder | Purpose | Notebooks | Main tools |
|---|---|---:|---|
| `00_Start_Here` | Exploit a deliberately vulnerable RAG/tool agent and define the first security contract | 1 | pandas, local Python double |
| `01_Threat_Modeling` | Express architecture, trust boundaries, and threats as code | 1 | OWASP `pytm` |
| `02_Prompt_Injection_and_Red_Teaming` | Build a repeatable attack corpus and scale probing | 2 | pandas, NVIDIA `garak` |
| `03_Agent_Tool_Security` | Put typed capabilities, policy, approvals, and idempotency between model and tool | 1 | Pydantic |
| `04_Output_Validation_and_Guardrails` | Separate parsing, invariants, policy, and repair | 1 | Pydantic, Guardrails AI |
| `05_PII_and_Data_Boundaries` | Detect and transform PII into purpose-specific views | 1 | Microsoft Presidio |
| `06_Evaluations_and_Security_Regression` | Turn red-team findings into deterministic release checks | 1 | pytest, Inspect AI |
| `07_Model_Supply_Chain` | Scan serialized artifacts before any deserialization | 1 | ModelScan |
| `08_Observability_and_Incident_Response` | Produce allow-listed, redacted traces and an incident packet | 1 | OpenTelemetry; Phoenix-compatible OTLP |
| `09_Fairness_and_Responsible_AI_Evidence` | Measure subgroup performance and publish limitations | 2 | Fairlearn, Hugging Face model cards |
| `10_Capstone_Secure_RAG_Agent` | Combine the controls into an end-to-end release gate | 1 | Pydantic, regression evidence |

**Totals:** 11 topic folders, 13 notebooks, 13 README files, and at least two Mermaid diagrams in every topic README.

## Root files

| File | Use |
|---|---|
| `README.md` | Workshop overview and recommended learning path |
| `AGENDA.md` | 4h30 default agenda, 90-minute route, and full-day extension |
| `FACILITATOR_GUIDE.md` | Guided prompts, timing cues, and debrief questions |
| `QUICKSTART.md` | Python 3.12 setup and troubleshooting |
| `TOOL_SELECTION.md` | Opinionated defaults and where each tool belongs |
| `LIBRARY_LANDSCAPE.md` | Broader Python toolkit map and alternatives |
| `ORIGINAL_ZIP_REVIEW.md` | Audit of the uploaded starter ZIP and what was changed |
| `SOURCES_AND_VERSIONS.md` | Official references and pinned versions |
| `VERIFICATION.md` | Exact validation scope, results, and limitations |
| `requirements.txt` | Complete pinned workshop environment |
| `requirements-core.txt` | Conference-Wi-Fi-safe fallback environment |
| `pyproject.toml` | Python runtime constraint and project metadata |
| `check_environment.py` | Dependency and runtime preflight |
| `verify_notebooks.py` | Static, core, and full notebook verifier |
| `demo_agent.py` | Shared deliberately vulnerable and constrained local agent components |
| `workshop_utils.py` | Shared evidence, redaction, and notebook helpers |
| `.env.example` | Safe environment-variable template; contains no credentials |
| `verification_report.json` | Machine-readable core verification result |
| `supplemental_execution_report.json` | Machine-readable fallback/preflight execution result |
| `SHA256SUMS.txt` | Checksums for package files, excluding the checksum file itself |

## Evidence and intentionally unsafe samples

`_evidence/` contains synthetic example outputs generated while validating the labs. It also contains `model_artifacts/suspicious_model.pkl`, an intentionally suspicious serialized artifact used only to demonstrate **scan-before-load** behavior. Do not deserialize it. The ModelScan lab invokes a scanner in a subprocess and never imports or opens the artifact with `pickle.load`.
