# CFIP Documentation Completion Plan

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** documentation-first; implementation intentionally held until documentation freeze.

## Purpose

Complete and integrate the migration documentation and executable evidence before broad CFIP implementation. The objective is to eliminate material ambiguity about CForex behavior, ownership, contracts, runtime topology and verification requirements.

This plan complements, and does not replace, `docs/CFIP-MIGRATION-CONTROL-INDEX.md`, `docs/CFIP-MIGRATION-MASTER-PLAN.md` or `docs/CFIP-GATE-0-SOURCE-CLOSURE.md`.

## Canonical documentation stack

1. `CFIP-MIGRATION-CONTROL-INDEX.md` — authoritative continuation rules and gate control.
2. `CFIP-MIGRATION-MASTER-PLAN.md` — migration sequence and release gates.
3. `CFIP-ARCHITECTURE-GUIDE.md` — target architecture and invariants.
4. `capabilities/source-study-integration.md` — evidence and parity method.
5. `CFIP-GATE-0-SOURCE-CLOSURE.md` — active evidence closure register.
6. `capabilities/CFIP-CAPABILITY-REGISTRY.md` — capability inventory and target ownership.
7. `capabilities/source-evidence-matrix.md` — source evidence map.
8. `capabilities/parity-matrix.md` — capability lifecycle and parity obligations.
9. `CFIP-SOURCE-TREE.md` — target ownership grammar.
10. This document — documentation completion sequence and freeze criteria.

If documents disagree, evidence precedence in the Control Index applies and the disagreement must be resolved before implementation continues.

## Completion workstreams

### D1 — Source/API evidence

Produce an exhaustive HTTP and WebSocket registry covering method/path or channel, owner, request/response schema, status/error behavior, authentication, workspace scope, entitlement, audit requirements, UI callers, event side effects and tests.

### D2 — Event evidence

Produce a producer/consumer registry covering event identity, version, subject, schema, producer, consumers, partition key, ordering, idempotency, retry/quarantine, replayability, retention and security classification. Keep application realtime snapshot/incremental delivery distinct from durable event transport.

### D3 — Data ownership

Map entities, tables and material columns to one authoritative bounded-context owner. Record read/write boundaries, derived projections, PIT/revision semantics, retention and cross-context access rules.

### D4 — Engine evidence

Map every executable analytical engine to its behavioral contract, deterministic parameter serialization, version descriptor, PIT input fingerprint, dependencies, failure semantics, provenance, golden fixtures, replay/backtest compatibility and observability contract.

### D5 — Runtime/worker evidence

Map API, worker, learning-worker and autonomy-worker entrypoints, scheduled jobs, subscriptions, producers, consumers, checkpoints/watermarks, concurrency, retries, shutdown, health and scaling assumptions.

### D6 — Frontend evidence

Map every meaningful route and interaction to capability, API/query/mutation, realtime channel, authentication, state, loading/error/empty behavior, i18n, RTL/LTR, accessibility, telemetry and tests. Preserve chart and terminal semantics rather than merely page names.

### D7 — Test evidence

Build capability-to-test coverage including positive, negative, security, authorization, PIT, replay, deterministic-engine, event-contract, migration/rollback, accessibility and performance cases. Missing tests become explicit gaps, never implied coverage.

### D8 — Policy/configuration evidence

Classify every setting as immutable domain invariant, deployment configuration, runtime operational setting, tenant/workspace setting, entitlement, feature flag or governed policy. Record legitimate constants separately from hardcoded policy.

### D9 — Adapter evidence

Inventory market-data providers, brokers, model providers, research sources and other external integrations. Record capability discovery, credentials boundary, rate limits, retries, normalization, failure modes, entitlements, provenance and isolation requirements.

### D10 — Operations evidence

Define runtime roles, SLOs, health/readiness/liveness, capacity dimensions, partitioning, retention/compaction, backup/restore, disaster recovery, rollback, observability, security posture and regional/data-residency requirements where applicable.

### D11 — Cross-document reconciliation

After D1–D10, reconcile the capability registry, source evidence matrix, parity matrix, source tree, architecture guide, master plan and Gate 0 register. Every capability must have one canonical owner and no contradictory lifecycle state.

## Evidence rule

A documentation statement is not authoritative merely because it sounds plausible. High-impact claims must be traceable to executable CForex evidence, migrations/contracts, runtime composition or verified operational configuration according to the established evidence hierarchy.

## Documentation freeze criteria

Documentation may be declared frozen for implementation when:

- all high-impact source capabilities are mapped;
- exhaustive API/WS evidence is complete or every residual item has an explicit bounded gap and owner;
- durable event families have lifecycle semantics;
- authoritative data ownership is unambiguous;
- executable engines have contract/test/PIT evidence;
- workers and frontend workflows are mapped;
- tests are mapped to capabilities and missing coverage is explicit;
- policy/config/entitlement classification is complete;
- external adapters are inventoried;
- operational obligations are explicit;
- all cross-document contradictions are resolved;
- intentional target divergences have ADRs and preserved source evidence;
- the parity matrix contains the evidence required for each implementation unit.

Documentation freeze does **not** mean every CForex feature is already implemented in CFIP. It means implementation can proceed without material semantic guessing.

## Implementation hand-off

Once the freeze criteria are satisfied, the first implementation milestone is Gate 1 Foundation and must establish a complete verified vertical slice:

`contract → domain → use case → port → adapter → persistence/event → API/realtime → tests → observability`

Only after that slice passes its gates should capability implementation expand.

## Progress accounting

Progress is reported in two separate dimensions:

- **Documentation/evidence readiness:** percentage of required closure work with verified evidence.
- **CFIP implementation:** percentage of capabilities actually implemented and verified in the target.

The second percentage must remain zero until executable target implementation exists; documentation progress must never be presented as implementation progress.
