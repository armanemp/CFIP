# CFIP — CForex Future Implementation Platform

CFIP is the clean-room target architecture and implementation repository for the next-generation implementation of CForex.

The canonical source for capability discovery is the existing `armanemp/CForex` repository. CFIP does not invent or discard capabilities merely to obtain a cleaner tree: every CForex capability must be mapped to a bounded context, contract, use case, adapter, persistence boundary, event contract, UI surface, and verification strategy before it is considered implemented.

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
- Configuration, provider capabilities, entitlements, feature flags and policies are data-driven rather than hardcoded.
- i18n, RTL/LTR, accessibility, performance and security are architecture concerns, not finishing tasks.

## Source of truth

1. `docs/CFIP-ARCHITECTURE-GUIDE.md` — architectural book and implementation rules.
2. `docs/CFIP-SOURCE-TREE.md` — canonical target repository tree and ownership rules.
3. The current `armanemp/CForex` repository — behavioral/capability source of truth.

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
├── infrastructure/       # deployment/runtime infrastructure
├── tests/                # cross-context and architecture verification
├── docs/                 # architecture, ADRs, contracts, operations
├── scripts/              # deterministic developer/release tooling
└── .github/              # CI, security and repository governance
```

The tree is intentionally target-oriented. It must not be treated as a mechanical file-by-file copy of CForex. Capability mapping determines where each source behavior belongs.
