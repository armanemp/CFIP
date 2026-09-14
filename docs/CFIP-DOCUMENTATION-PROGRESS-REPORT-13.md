# CFIP Documentation Progress Report 13

**Migration:** CForex → CFIP  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Date:** 2026-09-14  
**Gate:** Gate 0 — Source Closure  
**Status:** OPEN — evidence/documentation only

## 1. Continuation objective

This pass re-checked the migration control documents first, then re-inspected the current CForex source around the durable analysis path and API composition root. The purpose was to replace assumptions with executable evidence, identify source-path asymmetries that could affect CFIP design, and improve the migration control model where the existing documentation was too broad.

The target remains a modern, standard, globally scalable architecture. CForex behavior is preserved where parity requires it, but source ambiguities are not copied into CFIP as accidental architecture.

## 2. Control-state verification

- `cforex-platform` remains permanently excluded from the migration path.
- CForex `main` remains the behavioral source of truth at v0.9.154 / `900882154cab3b9b74d0543b9bbf72a708a08134`.
- CFIP runtime implementation remains **0% and LOCKED**.
- Gate 0 remains **OPEN**.
- Documentation and source-evidence work may continue.
- No capability is promoted to parity or implementation merely because its source documentation is complete.
- The current control index, master plan, source-evidence matrix, engine evidence and analysis execution-plane ADR remain mutually consistent after this pass.

## 3. Source re-check: durable analysis wiring

The source contains a concrete durable analysis implementation:

- `packages/application/src/fi_application/analysis/service.py` defines `AnalysisExecutionService`.
- `packages/infrastructure/src/fi_infrastructure/analysis.py` defines `SqlAlchemyAnalysisRunRepository`.
- The source persistence model contains durable `analysis_runs` state.
- The application service can persist requested/validating/running/terminal lifecycle states when the repository is injected, calculate canonical SHA-256 parameter/input/engine fingerprints, construct provenance and publish lifecycle events when a publisher is injected.

A new direct re-check of the CForex API composition root (`apps/api/src/fi_api/main.py`) shows that its visible application composition imports PostgreSQL/ClickHouse-backed infrastructure, usage/entitlement services, workspace/realtime services and other platform services, but does **not** visibly construct `AnalysisExecutionService` or `SqlAlchemyAnalysisRunRepository` in the inspected composition root.

Repository code-search queries for `AnalysisExecutionService`, `SqlAlchemyAnalysisRunRepository` and `analysis_run` did not return indexed call sites. This is recorded as **bounded negative evidence only** because GitHub code-search indexing is not an authoritative proof of repository-wide absence.

### Consequence

The migration documentation must not say that the durable analysis service is production-wired. The accurate source statement is:

> **Durable analysis execution is concretely implemented at application/infrastructure level, but production composition/wiring and its relationship to the V2 trading evidence route remain unverified.**

This is stronger and more precise than either treating the service as merely contractual or assuming that its existence proves production usage.

## 4. Source re-check: V1/V2 analysis asymmetry

The source still shows two execution/application paths around the same analytical capability family:

```text
Canonical analytical identity / contract
              │
       ┌──────┴──────┐
       │             │
 Durable V1       Runtime V2
 Analysis         Trading Evidence
ExecutionService  AnalysisFabric
       │             │
 Repository       EngineRuntime
       │             │
 durable run     low-latency evidence
       └──────┬──────┘
              ▼
       common engine semantics
```

The target decision remains:

- one canonical `(engine_id, version)` identity;
- one authoritative analytical implementation per semantic version;
- separate runtime and durable execution projections/adapters;
- no duplicate analytical algorithms merely for workload differences;
- explicit, versioned and ADR-governed divergence only when semantics genuinely differ;
- a single authoritative `AnalysisConsensusService` boundary above specialist evidence.

The distinction is operational, not a permission to create two competing analytical engines.

## 5. Source re-check: API composition boundary

The CForex API composition root confirms a broad platform boundary rather than a trading-only application. The inspected source visibly composes authentication/authorization, realtime, admin settings/autonomy/intelligence surfaces, trading, integrations, public intelligence, browser performance, research, Git/admin and billing/identity infrastructure, together with database and analytical dependencies.

This reinforces an important CFIP target rule:

> The API layer is an inbound composition/adaptation boundary; capability ownership remains in bounded contexts/application services, not in route modules.

The target must therefore avoid mechanically copying the growing CForex route module into one oversized controller. Capability ownership, query/read-model composition and command handling should remain explicit and testable.

## 6. Improvement: make execution-wiring evidence a first-class Gate 0 requirement

The previous Gate 0 plan tracked durable analysis existence and general engine evidence, but source existence alone is insufficient for migration closure. This pass therefore promotes **execution wiring evidence** to an explicit closure dimension.

For each durable or runtime capability, Gate 0 evidence should distinguish:

1. contract exists;
2. implementation exists;
3. adapter/repository exists;
4. composition/bootstrap wiring exists;
5. production entrypoint invokes it;
6. tests exercise the production path;
7. operational telemetry/recovery is present;
8. parity relationship with alternate execution paths is explicit.

This prevents a common migration error: treating a complete class or repository as equivalent to an operationally reachable feature.

## 7. Improvement: source search evidence classification

Migration documents now use the following rule for repository search:

- **Positive indexed evidence:** a search result identifies a concrete source location.
- **Bounded negative evidence:** a search returns no indexed result, but the search index/completeness cannot prove absence.
- **Verified absence:** only an exhaustive source/tree/entrypoint inspection establishes that a capability is absent.

GitHub code-search no-result responses must never be promoted directly to "not implemented" or "unused".

## 8. Improvement: target architecture for scalable execution

CFIP should retain explicit workload classes instead of allowing all analytical work into one unconstrained executor:

| Workload | Primary requirement | Target isolation |
|---|---|---|
| Interactive/live analysis | predictable low latency | bounded runtime pool |
| User replay | deterministic repeatability | replay worker pool |
| Backtest/research | throughput and long-running execution | research/backtest pool |
| Durable audit/reconstruction | persistence and provenance | durable execution pipeline |
| Learning/evaluation | temporal isolation and artifact production | evaluation/learning workers |

The same engine implementation can be reused where semantics are identical. Workload isolation is an execution concern, not an engine duplication mechanism.

## 9. Improvement: observability and provenance separation

Transient `EngineHealthSnapshot`-style runtime health is not a substitute for durable operational history. CFIP should model these as separate concerns:

- **runtime health:** bounded in-memory/fast operational state used for admission and degradation;
- **execution telemetry:** standardized OpenTelemetry traces/metrics/logs/events;
- **durable analysis evidence:** run identity, input/data revision, hashes, provenance and result/error state;
- **historical operational evidence:** persisted/evented execution outcomes when required for SLO analysis, incident investigation or model/engine reliability evaluation.

Sensitive AI/tool content must remain opt-in for telemetry; identifiers, timings, status and provenance should be preferred over raw content.

## 10. D4 update

D4 remains **advanced and not closed**.

### Confirmed

- 15 concrete runtime engine registrations.
- 14 top-level engine namespaces.
- 2 runtime-only builtin engines.
- Dedicated engine implementations and runtime descriptors.
- V1 durable `AnalysisExecutionService` implementation.
- PostgreSQL `AnalysisRunRepository` implementation.
- Canonical parameter/input/engine fingerprints.
- V2 `AnalysisFabric`/`EngineRuntime` execution path.
- Direct runtime/fabric tests.
- Replay/provenance/dataset-integrity schema evidence.
- Canonical one-engine-identity/two-execution-plane target decision.

### Still open

- production composition/wiring of the durable V1 service;
- authoritative V1↔V2 registration bridge;
- exact persistence relationship of the V2 trading evidence route;
- authoritative PIT snapshot/data reconstruction;
- dataset fingerprint producers/consumers;
- replay-case producer/loader/executor and event-order semantics;
- live/replay/backtest equivalence;
- per-engine golden/regression fixtures;
- durable engine telemetry/history;
- exhaustive engine-like component census;
- D4↔D7↔D11 reconciliation.

## 11. Cross-document consistency check

The following controlled documents were re-read or checked during this continuation:

- `docs/CFIP-MIGRATION-CONTROL-INDEX.md`
- `docs/CFIP-MIGRATION-MASTER-PLAN.md`
- `docs/CFIP-DOCUMENTATION-PROGRESS-REPORT-12.md`
- `docs/capabilities/source-evidence-matrix.md`
- `docs/adr/ADR-001-ANALYSIS-CATALOG-AND-RUNTIME-EXECUTION-PLANE.md`

No contradictory Gate 0 state was found. The only material documentation improvement required by this pass was to make execution-wiring evidence explicit and to tighten the classification of negative search evidence.

## 12. Gate 0 dashboard

| Dimension | Readiness | Current interpretation |
|---|---:|---|
| Target architecture | **100%** | established; continued refinement |
| Migration control framework | **99%** | execution-wiring evidence promoted to explicit closure requirement |
| Capability registry | **96%** | advanced |
| Documentation integration | **99%** | advanced; cross-document consistency maintained |
| D1 API/WS | **75%** | composition boundary confirmed; exhaustive endpoint registry still open |
| D2 Events | **69%** | advanced; lifecycle/consumer closure open |
| D3 Data ownership/PIT | **73%** | advanced; producer/reconstruction/retention closure open |
| **D4 Engines** | **96%** | durable implementation and runtime asymmetry strongly evidenced; wiring/replay/fixtures open |
| D5 Workers/runtime | **73%** | execution workload isolation and lifecycle mapping advanced |
| D6 Frontend | **40%** | in progress |
| D7 Tests | **37%** | in progress; production-path coverage still open |
| D8 Policy/config | **47%** | in progress |
| D9 Adapters | **35%** | in progress |
| D10 Operations | **33%** | in progress; durable telemetry/recovery mapping open |
| D11 Reconciliation | **15%** | execution-path reconciliation now explicit |

Unweighted D1-D11 planning indicator is approximately **53.8%**. This is a documentation/evidence planning indicator only, not implementation progress and not a Gate 0 exit criterion.

## 13. Next source-closure passes

Continue in this order:

1. trace the complete CForex composition/bootstrap graph for analysis, replay, dataset integrity and learning services;
2. trace dataset-fingerprint producers and consumers;
3. trace replay-case producers/loaders/executors and ordering guarantees;
4. trace authoritative PIT market-data reconstruction and watermarks;
5. trace V1/V2 engine registry/activation relationship;
6. trace durable engine telemetry and event producers/consumers;
7. locate per-engine golden/regression fixtures and map them to capability contracts;
8. extend D1/D2/D3/D5/D7/D10 evidence from the same execution-wiring standard;
9. perform a whole-document reconciliation pass before any Gate 0 closure proposal;
10. continue external standards review for material improvements in scalability, observability, security and AI/agent governance.

**Gate 0 remains OPEN. No CFIP runtime implementation is authorized by this report.**
