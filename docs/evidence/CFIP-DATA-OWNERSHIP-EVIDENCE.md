# CFIP Data Ownership Evidence

**Source:** `armanemp/CForex` `main` v0.9.154
**Target:** `armanemp/CFIP` `main`
**Workstream:** D3 — Data ownership evidence
**Status:** advanced; closure remains open

## Purpose

Establish one authoritative owner for each durable business entity and distinguish transactional state, analytical projections, cache state, durable event transport and immutable artifacts.

## Source runtime evidence

The general worker creates a PostgreSQL SQLAlchemy engine/session factory, NATS JetStream runtime, ClickHouse client/schema, durable PostgreSQL event outbox, canonical-observation outbox, ClickHouse consumer/writer and realtime runtime state/ledger/sink. This proves that CForex already separates transactional/outbox state, durable transport, analytical projection and realtime runtime state.

## Target ownership baseline

| Data class | Authoritative target owner | Non-authoritative consumers |
|---|---|---|
| Identity, organization, workspace | PostgreSQL/domain owner | cache/read projections |
| Market reference/instrument identity | PostgreSQL/domain owner | ClickHouse/read projections |
| Provider mappings/capabilities | PostgreSQL/integration owner | cache |
| Durable event outbox | PostgreSQL/eventing owner | NATS |
| Canonical high-volume observations | ClickHouse/market-data analytical owner | Redis/realtime projections |
| Realtime ephemeral state | Redis/runtime owner where appropriate | API/UI |
| Analysis/evaluation/governance records | PostgreSQL/application owner | analytical projections |
| Large immutable research/model/result artifacts | object storage when justified | PostgreSQL metadata |
| Document-oriented auxiliary intelligence | MongoDB only after demonstrated workload | projections |

## Cross-context rule

A shared physical database does not imply shared ownership. A bounded context may read another context only through an explicit application/query contract or approved projection. Direct cross-context writes are prohibited unless the owning contract explicitly defines them.

## PIT and revision requirements

Market and research data used for analysis, replay, backtest and learning must retain enough identity to reconstruct the point-in-time view. At minimum the target evidence model must preserve dataset identity/version, observation/event time, ingestion/observation provenance, revision identity and relevant provider/source identity. Learning already demonstrates deterministic data-revision fingerprinting over ordered journal outcomes.

## D3 closure gaps

- exhaustive table/entity inventory;
- authoritative column ownership;
- foreign-key/cross-context access inventory;
- projection/materialized-view ownership;
- retention and partitioning policy per high-volume entity;
- PIT/revision semantics per mutable or corrected data family;
- deletion/anonymization obligations;
- backup/restore ownership;
- analytical projection freshness guarantees;
- cache invalidation authority;
- explicit evidence for any MongoDB/document workload.

No entity is considered migrated until one authoritative owner and its write/read boundary are explicit.
