# CFIP Source Closure Batch 26 — Engine / Worker Lifecycle Reconciliation

**Source:** `armanemp/CForex` `main` v0.9.154
**Target:** `armanemp/CFIP` `main`
**Gate:** Gate 0 — Source Closure
**Status:** Evidence advanced; D4/D5 remain OPEN

## 1. Engine execution-plane reconciliation

CForex contains a durable/application analysis path and a low-latency trading evidence path. The inspected evidence establishes that these paths must not become two independent analytical implementations in CFIP.

The canonical target identity remains `(engine_id, version)`. The semantic implementation is unique per identity; runtime, durable, replay and research execution are projections/adapters around that canonical implementation.

### Canonical flow

`Engine Contract/Catalog → validated Runtime Projection`

`Engine Contract/Catalog → Durable/Research Execution Projection`

`Runtime/Durable Evidence → AnalysisConsensusService → Decision/Risk`

The runtime path currently uses `WorkspaceService.snapshot → AnalysisFabric → EngineRuntime → EngineOutput/evidence projection` for the inspected trading evidence endpoint. The durable path uses `AnalysisExecutionService → AnalysisRunRepository` when that service is composed. Their relationship is therefore an explicit closure item, not something that should be guessed from matching engine IDs.

## 2. Engine closure requirements

For every executable engine identity, Gate 0 requires:

- implementation location;
- descriptor source;
- canonical engine ID/version;
- input schema;
- output/evidence schema;
- parameters and serialization;
- warmup/timeframe semantics;
- upstream data dependencies;
- determinism contract;
- PIT/revision behavior;
- provenance/fingerprints;
- failure policy;
- latency budget;
- runtime registration path;
- durable/research path relationship;
- tests/fixtures;
- telemetry and persistent health evidence;
- replay/backtest compatibility.

## 3. Worker lifecycle evidence

The general worker directly composes PostgreSQL, NATS JetStream, ClickHouse, durable application-event outbox/publisher/dispatcher, canonical-observation outbox/publisher/dispatcher, realtime intelligence, signal lifecycle, provenance, runtime state/ledger, ClickHouse projection and bounded dispatch, with graceful shutdown.

The learning worker directly derives a deterministic revision from ordered journal outcomes and executes governed learning. This revision must remain distinct from market-data PIT revisions and dataset fingerprints.

The autonomy worker supervises governed lanes for intelligence, self-healing/evidence diagnosis, self-development, research, dataset acquisition readiness, control-plane snapshots, independent verification, post-promotion health guarding and audits. The inspected boundary keeps production/model mutation governed and disabled where evidence says so.

## 4. Realtime correctness lifecycle

CFIP must preserve the stronger event-time model:

`canonical event → partition ownership → sequence/deduplication → watermark → late-event policy → critical processing → runtime outcome → durable evidence/projection → checkpoint/recovery`

Local in-memory deduplication/sequence state may be a performance layer, but correctness-critical state requires durable or recoverable ownership/checkpoint semantics at global scale.

## 5. Worker scaling contract

Each target worker contract must declare:

- production entrypoint;
- schedules/subscriptions;
- produced/consumed event families;
- ordering/partition key;
- concurrency budget;
- idempotency key;
- retry/backoff policy;
- quarantine/DLQ behavior;
- checkpoint/watermark state;
- lease/ownership semantics;
- health/readiness/liveness;
- graceful shutdown/drain;
- resource budget;
- horizontal scaling rules;
- recovery and replay behavior;
- telemetry/SLOs.

This is stronger than simply reproducing the source process names and is required for global-scale readiness.

## 6. Evidence state

| Dimension | State | Reason |
|---|---|---|
| D4 Engines | ADVANCED / OPEN | canonical identity/execution-plane model confirmed; exhaustive executable census remains |
| D5 Workers | ADVANCED / OPEN | direct composition evidence established; lifecycle-complete deployment/scaling map remains |

No CFIP runtime engine or worker is declared implemented by this evidence.
