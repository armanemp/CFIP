# CFIP Documentation Progress Report 12

**Migration:** CForex → CFIP  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Date:** 2026-09-14  
**Gate:** Gate 0 — Source Closure  
**Status:** OPEN — evidence/documentation only

## 1. Continuation objective

This pass continued the source-first migration study and refined the analysis architecture decision. The objective was not to preserve CForex's structure mechanically. The target is required to be modern, standard, scalable and maintainable while preserving source behavior where parity is required.

## 2. Control state

- `cforex-platform` remains permanently excluded from the migration path.
- CFIP runtime implementation remains **0% and LOCKED**.
- Gate 0 remains OPEN.
- Documentation, source inspection, evidence extraction and target-architecture improvement may continue.
- No parity claim is advanced by this report.
- CForex executable implementation/tests remain behavioral source truth until parity closure.
- External standards can improve CFIP architecture, but such improvements must be explicitly classified as target divergence rather than falsely attributed to CForex.

## 3. Critical answer: should CFIP have two analysis engines?

**No — CFIP should not have two independent analytical implementations that compete or calculate the same capability twice.**

**Yes — CFIP should retain two execution/application planes when their operational requirements differ.**

The distinction is essential.

CForex exposes:

1. a V1 durable/application execution path through `AnalysisExecutionService`;
2. a V2 low-latency trading evidence path through `AnalysisFabric → EngineRuntime`.

The V1 service registers an `AnalysisEngine`, selects it through `EngineRegistry`, computes canonical parameter/input/engine hashes, persists lifecycle state when a repository is supplied, and can publish analysis lifecycle events. The source implementation was re-read directly during this pass.

The V2 runtime registers executable engine objects, enforces latency budgets, records timeout/failure counters and transient latency/health state, and is used by the trading evidence path.

These are different execution requirements, not two market opinions.

## 4. Target architecture decision

The preferred CFIP architecture is:

```text
                Canonical Engine Contract / Catalog
                              │
                    authoritative identity
                         (engine_id, version)
                              │
              ┌───────────────┴────────────────┐
              │                                │
      Runtime Execution Projection       Durable Run Projection
              │                                │
      low-latency evidence              research/replay/audit
              │                                │
              └───────────────┬────────────────┘
                              ▼
                       Engine Evidence
                              ▼
                  AnalysisConsensusService
                              ▼
                     Decision / Risk
```

### Decision

- **One canonical engine identity.**
- **One analytical implementation per semantic engine version.**
- **Separate runtime and durable execution adapters/use cases.**
- **No duplicate authoritative registries.**
- **No duplicate trading-vs-backtest algorithms unless semantic divergence is intentional, versioned and ADR-governed.**
- **Runtime activation must validate against the canonical contract.**
- **Consensus remains a separate authoritative boundary.**

This is more modern and safer than either of the two extremes:

- duplicating the same engine in two runtimes;
- or forcing low-latency trading, durable research, persistence and operational health into one giant engine class.

## 5. Why the execution planes should remain separate

### Interactive/trading path

Needs:

- strict latency budgets;
- bounded concurrency;
- timeout/failure policy;
- transient health;
- minimal synchronous persistence;
- partial-result policy where allowed;
- workload isolation from heavy replay/research jobs.

### Durable/research path

Needs:

- durable run identity;
- lifecycle states;
- input/data revision;
- parameter/input/engine fingerprints;
- provenance;
- replayability;
- durable result/error state;
- auditability.

Merging both into one runtime abstraction would couple analytical computation to persistence and operational infrastructure. It would also allow replay/research load to interfere with interactive trading analysis.

Therefore the target rule is:

> **Separate execution planes, shared analytical contract and implementation identity.**

## 6. Why the analytical implementation should normally be shared

If an engine represents a deterministic semantic capability, its implementation should be reused by both execution planes.

Example:

`fvg.causal@1.2.0`

should not become:

- `fvg.trading@1.2.0`
- `fvg.backtest@1.2.0`

merely because the callers differ.

Both callers should use the same versioned engine contract and deterministic implementation against explicit execution context.

A second implementation is justified only if the semantics genuinely differ. In that case the divergence must be explicit, versioned, documented, independently tested, provenance-visible, parity-classified and governed by ADR/change control.

## 7. Source finding from this pass

The CForex `AnalysisExecutionService` source confirms that the durable V1 path is not merely a passive contract. It can:

- persist REQUESTED/VALIDATING/RUNNING/terminal states through `AnalysisRunRepository` when injected;
- calculate SHA-256 canonical hashes for parameters, input snapshot and engine descriptor;
- produce `AnalysisProvenance`;
- emit lifecycle events through an injected publisher;
- resolve executable engines through the V1 registry.

This strengthens the earlier evidence that the source contains two real application execution paths, while still not proving production wiring of the durable service.

GitHub code-search attempts for the durable service/repository and replay/dataset identifiers returned no indexed call sites in this pass. This remains **bounded negative evidence only**, not proof of repository-wide absence.

## 8. Target improvements beyond CForex

The target will add or require the following improvements rather than copying source ambiguity:

### Canonical projection consistency

A release gate must compare the canonical descriptor against runtime projections and durable execution metadata for identity/version, input/output contracts, capability, dependencies, determinism, timeframe support, warmup, latency budget, failure policy, provenance and PIT/replay requirements.

### Duplicate implementation detection

The target architecture should detect multiple implementations claiming the same canonical `(engine_id, version)` unless explicitly marked as an approved adapter/deployment projection.

### Workload isolation

Low-latency analysis must not share an unbounded execution pool with heavy replay/backtest/research workloads.

### Durable telemetry

Transient runtime health must be distinguished from durable historical operational evidence. The latter requires an explicit persistence/event strategy rather than assuming an in-memory snapshot is sufficient.

### Standardized observability

OpenTelemetry semantic conventions should be reused where applicable. Custom telemetry fields require explicit justification.

### Agentic security

AI/agent authority remains outside analytical engine authority. Agents can request governed analysis capabilities through tools but must not gain direct persistence/infrastructure authority.

## 9. D4 status

D4 remains **95% evidence readiness**.

### Strong evidence

- 15 concrete runtime registrations.
- 14 top-level engine namespaces.
- 2 runtime-only builtin engines.
- 13 dedicated engines mapped.
- runtime descriptors/versions.
- deterministic runtime/fabric tests.
- FVG causal behavior.
- durable `analysis_runs` schema.
- repository implementation.
- `AnalysisExecutionService` implementation.
- canonical provenance hashes.
- V2 trading evidence route.
- replay/provenance/dataset-integrity schemas.
- explicit V1/V2 architectural interpretation.
- CFIP canonical identity/execution-plane ADR.

### Open evidence

- production wiring of durable analysis;
- authoritative V1/V2 bridge;
- V2 route persistence relationship;
- PIT snapshot/dataset producer;
- dataset fingerprint producer;
- replay-case loader/executor/order semantics;
- live/replay/backtest equivalence;
- per-engine golden/regression fixtures;
- durable engine telemetry/history;
- exhaustive engine-like component census;
- D4/D7/D11 reconciliation.

## 10. Gate 0 dashboard

| Dimension | Readiness | State |
|---|---:|---|
| Target architecture | **100%** | established |
| Migration control framework | **98%** | established; Gate 0 open |
| Capability registry | **96%** | advanced |
| Documentation integration | **99%** | advanced |
| D1 API/WS | **74%** | advanced; exhaustive registry open |
| D2 Events | **69%** | advanced; lifecycle closure open |
| D3 Data ownership/PIT | **73%** | advanced; producer/reconstruction/retention closure open |
| **D4 Engines** | **95%** | strong; execution/replay/fixture closure open |
| D5 Workers/runtime | **72%** | advanced; lifecycle mapping open |
| D6 Frontend | **40%** | in progress |
| D7 Tests | **36%** | in progress |
| D8 Policy/config | **47%** | in progress |
| D9 Adapters | **35%** | in progress |
| D10 Operations | **32%** | in progress |
| D11 Reconciliation | **12%** | begun; not formal closure |

Unweighted D1-D11 planning indicator remains approximately **53.2%**. This is not implementation progress and is not a Gate 0 exit criterion.

## 11. Current architectural conclusion

The target should **not** become a system with two competing analysis engines.

It should become a system with:

`one canonical engine capability + one versioned implementation identity + multiple governed execution modes`

where the execution modes are separated only because their operational requirements differ.

This is the selected modern architecture because it minimizes semantic drift, avoids duplicated algorithms, preserves low-latency isolation, supports durable research/replay, and remains compatible with horizontal scaling.

## 12. Next work

Continue evidence-first closure across:

1. durable analysis production wiring;
2. PIT/data fingerprint production;
3. replay-case production and execution;
4. V1/V2 bridge evidence;
5. durable engine telemetry;
6. golden/regression fixtures;
7. D4/D7 reconciliation;
8. API/WS, events, data, workers, frontend, policy, adapters and operations closure;
9. final D11 reconciliation;
10. external standards review for material architectural/security/performance improvements.

No CFIP runtime implementation is authorized before Documentation Freeze and formal Gate 0 closure.
