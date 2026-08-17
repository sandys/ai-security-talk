# 10 — Capstone: Secure a RAG Agent End to End

**Time:** 40 minutes  
**Tooling:** Python, Pydantic, deterministic retrieval, structured evidence  
**Outcome:** one runnable agent whose release evidence covers security, privacy, utility, authorization, and monitoring.

The capstone is not “add all libraries.” It integrates the boundaries learned in the earlier labs: untrusted input/data, trusted policy, limited model authority, privacy-safe telemetry, regression evidence, and explicit residual risk.

## Target architecture

```mermaid
flowchart LR
    U[Authenticated user] --> IN[Input minimization + PII transform]
    IN --> R[Retriever<br/>tenant filter + source trust]
    R --> P[Prompt builder<br/>data delimited from policy]
    P --> M[Model / deterministic workshop proposer]
    M --> V[Pydantic parse<br/>extra fields forbidden]
    V --> PE[Server policy<br/>identity + tenant + amount]
    PE -->|answer / draft| O[Response]
    PE -->|high risk| H[Human approval queue]
    PE -->|authorized capability| T[Constrained tool]
    IN --> TR[Redacted trace]
    R --> TR
    V --> TR
    PE --> TR
    T --> TR
```

## Request decision sequence

```mermaid
sequenceDiagram
    participant User
    participant App
    participant Retrieval
    participant Model
    participant Policy
    participant Human
    participant Tool

    User->>App: Prompt + authenticated tenant
    App->>App: Minimize and redact telemetry view
    App->>Retrieval: Tenant-scoped query
    Retrieval-->>App: Chunks + source + trust
    App->>Model: Trusted rules + delimited data
    Model-->>App: Candidate typed proposal
    App->>App: Parse and validate
    App->>Policy: Proposal + authenticated context
    alt Safe answer or draft
      Policy-->>App: allow
    else High-risk action
      Policy->>Human: approval with payload hash
      Human-->>Policy: approve / reject
    end
    Policy-->>Tool: capability only when authorized
    App-->>User: Answer / approval status
```

## Release-evidence pipeline

```mermaid
flowchart TD
    C[Versioned attack + benign corpus] --> RUN[Run end-to-end cases]
    RUN --> H1[Hard gates<br/>leak, tenant, side effect, PII]
    RUN --> U1[Utility gates<br/>answer and false refusal]
    H1 --> D{All hard gates zero?}
    U1 --> D
    D -->|No| B[BLOCK release]
    D -->|Yes| E[Evidence JSON<br/>versions, hashes, rows, limits]
    E --> R[Named reviewer / decision]
    R --> M[Deploy + monitor + rollback]
```

## Team exercise

1. Run `10_capstone.ipynb` without changing code; inspect the trace and release evidence.
2. One team adds an attack, one adds a benign edge case, one adds a control assertion, and one reviews residual risk.
3. Deliberately weaken a boundary (for example, allow untrusted retrieval instructions) and confirm the gate blocks release.
4. Restore the control and record the exact evidence diff.

## Definition of done

- no canary, direct identifier, or foreign-tenant source reaches output/evidence;
- no test case produces an irreversible side effect;
- high-value refund is approval-gated;
- benign returns utility passes;
- every decision includes version/hash metadata and a reason code;
- `release_evidence.json` says `PASS` only because named hard and utility gates passed;
- limitations explicitly say what has **not** been proven.
