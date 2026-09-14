# CFIP Source Runtime / Worker Evidence

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Workstream:** D5 — Runtime/worker evidence  
**Status:** evidence pass advanced; closure still open

## Purpose

Record executable source evidence for the CForex runtime roles before CFIP implementation. This document is an evidence artifact, not a target implementation design. Source code remains authoritative.

## Runtime roles proven

| Role | Source entrypoint | Primary responsibility | Evidence state |
|---|---|---|---|
| API | `apps/api/src/fi_api/main.py` | HTTP/WebSocket API composition, auth, realtime, admin, trading, integrations, research, billing, health and platform-intelligence surfaces | Verified at composition-root level; endpoint catalog still open |
| General worker | `apps/worker/src/fi_worker/main.py` | canonical market observation ingestion, durable outbox dispatch, NATS transport, ClickHouse projection, realtime intelligence orchestration and signal lifecycle | **Executable evidence verified** |
| Learning worker | `apps/learning_worker/src/fi_learning_worker/main.py` | periodic governed learning from trading-journal outcomes, evidence fingerprinting and learning-record persistence | **Executable evidence verified** |
| Autonomy worker | `apps/autonomy_worker/src/fi_autonomy_worker/main.py` | continuous governed intelligence lanes, self-healing/self-development/research/audit/verification/control-plane supervision with circuit breakers | **Executable evidence verified** |
| Web | `apps/web` | Next.js product surface and realtime/chart/workspace UX | Frontend evidence tracked by D6; runtime mapping remains open |

## General worker evidence

`apps/worker/src/fi_worker/main.py` constructs the production runtime through real infrastructure adapters. The executable path establishes:

1. PostgreSQL engine/session factory.
2. NATS connection and JetStream streams/consumers.
3. ClickHouse client and schema initialization.
4. Durable application event outbox and NATS event-envelope publisher/dispatcher.
5. Signal lifecycle service and provenance graph repository.
6. Realtime intelligence orchestration and realtime market-feed ingestion.
7. Canonical-observation PostgreSQL outbox and NATS publisher/dispatcher.
8. ClickHouse canonical-observation consumer/writer.
9. Realtime runtime state/ledger/sink and durable canonical-observation consumer.
10. A bounded dispatch loop for both event outbox and market-data outbox.
11. Graceful shutdown that cancels dispatcher/ClickHouse tasks, drains NATS, closes ClickHouse and disposes the SQLAlchemy engine.

This proves that the target migration must preserve both durable event transport and the separate realtime intelligence/application path; they are not interchangeable.

### Worker scheduling/concurrency evidence

The worker's `run()` creates a dispatcher task and a ClickHouse consumer task while the main realtime runner remains active. The dispatcher performs bounded batches (`limit=100`) and sleeps between iterations. This is source behavior that must be represented in the target worker contract, including backpressure, retry and idempotency evidence.

## Learning worker evidence

`apps/learning_worker/src/fi_learning_worker/main.py` establishes:

- a periodic cycle driven by `FI_LEARNING_INTERVAL_SECONDS` with a 300-second default;
- a minimum evidence threshold driven by `FI_LEARNING_MIN_OUTCOMES` with a 20-outcome default;
- deterministic outcome collection ordered by `closed_at` and `trade_id`;
- a SHA-256 data revision fingerprint over journal outcome identity, close time and realized R;
- explicit evidence references in the learning request;
- project/dataset/data-revision identity in the learning request;
- a hard guard that raises if governed learning reports model mutation as allowed;
- persistence of lessons through a repository boundary;
- atomic state-file replacement;
- failure isolation: a failed cycle is logged and the worker continues to the next scheduled cycle;
- disposal of the database engine on shutdown.

Target requirements derived from this evidence:

- learning cycles require explicit dataset identity and point-in-time data revision;
- evidence references are mandatory for learning outputs;
- learning artifacts must remain distinct from production model mutation;
- schedule and thresholds are operational configuration, not domain invariants;
- persistence and state publication must be atomic and observable.

## Autonomy worker evidence

`apps/autonomy_worker/src/fi_autonomy_worker/main.py` establishes a continuously running supervisor with independent lanes for:

- model-independent intelligence;
- self-healing/evidence diagnosis;
- self-development;
- local self-development;
- autonomous research;
- research-fetch/network readiness;
- dataset acquisition/readiness;
- control-plane snapshots;
- independent verification;
- post-promotion health guard;
- learning observability;
- deep audit;
- capability sweep;
- self-contained workflow audit.

The source also establishes:

- independently configurable lane intervals through environment-backed operational settings;
- bounded script execution with a configurable timeout;
- process-group termination on timeout;
- per-lane circuit-breaker state with failure and timeout streaks;
- cooldown after repeated failure/timeouts;
- durable lane telemetry/state written by atomic temporary-file replacement;
- fail-closed handling for malformed circuit state;
- durable lookup of autonomy mode, with fallback to governed mode;
- explicit `production_mutation_allowed: false` and `model_mutation_allowed: false` in supervisor state;
- startup of all intelligence lanes as independent tasks;
- cleanup/cancellation of all lane tasks on shutdown;
- bounded runtime boot-smoke mode for release verification.

Target requirements derived from this evidence:

- autonomy must be represented as a governed control plane, not as an unrestricted scheduler;
- each lane needs an explicit identity, schedule, timeout, retry/circuit policy, evidence output and health status;
- autonomous actions must remain behind the target Change Governor and release gates;
- circuit-breaker state and evidence history must be durable and tamper-resistant;
- malformed safety state must fail closed;
- self-healing and self-development remain distinct capabilities;
- post-promotion health guarding and rollback evidence are mandatory for autonomous promotion.

## Required target worker contract

Before implementation, every migrated worker/job must have:

1. entrypoint and runtime role;
2. capability owner;
3. input/output contracts;
4. producer/consumer/event bindings;
5. schedule or trigger semantics;
6. concurrency and partition key;
7. idempotency key and duplicate handling;
8. retry/backoff/quarantine policy;
9. watermark/checkpoint semantics where applicable;
10. timeout and cancellation behavior;
11. health/readiness/liveness signals;
12. resource budget and scaling dimension;
13. observability/trace/metric/log contract;
14. security and credential boundary;
15. evidence/provenance requirements;
16. recovery and rollback behavior;
17. replay/backtest compatibility where applicable;
18. tests, including failure and restart cases.

## Remaining D5 closure gaps

The current pass proves the major worker entrypoints and important runtime behavior, but D5 is not closed. Remaining evidence must map:

- every scheduled lane to its exact script contract and source tests;
- all event producers/consumers and JetStream subjects;
- checkpoint/watermark/lease semantics;
- retry/dead-letter/quarantine behavior at each consumer;
- resource/concurrency limits and scaling assumptions;
- worker health/readiness telemetry;
- deployment manifests/compose services and environment contracts;
- worker-to-UI/API side effects;
- capability-to-worker-to-test traceability;
- operational SLO, retention and recovery requirements.

## Evidence rule

No CFIP worker is considered migrated because a similarly named process exists. Promotion requires executable target behavior plus contract, failure, observability and parity evidence.
