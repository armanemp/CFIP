# CFIP 2026-09 Standards and Target Improvements

**Date:** 2026-09-15  
**Scope:** migration architecture, runtime contracts, observability and documentation governance  
**Gate:** Gate 0 — controlled target implementation permitted; production promotion remains locked

## 1. Standards baseline refresh

Current OpenTelemetry Semantic Conventions are the preferred baseline for common HTTP, database, messaging, events, logs, metrics, traces, resources and related telemetry semantics. CFIP should reuse standard attributes before creating project-specific attributes. New attributes require a concrete operational use case, documented type/meaning/sensitivity and a stability strategy. citeturn0search0turn0search1

Telemetry evolution is a compatibility surface: changes that can break dashboards, alerts or consumers require controlled schema/version handling rather than casual renaming. OpenTelemetry's event guidance also distinguishes point-in-time events from duration-bearing spans and recommends stable, domain-specific event names with documented attributes. citeturn0search10turn0search4

## 2. Target improvements confirmed

### 2.1 Contract-first observability

CFIP uses:

`standard semantic convention → stable CFIP extension only when necessary → versioned telemetry schema → dashboards/alerts/tests`

Telemetry is observational and cannot become an implicit correctness store.

The realtime contract now explicitly represents a low-cardinality `RealtimeTelemetrySnapshot` containing queue depth, capacity, consumer lag, event-time watermark, lateness, processing latency and bounded backpressure action. The snapshot is immutable and observational; durable checkpoints, leases, event logs and domain state remain authoritative.

### 2.2 Realtime session isolation

The target separates:

`durable market event stream → realtime processing state → client session/WebSocket`

Client queues and subscriptions are edge state, not the authoritative market/replay ledger.

### 2.3 Synthetic/demo data isolation

Synthetic/demo observations receive explicit provenance and data classification. Demo defaults cannot leak into provider/live semantics, entitlement decisions or historical datasets.

### 2.4 One analytical identity

There remains exactly one canonical `(engine_id, version)` identity and one semantic implementation per version. Runtime, durable and replay projections may differ operationally but must consume the same engine contract and produce traceable evidence.

### 2.5 Evidence graph before implementation

A capability advances only when the chain is reconstructable:

`source → contract → owner → use case → port → adapter → data/event/API/UI → composition → production path → tests → telemetry/recovery → parity`

This reduces rework because target implementation starts only after the semantic dependencies are known.

### 2.6 Global-scale correctness state

Local memory may accelerate execution but cannot be the sole authority for state whose loss or duplication changes correctness. Such state requires explicit partition ownership, leases/checkpoints, persistence and recovery semantics.

### 2.7 Configuration classification

CFIP will not blindly remove every literal. Immutable domain invariants remain code/contracts. Deploy/runtime settings, workspace/tenant policy, entitlements, provider capabilities and governed policies become explicit configuration surfaces where appropriate.

## 3. New architecture guardrails

1. No direct vendor SDK dependency from domain contexts.
2. No API route may become a hidden domain-service registry.
3. No frontend component may become the source of market semantics.
4. No client WebSocket state may become the replay source of truth.
5. No synthetic/demo data may enter canonical licensed-data datasets without explicit classification and provenance.
6. No telemetry attribute containing sensitive AI/tool content is captured by default.
7. No agent action is authorized solely because an analytical engine recommends it.
8. No new datastore is introduced solely for fashion; ownership, consistency, retention, backup and workload evidence are mandatory.
9. No microservice split is accepted without measured scaling, isolation, ownership or security justification.
10. No documentation status may imply runtime parity without executable evidence.
11. Realtime operational telemetry must remain low-cardinality, bounded and non-authoritative; correctness state is persisted through its explicit ownership boundary.
12. Realtime telemetry schema changes must be compatibility-reviewed before changing dashboards, alerts or consumers.

## 4. Speed without loss of rigor

Investigation can proceed in parallel across API, events, data/PIT, engines, workers, frontend, tests, policy/config, adapters and operations. Canonical status changes remain serialized through a reconciliation barrier.

The fastest safe unit is a **closure packet** containing direct source evidence, target implication, unresolved questions, and verification references. This avoids repeatedly rereading the same source surface while preventing unsupported closure claims.

## 5. Verification boundary

The realtime telemetry contract and its focused tests have been added to the target. Repository read-back verifies the intended source changes; executable CI remains the authoritative final verification surface.

This batch does **not** claim:

- live broker integration;
- durable checkpoint/lease repository integration;
- PostgreSQL runtime migration evidence;
- production telemetry backend readiness;
- global-scale capacity;
- production readiness.

## 6. Gate impact

These improvements remain Gate-0-compatible. Controlled implementation is permitted when source-evidenced, contract-first, reversible and testable. Gate 1 and production promotion remain separately gated by their required evidence.
