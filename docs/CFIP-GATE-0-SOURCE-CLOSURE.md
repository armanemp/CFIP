# CFIP Gate 0 — Source Closure

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** controlled closure in progress

## Purpose

Gate 0 converts the CForex source study into implementation-grade evidence. CForex executable behavior remains authoritative until parity closure; the source-study package accelerates discovery but never overrides executable evidence.

## Required closure dimensions

| Area | Required evidence | Status |
|---|---|---|
| API/WS | exhaustive routes/channels, contracts, auth, entitlements, callers, side effects, tests | **ADVANCED — exhaustive catalog still open** |
| Events | producers, consumers, subjects, schemas, ordering, idempotency, retry, replay, retention | IN PROGRESS |
| Data | entity/table/column ownership and cross-context access | IN PROGRESS |
| Engines | implementation, deterministic contract, PIT fixture, provenance, tests, replay compatibility | IN PROGRESS |
| Workers | entrypoints, jobs, subscriptions, producers, checkpoints, retries, scaling, health | **ADVANCED — entrypoints and major runtime behavior verified; lifecycle closure still open** |
| Frontend | routes/components/hooks/API/realtime/auth/state/i18n/a11y/telemetry/tests | IN PROGRESS |
| Tests | capability mapping plus negative/security/PIT/replay coverage | IN PROGRESS |
| Policy | invariant/config/runtime setting/tenant setting/entitlement/flag/governed policy classification | IN PROGRESS |
| Adapters | provider/broker/model/research boundaries, capabilities, credentials, failure behavior | IN PROGRESS |
| Operations | SLO, retention, partitioning, recovery, rollback and DR requirements | IN PROGRESS |

## Current evidence advancement

### D1 — API/WS

The D1 API/WS pass has verified the broad API composition surface and a substantial portion of `/v1/trading` directly from executable CForex source. Verified trading contracts include demo candle lifecycle, realtime WebSocket, canonical observation ingestion, deterministic engine registry/evidence, watchlist, workspace, terminal context, MTF, decision/live-decision, technical analysis, decision explanation, market state, notifications, intelligence supervisor/overview/graph, calibration evaluation, provider reliability and learning analytics. Router wiring also proves the presence of risk, safety, entry guidance, execution intelligence/lifecycle, broker registry, execution quality, learning, self-diagnosis/self-healing and governed competition components.

This is evidence advancement, not closure. The remainder of the trading router and every mounted API module still require exhaustive endpoint-level extraction including request/response/error contracts, authentication/workspace/entitlement rules, UI callers, event side effects and tests.

### D5 — Runtime/workers

The executable source pass now directly verifies the major runtime entrypoints:

- `apps/worker/src/fi_worker/main.py`: PostgreSQL + NATS JetStream + ClickHouse initialization, durable application-event outbox dispatch, canonical-observation outbox dispatch, ClickHouse projection, realtime intelligence orchestration, signal lifecycle/provenance, bounded dispatch loops and graceful shutdown.
- `apps/learning_worker/src/fi_learning_worker/main.py`: periodic journal-outcome collection, deterministic data-revision fingerprinting, evidence references, governed learning gate, lesson persistence, atomic state publication and failure-isolated continuation.
- `apps/autonomy_worker/src/fi_autonomy_worker/main.py`: independent governed intelligence lanes, bounded script execution, circuit breakers, atomic lane telemetry, fail-closed malformed safety state, independent verification/post-promotion guard lanes and explicit production/model mutation guards.
- `apps/api/src/fi_api/realtime.py`: authenticated application WebSocket path with snapshot-plus-incremental delivery, subscription authorization/registry, validation, unsubscribe handling and bounded failure responses.

The detailed evidence is recorded in `docs/evidence/CFIP-RUNTIME-WORKER-EVIDENCE.md`.

This remains an **advanced evidence pass, not closure**. Exact job-to-event mappings, checkpoint/watermark/lease semantics, retry/quarantine behavior, resource/scaling contracts, deployment manifests, worker health telemetry and complete worker-to-test/capability traceability remain open.

## Established facts

- CForex is broader than trading: identity/workspaces, realtime, administration, intelligence, trading, integrations, public intelligence, research, billing, journals, health/readiness, model-provider boundaries and security posture are part of the source surface.
- Canonical market data flow: `provider → raw → normalize → validate → deduplicate → event-time → quality → canonical → outbox → event bus`.
- Durable events use PostgreSQL outbox before NATS JetStream fan-out. Application realtime is a separate snapshot-plus-incremental path.
- `AnalysisConsensusService` is the authoritative analytical fusion boundary.
- PostgreSQL is transactional/system-of-record; ClickHouse serves high-volume analytical/time-series workloads; Redis is cache/ephemeral coordination; object storage is for justified large immutable artifacts; MongoDB requires a demonstrated document workload and explicit ownership decision.

## Closure rule

Gate 0 closes only when every high-impact capability has executable evidence, every authoritative entity has one owner, durable event families have lifecycle semantics, executable engines have deterministic/PIT/replay evidence, workers and UI workflows are mapped, and no material capability loss remains unexplained.

## Implementation hand-off

**Implementation remains paused by project policy until documentation/evidence freeze.** Once Gate 0 is closed, foundation work may begin only for evidence-backed contracts. The first Gate 1 slice must prove the complete chain:

`contract → domain → use case → port → adapter → persistence/event → API/realtime → tests → telemetry`

Unresolved source behavior must never be guessed. Intentional divergence requires an ADR and preserved source evidence.

## Continuation rule

At every continuation: read the migration control index first, inspect both repositories, identify the active evidence gap, make the smallest coherent documentation/evidence change, verify it, update evidence/status, and re-read GitHub state before reporting progress.
