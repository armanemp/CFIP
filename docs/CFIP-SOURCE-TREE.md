# CFIP Canonical Source Tree

**Status:** canonical target structure; runtime materialization remains gated by Gate 0.

This document defines both the logical target tree and the rules for materializing it. The current GitHub repository intentionally contains the migration-control/documentation system rather than runtime implementation. Empty production folders or placeholder modules must not be committed merely to make the diagram look complete.

## 1. Canonical target tree

```text
cfip/
├── apps/                         # deployable process composition roots
│   ├── api/
│   ├── realtime/
│   ├── market_data_worker/
│   ├── analysis_worker/
│   ├── learning_worker/
│   ├── autonomy_worker/
│   └── web/
│
├── contexts/                     # bounded business contexts
│   ├── identity/
│   ├── organization/
│   ├── workspace/
│   ├── market_reference/
│   ├── market_data/
│   ├── data_lineage/
│   ├── realtime/
│   ├── chart_workspace/
│   ├── technical_analysis/
│   ├── market_structure/
│   ├── liquidity/
│   ├── fair_value_gap/
│   ├── order_block/
│   ├── market_regime/
│   ├── multi_timeframe/
│   ├── confluence/
│   ├── contradiction/
│   ├── intelligence_consensus/
│   ├── signals/
│   ├── strategy_research/
│   ├── backtest/
│   ├── replay/
│   ├── risk/
│   ├── decision/
│   ├── journal/
│   ├── execution_boundary/
│   ├── research_intelligence/
│   ├── learning_evaluation/
│   ├── platform_intelligence/
│   ├── ai_gateway/
│   ├── entitlements/
│   ├── governance/
│   ├── observability/
│   └── operations/
│
├── packages/                    # cross-context contracts/platform primitives
│   ├── contracts/
│   ├── domain_kernel/
│   ├── application_kernel/
│   ├── eventing/
│   ├── observability/
│   ├── security/
│   ├── testing/
│   └── configuration/
│
├── adapters/
│   ├── inbound/
│   │   ├── http/
│   │   ├── websocket/
│   │   ├── cli/
│   │   └── scheduled_jobs/
│   └── outbound/
│       ├── postgres/
│       ├── clickhouse/
│       ├── redis/
│       ├── nats/
│       ├── object_storage/
│       ├── market_providers/
│       ├── broker_providers/
│       ├── model_providers/
│       ├── research_providers/
│       └── notification_providers/
│
├── engines/
│   ├── technical/
│   ├── structure/
│   ├── liquidity/
│   ├── fvg/
│   ├── order_block/
│   ├── regime/
│   ├── mtf/
│   ├── confluence/
│   ├── contradiction/
│   ├── intelligence_score/
│   ├── scoring/
│   ├── signal/
│   ├── strategy/
│   └── backtest/
│
├── data/
│   ├── migrations/
│   ├── schemas/
│   ├── seeds/
│   ├── fixtures/
│   └── retention/
│
├── frontend/
│   ├── app/
│   ├── features/
│   ├── domain/
│   ├── infrastructure/
│   ├── components/
│   ├── chart/
│   ├── i18n/
│   ├── accessibility/
│   └── tests/
│
├── infrastructure/
│   ├── docker/
│   ├── compose/
│   ├── observability/
│   └── security/
│
├── tests/
│   ├── architecture/
│   ├── contracts/
│   ├── integration/
│   ├── e2e/
│   ├── replay/
│   ├── pit/
│   ├── performance/
│   ├── security/
│   └── fixtures/
│
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── capabilities/
│   ├── evidence/
│   ├── contracts/
│   ├── operations/
│   ├── security/
│   └── research/
│
├── scripts/
│   ├── bootstrap/
│   ├── audit/
│   ├── codegen/
│   ├── database/
│   ├── release/
│   └── verification/
│
├── .github/
│   ├── workflows/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   └── pull_request_template.md
│
├── pyproject.toml
├── uv.lock
├── package.json
├── pnpm-lock.yaml
├── docker-compose.yml
├── .env.example
├── .python-version
├── .node-version
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
└── README.md
```

## 2. Context-internal structure

Every backend bounded context should converge on this grammar unless a documented architectural reason requires otherwise:

```text
contexts/<context>/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── services/
│   ├── events/
│   ├── policies/
│   └── errors/
├── application/
│   ├── commands/
│   ├── queries/
│   ├── handlers/
│   ├── ports/
│   └── dto/
├── infrastructure/
│   ├── persistence/
│   ├── projections/
│   └── configuration/
└── tests/
    ├── unit/
    ├── integration/
    └── contract/
```

Technology adapters remain outside domain/application layers. A context depends on technology through ports, never by importing vendor implementations directly.

## 3. Engine structure

```text
engines/<engine>/
├── contract.py
├── inputs.py
├── outputs.py
├── implementation.py
├── version.py
└── tests/
```

The canonical executable identity is `(engine_id, version)`. A directory is not an engine registration. Runtime, durable and replay execution paths must reuse the same semantic implementation rather than creating duplicate analytical authorities.

The source study currently identifies 15 concrete runtime engine classes while the repository has 14 top-level engine namespaces. The target must preserve the complete runtime inventory without assuming one-to-one namespace/class cardinality.

## 4. Data/evidence structure

The data layer must explicitly accommodate distinct identities for:

- dataset artifact/version;
- dataset fingerprint/content integrity;
- PIT market-data revision/view;
- replay-case identity and expected invariants;
- replay verification result;
- learning revision;
- provenance nodes/edges;
- immutable evidence references.

These identifiers must not collapse into a generic revision field.

## 5. Frontend structure

```text
frontend/features/<feature>/
├── domain/
├── application/
├── infrastructure/
├── components/
├── hooks/
├── state/
├── translations/
└── tests/
```

Market/timeframe/candle/event semantics are owned by canonical domain contracts, not by chart rendering components.

## 6. Verification structure

Cross-context verification belongs under `tests/`; context-local tests stay with the owning context. The cross-context tree is:

```text
tests/
├── architecture/
├── contracts/
├── integration/
├── e2e/
├── replay/
├── pit/
├── performance/
├── security/
└── fixtures/
```

Every important capability must map to verification evidence before implementation status can advance.

## 7. Materialization policy

The target tree is materialized incrementally in this order:

1. repository governance and deterministic tooling;
2. shared contracts and dependency-boundary verification;
3. identity/workspace and market reference;
4. market-data, lineage and PIT foundations;
5. realtime/eventing foundations;
6. analytical engine contracts and implementations;
7. replay/backtest/decision/risk;
8. research/learning/AI/platform intelligence;
9. frontend/product surface;
10. governance/autonomy and operations hardening.

A production path must not be created solely to satisfy this diagram. It must have an architectural owner, source/capability mapping, contract or implementation purpose and verification plan. Empty directories are not committed.

## 8. Repository-level rules

- Python packages/modules use `snake_case`.
- TypeScript uses project-standard `camelCase`/`PascalCase` according to artifact type.
- Bounded contexts use stable domain names, not vendor names.
- Contracts carry explicit versions.
- Generated artifacts do not become source ownership by accident.
- Generic `utils`, `helpers`, `misc` and `common` dumping grounds are prohibited without explicit ownership justification.
- `uv.lock` and `pnpm-lock.yaml` are required once their corresponding runtime/toolchain is materialized; lockfiles are not optional production metadata.
- Deployment-specific `kubernetes/` or `terraform/` trees are added only when operational evidence justifies them.
- Microservice boundaries are introduced only for measured scale, fault isolation, ownership or security requirements.

## 9. Current physical state

The current CFIP repository intentionally materializes the migration-control/documentation system and does not claim that the target runtime tree already contains implementation. This is required by the canonical Gate 0 lock. The tree above is therefore the controlled implementation manifest, while actual production paths are created only when their Gate 0 evidence is sufficient.

## 10. Tree health invariant

The tree is healthy only when:

1. every production file has one architectural owner;
2. every CForex capability maps to one target location;
3. every target capability maps back to source evidence or an explicit platform concern;
4. no duplicate authoritative implementation exists;
5. persistence ownership is explicit;
6. contracts are versioned/discoverable;
7. tests map to capabilities;
8. operational scripts are deterministic;
9. documentation cannot contradict the canonical Gate 0 register;
10. deployment topology can evolve without turning every bounded context into a microservice.
