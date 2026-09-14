# CFIP — CForex Intelligence Platform

CFIP is the clean-room target architecture and implementation repository for the next-generation **CForex Intelligence Platform**.

The canonical source for capability discovery is the existing `armanemp/CForex` repository. CFIP does not invent or discard capabilities merely to obtain a cleaner tree: every CForex capability must be mapped to a bounded context, contract, use case, adapter, persistence boundary, event contract, UI surface, and verification strategy before it is considered implemented.

## Start here

**Canonical migration control:** `docs/CFIP-MIGRATION-CONTROL-INDEX.md`

At the beginning of every continuation, read the control index first, then the migration master plan and architecture/evidence guides referenced by it. The control index defines the active migration gate, evidence precedence, capability lifecycle and rules for starting implementation without guessing or losing CForex behavior.

## Mission

Build a production-grade, globally scalable, AI-native financial-market intelligence platform while preserving the externally meaningful capabilities and correctness guarantees of CForex.

**CFIP means CForex Intelligence Platform. The `I` is explicitly _Intelligence_.** Intelligence is a cross-cutting platform capability spanning market data, analysis, consensus, risk/decision, research, learning, product experience, operations, security and governed software evolution; it is not merely a chatbot or a UI feature.

## Architectural principles

- Domain-first, modular, ports-and-adapters architecture.
- Bounded contexts before deployment boundaries; no premature microservice fragmentation.
- Explicit application use cases and contracts.
- Infrastructure adapters are replaceable and never leak into domain logic.
- Point-in-time correctness, provenance, lineage, revision semantics and causal ordering are mandatory.
- Live, replay and backtest share canonical market and decision semantics.
- Analysis consensus has one authoritative fusion boundary.
- Risk and position sizing are account-aware and policy-driven.
- Events are versioned, idempotent, observable and replayable.
- PostgreSQL owns transactional/control-plane state; analytical storage owns analytical workloads; caches are never the system of record.
- AI agents operate through explicit tools and governance boundaries; they do not receive direct SQL or unrestricted infrastructure authority.
- Learning produces governed artifacts and evidence; it cannot silently mutate production behavior.
- Every production capability has tests, observability and an explicit operational owner.
- Configuration, provider capabilities, entitlements, feature flags and policies are data-driven rather than hardcoded where appropriate.
- i18n, RTL/LTR, accessibility, performance and security are architecture concerns, not finishing tasks.
- Platform Intelligence is a governed cross-cutting fabric, not a second domain authority; authoritative domain contracts, deterministic engines, risk policies and execution controls remain the source of truth.

## Canonical documents

1. `docs/CFIP-MIGRATION-CONTROL-INDEX.md` — single project/migration entrypoint and active gate.
2. `docs/CFIP-MIGRATION-MASTER-PLAN.md` — complete implementation sequencing and release gates.
3. `docs/CFIP-ARCHITECTURE-GUIDE.md` — target architecture and invariants.
4. `docs/capabilities/source-study-integration.md` — source-study and evidence workflow.
