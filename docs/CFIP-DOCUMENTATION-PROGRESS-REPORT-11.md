# CFIP Documentation Progress Report 11

**Migration:** CForex → CFIP  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD verified:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Date:** 2026-09-14  
**Gate:** Gate 0 — Source Closure  
**Status:** OPEN — evidence/documentation only

## 1. Control state

- `cforex-platform` remains permanently excluded from the migration path.
- CFIP runtime implementation remains **0% and LOCKED**.
- Gate 0 remains OPEN.
- Documentation and source-evidence work may continue.
- No parity claim is advanced by this report.
- Source evidence precedence remains executable implementation/tests → migrations/contracts → runtime/adapters → CI/operations → architecture docs → release prose.

## 2. This continuation's main correction: there are not two competing analysis engines

The CForex source was re-opened at the contract, domain registry and runtime layers.

The apparent “two analysis engines” are actually two infrastructure planes:

### A. V1 catalog / durable-execution plane

`fi_domain.analysis.registry.EngineRegistry` registers the framework-independent `EngineDescriptor` contract. It explicitly separates registration from execution.

The V1 analysis contracts also define `AnalysisRequest`, `AnalysisResult`, `AnalysisRunRecord`, execution lifecycle states and durable provenance hashes.

### B. V2 operational execution plane

`fi_application.analysis_engine.runtime.EngineRuntime` registers concrete executable engine objects through `EngineDescriptorV2`. It adds operational concerns such as:

- execution;
- latency budget enforcement;
- timeout counting;
- failure counting;
- bounded latency samples;
- transient health classification;
- exact/latest runtime descriptor lookup.

Therefore the source does **not** contain two independent analytical algorithms competing to decide the market. It contains two layers around the same analytical engine family:

`catalog/contract identity` versus `runtime execution/health`.

This separation is valid architecturally. The source problem is that an authoritative bridge/synchronization relationship between the V1 and V2 definitions is not yet proven.

## 3. Target decision: one canonical engine identity, separate projections

A new CFIP ADR was added:

`docs/adr/ADR-001-ANALYSIS-CATALOG-AND-RUNTIME-EXECUTION-PLANE.md`

The target decision is:

- one authoritative `(engine_id, version)` identity;
- one canonical engine contract/catalog;
- runtime execution metadata as a validated projection/extension;
- durable analysis as a separate execution use case where required;
- no duplicate authoritative engine registries;
- runtime activation requires catalog/contract consistency checks;
- specialist engines remain evidence producers;
- `AnalysisConsensusService` remains the sole authoritative consensus boundary.

This is a deliberate target improvement rather than a claim that CForex already implements this bridge.

## 4. Why keeping the separation is useful

The two planes should not simply be collapsed into one class because they have different responsibilities:

- catalog inspection must not require execution;
- runtime health and latency are operational state, not domain identity;
- durable analysis provenance/replay state has a different lifecycle from transient runtime health;
- low-latency trading evidence and durable research execution can be different application use cases;
- execution infrastructure must not leak into domain contracts.

The improvement is therefore **not “remove one engine”**. It is **remove duplicate authority** while preserving the valid separation of concerns.

## 5. New target release gate for engine consistency

CFIP will require a release-gated projection audit covering:

- engine ID/version;
- capability identity;
- input/output contracts;
- dependencies;
- determinism/reproducibility;
- timeframe support;
- warmup requirements;
- latency budget;
- failure policy;
- provenance requirements;
- replay/PIT requirements;
- runtime implementation presence;
- durable execution compatibility where applicable.

The audit must fail closed on conflicting authoritative definitions.

## 6. External standards / improvement pass

This continuation did not treat CForex as the only architectural authority.

Current external standards/guidance reviewed include:

- OpenTelemetry semantic conventions, including current guidance for common telemetry naming and GenAI observability.
- OWASP Top 10 for Agentic Applications 2026.
- OWASP current agentic security/governance guidance.

Target implications recorded in the migration plan:

- reuse stable OpenTelemetry semantic conventions instead of inventing duplicate telemetry vocabularies;
- keep sensitive AI prompt/tool content opt-in rather than default telemetry capture;
- explicitly test agent tool authorization, identity, memory, oversight and autonomous-action boundaries;
- preserve separation between analytical evidence and agent authority.

These are architectural improvements and security hardening requirements, not source-parity claims.

## 7. GitHub changes completed in this continuation

### Commit 1

`f9128d2ea6f3851f1239a4c7231b7360ca734d7f`

Created:

`docs/adr/ADR-001-ANALYSIS-CATALOG-AND-RUNTIME-EXECUTION-PLANE.md`

Purpose: formally resolve the “two analysis engines” architectural ambiguity and establish the target convergence rule.

### Commit 2

`ec962a56e4005fb89a43485adf69800ee8bdb23c`

Updated:

`docs/CFIP-MIGRATION-MASTER-PLAN.md`

Changes:

- canonical engine identity/projection rule added to Phase 3;
- engine projection audit added;
- current OWASP agentic-security review added to Phase 5;
- OpenTelemetry semantic-convention rule strengthened in operations;
- analytical/AI-specific release evidence strengthened.

## 8. D4 engine status after this pass

### Strong/closed evidence

- [x] 15 concrete runtime engine registrations identified.
- [x] 14 top-level engine namespaces distinguished from runtime inventory.
- [x] 2 runtime-only builtin engines identified.
- [x] 13 dedicated engines mapped to implementations.
- [x] runtime descriptors and versions identified.
- [x] runtime/fabric tests identified.
- [x] deterministic behavior coverage identified.
- [x] FVG causal behavior evidence identified.
- [x] durable `analysis_runs` schema identified.
- [x] durable repository implementation identified.
- [x] `AnalysisExecutionService` identified.
- [x] canonical provenance hash production identified.
- [x] V2 trading evidence route identified separately.
- [x] replay/provenance/dataset-integrity schemas identified.
- [x] architectural reason for V1/V2 separation established.
- [x] CFIP target convergence decision recorded.

### Still open

- [ ] production dependency wiring for durable analysis;
- [ ] authoritative V1↔V2 bridge in CForex;
- [ ] V2 route lifecycle/persistence relationship;
- [ ] canonical PIT snapshot/dataset producer;
- [ ] dataset fingerprint production path;
- [ ] replay-case loader/executor and ordering semantics;
- [ ] live/replay/backtest equivalence;
- [ ] per-engine golden/regression fixtures;
- [ ] durable engine telemetry/health history;
- [ ] exhaustive engine-like component census;
- [ ] D4/D7/D11 final reconciliation.

D4 remains **95% readiness**, because the new ADR improves target architecture but does not manufacture missing source evidence.

## 9. Gate 0 blockers remaining outside D4

- exhaustive API/WS registry;
- lifecycle-complete event registry;
- authoritative data ownership, PIT reconstruction, later-source migration, retention and recovery evidence;
- worker lifecycle/checkpoint/retry/scaling/deployment mapping;
- frontend workflow/chart/terminal mapping;
- capability-to-test mapping including negative/security/PIT/replay/regression coverage;
- policy/config/entitlement/feature-flag classification;
- adapter inventory/security/failure/health behavior;
- operations/SLO/backpressure/scaling/recovery/rollback evidence;
- final D11 cross-document reconciliation.

## 10. Updated evidence-readiness dashboard

| Dimension | Current readiness | State |
|---|---:|---|
| Target architecture | **100%** | established |
| Migration control framework | **98%** | established; Gate 0 open |
| Capability registry | **96%** | advanced |
| Documentation integration | **99%** | advanced |
| D1 API/WS | **74%** | advanced; exhaustive registry open |
| D2 Events | **69%** | advanced; lifecycle closure open |
| D3 Data ownership/PIT | **73%** | advanced; producer/reconstruction/retention closure open |
| **D4 Engines** | **95%** | strongly evidenced; integration/replay closure open |
| D5 Workers/runtime | **72%** | advanced; lifecycle mapping open |
| D6 Frontend | **40%** | in progress |
| D7 Tests | **36%** | in progress |
| D8 Policy/config | **47%** | in progress |
| D9 Adapters | **35%** | in progress |
| D10 Operations | **32%** | in progress |
| D11 Reconciliation | **12%** | ADR/control reconciliation begun; not formal closure |

The unweighted D1–D11 indicator recalculated from the listed values is approximately **53.2%**. This is only a documentation/evidence planning indicator; it is not implementation progress and is not a Gate 0 exit criterion.

## 11. Important interpretation

The phrase “two analysis engines” should not be carried into CFIP as two competing engines.

The correct model is:

`one analytical capability family → canonical engine identity/contract → runtime executor + durable execution projections → normalized evidence → AnalysisConsensusService`

This preserves the source's valid boundaries while eliminating target-level ambiguity and registry drift.

## 12. Next source pass

The next continuation remains evidence-first:

1. trace all composition/bootstrap paths around `AnalysisExecutionService` and its repository dependency;
2. trace producers/consumers for `dataset_fingerprints` and `replay_cases`;
3. trace PIT market-data reconstruction and availability watermark semantics;
4. trace any remaining V1/V2 registration bridge or adapter;
5. trace durable engine telemetry/event projection;
6. locate and assess per-engine golden/regression fixtures;
7. reconcile engine evidence with D7 tests;
8. expand D11 cross-document reconciliation;
9. continue API/events/data/workers/frontend/policy/adapter/operations closure in parallel as evidence becomes available.

No CFIP runtime implementation is authorized before Documentation Freeze and Gate 0 closure.
