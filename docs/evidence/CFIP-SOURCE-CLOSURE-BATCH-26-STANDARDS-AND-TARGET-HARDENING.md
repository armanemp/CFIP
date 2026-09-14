# CFIP Source Closure Batch 26 — Standards and Target Hardening

**Date:** 2026-09-14
**Gate:** Gate 0 — Source Closure

## 1. Standards refresh

The current OpenTelemetry semantic-convention specification is version 1.44.0 and covers common conventions for traces, metrics, logs, events, resources and protocol/database/messaging domains. CFIP therefore continues the standard-first telemetry rule: reuse an applicable OpenTelemetry semantic convention before inventing a CFIP-specific attribute. citeturn0search1turn0search4

OpenTelemetry guidance also recommends reusing existing attributes and defining new attributes only when there is a clear end-user use case, with documented type/requirement/sensitivity semantics. CFIP's future custom telemetry registry should therefore be treated as a governed schema rather than an unconstrained key/value namespace. citeturn0search6

Messaging telemetry must preserve semantic stability and migration discipline; HTTP and RPC conventions likewise have explicit transition guidance. This is relevant to CFIP's API, NATS/event and realtime boundaries. citeturn0search7turn0search8turn0search9

OWASP's 2026 Agentic AI security material emphasizes inspectable, traceable and instrumentable agents, while its APTS framework explicitly covers scope enforcement, safety/impact management, human oversight, graduated autonomy, auditability/reproducibility, manipulation resistance and third-party/supply-chain trust. These reinforce CFIP's separation of agent identity/capability/policy/tool/action/evidence and its governed autonomy lifecycle. citeturn0search14turn0search13turn0search17

## 2. Target hardening decisions

1. **Telemetry schema governance:** introduce a future machine-readable telemetry catalog under `packages/contracts`/`docs/contracts` before broad runtime instrumentation; standard OTel fields are preferred and custom fields require ownership and use-case documentation.
2. **Event telemetry separation:** business events remain durable domain/application evidence; OTel events/spans/metrics remain observational. Neither should silently replace the other.
3. **WebSocket observability:** instrument connection lifecycle, subscription lifecycle, snapshot latency, incremental delivery latency, queue depth/backpressure and disconnect reasons using standard messaging/network conventions where applicable.
4. **Agent control evidence:** every autonomous action must be reconstructable across agent identity, capability, policy decision, authorized tool, action outcome and post-action evidence.
5. **Multi-agent coordination:** shared-state ownership, authenticated messaging, bounded authority and coordination evidence are mandatory before autonomous horizontal scaling is considered safe.
6. **Custom telemetry cardinality:** high-cardinality IDs and sensitive AI content remain opt-in and should not be used as uncontrolled metric labels.

## 3. Structural improvement

The existing target tree already separates contexts, applications, engines, adapters, packages, data, frontend, infrastructure and tests. The next architectural improvement is not adding arbitrary directories; it is making the contracts between these boundaries machine-checkable and evidence-linked. This reduces migration drift while avoiding premature microservice fragmentation.

## 4. Gate impact

These decisions strengthen D10 and the future Gate 1 observability/security foundation, but do not close Gate 0 and do not authorize runtime implementation.
