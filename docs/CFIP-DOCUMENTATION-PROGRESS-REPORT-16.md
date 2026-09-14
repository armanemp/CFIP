# CFIP Documentation Progress Report 16

**Migration:** CForex → CFIP  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Date:** 2026-09-14  
**Gate:** Gate 0 — Source Closure  
**Status:** OPEN — evidence/documentation only

## 1. Scope of this continuation

This pass performed four activities:

1. re-read the current CFIP control stack before source analysis;
2. directly inspected the CForex realtime worker bootstrap and runtime implementation;
3. promoted concrete realtime ordering, restart, watermark, deduplication and backpressure semantics into migration evidence;
4. performed a consistency check between the latest progress reports, Control Index and canonical Gate 0 register.

No CFIP runtime implementation was added.

## 2. New source evidence: realtime runtime is semantically richer than a simple consumer

Direct inspection of `packages/application/src/fi_application/realtime_runtime.py` establishes that the CForex realtime runtime is a stateful event-time processing system, not merely a NATS consumer.

Confirmed semantics include:

- per-instrument sequence lanes protected by locks;
- persisted runtime-state hydration on restart;
- bounded event-ID and deduplication-key windows;
- event-time watermark calculation using configurable delay;
- duplicate and in-flight event suppression;
- configurable late-event policy with explicit drop/accept dispositions;
- critical-handler failure accounting;
- correlation/causation-aware runtime event emission;
- watermark advancement events;
- bounded subscriber queues;
- explicit backpressure-drop events;
- runtime metrics for receipt, acceptance, duplicates, late events, backpressure, failures, lateness and watermark.

This is now a **mandatory CFIP realtime semantic contract**, subject to later PIT/replay and scaling reconciliation.

## 3. Important target improvement: make event-time semantics a first-class capability

CFIP must not hide watermark/lateness/deduplication behavior inside an infrastructure consumer. These are domain/application-level runtime semantics because they affect the meaning and ordering of market observations.

Target structure should therefore separate:

```text
Canonical Market Event
        ↓
Event-Time / Ordering Policy
        ↓
Idempotency + Deduplication
        ↓
Critical Processing
        ↓
Runtime Outcome
        ↓
Durable Evidence / Projections
```

Infrastructure adapters may transport events, but they must not silently define market-event semantics.

The target should also expose explicit policies for:

- watermark delay;
- lateness tolerance;
- late-event disposition;
- dedupe window;
- sequence key;
- backpressure behavior;
- retry/quarantine behavior.

These are configuration/policy contracts, not arbitrary constants.

## 4. Scaling improvement: avoid unbounded per-key state

The source uses per-sequence locks and in-memory maps for event-time state, then persists runtime snapshots. CFIP should preserve the semantic guarantee but improve its scale boundary by explicitly specifying lifecycle and cardinality controls for sequence-key state.

Target requirements:

- bounded active sequence-key state;
- deterministic state eviction/checkpoint rules;
- persisted checkpoint/recovery semantics;
- ownership/lease semantics when multiple workers process the same partition;
- partition key compatibility with ordering guarantees;
- lag and queue-depth telemetry;
- overload behavior that is observable and policy-driven.

Do not blindly reproduce an in-memory map architecture at global scale.

## 5. Replay/PIT implication

The newly confirmed watermark and late-event behavior means replay cannot simply iterate stored rows. A faithful replay must preserve or explicitly model:

- event-time ordering;
- watermark progression;
- duplicate suppression;
- late-event policy;
- sequence partitioning;
- runtime state hydration/checkpoint boundaries;
- backpressure semantics where they affect externally observable behavior.

Therefore the existing replay closure requirement is strengthened to require a **runtime-semantic replay profile**, not merely an input/output comparison.

## 6. Documentation consistency finding

The current Control Index and latest Progress Reports classify D11 Reconciliation as **in progress**. The older body of the canonical Gate 0 register still contains historical wording that says D11 had not formally started.

This is a documentation inconsistency and must not remain unresolved.

Until the canonical register is rewritten, the controlled interpretation is:

> D11 is **IN PROGRESS**. The earlier "NOT STARTED" wording is stale historical state and is superseded by the current Control Index and Progress Reports. Final Gate 0 closure still requires the complete D11 contradiction/staleness sweep.

This report records the discrepancy explicitly so it cannot be mistaken for current state. The canonical register must be normalized in the next documentation reconciliation write rather than creating a second competing source of truth.

## 7. Current source/target evidence hierarchy

The migration process now explicitly distinguishes four levels:

1. **Component evidence** — class/module/schema exists.
2. **Composition evidence** — bootstrap/application graph instantiates it.
3. **Runtime lifecycle evidence** — an executable process actually invokes it with state/start/stop behavior.
4. **Operational evidence** — tests, telemetry, recovery, scaling, deployment and failure behavior establish production readiness.

Only level 4 can support a production-readiness conclusion. Levels 1–3 remain migration/source evidence, not CFIP parity proof.

## 8. Standards freshness update

Current OpenTelemetry guidance continues to recommend standardized semantic conventions for common telemetry domains, while GenAI observability conventions cover model/tool operations and token usage. citeturn0search10turn0search3

OWASP's September 2026 Agent Control Standard adds a useful architectural requirement for CFIP: agent behavior should be inspectable, traceable and controllable through runtime-enforceable policy hooks rather than relying only on prompts or conventions. citeturn0search0turn0search2

The CFIP target therefore retains:

`agent identity → capability → policy hook → authorized tool/action → telemetry/evidence → post-action control`

and keeps agent authority outside the analytical-engine authority boundary.

## 9. Updated D4/D5/D10 implications

### D4 Engines

No closure change yet. Realtime runtime evidence strengthens the execution environment around engines, but does not replace missing per-engine PIT/replay/fixture/registration/telemetry evidence.

### D5 Workers/Runtime

D5 evidence materially improves because the realtime worker and runtime now have direct source-path and lifecycle semantics. Remaining worker topology and operational closure are still required.

### D10 Operations

Backpressure, graceful shutdown, runtime-state hydration and bounded queues are now concrete operational requirements. Global-scale acceptance must add lag SLOs, partition ownership, state checkpointing, recovery time objectives and overload tests.

## 10. Current readiness dashboard

| Dimension | Readiness | State |
|---|---:|---|
| Target architecture | **100%** | established; event-time/runtime semantics refined |
| Migration control framework | **99%** | evidence hierarchy and execution-wiring rules established |
| Capability registry | **96%** | advanced |
| Documentation integration | **98%** | advanced; one stale Gate 0 D11 wording item explicitly identified for normalization |
| D1 API/WS | **75%** | exhaustive registry open |
| D2 Events | **73%** | worker/runtime semantics strengthened; full lifecycle census open |
| D3 Data/PIT | **76%** | canonical observation/runtime state stronger; authoritative reconstruction open |
| D4 Engines | **96%** | strong; PIT/replay/fixtures/registration/telemetry open |
| D5 Workers/runtime | **81%** | realtime runtime semantics directly evidenced; full topology/operations open |
| D6 Frontend | **40%** | in progress |
| D7 Tests | **38%** | runtime semantics require broader test mapping |
| D8 Policy/config | **49%** | event-time/backpressure policies now explicitly classified |
| D9 Adapters | **35%** | in progress |
| D10 Operations | **39%** | backpressure/recovery/shutdown evidence improved; SLO/scale/DR open |
| D11 Reconciliation | **20%** | active; stale-state cleanup and whole-stack reconciliation remain |

Unweighted D1–D11 evidence/planning indicator is approximately **56.1%**. This is not implementation percentage and is not a Gate 0 exit criterion.

## 11. Next actions

1. normalize the stale D11 wording in the canonical Gate 0 register;
2. trace remaining worker entrypoints and deployment configuration;
3. trace dataset fingerprint producers/consumers;
4. trace replay-case producer/loader/executor;
5. trace PIT reconstruction, watermark and revision persistence end-to-end;
6. trace V1/V2 engine activation and registration bridge;
7. map every engine to golden/regression fixtures and production-path tests;
8. trace durable engine telemetry and health projections;
9. perform D1–D10 source-to-document reconciliation;
10. perform a final whole-document contradiction/staleness sweep before Documentation Freeze.

**Gate 0 remains OPEN. CFIP runtime implementation remains 0% / LOCKED.**
