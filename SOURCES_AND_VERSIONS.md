# Sources and version snapshot

Researched on **2026-08-17**; recheck before future reuse.

## Frameworks

- OWASP LLM Top 10 for 2026: <https://genai.owasp.org/llm-top-10/>
- OWASP Top 10 for Agentic Applications 2026: <https://genai.owasp.org/agentic-applications/>
- NIST AI RMF Generative AI Profile: <https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence>
- NIST AI RMF Playbook (Govern, Map, Measure, Manage): <https://airc.nist.gov/airmf-resources/playbook/>

## Official tool docs

OWASP pytm <https://owasp.org/www-project-pytm/> · NVIDIA garak <https://reference.garak.ai/> · Guardrails AI <https://www.guardrailsai.com/docs> · Presidio <https://data-privacy-stack.github.io/presidio/> · Inspect AI <https://inspect.aisi.org.uk/> · ModelScan <https://github.com/protectai/modelscan> · OpenTelemetry Python <https://opentelemetry.io/docs/languages/python/> · Phoenix <https://arize.com/docs/phoenix> · Fairlearn <https://fairlearn.org/> · Hugging Face model cards <https://huggingface.co/docs/huggingface_hub/guides/model-cards>

| Package | Version | Release date observed |
|---|---:|---:|
| pytm | 1.4.0 | 2026-07-06 |
| garak | 0.16.0 | 2026-08-04 |
| guardrails-ai | 0.11.0 | 2026-08-14 |
| presidio analyzer/anonymizer | 2.2.364 | 2026-07-22 |
| inspect-ai | 0.3.259 | 2026-08-16 |
| modelscan | 0.8.8 | 2026-02-18 |
| fairlearn | 0.14.0 | 2026-06-07 |
| en-core-web-sm (spaCy model, Presidio NLP engine) | 3.8.0 | wheel from the spaCy models GitHub release |
| torch (transitive, via garak) | 2.13.0 (+cpu on Linux/Windows) | CPU wheel index `https://download.pytorch.org/whl/cpu` |
| ipywidgets (required by Inspect AI inside Jupyter) | 8.1.x | — |
| opentelemetry-sdk / exporter-otlp-proto-http | 1.44.0 | — |

The complete transitive set is in `uv.lock` (cross-platform) and `requirements.txt` (exported with
`--hash` lines). Regenerate with `uv lock && uv export --format requirements-txt --no-dev
--no-emit-project --emit-index-url -o requirements.txt`.

## API facts confirmed while executing the labs (worth knowing before you copy old snippets)

| Tool | Fact |
|---|---|
| garak 0.16 | `function` targets must return `list[str]`; `--probes` is deprecated in favour of `--spec`; `--report_prefix` is relative to garak's data dir unless absolute; `python -m garak` works |
| pytm 1.4 | `tm.resolve()` can be called in-process (set `sys.argv` first — `tm.process()` parses argv); `tm.dfd()` returns DOT; the `LLM` and `Agent` elements expose `hasRAG`, `hasAgentCapabilities`, `hasAccessToSensitiveSystems`, `controls.implementsPOLP`, `usesExternalTools`, `validatesToolLaunchConfig` and drive `LLM01`–`LLM09`; `Classification` has no `PII` member (use `isPII=True`) |
| Guardrails AI 0.11 | attach validators with `Field(..., json_schema_extra={"validators": [...]})` (the `validators=` kwarg triggers a Pydantic deprecation warning); custom validators via `@register_validator` + `_validate()`; `OnFailAction.EXCEPTION` raises `guardrails.errors.ValidationError`, `FIX` substitutes `fix_value`; anonymous metrics on by default (`guardrails configure --disable-metrics`) |
| Presidio 2.2.364 | `EmailRecognizer` validates TLDs (misses reserved `.test`); `UK_NHS` matches 10-digit Indian mobiles at score 1.0; `PatternRecognizer` regexes are case-insensitive; `return_decision_process=True` populates `analysis_explanation.recognizer`; `OperatorConfig("keep")` exists |
| Inspect AI 0.3.259 | `eval()` works inside Jupyter but requires `ipywidgets`; `mockllm/model` satisfies the model requirement without generating; task params map to `-T key=value`; console-script CLI does **not** put cwd on `sys.path` (task files must handle their own imports) |
| ModelScan 0.8.8 | requires Python < 3.13; `-r json -o file` writes a machine-readable report; exit codes 0/1/2/3/4; no `python -m modelscan` (use the console script or `modelscan.cli:main`) |
| Fairlearn 0.14 | `fairlearn.metrics` ships `count`, `selection_rate`, `false_positive_rate`, `false_negative_rate`, `demographic_parity_difference`, `equalized_odds_difference` |
| OpenTelemetry SDK 1.44 | `opentelemetry.sdk.trace.export.in_memory_span_exporter.InMemorySpanExporter` is the right test exporter; `add_event()` on a span for incident markers |
| JupyterLab 4.x | kernels start with cwd = the notebook's folder; every notebook here has a bootstrap cell for that reason |
