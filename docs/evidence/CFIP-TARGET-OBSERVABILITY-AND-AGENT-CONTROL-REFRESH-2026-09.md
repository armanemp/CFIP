# CFIP Target Observability and Agent-Control Refresh — 2026-09

**Date:** 2026-09-14  
**Target:** `armanemp/CFIP`  
**Purpose:** standards-driven architecture hardening; this document is target guidance, not source parity evidence.

## 1. Standards refresh

The target observability model is refreshed against current OpenTelemetry Semantic Conventions 1.44.0. OTel currently provides standardized conventions across HTTP, databases, messaging, events, sessions, resources, metrics, logs and traces, and the project guidance favors reuse of existing semantic attributes before introducing custom ones. citeturn0search1turn0search10

CFIP therefore uses this precedence:

`existing OTel semantic convention → stable domain convention → CFIP-specific attribute only when a demonstrated semantic gap remains`.

## 2. Event telemetry rule

Named telemetry events must represent meaningful occurrences such as state transitions, checkpoints or outcomes. Dynamic identifiers belong in attributes rather than event names, and failure/outcome events should carry an appropriate `error.type` when applicable. citeturn0search12

CFIP event instrumentation must therefore avoid dynamic event names such as embedding instrument IDs, workspace IDs or run IDs in the event name.

## 3. Messaging migration rule

Messaging instrumentation must account for the current OpenTelemetry stability/opt-in migration guidance rather than inventing a private messaging vocabulary. During any future migration between semantic-convention generations, the transition strategy must be explicit and version-aware. citeturn0search9

## 4. Client session observability

Frontend telemetry should use a session identity that correlates client logs/events/spans over a session lifecycle, while preserving privacy and avoiding sensitive market/account/AI content by default. OpenTelemetry defines session semantics specifically for client applications. citeturn0search14

## 5. Agent-control modernization

Current OWASP guidance has materially strengthened the agent-control requirement. The OWASP Agent Control Standard (ACS), published September 1, 2026, emphasizes agents being inspectable, traceable and instrumentable, with runtime policy hooks for portable safety controls. citeturn0search19

CFIP target agent architecture is therefore:

`Agent Identity → Capability → Policy Hook → Authorized Tool → Action → Evidence/Telemetry → Post-action Control`

Required controls:

- explicit agent identity;
- capability allow-list;
- tool-level authorization;
- policy evaluation before sensitive actions;
- scoped credentials;
- human/approval boundary for high-impact actions;
- action evidence and correlation;
- memory/data provenance;
- post-action health/effect verification;
- immediate revocation/circuit-breaker capability;
- immutable governance evidence.

## 6. Agent threat model additions

The target threat model explicitly covers prompt injection, tool abuse/privilege escalation, data exfiltration and memory poisoning, all of which are identified as agent-specific risks in current OWASP guidance. citeturn0search18

The architecture must also preserve the existing rule that analytical engines and agents have separate authority domains. An agent cannot gain analytical, execution, governance or infrastructure authority merely because a tool is available.

## 7. Architecture consequence

This refresh does not introduce a new runtime dependency or force a new framework. It strengthens contracts, telemetry naming, security policy hooks and evidence requirements while preserving provider/framework neutrality.

## 8. Gate impact

This is a target-hardening artifact. It does not close Gate 0 and does not advance implementation/parity status. The canonical Gate 0 register remains authoritative.
