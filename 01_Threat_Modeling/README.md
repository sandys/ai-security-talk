# 01 — Threat-Model an AI System as Code

**Time:** 25 minutes  
**Primary tool:** OWASP `pytm`  
**Artifact:** version-controlled data-flow model plus a prioritized control backlog.

Start with the system, not a generic list of “AI risks.” The useful unit is an end-to-end product: users, orchestration code, model endpoint, retrieval stores, tools, logs, human approvers, and the trust boundaries between them.

## Reference architecture and trust boundaries

```mermaid
flowchart LR
    subgraph Public[Untrusted / public]
      U[User]
      D[Uploaded document]
    end
    subgraph App[Application boundary]
      API[API gateway]
      AG[Agent orchestrator]
      PE[Policy enforcement point]
    end
    subgraph Data[Restricted data boundary]
      V[(Vector store)]
      L[(Redacted audit log)]
    end
    subgraph Vendor[External model boundary]
      M[LLM endpoint]
    end
    subgraph Priv[Privileged action boundary]
      AP[Human approver]
      T[Refund / email tool]
    end

    U -->|prompt| API --> AG
    D -->|untrusted content| V
    AG -->|query| V -->|chunks + provenance| AG
    AG -->|minimum necessary context| M -->|candidate output| AG
    AG -->|typed proposal| PE
    PE -->|high-risk request| AP -->|signed approval| PE
    PE -->|scoped capability| T
    AG -->|redacted event| L
```

## Threat-to-control derivation

```mermaid
flowchart TD
    A[Asset or unacceptable outcome] --> F[Data flow crossing a boundary]
    F --> T[Threat hypothesis]
    T --> P{Prevent at source?}
    P -->|Yes| PC[Preventive control]
    P -->|No / residual risk| DC[Detective control]
    PC --> V[Verification method]
    DC --> V
    V --> O[Named owner + due date]
    O --> R[Residual-risk decision]
```

## Guided exercise

1. Open `01_pytm_threat_model.ipynb`. It imports the model from `rag_agent_tm.py`, calls `tm.resolve()` in-process, and lists the findings — including pytm 1.4's LLM/agent-specific threats (`LLM01`–`LLM09`) that fire because the model declares `hasRAG`, `hasAgentCapabilities`, `hasAccessToSensitiveSystems`, `processesPersonalData`, and `usesExternalTools`.
2. Flip a control (`llm.controls.implementsPOLP = True`, `llm.hasContentFiltering = True`, `agent.validatesToolLaunchConfig = True`), re-resolve, and watch `LLM05` and friends disappear while `LLM03`/`LLM08` (third-party data leakage, output disclosure) remain until modules 05 and 08 address them.
3. Generate the DFD (`tm.dfd()` → Graphviz DOT, plus a Mermaid rendering derived from the same flows) and the JSON export via the CLI.
4. Mark each data flow by **origin trust**, **sensitivity**, **authorization context**, and **side-effect potential**.
5. Choose three unacceptable outcomes, for example secret disclosure, cross-tenant retrieval, and unauthorized refund.
6. For each, write an attack path (the notebook asserts every backlog row cites a threat ID pytm actually raised) and attach at least one prevention, one detection, and one executable verification.
7. Commit `rag_agent_tm.py` beside the application code and review it whenever a boundary or tool changes.

## Recommended use of `pytm`

Use `pytm` for repeatable architecture-as-code and threat enumeration. Do not treat generated findings as an automatically prioritized answer. Add your product’s business impact, data classification, tenant model, tool permissions, and deployment assumptions. Keep a small, reviewable model rather than a decorative diagram no one updates.

**Done means:** the DFD is generated, three high-risk paths are recorded, every selected threat has an owner/control/test, and the model is ready for code review.
