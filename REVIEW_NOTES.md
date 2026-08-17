# Review notes — what was checked, what was broken, what changed

This revision (1.1.0) started from the previous package in this directory. The structure, agenda,
and tool choices were sound. The claim "verified" was not: 7 of 13 notebooks had only ever run in a
*fallback* mode where the specialist-tool cells were skipped, and several defects were invisible
because of that. Everything below was found by actually installing the pinned tools in a Python
3.12 environment and executing every notebook the way JupyterLab does.

## Defects found and fixed

| # | Severity | Where | Problem | Fix |
|---|---|---|---|---|
| 1 | **Blocker** | every notebook | Notebooks assumed the kernel's cwd is the repo root. JupyterLab starts kernels in the *notebook's folder*, so `from demo_agent import …` failed for anyone opening a notebook normally. The verifier ran with `cwd=ROOT` and hid it. | Bootstrap cell at the top of every notebook (finds root, `chdir`, `sys.path`); verifier now executes each notebook from its own folder. |
| 2 | **Blocker** | `02B_garak_scan` | garak ≥ 0.16 `function` targets must return `list[str]`; the target returned `str`, so garak iterated over the *characters* of each response ("asked for 1 got 13") and every detector result was garbage. The cell printed the exit code but never asserted anything, so this passed. | Targets return one-element lists; scan asserts exit code and ASR; a second (constrained) target is scanned for comparison. |
| 3 | High | `02B_garak_scan` | `--probes` is deprecated (0.15+); `--report_prefix` was relative and would have landed in `~/.local/share/garak/garak_runs/_evidence/...` (crash: directory does not exist). | `--spec probes.promptinject.HijackHateHumans`; absolute `--report_prefix` under `_evidence/garak/`; reports parsed with pandas. |
| 4 | High | `06_inspect_security_eval`, `07_modelscan` | Shelled out to bare `inspect` / `modelscan` binaries — fails whenever the kernel's PATH lacks the venv `bin/` (VS Code, IDE-launched kernels, `python -m jupyter`). | `workshop_utils.cli()` resolves console scripts next to `sys.executable`; Inspect is also run in-process via `inspect_ai.eval()`. |
| 5 | High | `06/security_eval.py` | `inspect eval` from the CLI could not import `demo_agent` (console scripts do not put cwd on `sys.path`). Latent because the CLI path never ran. | Task file inserts the toolkit root on `sys.path`; root `conftest.py` does the same for bare `pytest`. |
| 6 | Medium | `06_inspect_security_eval` | Inspect's `eval()` inside Jupyter requires `ipywidgets`, which was not a dependency. | Added to the lock. |
| 7 | Medium | environment | garak pulls CUDA PyTorch: the venv was **6.1 GB** (≈4.5 GB of `nvidia-*`, `torch`, `triton`) — hostile to conference Wi-Fi. | `[tool.uv.sources]` pins torch to the CPU wheel index on Linux/Windows; exported `requirements.txt` carries `--extra-index-url`. Venv is now **2.3 GB**. |
| 8 | Medium | `05_presidio_redaction` | Avoided `AnalyzerEngine` entirely to dodge a spaCy download, so the lab never showed Presidio's actual API, never detected the person name, and could not demonstrate false positives / recall gaps. | `en_core_web_sm` pinned as a wheel URL in the lock; lab uses `NlpEngineProvider` + `RecognizerRegistry` + `AnalyzerEngine`, shows the `UK_NHS` false positive and the `.test`-TLD e-mail false negative, measures recall (67 % → 100 %) after adding recognizers, and uses per-entity `OperatorConfig`s. |
| 9 | Medium | `01_pytm_threat_model` | Only shelled out to the model script; pytm's LLM-specific threats never fired because the `LLM`/`Agent` attributes were left at defaults. | Model declares `hasRAG`, `hasAgentCapabilities`, `hasAccessToSensitiveSystems`, `processesPersonalData`, `usesExternalTools`; notebook calls `tm.resolve()` in-process, shows `LLM01/02/03/05/07/08/09`, flips `implementsPOLP` etc. and shows `LLM05/09/01/02/07` disappearing; DFD emitted as DOT and Mermaid; JSON export via CLI. |
| 10 | Medium | `04_guardrails_pydantic` | Guardrails section only parsed one valid string. | Custom `@register_validator` attached via `json_schema_extra`, `EXCEPTION` vs `FIX`, and a structurally-valid-but-secret-bearing candidate that only the content validator catches. |
| 11 | Medium | `07_modelscan` | No assertions on scan results; JSON report not used. | Asserts exit codes (0 / 1), `CRITICAL` operator `system`, Python-API issue counts; admission-policy table. |
| 12 | Low | `08_otel_incident_trace` | Only traced the secure agent, so the "incident packet" was always empty; hand-rolled exporter. | Traces vulnerable **and** constrained agents with the SDK `InMemorySpanExporter`; incident detection from span attributes/events; asserts affected implementations == `["vulnerable"]`; optional OTLP export gated by env var. |
| 13 | Low | `09A_fairlearn` | Hand-rolled metric functions with a pandas fallback path. | Fairlearn built-ins (`count`, `selection_rate`, FPR, FNR, `demographic_parity_difference`, `equalized_odds_difference`); no fallback branch. |
| 14 | Low | `02A_attack_harness` | "Mutations" were labelled by line number and never executed against the agents. | Six named mutations, run against both agents, included in the gate. |
| 15 | Low | `demo_agent.py`, `workshop_utils.py` | Minified one-line style (semicolons, 1-space indents) in files attendees are told to read. | Reformatted with docstrings; bugs in the vulnerable agent marked `BUG 1/2/3`. |
| 16 | Low | notebooks 01/02B/04/05/06/07/09A | `if installed: … else: print("install …")` guards let `--mode full` "pass" with the tool cells skipped. | `require_package()` raises with the fix; the verifier's full mode preflights all specialist packages and exits 2 if any is missing. |
| 17 | Low | repo hygiene | No `.gitignore`; generated `_evidence/` and a malicious pickle tracked; `.env.example` referenced but missing; stale checksum file. | `.gitignore`; `_evidence/` generated (README tracked); `.env.example`; stale checksum/report files removed. |

## Environment / packaging changes

- `pyproject.toml` is now the single source of truth (top-level pins, CPU-torch index, `package = false`).
- `uv.lock` (cross-platform) + `.python-version` (`3.12`).
- `requirements.txt` is **generated** by `uv export` with `--hash` for every wheel and the extra index; verified to resolve with `pip install --dry-run --require-hashes` in a fresh 3.12 venv.
- `requirements-core.txt` remains as the small offline fallback for the six core notebooks.
- `verify_notebooks.py`: JupyterLab cwd semantics, specialist preflight in `full` mode, per-notebook timing, `--inplace` to keep executed outputs.
- `check_environment.py`: reports interpreter prefix, every required distribution, and whether torch is the CPU build.

## What was deliberately kept

The agenda, facilitator guide, tool selection, library landscape, module READMEs and their Mermaid
diagrams, the capstone design, and the system-card template were sound and are retained with
targeted edits where a lab's behaviour changed.

## Known limitations that remain

- The "model" in every lab is a deterministic rule-based double. That is intentional (offline,
  reproducible) but a real LLM would fail the mutation and garak probes in *different* ways; the
  notebooks say so where it matters.
- garak is exercised with one fast probe family per target to fit the workshop clock; wider sweeps
  (`--spec "probes.promptinject,probes.latentinjection,tag:owasp:llm01"`) are documented, not run.
- The Phoenix export in module 08 is opt-in via environment variable and not executed by the verifier.
- Graphviz `dot` is optional; the pytm DFD is emitted as DOT text and a derived Mermaid diagram.
