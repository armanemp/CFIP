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

These are therefore not two independent analytical algorithms producing competing market opinions. They are two infrastructure planes around the same analytical capability family:

- **Catalog/contract plane:** what an engine is, which capability it provides, its dependencies and reproducibility contract.
- **Execution plane:** how a concrete engine is selected, invoked, timed, observed and failure-handled at runtime.

CForex also contains a V2 trading evidence path (`WorkspaceService.snapshot → AnalysisFabric → EngineRuntime → EngineOutput → evidence projection`) that is not proven to persist `AnalysisRunRecord` records through the durable V1 service. This distinction must not be erased during migration.

## Decision

CFIP will converge these concepts into **one canonical analysis-engine identity model with explicit projections**, rather than preserving two independently authoritative registries.

The target model is:

```text
Canonical Engine Catalog / Contract Registry
                 │
        ┌────────┴────────┐
        │                 │
  Execution Descriptor   Durable Analysis Contract
        │                 │
        ▼                 ▼
 Runtime Executor     Analysis Run / Provenance Store
        │
        ▼
 Engine Output / Evidence
        │
        ▼
 AnalysisConsensusService
```

Rules:

- One `(engine_id, version)` identity is authoritative.
- Operational execution metadata is a projection/extension of the canonical descriptor, not a second identity system.
- Runtime registration must validate against the canonical contract before activation.
- Durable execution and transient evidence execution may remain separate use cases, but their engine identity, input semantics, provenance, version and determinism contracts must be compatible.
- No route may silently bypass the authoritative analysis contract.
- The final trade/decision boundary remains the sole `AnalysisConsensusService`; specialist engines emit evidence and do not independently become the final decision authority.
- V1/V2 compatibility must be proven during CFIP implementation with contract tests before either source behavior or target improvements are declared parity-safe.

## Why the separation is still useful

Keeping catalog and execution concerns separate is architecturally sound when the boundary is explicit:

- catalog metadata can be inspected without executing an engine;
- execution can enforce latency/failure policy without putting infrastructure concerns into domain descriptors;
- durable analysis can capture reproducibility and provenance independently of transient runtime health;
- different callers can request a durable experiment or a low-latency evidence projection without creating duplicate engine implementations.

What is undesirable is having two independently authoritative definitions of the same engine. That creates drift risk in version, capability, dependency and reproducibility semantics.

## Target improvement beyond source

CFIP will add a canonical registration/projection check that CForex does not currently prove. It should detect:

- descriptor/version mismatch;
- missing runtime implementation;
- runtime implementation with no contract;
- capability drift;
- dependency drift;
- determinism mismatch;
- unsupported timeframe/warmup/latency claims;
- missing provenance/replay requirements.

This check becomes a Gate 3 release gate and a migration-parity prerequisite.

## Observability and governance requirements

Analysis execution must emit correlation-compatible telemetry across:

`request → engine selection → execution → evidence → consensus → decision → risk → outcome`

OpenTelemetry semantic conventions should be reused where applicable rather than inventing conflicting attribute names.

For AI/agent-assisted analysis or governance, tool access, persistent memory, identity and human-oversight boundaries must remain explicit and auditable. Current OWASP Agentic AI guidance treats these as material attack surfaces; CFIP therefore keeps analysis evidence and agent authority separate.

## Consequences

### Positive

- removes ambiguity around “two analysis engines”;
- preserves the valid separation of metadata, execution and durable provenance;
- prevents duplicate engine identity systems in CFIP;
- enables low-latency runtime evidence and durable research execution to coexist;
- improves replay, regression, observability and governance;
- supports global-scale execution without coupling domain contracts to runtime infrastructure.

### Negative / cost

- CFIP needs a canonical registry contract and projection validation;
- V1/V2 source semantics must be reconciled explicitly during implementation;
- additional contract tests are required;
- production wiring and invocation coverage must still be proven from CForex before parity claims.

## Gate 0 evidence status

This ADR does **not** close Gate 0. It records the target architectural improvement while preserving unresolved source evidence questions:

- production wiring of durable analysis;
- V1/V2 bridge in source;
- V2 route persistence relationship;
- replay/PIT producer and execution semantics;
- durable engine telemetry/history;
- per-engine golden/regression fixtures.
