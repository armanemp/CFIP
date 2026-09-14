# CFIP Source Closure Batch 30 — Evidence Graph and Execution Census

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Runtime implementation:** 0% / LOCKED

## 1. Objective

Advance source closure using execution-path evidence rather than file-count evidence. This batch cross-checks the current CForex worker composition, analysis application service and realtime WebSocket transport and defines the exact evidence graph required before each capability can be considered operationally closed.

## 2. Evidence graph

For every material capability the canonical chain is:

`source artifact → behavior → capability → contract → domain owner → application use case → port → adapter → data/event contract → composition/bootstrap → production entrypoint → tests → telemetry/recovery → alternate-path relationship → parity evidence`.

A capability with a missing link remains OPEN even when its source implementation is substantial.

## 3. Direct analysis execution evidence

CForex `AnalysisExecutionService` directly demonstrates:

- canonical `(engine_id, version)` lookup through the domain registry;
- engine registration into the registry and executable map;
- optional durable `AnalysisRunRepository` persistence;
- lifecycle event publication when configured;
- deterministic SHA-256 hashing of parameters, input snapshot and descriptor;
- provenance construction;
- requested → validating → running → terminal execution states;
- timeout and failure result construction;
- completed result persistence and lifecycle publication.

This confirms a strong durable/application execution capability. It does **not** prove that every production analysis route invokes this service.

## 4. Direct realtime production-composition evidence

CForex `apps/worker/src/fi_worker/main.py` directly composes:

- PostgreSQL engine/session;
- NATS/JetStream streams and durable consumers;
- ClickHouse initialization;
- durable application-event outbox/publisher/dispatcher;
- signal lifecycle repository/service;
- provenance repository;
- vertical intelligence/orchestration;
- realtime market-feed service;
- persisted realtime runtime state and ledger;
- canonical observation outbox/publisher/dispatcher;
- ClickHouse observation consumer/writer;
- realtime runtime and durable observation consumer;
- bounded dispatch loops;
- graceful shutdown/drain/close behavior.

This is production-entrypoint evidence for the realtime worker composition.

## 5. Alternate execution-path obligation

The source still requires explicit relationship mapping between:

`AnalysisExecutionService durable/application path`

and

`Workspace snapshot → AnalysisFabric → EngineRuntime → EngineOutput evidence path`.

The target must retain one semantic engine implementation per canonical `(engine_id, version)` while allowing separate execution projections. No duplicate engine implementation is authorized.

## 6. Bounded negative evidence

Current GitHub code-search attempts for `AnalysisExecutionService` and `RealtimeIntelligenceRuntime` returned no indexed matches despite direct file evidence proving those symbols exist. This is classified **BOUNDED NEGATIVE EVIDENCE** and is not treated as absence. Direct file/tree/entrypoint evidence remains authoritative.

## 7. Target acceptance improvement

The target file manifest now requires every runtime file to carry:

`owner + source mapping/target rationale + contract + implementation purpose + dependency direction + tests + telemetry/recovery requirements + migration/parity status`.

This prevents architecture directories from becoming implementation by implication and accelerates future work by making each runtime slice independently acceptance-testable.

## 8. Gate impact

D1, D2, D3, D4 and D5 evidence is advanced, but Gate 0 remains OPEN. No parity or production-readiness status is advanced solely from this document.
