# CFIP Gate 0 — Source Closure — Controlled Implementation Register

**Source:** `armanemp/CForex` `main` current evidence snapshot `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Status:** **OPEN — controlled implementation permitted; production promotion locked**  
**Supersedes for current operating decisions:** `docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md`

> The historical final register remains immutable history. This successor register changes only the implementation restriction: CFIP may now implement evidence-backed, reversible, independently verifiable target slices while Gate 0 remains open. It does **not** close Gate 0, waive source closure, waive parity evidence, or authorize production promotion/live trading.

## 1. Gate purpose

Gate 0 exists to prevent semantic loss during migration from CForex to CFIP. It remains an evidence-completeness gate, but it is no longer a blanket coding freeze.

The project now follows a **parallel evidence + engineering model**: source closure and target implementation advance together whenever the target slice has sufficient evidence and a clear contract.

## 2. Controlled implementation policy

### Permitted while Gate 0 is OPEN

- domain/application implementation where the source behavior is sufficiently understood;
- ports and adapters;
- contracts, schemas and migrations;
- deterministic analysis engines and runtime infrastructure;
- API/WebSocket adapters;
- frontend foundations and user workflows;
- worker/realtime infrastructure;
- governance/security/observability tooling;
- tests, fixtures, validators and CI;
- reversible performance and scale foundations;
- intelligence infrastructure and governed memory/evidence projections.

### Still locked

- production promotion;
- `PARITY-VERIFIED` or `PRODUCTION-READY` claims without their evidence gates;
- live trading/execution authorization;
- irreversible high-impact autonomous mutations;
- uncontrolled self-modification of governance/safety/evidence controls;
- dataset/model promotion based only on source prose or incomplete artifacts.

## 3. Required implementation evidence

Every Gate-0-compatible implementation slice must have:

`source evidence → capability ID → behavioral contract → target owner → implementation → tests → verification → observability → rollback/change identity`

If source semantics are incomplete, implementation must either:

1. remain at a clearly bounded contract/interface level; or
2. use an explicit target decision/ADR that identifies the unresolved behavior and prevents accidental parity claims.

## 4. Capability lifecycle

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

Gate 0 may now permit `IMPLEMENTED` and `VERIFIED` where evidence supports them. `PARITY-VERIFIED` and `PRODUCTION-READY` require their own evidence and later release gates.

## 5. D1–D11 closure status

| ID | Dimension | Status | Remaining closure requirement |
|---|---|---|---|
| D1 | API/WS | ADVANCED | exhaustive route/channel registry |
| D2 | Events | ADVANCED | lifecycle-complete producer/consumer registry |
| D3 | Data/PIT | ADVANCED | authoritative ownership + reconstruction |
| D4 | Engines | ADVANCED / bounded closure | alternate registration, V1/V2, PIT, replay, fixtures, telemetry |
| D5 | Workers | ADVANCED | lifecycle-complete mapping |
| D6 | Frontend | IN PROGRESS | workflow/evidence closure |
| D7 | Tests | IN PROGRESS | capability/test coverage closure |
| D8 | Policy/config | IN PROGRESS | exhaustive classification |
| D9 | Adapters | IN PROGRESS | adapter inventory closure |
| D10 | Operations | IN PROGRESS | SLO/capacity/DR/residency closure |
| D11 | Reconciliation | IN PROGRESS | zero unresolved material contradiction |

## 6. Implementation safety model

All implementation is classified through the ECP risk model:

- R0 — documentation/evidence
- R1 — low-risk reversible implementation
- R2 — material runtime/configuration
- R3 — high-impact/security/data/risk/execution
- R4 — irreversible/high-consequence

R0/R1 work may proceed when source evidence and tests are sufficient. R2 requires explicit checkpoint and independent verification. R3/R4 remain fail-closed until their applicable gate, policy and recovery evidence exists.

No autonomous agent receives unrestricted Git, SQL, infrastructure or production-execution authority.

## 7. Global-scale constraints remain active

Controlled implementation must preserve:

- stateless horizontal API design;
- partitionable workers/streams;
- deterministic idempotency;
- bounded concurrency/backpressure;
- PostgreSQL transactional authority;
- ClickHouse analytical isolation;
- explicit Redis authority limits;
- conditional MongoDB adoption only with demonstrated workload;
- PIT/revision correctness;
- event-time/watermark semantics;
- SLO/capacity methodology;
- recovery/rollback;
- regional/data-residency semantics;
- schema/data evolution compatibility;
- quotas/rate limits/fair-use boundaries.

## 8. Intelligence and autonomous development

Platform Intelligence remains cross-cutting over every capability. Applicable lifecycle hooks are:

`observe → context → reason → act → verify → learn → audit → safety`

Autonomous development remains sandboxed and governed. The system may propose, implement and verify changes automatically, but promotion is policy-gated and rollback-capable. Runtime autonomy cannot modify its own governor, safety controls or evidence history.

## 9. Dataset and learning restrictions

Dataset eligibility, model promotion and intelligence-memory activation remain independently governed. Manifest-declared counts are not verified counts. Synthetic data remains synthetic. PIT leakage controls, provenance, temporal split, evaluation, attribution, calibration and drift checks remain mandatory.

## 10. Gate 0 exit criteria

Gate 0 still closes only after:

- D1–D11 source-closure evidence reaches the required threshold;
- material source capabilities are classified `PRESERVE / IMPROVE / REPLACE / INTENTIONALLY-DIVERGE`;
- contradictions are resolved or explicitly dispositioned;
- parity matrix obligations are complete;
- intentional divergences have ADRs;
- dataset/replay/PIT blockers are resolved or formally bounded;
- formal source/target baselines and unresolved risks are recorded;
- an explicit Gate-0 exit decision authorizes the next release gate.

Controlled implementation **does not** close Gate 0.

## 11. Current decision

**Gate 0 remains OPEN.**

**Implementation restriction:** removed.  
**Production restriction:** remains active.  
**Parity restriction:** remains active.  
**Live execution restriction:** remains active.  
**High-impact autonomous mutation restriction:** remains active.

This is the authoritative operating interpretation for current continuation work until a later canonical Gate-0 register supersedes it.
