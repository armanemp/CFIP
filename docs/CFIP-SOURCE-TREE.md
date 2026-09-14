# CFIP Canonical Source Tree

This is the **target source tree**, not a promise that every directory must exist on day one. Empty structural folders should not be committed merely to make a diagram look complete. A directory becomes real when it owns an implementation, contract, test, or documented architectural artifact.

```text
cfip/
│
├── apps/
│   ├── api/                         # HTTP/API composition root
│   ├── realtime/                    # realtime/WebSocket composition root
│   ├── market_data_worker/          # ingestion and canonicalization workers
│   ├── analysis_worker/             # analysis/event processing workers
│   ├── learning_worker/             # evaluation/learning worker
│   ├── autonomy_worker/             # governed engineering/autonomy worker
│   └── web/                         # Next.js application
│
├── contexts/
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
├── packages/
│   ├── contracts/                   # versioned API/event/data schemas
│   ├── domain_kernel/               # shared domain primitives only
│   ├── application_kernel/          # use-case/application primitives
│   ├── eventing/                    # event envelope/outbox abstractions
│   ├── observability/               # telemetry abstractions
│   ├── security/                    # security primitives/policies
│   ├── testing/                     # reusable test infrastructure
│   └── configuration/               # typed configuration infrastructure
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
│   ├── migrations/                  # authoritative schema migrations
│   ├── seeds/                       # deterministic non-production seed data
│   ├── schemas/                     # canonical data contracts
│   ├── fixtures/                    # bounded test fixtures
│   └── retention/                   # retention/partition policies
│
├── frontend/
│   ├── app/                         # route composition
│   ├── features/                    # feature modules aligned to contexts
│   ├── domain/                      # frontend domain types/semantics
│   ├── infrastructure/              # API/realtime adapters
│   ├── components/                  # reusable presentation primitives
│   ├── chart/                       # renderer-neutral chart intelligence
│   ├── i18n/                        # translation infrastructure
│   ├── accessibility/               # a11y utilities and tests
│   └── tests/                       # frontend integration/e2e tests
│
├── infrastructure/
│   ├── docker/
│   ├── compose/
│   ├── kubernetes/                  # added only when operationally justified
│   ├── terraform/                   # added only when infrastructure-as-code is adopted
│   ├── observability/
│   └── security/
│
├── tests/
│   ├── architecture/               # dependency and boundary tests
│   ├── contracts/                   # API/event/schema compatibility
│   ├── integration/
│   ├── e2e/
│   ├── replay/
│   ├── pit/                         # point-in-time correctness
│   ├── performance/
│   ├── security/
│   └── fixtures/
│
├── docs/
│   ├── architecture/
│   │   ├── CFIP-ARCHITECTURE-GUIDE.md
│   │   ├── ADR/
│   │   ├── context-map.md
│   │   ├── dependency-rules.md
│   │   └── runtime-topology.md
│   ├── capabilities/
│   │   ├── capability-registry.md
│   │   ├── source-evidence-matrix.md
│   │   └── parity-matrix.md
│   ├── contracts/
│   │   ├── api-catalog.md
│   │   ├── event-catalog.md
│   │   └── data-ownership.md
│   ├── operations/
│   │   ├── deployment.md
│   │   ├── runbooks/
│   │   └── disaster-recovery.md
│   ├── security/
│   ├── research/
│   └── decisions/
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
├── pnpm-lock.yaml               # only if frontend workspace tooling requires it
├── docker-compose.yml
├── .env.example
├── .python-version
├── .node-version
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
└── README.md
```

## Context-internal structure

Every backend bounded context should converge on the same grammar unless there is a documented reason not to:

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

Technology adapters themselves remain outside the domain and application layers. A context may depend on an adapter through a port; it must not depend on the adapter implementation directly.

## Engine-internal structure

Deterministic analytical engines should use:

```text
engines/<engine>/
├── contract.py
├── inputs.py
├── outputs.py
├── implementation.py
├── version.py
└── tests/
```

The runtime registry is the only executable discovery mechanism. A namespace existing in the repository does not make an engine executable.

## Frontend feature structure

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

The frontend follows the same dependency inversion principle as the backend: presentation does not own transport details, and renderer-specific chart code does not own market semantics.

## Naming rules

- Python packages/modules: `snake_case`.
- TypeScript modules: project-standard `camelCase`/`PascalCase` according to artifact type.
- Bounded contexts use stable domain names, not vendor names.
- Provider adapters include provider identity only at the adapter boundary.
- Contracts carry explicit versions.
- Files should have one clear architectural owner.
- Avoid generic `utils`, `helpers`, `misc`, `common` dumping grounds. Shared code must have a documented ownership reason.

## Tree governance

The tree is considered healthy only when:

1. every production file has an owning context/package;
2. dependencies obey the architecture graph;
3. no duplicate implementation path exists for the same capability;
4. persistence ownership is explicit;
5. contracts are discoverable;
6. tests follow the owning boundary;
7. generated artifacts are excluded from source ownership unless intentionally committed;
8. operational scripts are deterministic;
9. the capability registry can map every CForex capability to a CFIP location;
10. the tree can evolve without converting every context into a microservice.
