# ADR-003 — Observability and Agent-Control Semantics

**Status:** Accepted for target architecture; implementation blocked by Gate 0  
**Date:** 2026-09-14  
**Scope:** CFIP-wide telemetry, event semantics and autonomous/agentic control

## Context

CFIP must operate at global scale across API, workers, realtime processing, analytical engines, research, learning and governed autonomy. The platform therefore needs telemetry that remains interoperable across polyglot infrastructure rather than creating a proprietary vocabulary for every subsystem.

Current CForex evidence already contains event envelopes, correlation/causation, realtime lifecycle events, worker health/backpressure signals, engine provenance and autonomous lanes. The migration must preserve those semantics while avoiding telemetry fragmentation.

Current OpenTelemetry semantic conventions provide standardized conventions across traces, metrics, logs, events, databases and messaging. OpenTelemetry guidance also recommends reusing existing attributes before introducing new conventions and treating sensitive or expensive attributes carefully. OWASP's Agent Control Standard, published September 1, 2026, establishes a complementary runtime-control model for inspectable, traceable and instrumentable agents.

## Decision

### 1. Standard-first telemetry

CFIP MUST use applicable OpenTelemetry semantic conventions before defining CFIP-specific attributes.

Priority:

1. OpenTelemetry standard semantic convention;
2. technology-specific OpenTelemetry convention;
3. CFIP domain attribute only when no adequate standard exists;
4. undocumented ad-hoc telemetry is prohibited.

Database and messaging operations MUST use the corresponding OpenTelemetry semantic conventions where applicable. CFIP-specific attributes must be low-cardinality where possible and must document requirement level, sensitivity and intended query/use.

### 2. Event semantics

A meaningful point-in-time occurrence is modeled as an event; a duration-bearing operation is modeled as a span. Event names are stable, domain-qualified and never contain dynamic identifiers. Occurrence time represents when the event happened; observation/ingestion time is separate.

CFIP event telemetry MUST preserve correlation and causation context where the domain event already carries those concepts. Payloads containing secrets, credentials, private user content or unnecessarily large/high-cardinality data are not emitted by default.

### 3. Realtime telemetry

Realtime processing MUST expose enough telemetry to diagnose partition/ordering ownership, consumer lag, processing duration, watermark lag, event lateness, deduplication outcomes, retry/failure outcomes, backpressure/dropped work and checkpoint/recovery state.

Telemetry is observational and must not become the correctness authority. Durable state and event-time rules remain authoritative.

### 4. Engine telemetry

Each analytical execution MUST be correlatable to canonical `(engine_id, version)` identity, execution context, data revision/PIT identity where available, outcome and latency. Engine telemetry must distinguish transient runtime health from durable analytical execution evidence.

The runtime execution projection must not create a second engine identity or silently invent provenance fields. Durable execution records remain the authority for audit/replay evidence.

### 5. Agent authority separation

Agentic/autonomous components MUST NOT acquire analytical-engine authority merely because they can invoke analytical tools.

The minimum control chain is:

`agent identity → capability → policy decision → authorized tool → action → telemetry/evidence → post-action control`

Tool authorization, workspace/tenant scope, entitlement, risk class and mutation authority are explicit control-plane concerns. Analytical engines remain deterministic evidence producers and do not delegate their authority to an agent.

### 6. Autonomous change controls

Self-development, self-healing and autonomous promotion paths MUST retain inspectable identity, policy decision, evidence references, verification result and rollback/health-guard linkage. A runtime agent MUST NOT modify its own governor, safety policy, evidence history or authority boundary.

For high-impact actions, policy enforcement and independent verification remain mandatory even when a low-risk path supports automated promotion.

### 7. Multi-agent reconstruction

When multiple autonomous workers/agents act concurrently, evidence MUST be reconstructable per agent and across coordination events. Shared-state writes require explicit ownership and freshness semantics. Aggregate rate/impact limits must not rely only on per-agent local limits.

### 8. Performance rule

Telemetry collection must be bounded and non-blocking on latency-sensitive paths where possible. High-volume detailed evidence should use asynchronous export, sampling, aggregation or durable analytical projection rather than forcing every runtime operation through synchronous persistence.

Telemetry failures must not silently change trading/analysis correctness semantics. Critical audit evidence has an explicit durability policy; ordinary diagnostic telemetry may degrade according to documented policy.

## Consequences

### Positive

- interoperable telemetry across services and infrastructure;
- lower vendor lock-in and lower migration cost;
- consistent correlation across realtime, engines, workers and autonomous workflows;
- explicit separation of analytical authority and agent authority;
- stronger audit and incident reconstruction;
- clearer global-scale observability requirements.

### Trade-offs

- telemetry conventions require versioning and governance;
- high-cardinality data must be deliberately controlled;
- some source-specific telemetry must be translated into standard semantics;
- autonomous workflows require additional policy/evidence boundaries.

## Gate 0 impact

This ADR changes **target architecture and evidence requirements only**. It does not authorize CFIP runtime implementation.

Gate 0 must establish sufficient source evidence for existing CForex telemetry/event/agent behavior before CFIP implementation. Intentional target improvements must be recorded as target divergence rather than presented as source parity.

## Verification obligations

Before Gate 1 implementation:

- map CForex event/telemetry vocabulary to standard and CFIP-specific conventions;
- identify high-cardinality and sensitive fields;
- map realtime lag/watermark/backpressure signals;
- map engine execution/provenance telemetry;
- map autonomous lane identity/policy/evidence/verification controls;
- define telemetry degradation policy by workload criticality;
- add parity tests for preserved source semantics.
