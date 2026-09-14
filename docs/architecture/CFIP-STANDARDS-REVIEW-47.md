# CFIP Standards Review — Batch 47

**Review date:** 2026-09-15
**Purpose:** record current external standards that materially affect CFIP architecture without introducing novelty-only dependencies.

## 1. OpenTelemetry

OpenTelemetry currently publishes Semantic Conventions **1.44.0**. The conventions cover HTTP, databases, messaging, RPC, object stores, CI/CD, feature flags, GenAI and multiple telemetry signals. CFIP therefore continues to use an OTel-first semantic model rather than inventing parallel telemetry vocabulary.

CFIP implication:

- standard OTel semantic conventions are the default vocabulary;
- CFIP-specific attributes are allowed only where the standard model has no suitable semantic field;
- telemetry schema evolution must preserve downstream compatibility;
- trace/metric/log correlation remains observational and must not become a hidden correctness store;
- messaging, database and GenAI instrumentation must be version-aware because several convention families are at different stability stages.

## 2. OWASP Agent Control Standard

OWASP GenAI Security Project released the **Agent Control Standard (ACS)** on 2026-09-01. ACS emphasizes inspectable, traceable and instrumentable agents and runtime-enforceable controls through middleware hooks.

CFIP implication:

- agent identity, capabilities, tools, policy decisions and actions must remain inspectable;
- policy enforcement belongs at governed control points, not only in prompts;
- every material autonomous action requires reconstructable evidence;
- agent runtime controls must remain independent from the agent's own authority to change them;
- tool invocation must preserve authorization, isolation and post-action verification boundaries.

This reinforces, rather than replaces, CFIP ADR-005. CFIP remains provider/framework neutral and does not require ACS as a runtime dependency.

## 3. OWASP Agentic Security

OWASP's 2026 Agentic Applications guidance treats autonomous systems as a distinct security surface, including persistent state, tool use and multi-step action. CFIP therefore keeps memory/context, tool authority, shared state, multi-agent coordination and autonomous change under explicit governance and evidence requirements.

## 4. Architecture decision

No new external dependency is required by this review. The material architectural improvement is to make current standards an explicit verification input for telemetry and agent-control contracts, while keeping the implementation provider-neutral and Gate-0 compatible.
