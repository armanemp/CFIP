# CFIP — CForex Future Implementation Platform

CFIP is the clean-room target architecture and implementation repository for the next-generation implementation of CForex.

The canonical source for capability discovery is the existing `armanemp/CForex` repository. CFIP does not invent or discard capabilities merely to obtain a cleaner tree: every CForex capability must be mapped to a bounded context, contract, use case, adapter, persistence boundary, event contract, UI surface, and verification strategy before it is considered implemented.

## Start here

**Canonical migration control:** `docs/CFIP-MIGRATION-CONTROL-INDEX.md`

At the beginning of every continuation, read the control index first, then the migration master plan and architecture/evidence guides referenced by it. The control index defines the active migration gate, evidence precedence, capability lifecycle and rules for starting implementation without guessing or losing CForex behavior.

## Mission

Build a production-grade, globally scalable, AI-native financial-market intelligence platform while preserving the externally meaningful capabilities and correctness guarantees of CForex.

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

## Canonical documents

1. `docs/CFIP-MIGRATION-CONTROL-INDEX.md` — single project/migration entrypoint and active gate.
2. `docs/CFIP-MIGRATION-MASTER-PLAN.md` — complete implementation sequencing and release gates.
3. `docs/CFIP-ARCHITECTURE-GUIDE.md` — target architecture and invariants.
4. `docs/capabilities/source-study-integration.md` — source-study and evidence workflow.
5. `docs/capabilities/CFIP-CAPABILITY-REGISTRY.md` — capability ownership map.
6. `docs/capabilities/source-evidence-matrix.md` — executable/source evidence map.
7. `docs/capabilities/parity-matrix.md` — implementation and parity lifecycle.
8. `docs/CFIP-SOURCE-TREE.md` — target tree and ownership rules.

## Source of truth

1. The current `armanemp/CForex` repository is the behavioral/capability source of truth until parity closure.
2. CFIP architecture documents define the target boundaries and rules.
3. Source-study artifacts accelerate evidence discovery but never override executable source evidence.

## Initial target shape

```text
cfip/
├── apps/                 # deployable entrypoints only
├── contexts/             # bounded business contexts
├── packages/             # cross-context contracts and platform libraries
├── adapters/             # inbound/outbound technology adapters
├── engines/              # deterministic analytical engines
├── data/                 # migrations, seeds, schemas, data contracts
├── frontend/             # web application and UI platform
├── infrastructure/      # deployment/runtime infrastructure
├── tests/                # cross-context and architecture verification
├── docs/                 # architecture, contracts, operations, evidence
├── scripts/              # deterministic developer/release tooling
└── .github/              # CI, security and repository governance
```

The tree is intentionally target-oriented. It must not be treated as a mechanical file-by-file copy of CForex. Capability mapping determines where each source behavior belongs.

## Definition of success

A clean target tree is not sufficient. Migration succeeds only when CForex capabilities are behaviorally preserved, intentionally improved differences are documented, contracts are verified, and the resulting platform passes parity, security, observability, performance and operational gates.
