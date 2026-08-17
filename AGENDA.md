# Hands-on-first agenda

The workshop uses slides only for transitions. Every block follows the same rhythm: **predict → exploit → identify the missing boundary → implement or inspect one control → replay → save evidence**.

## Recommended half-day: 4 hours 30 minutes

| Clock | Lab | What developers do | Facilitator guidance | Evidence produced |
|---:|---|---|---|---|
| 0:00–0:15 | 00 Break the agent | Leak a canary and trigger an unsafe refund | Do not explain frameworks yet. Ask teams to predict the failure first. | Baseline attack-success rate |
| 0:15–0:35 | 01 Threat model | Mark trust boundaries and three unacceptable outcomes | Keep discussion anchored to actual data flows and side effects. | `pytm` model + owned backlog |
| 0:35–1:05 | 02 Red team | Extend an attack corpus and its mutations; run the local harness; scan the vulnerable and constrained targets with `garak` and read the reports | Make teams distinguish direct injection, indirect injection, and authorization failure. Point out that the rule-based double resists mutations for the *wrong* reason. | Per-category ASR + two garak reports |
| 1:05–1:30 | 03 Tool security | Feed valid-looking but unauthorized proposals through a capability gate | Ask: “Which check still works if the model is fully compromised?” | Policy decisions + replay rejection |
| 1:30–1:40 | Break | Leave the failed exploit and fixed trace visible | — | — |
| 1:40–2:00 | 04 Output validation | Break JSON/schema/invariants; show valid-but-forbidden output | Stress that validation is not authorization. | Validation report |
| 2:00–2:20 | 05 Privacy | Detect PII and build separate model/log/correlation views | Ask which destination actually needs each field. | Pre-egress transformation evidence |
| 2:20–2:45 | 06 Security regression | Turn a finding into pytest and Inspect checks | Use exact oracles for leaks and side effects; reserve model judges for nuance. | CI-ready gate policy |
| 2:45–3:00 | 07 Supply chain | Create and scan a suspicious pickle without loading it | Repeat: quarantine and scan come before import/deserialization. | Digest + admission decision |
| 3:00–3:20 | 08 Observability | Trace retrieval, policy, and outcome without raw secrets | Ask what an on-call engineer needs 30 days later—and what they should not see. | Redacted trace + incident packet |
| 3:20–3:45 | 09 Responsible-AI evidence | Compare aggregate and subgroup errors; generate a system card | Do not let one ratio become an ethical or legal verdict. Require limitations and owners. | Fairness assessment + system card |
| 3:45–4:20 | 10 Capstone | In teams, add one attack, one benign edge case, and one hard gate | Deliberately weaken one boundary and confirm the release changes to BLOCK. | End-to-end `release_evidence.json` |
| 4:20–4:30 | Report-out | Each team states one control, one proof, and one residual risk | Close on evidence and ownership, not “AI safety” slogans. | Team release decision |

## 90-minute developer talk/workshop

Use this when the room expects a talk but you still want real keyboard time.

| Time | Activity |
|---:|---|
| 0:00–0:10 | Module 00: exploit and baseline |
| 0:10–0:20 | Module 01: mark trust boundaries on the supplied architecture |
| 0:20–0:35 | Module 02A: replay direct, indirect, and excessive-agency attacks |
| 0:35–0:50 | Module 03: typed proposal, policy, approval, one-time capability |
| 0:50–1:02 | Module 05: PII before model and telemetry egress |
| 1:02–1:15 | Module 06: convert the exploit into a build-breaking test |
| 1:15–1:28 | Module 10: run the integrated release gate, then break one boundary |
| 1:28–1:30 | Close: control, evidence, residual risk |

Demonstrate—not run—modules 04, 07, 08, and 09. Give the repository as the follow-up lab.

## Full-day extension

Run the half-day route in the morning. After lunch, split into four teams:

1. **Prompt/retrieval:** add multilingual, encoded, multi-turn, and document-borne attacks.
2. **Identity/tools:** add a real sandboxed application adapter, approval binding, rate limits, and replay tests.
3. **Privacy/operations:** add domain recognizers, retention decisions, redacted OTLP export, and an incident tabletop.
4. **Evaluation/governance:** add utility and subgroup datasets, thresholds, change triggers, and a reviewed system card.

Each team contributes one confirmed failure, one control, one executable verification, and one residual risk to the capstone before the final release review.
