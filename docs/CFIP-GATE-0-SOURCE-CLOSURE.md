# CFIP Gate 0 — Source Closure

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** controlled closure in progress

## Purpose

Gate 0 converts the CForex source study into implementation-grade evidence. CForex executable behavior remains authoritative until parity closure; the source-study package accelerates discovery but never overrides executable evidence.

## Required closure dimensions

| Area | Required evidence | Status |
|---|---|---|
| API/WS | exhaustive routes/channels, contracts, auth, entitlements, callers, side effects, tests | IN PROGRESS |
| Events | producers, consumers, subjects, schemas, ordering, idempotency, retry, replay, retention | IN PROGRESS |
| Data | entity/table/column ownership and cross-context access | IN PROGRESS |
| Engines | implementation, deterministic contract, PIT fixture, provenance, tests, replay compatibility | IN PROGRESS |
| Workers | entrypoints, jobs, subscriptions, producers, checkpoints, retries, scaling, health | IN PROGRESS |
| Frontend | routes/components/hooks/API/realtime/auth/state/i18n/a11y/telemetry/tests | IN PROGRESS |
| Tests | capability mapping plus negative/security/PIT/replay coverage | IN PROGRESS |
| Policy | invariant/config/runtime setting/tenant setting/entitlement/flag/governed policy classification | IN PROGRESS |
| Adapters | provider/broker/model/research boundaries, capabilities, credentials, failure behavior | IN PROGRESS |
| Operations | SLO, retention, partitioning, recovery, rollback and DR requirements | IN PROGRESS |

## Established facts

- CForex is broader than trading: identity/workspaces, realtime, administration, intelligence, trading, integrations, public intelligence, research, billing, journals, health/readiness, model-provider boundaries and security posture are part of the source surface.
- Canonical market data flow: `provider → raw → normalize → validate → deduplicate → event-time → quality → canonical → outbox → event bus`.
- Durable events use PostgreSQL outbox before NATS JetStream fan-out. Application realtime is a separate snapshot-plus-incremental path.
- `AnalysisConsensusService` is the authoritative analytical fusion boundary.
- PostgreSQL is transactional/system-of-record; ClickHouse serves high-volume analytical/time-series workloads; Redis is cache/ephemeral coordination; object storage is for justified large immutable artifacts; MongoDB requires a demonstrated document workload and explicit ownership decision.

## Closure rule

Gate 0 closes only when every high-impact capability has executable evidence, every authoritative entity has one owner, durable event families have lifecycle semantics, executable engines have deterministic/PIT/replay evidence, workers and UI workflows are mapped, and no material capability loss remains unexplained.

## Implementation hand-off

Foundation work may begin only for evidence-backed contracts. The first Gate 1 slice must prove the complete chain:

`contract → domain → use case → port → adapter → persistence/event → API/realtime → tests → telemetry`

Unresolved source behavior must never be guessed. Intentional divergence requires an ADR and preserved source evidence.

## Continuation rule

At every continuation: read the migration control index first, inspect both repositories, identify the active evidence gap or implementation slice, make the smallest coherent change, verify it, update evidence/status, and re-read GitHub state before reporting progress.
