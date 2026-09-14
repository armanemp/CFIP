# CFIP Documentation Progress Report 15

**Migration:** CForex → CFIP  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Date:** 2026-09-14  
**Gate:** Gate 0 — Source Closure  
**Status:** OPEN — evidence/documentation only

## 1. Objective

This continuation moved from class-level existence toward executable composition evidence. The worker entrypoint was inspected directly to determine which source capabilities are actually composed into a long-running process and which remain only application/infrastructure components.

The target remains a modern modular architecture with bounded contexts, explicit application services, technology-independent contracts, workload-specific execution planes, durable provenance and standard observability. Source behavior is preserved for parity, but accidental source coupling is not promoted to CFIP architecture.

## 2. Strong new source evidence: realtime worker composition

`apps/worker/src/fi_worker/main.py` provides direct executable composition evidence for a substantial production worker path.

The worker builds and wires:

- PostgreSQL async engine/session factory;
- NATS client and JetStream;
- market and event streams/consumers;
- ClickHouse client and schema initialization;
- durable application-event outbox;
- NATS event publisher and durable event dispatcher;
- signal lifecycle repository/service;
- provenance graph repository;
- vertical intelligence service;
- realtime intelligence orchestrator;
- realtime market-feed service;
- runtime state repository and runtime ledger;
- runtime event sink;
- canonical-observation outbox/publisher/dispatcher;
- ClickHouse canonical-observation consumer/writer;
- durable canonical-observation consumer;
- bounded dispatch loops;
- graceful NATS drain, ClickHouse close and SQLAlchemy engine disposal.

This changes the evidence level for the realtime/event/data path from merely architectural composition to **direct executable bootstrap evidence**.

## 3. Important boundary finding

The worker composition does **not** visibly construct `AnalysisExecutionService` or `SqlAlchemyAnalysisRunRepository` in the inspected entrypoint.

Therefore the source now has a more precise execution map:

```text
API / trading evidence
        │
        └── AnalysisFabric → EngineRuntime → engine outputs

Realtime worker
        │
        ├── canonical observation outbox → NATS
        ├── durable event outbox → NATS
        ├── realtime consumer
        ├── vertical intelligence
        ├── signal lifecycle
        ├── provenance graph
        └── ClickHouse projection

Durable analysis service
        │
        └── AnalysisExecutionService → AnalysisRunRepository
            (production composition still unverified)
```

This is not evidence that durable analysis is unused. It is evidence that the inspected worker bootstrap does not compose it directly. Additional application/service consumers must still be traced before making a stronger absence claim.

## 4. Runtime lifecycle evidence

The worker has a real long-running lifecycle rather than a static dependency container:

1. build infrastructure;
2. ensure streams/consumers;
3. create repositories/services/orchestrators;
4. create runtime and sinks;
5. start bounded dispatch loops;
6. start ClickHouse consumer;
7. run realtime consumer/runtime;
8. signal shutdown;
9. cancel background tasks;
10. gather task termination;
11. drain NATS;
12. close ClickHouse;
13. dispose database engine.

This is direct evidence for graceful startup/shutdown and resource ownership in the realtime worker.

## 5. Scaling interpretation

The worker's architecture already separates durable application events, canonical market observations and analytical/realtime processing. CFIP should preserve this separation while making scaling semantics explicit:

- each consumer group must have an explicit partition/ordering key;
- handlers must be idempotent;
- bounded dispatch must expose queue depth/lag/backpressure telemetry;
- long-running research/replay workloads must not compete with low-latency realtime processing;
- resource ownership and shutdown must be explicit;
- retry/dead-letter/quarantine behavior must be part of the event contract.

The presence of separate paths is therefore a useful source invariant, but exact partitioning, retention and overload semantics remain source-closure work.

## 6. Documentation correction applied conceptually

The migration evidence model now distinguishes:

**Component existence** → **composition evidence** → **runtime lifecycle evidence** → **operational evidence**.

A repository or service class alone is not production evidence. A bootstrap that instantiates it is stronger. A long-running entrypoint that executes it under real infrastructure is stronger again. Tests, telemetry, failure recovery and production deployment evidence complete the operational chain.

This hierarchy should be used consistently across D1–D10 rather than only for analysis engines.

## 7. Data/PIT boundary remains open

The worker proves canonical observation flow into NATS and ClickHouse, but this alone does not establish authoritative historical reconstruction.

Still required before Gate 0 closure:

- canonical source of historical snapshots;
- exact event-time/watermark semantics;
- late-arrival correction policy;
- revision supersession rules;
- dataset fingerprint producer;
- snapshot retention/partition strategy;
- reconstruction API/service;
- replay ordering guarantees;
- equivalence between reconstructed history and live canonical state.

The deterministic workspace snapshot used by the trading evidence route must remain classified as a bounded/demo/replay source rather than authoritative historical PIT storage until these questions are proven.

## 8. Replay boundary remains open

The existence of `replay_cases` schema and a deterministic `backtest.replay` engine is insufficient to claim full replay capability.

Gate 0 still requires tracing:

`case producer → case persistence → loader → dataset resolution → engine/version resolution → ordered event replay → expected invariant evaluation → result persistence → provenance → report/telemetry`.

If any of these links are absent in CForex, the migration record must say so explicitly rather than filling the gap with assumptions.

## 9. Analysis-engine closure status

D4 remains **96% / advanced / not closed**.

### Confirmed

- 15 runtime engine registrations;
- 14 top-level engine namespaces;
- two runtime-only builtin engines;
- deterministic runtime execution;
- descriptor/version/warmup/latency/failure semantics;
- direct runtime/fabric tests;
- durable `analysis_runs` schema;
- `AnalysisRunRepository` implementation;
- `AnalysisExecutionService` implementation;
- canonical SHA-256 fingerprints;
- V2 trading evidence route;
- worker/runtime infrastructure evidence;
- replay/provenance/dataset-integrity schema evidence;
- one canonical engine identity + separate execution planes as target architecture.

### Open

- durable analysis production wiring;
- V1↔V2 activation/registration bridge;
- durable relationship of V2 trading evidence;
- authoritative PIT reconstruction;
- dataset fingerprint producer/consumer;
- replay-case executable lifecycle;
- live/replay/backtest equivalence;
- per-engine golden/regression fixtures;
- durable engine telemetry/history;
- exhaustive engine-like component census;
- D4/D7/D11 reconciliation.

## 10. Cross-document quality rules

Before Gate 0 closure, every migration document must satisfy:

- source version/commit is explicit;
- evidence is traceable to source paths;
- implementation and production wiring are not conflated;
- negative evidence is bounded unless absence is exhaustively proven;
- source parity and target improvement are clearly separated;
- runtime implementation percentage is never inferred from documentation readiness;
- Gate state is consistent across control index, master plan, final gate document, capability registry, parity matrix and progress reports;
- current external standards are reflected where materially relevant;
- stale claims are corrected rather than merely superseded by newer prose.

## 11. Current readiness dashboard

| Dimension | Readiness | State |
|---|---:|---|
| Target architecture | **100%** | established; execution/workload boundaries refined |
| Migration control framework | **99%** | execution-wiring evidence generalized across domains |
| Capability registry | **96%** | advanced |
| Documentation integration | **99%** | advanced; stale-claim cleanup remains part of final reconciliation |
| D1 API/WS | **75%** | composition evidence stronger; exhaustive endpoint census open |
| D2 Events | **72%** | realtime worker composition now directly evidenced; consumer/ordering census open |
| D3 Data ownership/PIT | **75%** | canonical observation flow strengthened; historical reconstruction open |
| D4 Engines | **96%** | strong; production durable wiring/replay/fixtures open |
| D5 Workers/runtime | **78%** | direct worker lifecycle evidence established; remaining workers still require tracing |
| D6 Frontend | **40%** | in progress |
| D7 Tests | **37%** | in progress; production-path evidence still open |
| D8 Policy/config | **47%** | in progress |
| D9 Adapters | **35%** | in progress |
| D10 Operations | **36%** | startup/shutdown evidence improved; SLO/recovery/scale evidence open |
| D11 Reconciliation | **18%** | execution-wiring reconciliation generalized |

Unweighted D1–D11 planning/evidence indicator is approximately **55.5%**. This is not implementation percentage and is not a Gate 0 exit criterion.

## 12. Gate status

**Gate 0 remains OPEN.**

**CFIP runtime implementation remains 0% / LOCKED.**

No documentation completion is being treated as parity implementation.

## 13. Next continuation

1. trace all remaining worker entrypoints and their actual compositions;
2. trace dataset fingerprint producers/consumers;
3. trace replay-case producers/loaders/executors;
4. trace PIT reconstruction/watermark/revision semantics;
5. trace V1/V2 registry activation;
6. trace durable engine telemetry and lifecycle events;
7. map golden/regression fixtures per engine;
8. reconcile source-evidence matrix, capability registry, parity matrix, Gate 0 final and progress reports;
9. identify and correct any stale/overstated source claims;
10. only after evidence closure, prepare a formal Gate 0 exit proposal.

**No CFIP runtime implementation is authorized by this report.**
