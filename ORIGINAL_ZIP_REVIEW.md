# Review of the supplied ZIP

The original archive had a sensible first cut: red teaming, guardrails, quantitative evaluation, and privacy. It was easy to navigate.

It was not yet workshop-ready:

1. **Named tools were not actually used.** Giskard, Colang, DeepEval-style evaluation, and Presidio were represented by substring or regex functions.
2. **Demonstrations looked like boundaries.** A keyword deny-list appeared to be a guardrail, but there was no typed command, authorization decision, approval token, or side-effect boundary.
3. **Evaluation was too small and brittle.** Seven-cell notebooks did not create versioned datasets, uncertainty, thresholds, or CI-ready failures.
4. **Major developer attack surfaces were absent.** No threat model, indirect prompt path, agent authorization, supply-chain scan, incident trace, subgroup analysis, or capstone release gate.

This rebuild keeps the useful themes and distinguishes:

- a **training double**, making a failure deterministic and teachable;
- a **real library integration**, showing actual installation and API use;
- an **enforceable production boundary**, implemented outside the model.
