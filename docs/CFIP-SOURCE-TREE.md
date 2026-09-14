# CFIP Canonical Source Tree

**Status:** canonical target structure; runtime implementation remains gated by Gate 0.

This document defines the logical target tree and the rules for materializing it. Gate 0 now permits **architecture-contract materialization**: meaningful ownership/evidence files are physically present, while production runtime modules remain locked. Empty production folders and fake placeholder modules are prohibited.

**File-level implementation contract:** `docs/evidence/CFIP-TARGET-FILE-MANIFEST.md` is the authoritative file-by-file materialization manifest. This tree defines ownership and boundaries; the manifest defines concrete target artifacts and acceptance status.

## 1. Canonical target tree

```text
cfip/
├── apps/
│   ├── api/
│   ├── realtime/
│   ├── market_data_worker/
│   ├── analysis_worker/
│   ├── learning_worker/
│   ├── autonomy_worker/
│   └── web/
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
├── packages/
│   ├── contracts/
│   ├── domain_kernel/
│   ├── application_kernel/
│   ├── eventing/
│   ├── observability/
│   ├── security/
│   ├── testing/
│   └── configuration/
├── adapters/
│   ├── inbound/{http,websocket,cli,scheduled_jobs}/
│   └── outbound/{postgres,clickhouse,redis,nats,object_storage,market_providers,broker_providers,model_providers,research_providers,notification_providers}/
├── engines/{technical,structure,liquidity,fvg,order_block,regime,mtf,confluence,contradiction,intelligence_score,scoring,signal,strategy,backtest}/
├── data/{migrations,schemas,seeds,fixtures,retention}/
├── frontend/{app,features,domain,infrastructure,components,chart,i18n,accessibility,tests}/
├── infrastructure/{docker,compose,observability,security}/
├── tests/{architecture,contracts,integration,e2e,replay,pit,performance,security,fixtures}/
├── docs/{architecture,adr,capabilities,evidence,contracts,operations,security,research}/
├── scripts/{bootstrap,audit,codegen,database,release,verification}/
└── .github/{workflows,CODEOWNERS,dependabot.yml,pull_request_template.md}
```

## 2. Context-internal structure

Every backend bounded context should converge on:

```text
contexts/<context>/
├── README.md
├── domain/{entities,value_objects,services,events,policies,errors}/
├── application/{commands,queries,handlers,ports,dto}/
├── infrastructure/{persistence,projections,configuration}/
└── tests/{unit,integration,contract}/
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
└── tests/{test_engine.py,test_pit.py,test_replay.py}
```

The canonical executable identity is `(engine_id, version)`. A directory is not an engine registration. Runtime, durable and replay execution paths reuse the same semantic implementation rather than creating duplicate analytical authorities.

The source study identifies 15 concrete runtime engine classes while the repository has 14 top-level engine namespaces. The target preserves the complete runtime inventory without assuming one-to-one namespace/class cardinality.

## 4. Data/evidence structure

Distinct identities are required for dataset artifact/version, dataset fingerprint/content integrity, PIT market-data revision/view, replay-case identity/expected invariants, replay verification result, learning revision, provenance nodes/edges and immutable evidence references. These must not collapse into a generic revision field.

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

Market/timeframe/candle/event semantics are owned by canonical domain contracts, not chart rendering components.

## 6. Verification structure

```text
tests/{architecture,contracts,integration,e2e,replay,pit,performance,security,fixtures}/
```

Every important capability must map to verification evidence before implementation status advances.

## 7. Materialization policy

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

A production path must have an architectural owner, source/capability mapping, contract or implementation purpose and verification plan. Empty directories are not committed.

## 8. Repository-level rules

- Python modules use `snake_case`.
- TypeScript uses project-standard `camelCase`/`PascalCase` according to artifact type.
- Bounded contexts use stable domain names, not vendor names.
- Contracts carry explicit versions.
- Generated artifacts do not become source ownership by accident.
- Generic `utils`, `helpers`, `misc` and `common` dumping grounds are prohibited without explicit ownership justification.
- `uv.lock` and `pnpm-lock.yaml` are required once their corresponding runtime/toolchain is materialized.
- Kubernetes/Terraform trees are added only when operational evidence justifies them.
- Microservice boundaries are introduced only for measured scale, fault isolation, ownership or security requirements.

## 9. Current physical state

Architecture-contract materialization is now visible in GitHub. The repository contains meaningful `README.md` ownership/boundary contracts for all top-level target areas, all seven application roots, all 33 bounded contexts, all 14 engine namespaces, shared packages, inbound/outbound adapter families, data areas, frontend areas, infrastructure areas, test categories and script categories.

These files are **not runtime implementations**. They explicitly preserve the Gate 0 lock and identify source mapping, ownership, invariants and target responsibility. Production modules remain unmaterialized until their evidence and gate authorize implementation.

## 10. Tree health invariant

The tree is healthy only when every production file has one owner; every CForex capability maps to one target location; every target capability maps back to source evidence or an explicit platform concern; no duplicate authoritative implementation exists; persistence ownership is explicit; contracts are versioned/discoverable; tests map to capabilities; operational scripts are deterministic; documentation cannot contradict the canonical Gate 0 register; and deployment topology can evolve without turning every bounded context into a microservice.
