# ADR-001 — Analysis Catalog and Runtime Execution Plane

**Status:** Accepted as migration target decision; source evidence still under Gate 0 closure  
**Date:** 2026-09-14  
**Source baseline:** CForex `main` v0.9.154 (`900882154cab3b9b74d0543b9bbf72a708a08134`)  
**Target:** CFIP

## Context

CForex contains two analytical infrastructure layers that can look like “two analysis engines” if read only by package names:

1. `fi_domain.analysis.registry.EngineRegistry` using the V1 `EngineDescriptor` contract.
2. `fi_application.analysis_engine.runtime.EngineRuntime` using the V2 `EngineDescriptorV2` contract and executable engine objects.

The V1 registry explicitly separates registration/catalog metadata from execution. The V2 runtime performs execution, timeout enforcement and in-memory health/latency accounting. The V1 durable execution contract additionally models `AnalysisRequest`, `AnalysisResult`, `AnalysisRunRecord` and provenance hashes.

The source also exposes two distinct application execution paths:

- **Durable/V1 path:** `AnalysisExecutionService → EngineRegistry → AnalysisEngine → AnalysisRunRepository` with optional lifecycle publishing and canonical input/parameter/engine hashes.
- **Low-latency/V2 evidence path:** `WorkspaceService.snapshot → AnalysisFabric → EngineRuntime → EngineOutput → evidence projection` in the trading analysis route.

These are therefore not two independent analytical algorithms producing competing market opinions. They are separate infrastructure/application execution planes around the same analytical capability family. The source does not yet prove that the two paths share a single authoritative registration bridge or that the V2 trading path persists the durable V1 `AnalysisRunRecord` lifecycle.

## Decision

CFIP will **not** collapse catalog, execution, and durable-run concerns into one class or one process abstraction. It will instead converge them on **one canonical engine identity and contract model with explicit projections and adapters**.

The target model is:

```text
                  Canonical Engine Catalog
                   / Contract Registry
                           │
             ┌─────────────┴─────────────┐
             │                           │
      Runtime Projection          Durable Run Projection
             │                           │
             ▼                           ▼
      Low-Latency Executor        Analysis Run / Provenance
             │                           │
             └─────────────┬─────────────┘
                           ▼
                    Engine Evidence
                           │
                           ▼
                AnalysisConsensusService
                           │
                           ▼
                  Decision / Risk Boundary
```

Rules:

- One `(engine_id, version)` identity is authoritative.
- There is one canonical engine contract/catalog; runtime and durable execution metadata are projections/extensions, not competing identity systems.
- A concrete analytical algorithm should have one implementation identity per version; it must not be duplicated merely because it has low-latency and durable callers.
- Runtime activation must validate the executable descriptor against the canonical contract before activation.
- Durable analysis and low-latency evidence may remain separate use cases because they have different latency, persistence, replay and operational requirements.
- Their engine identity, input semantics, version, determinism and provenance requirements must remain compatible.
- No API/WS route may silently create an alternate engine identity or bypass the canonical analysis contract.
- Specialist engines produce evidence. They do not independently become the final trade/decision authority.
- `AnalysisConsensusService` remains the sole authoritative consensus boundary before decision/risk/execution policy.
- V1/V2 compatibility must be proven with contract and integration tests during CFIP implementation before parity or production-readiness claims.

## Why two execution planes are better than one “analysis engine” class

The correct question is not whether CFIP should have two market-analysis algorithms. It should not. The question is whether one analytical capability should support multiple execution modes. It should.

### Low-latency execution needs

Trading/interactive evidence requires:

- bounded latency;
- concurrency control;
- timeout/failure policy;
- transient health state;
- minimal persistence overhead;
- immediate evidence projection;
- graceful partial-result behavior where policy allows.

### Durable execution needs

Research/replay/audit execution requires:

- durable run identity;
- lifecycle state;
- input snapshot/reference;
- parameter and engine fingerprints;
- data revision;
- provenance;
- replayability;
- historical auditability;
- durable result/error state.

Combining these responsibilities into a single “engine” object would couple domain analysis to persistence and operational concerns. It would also make the latency-sensitive path unnecessarily dependent on durable-run infrastructure.

Therefore **separation of execution planes is preferred, while duplication of analytical implementations is prohibited**.

## When a single implementation is preferable

The same deterministic engine implementation should be reused by both planes whenever its computational contract permits it. For example:

`FVG detector v1.2.0`

should not have a separate “trading FVG algorithm” and “backtest FVG algorithm”. Both callers should invoke the same versioned analytical capability against an explicit execution context.

Only an explicit, versioned semantic difference justifies a second implementation identity. Such divergence requires evidence, tests and an ADR rather than an accidental fork.

## Why not merge everything into one runtime

A single monolithic analysis runtime would make several properties harder to guarantee:

- durable research could contaminate low-latency trading workloads;
- persistence failures could become trading-analysis failures;
- replay workloads could exhaust interactive execution capacity;
- operational health would mix transient and durable concerns;
- horizontal scaling would become less workload-specific;
- different SLOs would be difficult to enforce cleanly.

CFIP should therefore use a **shared analytical contract and implementation identity with separate execution/application adapters**, and only split deployment/process boundaries when measured scale, isolation, ownership or security requires it.

## Target improvement beyond source

CFIP will add a canonical registration/projection consistency gate that CForex does not currently prove. It must detect:

- descriptor/version mismatch;
- missing runtime implementation;
- runtime implementation with no canonical contract;
- capability drift;
- dependency drift;
- determinism/reproducibility mismatch;
- unsupported timeframe/warmup/latency claims;
- missing provenance requirements;
- missing PIT/replay compatibility;
- duplicate analytical implementation identity;
- divergent output-contract semantics between execution planes.

The check becomes a Gate 3 release gate and a migration-parity prerequisite.

## Observability and governance requirements

Analysis execution must emit correlation-compatible telemetry across:

`request → engine selection → execution → evidence → consensus → decision → risk → outcome`

OpenTelemetry semantic conventions should be reused where applicable rather than inventing conflicting telemetry vocabularies.

For AI/agent-assisted analysis or governance, tool access, persistent memory, identity and human-oversight boundaries must remain explicit and auditable. CFIP therefore keeps analytical evidence and agent authority separate.

## Consequences

### Positive

- removes ambiguity around “two analysis engines”;
- preserves the valid separation of metadata, runtime execution and durable provenance;
- prevents duplicate engine identity systems in CFIP;
- prevents duplicate analytical implementations for different callers;
- enables low-latency trading evidence and durable research/replay execution to coexist;
- improves replay, regression, observability and governance;
- allows workload-specific scaling without premature microservice fragmentation;
- keeps domain analysis independent of persistence/runtime infrastructure.

### Negative / cost

- CFIP needs a canonical registry/contract and projection validation mechanism;
- V1/V2 source semantics must be reconciled explicitly during implementation;
- additional contract, integration and golden tests are required;
- production wiring and invocation coverage must still be proven from CForex before parity claims.

## Gate 0 evidence status

This ADR does **not** close Gate 0. It records the target architectural improvement while preserving unresolved source evidence questions:

- production wiring of durable analysis;
- V1/V2 bridge in source;
- V2 route persistence relationship;
- replay/PIT producer and execution semantics;
- durable engine telemetry/history;
- per-engine golden/regression fixtures.
