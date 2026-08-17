---
language:
- en
library_name: responsible-ai-workshop
license: apache-2.0
tags:
- rag
- agent
- security-evaluation
- system-card
card_type: ai-system-card
status: workshop-example
---

# System Card: Constrained Support RAG Agent v1.0

## Decision summary

**Workshop release decision:** PASS for the included synthetic corpus.  
**Owner:** Agent platform lead.  
**Expiry:** Re-evaluate after any model, prompt, retriever, knowledge source, tool, policy, or data-use change.

## Intended use and affected users

The system answers synthetic customer-support return questions and drafts refund decisions. It is intended to assist a human-supported workflow. Users and customers are affected by answer quality, privacy, refusal behavior, and refund handling.

## Out-of-scope and prohibited use

Not approved for autonomous payments, legal/medical/credit decisions, unrestricted web or shell access, real customer data, cross-tenant retrieval, or use without the application-side policy and approval controls.

## System architecture and boundaries

- Deterministic workshop agent; no external model call in the default path.
- Mixed-trust retrieval corpus with source trust labels.
- Pydantic-style typed action proposals.
- Server-side policy: high-value refund requires human approval.
- No model-generated command reaches an executor directly.
- Redacted, decision-oriented traces; raw prompts are not default span attributes.

## Data and privacy

All bundled examples use synthetic data. Email, Indian mobile numbers, internal customer IDs, and canaries are transformed before model/log destinations. General evidence contains hashes and redacted views, not raw direct identifiers. Production use would require purpose, processor, residency, retention, deletion, access, and data-subject workflow decisions.

## Security controls

- Threat model as code and explicit trust boundaries.
- Direct secret-request denial; retrieved instructions treated as untrusted data.
- Typed action allow-list, tenant checks, amount threshold, approval binding, one-time capability, replay protection.
- Deterministic prompt-injection and excessive-agency regression corpus.
- Model artifacts quarantined and scanned before loading.
- Kill switches: disable tool, force approval, revoke capability/credential, disable source, read-only mode.

## Evaluation evidence

- Constrained attack-success rate on bundled corpus: **0.0**.
- Hard gates: zero canary leaks, zero unauthorized side effects, benign return answer includes the documented 30-day policy.
- Telemetry incident detected in the bundled secure run: **False**.
- Evidence is synthetic and small; it does not establish general robustness.

## Fairness and accessibility

A separate synthetic assessment demonstrates how aggregate accuracy can hide higher false-negative rates for one interaction language. Production assessment must identify domain-specific harms, relevant groups/intersections, sample sizes, uncertainty, accessibility needs, and mitigation trade-offs.

## Human oversight and appeals

High-value refunds require an identified human approver bound to the exact proposal. A production UI must show source, amount, reason, uncertainty, and proposed action; support rejection, correction, and customer escalation; and never dark-pattern approval.

## Monitoring and incident response

Monitor canary leakage, foreign-tenant source IDs, unexpected tools, policy bypass, approval mismatch, replay, false-refusal/utility drift, subgroup error drift, and trace/export failures. Preserve redacted traces and restricted evidence references. Convert confirmed incidents into stable evaluation IDs before re-enable.

## Known limitations and residual risks

- Rule-based workshop target is not representative of open-ended model behavior.
- Included attacks are not exhaustive and multilingual/encoded/multi-turn coverage is limited.
- Pattern PII recognition can miss context-specific or malformed identifiers and over-redact useful text.
- Source trust labels, tenant metadata, identity, and approvals must themselves be protected from tampering.
- A clean static artifact scan or red-team run cannot prove absence of vulnerabilities.

## Change management

Re-run threat modeling, privacy review, security/utility evals, subgroup assessment, supply-chain scan, and incident tabletop for material changes. Deploy by immutable version/digest and retain a tested rollback path.

## Evidence owners and approval

- Product outcome owner: **TBD in production**
- Engineering/control owner: **TBD in production**
- Security review: **TBD in production**
- Privacy/legal/compliance review where applicable: **TBD in production**
