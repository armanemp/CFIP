# CFIP Data Ownership Evidence — CForex D3

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** advanced evidence pass; Gate 0 remains open

## 1. Evidence basis

This pass uses executable CForex migrations and domain package structure as primary evidence. The source database evolution is not treated as the target schema; it is treated as behavioral evidence for ownership, durability, temporal semantics and cross-context boundaries.

Verified migration evidence includes `0001_initial_market_reference`, `0002_domain_kernel`, `0003_market_data_outbox`, `0004_durable_outbox_leases`, `0005_analysis_execution_runs`, `0006_agent_ai_durability`, `0007_admin_settings_i18n_ux_foundation`, `0008_event_replay_provenance`, `0009_intelligence_learning`, `0010_learning_corpora_ci_artifacts`, `0011_durable_evaluation_outcomes_drift` and `0012_dataset_integrity_intelligence_memory`.

## 2. Source domain ownership signals

The executable domain tree contains distinct areas for `admin`, `agentic`, `ai`, `analysis`, `eventing`, `identity`, `instrument`, `intelligence`, `lineage`, `market_data`, `market_reference` and related domain concerns. This confirms that target ownership must be context-oriented rather than table-oriented. fileciteturn34file0

The market-data domain explicitly exposes entities and ports beneath `fi_domain.market_data`, reinforcing the rule that persistence technology is not itself the domain boundary. fileciteturn35file0

## 3. Authoritative source entities verified

### Market reference

`0001_initial_market_reference` establishes `instruments` as canonical instrument reference and `candles` as market observations keyed by instrument, timeframe, timestamp and source. It also preserves high-precision OHLC/volume/spread values, source identity and schema version, with a unique candle identity across `(instrument_id, timeframe, timestamp, source)`. fileciteturn47file0

### Identity / organization / workspace / provider / quality / lineage

`0002_domain_kernel` establishes `users`, `organizations`, `workspaces`, `memberships`, `providers`, `provider_instrument_mappings`, `market_sessions`, `quality_assessments` and `lineage_links`. Relational ownership and uniqueness constraints exist for organization/workspace membership and provider/instrument mappings; quality records retain rule-set version and lineage records retain source/target/relation metadata. fileciteturn43file0

### Canonical market-data durability

`0003_market_data_outbox` establishes a separate `market_observation_outbox` with dedupe key, event type, schema version, payload, lifecycle status, attempts and availability/publication timestamps. `0004` adds worker lease ownership/expiry. fileciteturn48file0 fileciteturn56file0

This is distinct from the general application-event outbox and must remain distinct in CFIP ownership and contracts.

### Analysis execution

`0005_analysis_execution_runs` establishes durable analysis execution identity around `engine_id`, `engine_version`, status, input snapshot, parameters, data revision, request time, correlation/causation and result. Analytical execution is therefore reproducibility/state evidence rather than a transient function call. fileciteturn49file0

### AI / agent / learning / incidents

`0006_agent_ai_durability` establishes durable records for agent tasks, change proposals, learning records, incidents and AI inferences. Change proposals preserve affected paths, expected invariants, rollback plan and human-approval requirement; AI inference records preserve provider/model identity, model version, context/input snapshots, hashes and correlation/causation. fileciteturn52file0

### Settings / policy

`0007_admin_settings_i18n_ux_foundation` establishes scoped `admin_settings` with key, organization/user targeting, value, update actor and update time. This is evidence for scoped configuration; it is not evidence that every domain invariant should become a setting. fileciteturn53file0

### Event/replay/provenance

`0008_event_replay_provenance` establishes `event_outbox`, `replay_cases`, `provenance_nodes` and `provenance_edges`. Replay cases preserve input snapshots, expected invariants/output, data revision, engine versions, provenance references and dataset version. Provenance nodes/edges preserve revision/hash, relations and correlation. fileciteturn44file0

### Intelligence / learning

`0009_intelligence_learning` establishes intelligence snapshots containing direction, score, confidence, components, evidence references, contradiction IDs, rationale, data revision and engine versions. Learning feedback preserves subject, outcome, evidence, lesson, confidence and training approval. fileciteturn55file0

### Learning corpus / CI evidence

`0010_learning_corpora_ci_artifacts` establishes CI artifacts with pipeline/job/revision/content hash/evidence references and learning-corpus memberships with dataset version, content hash, license class, PIT verification and approval. fileciteturn54file0

### Evaluation / attribution / drift

`0011_durable_evaluation_outcomes_drift` establishes durable drift baselines, evaluation runs, outcome attributions and drift evaluations. These preserve dataset version, data revision, metrics, evidence/provenance and signal-level attribution. fileciteturn45file0

### Dataset integrity / intelligence memory

`0012_dataset_integrity_intelligence_memory` establishes dataset fingerprints containing content/schema/feature hashes, row count, data revision, rights verification and PIT verification. Intelligence memories preserve observed/available timestamps, data revision, dataset version, confidence, data/license class, rights verification and provenance/evidence references. fileciteturn42file0

## 4. Target ownership baseline

| Data class | Authoritative owner | Supporting technology | Rule |
|---|---|---|---|
| Identity/access | identity context | PostgreSQL | one transactional owner |
| Organization/workspace | organization/workspace context | PostgreSQL | tenant boundary, no cross-context writes |
| Instruments/reference | market_reference | PostgreSQL + analytical projections | canonical reference owner |
| Raw/canonical market observations | market_data | PostgreSQL control/outbox + ClickHouse analytical store | canonical pipeline owns semantics |
| Durable application events | eventing/realtime context | PostgreSQL outbox + NATS JetStream | transport does not own business state |
| Analysis execution evidence | analysis context | PostgreSQL | engine/version/PIT execution identity |
| Replay/provenance | replay/lineage context | PostgreSQL + justified artifact storage | immutable evidence semantics |
| Intelligence snapshots | intelligence/consensus context | PostgreSQL + projections | one authoritative analytical fusion boundary |
| Learning/evaluation/drift | learning_evaluation | PostgreSQL + analytical projections | temporal/leakage-aware evidence |
| AI/agent governance | ai_gateway/governance | PostgreSQL + immutable artifacts where needed | governed and auditable |
| Admin/runtime settings | configuration/entitlements | PostgreSQL | scope/actor/entitlement controlled |
| CI/evidence artifacts | governance/operations | PostgreSQL metadata + object storage when justified | hash/reference based |
| Cache/ephemeral coordination | infrastructure/cache | Redis | never unique business authority |
| Durable transport | infrastructure/eventing | NATS JetStream | not source of business truth |
| Large immutable artifacts | artifact/evidence boundary | object storage | only justified payloads |
| Document workloads | none by default | MongoDB only after explicit decision | no speculative Mongo ownership |

## 5. Cross-context access rules

A shared physical database does not imply shared ownership. A bounded context may read another context only through an explicit application/query contract, versioned event or approved projection. Direct cross-context writes to another context's tables are prohibited unless an explicit ADR establishes an exceptional transactional boundary.

## 6. Temporal / PIT semantics

The source schema repeatedly carries `data_revision`, dataset version, observed/available timestamps, engine versions, input snapshots, provenance references and PIT verification. CFIP data contracts must therefore distinguish event/observation time, availability time, ingestion/publication time where applicable, dataset version, data revision, engine/model version and provenance/evidence identity.

A record containing only `created_at` is insufficient for research, replay, backtest or learning-sensitive data.

## 7. Retention, deletion and recovery status

The inspected source migrations establish durable records and indexes but do not, by themselves, establish complete production retention, anonymization, backup/restore or regional residency policy for every entity. These remain bounded D3/D10 evidence gaps and must be resolved from later migrations, runtime configuration, deployment/operations evidence and executable policy.

The current source tree contains migration evolution beyond `0012`; this pass intentionally does not infer later table names or semantics from uninspected filenames. Those later migrations remain an explicit evidence-collection task.

## 8. D3 closure assessment

**D3: ADVANCED.**

Substantially evidenced:

- transactional ownership model;
- market-reference ownership;
- market-data/outbox separation;
- identity/workspace/provider ownership;
- analysis execution evidence;
- AI/agent governance persistence;
- replay/provenance persistence;
- intelligence/learning/evaluation/drift evidence;
- dataset/PIT/revision evidence;
- configuration scope model.

Remaining closure work:

1. exhaustive later migration census through the current source head;
2. complete table/column inventory;
3. ORM/repository read/write verification;
4. projection/materialized-read-model ownership;
5. deletion/anonymization behavior;
6. retention/partitioning policy;
7. backup/restore evidence;
8. regional/data-residency constraints;
9. cross-context query/write call graph;
10. reconciliation against every capability row.

No D3 capability is promoted to implemented or parity-verified by this document.
