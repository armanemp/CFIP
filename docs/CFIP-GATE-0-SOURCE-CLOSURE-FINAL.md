# CFIP Gate 0 — Source Closure — Canonical Final Register

**Source:** `armanemp/CForex` `main` current evidence snapshot `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Status:** **OPEN — controlled implementation permitted; production promotion locked**  
**Runtime implementation:** **CONTROLLED / PROMOTION-LOCKED**

> This register is the canonical Gate-0 status surface. Historical reports remain evidence history. Current operating semantics are governed by this register plus `docs/CFIP-GATE-0-SOURCE-CLOSURE-CONTROLLED-IMPLEMENTATION.md`, the continuation prompts, active amendments and the engineering integrity protocol.

## 1. Gate purpose

Gate 0 prevents semantic loss during migration from CForex to CFIP. It establishes source evidence, target ownership, contract boundaries, verification requirements and explicit promotion locks before any uncontrolled production behavior is permitted.

Gate 0 is **not** a prohibition on all coding. Controlled implementation is permitted when it is source-evidenced or explicitly justified as a target addition, contract-first, reversible, testable, observable, tied to an ECP/change identity and kept behind the applicable runtime/promotion gates.

## 2. Operating rules

- Source behavior is established from executable CForex implementation/tests first, then migrations/contracts/runtime composition, then CI/configuration, then documentation.
- Target directory existence is never evidence of capability, parity, scale or production readiness.
- One canonical analytical implementation owns each `(engine_id, version)`; runtime/durable/replay surfaces are adapters/projections, not duplicate engines.
- Platform Intelligence is cross-cutting and governed; it never becomes a second domain authority.
- AI/agent execution is limited to governed application tools/policies; agents do not receive direct SQL/infrastructure authority.
- High-impact or irreversible runtime actions remain locked until their specific release and safety evidence is complete.
- Every report separates **Applied**, **Verified**, and **Open**. Previous CI is not silently reused as current-head evidence.

## 3. Evidence precedence

1. executable implementation and executable tests;
2. migrations, database schemas and machine-readable contracts;
3. runtime composition, adapters and deployment configuration;
4. CI, scripts and operational configuration;
5. architecture/state documentation;
6. release prose and historical descriptions.

Unresolved behavior remains explicitly unresolved; names alone are not semantic evidence.

## 4. Atomic migration unit

Every capability is migrated as:

`source implementation → behavioral contract → data contract → event contract → runtime boundary → API/UI contract → verification evidence → target ownership → parity evidence`

Lifecycle:

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

No lifecycle stage may be skipped or inferred from repository structure alone.

## 5. Current D1–D11 state

| ID | Domain | Current state | Principal closure gap |
|---|---|---|---|
| D1 | API/WS | ADVANCED / OPEN | exhaustive route/channel lifecycle/auth/entitlement evidence |
| D2 | Events | ADVANCED / INTEGRATION OPEN | live PostgreSQL/NATS lifecycle, topology, ordering and recovery evidence |
| D3 | Data/PIT | ADVANCED / OPEN | authoritative PIT/revision reconstruction, dataset integrity, residency/retention evidence |
| D4 | Engines | ADVANCED / STRUCTURE VERIFIED / PARITY OPEN | source-wide parity, golden fixtures, PIT/replay and engine integration evidence |
| D5 | Workers | ADVANCED / OPEN | lifecycle-complete worker topology, checkpoint/lease/recovery/capacity evidence |
| D6 | Frontend | IN PROGRESS / OPEN | workflow, realtime, i18n, accessibility, performance and integration evidence |
| D7 | Tests | STRONGER / OPEN | whole-capability negative/security/integration/PIT/replay closure |
| D8 | Policy/config | IN PROGRESS / OPEN | exhaustive invariant/config/tenant/entitlement/feature/policy classification |
| D9 | Adapters | ADVANCED / OPEN | concrete provider/broker/model/research lifecycle and failure evidence |
| D10 | Operations | IN PROGRESS / OPEN | SLO/capacity/DR/RPO/RTO/residency/security/observability closure |
| D11 | Reconciliation | STRONGER / OPEN | zero unresolved material contradiction across canonical docs and source/target matrices |

## 6. Current implementation policy

The repository may contain controlled runtime implementation during Gate 0. Such code is explicitly **not** parity evidence and does not authorize production promotion. Each implementation slice must have an owner, contract, tests, observability/recovery requirements, rollback path and current verification evidence.

The previous wording that made all runtime implementation categorically locked before Gate-0 closure is superseded by this register and the active controlled-implementation protocol.

## 7. Global-scale requirement

Global scale is a first-class architecture constraint from the beginning: stateless regional APIs, deterministic partition ownership, lease/checkpoint recovery, bounded queues/backpressure, tenant/noisy-neighbor isolation, regional routing and data residency, PostgreSQL partitioning/retention, ClickHouse analytical isolation, cache bounds, workload isolation, schema evolution, quotas/fair use, SLO/capacity methodology, RPO/RTO and cost-aware degradation.

No production capacity claim is valid until representative load methodology and executable evidence exist.

## 8. Platform Intelligence requirement

Every applicable capability is evaluated against:

`observe → context → reason → act → verify → learn → audit → safety`

The intelligence layer records provenance, policy context, evidence and outcomes and may propose governed actions. It cannot bypass domain ownership, safety policy, approval requirements, audit history or release gates. `packages/intelligence-runtime` is a dependency-free lifecycle contract boundary, not an autonomous execution authority.

## 9. Analytical/indicator requirement

Technical indicators are implemented under one physical owner per family in `engines/technical/src/cfip_technical/indicators/`, with a versioned catalog and semantic evidence adapter. Current target engineering includes 24 registered indicator families/output sets, including DEMA, TEMA, TRIX and Parabolic SAR in the current controlled slice.

These implementations remain **PARITY UNVERIFIED** until source-specific formulas/defaults, warm-up/missingness semantics, numerical tolerances, golden fixtures and PIT/replay evidence are closed.

The single final analysis boundary is `AnalysisConsensusService`. Indicator outputs are translated to `SpecialistEvidence`; unsupported semantics fail closed. Consensus exposes deterministic conflict classification and an explanation trace in addition to direction, score, confidence, agreement and revision identity.

## 10. Repository structure hygiene

Empty or README-only directories are not created merely to mirror source names. A target namespace is retained only when it is an explicit architecture contract/ownership boundary or contains executable implementation. Redundant compatibility facades and unused placeholder engine namespaces are removed after reference analysis. Source engine census documents remain evidence records and must not be confused with physical target implementation.

## 11. Gate closure criteria

Gate 0 can close only when the evidence graph supports all high-impact capabilities: exhaustive API/WS and event lifecycle mapping; authoritative data/PIT/revision ownership; executable engine contracts and deterministic/replay evidence; worker/frontend workflow closure; complete test/security/policy/config/adapter/operations classification; global-scale methodology; Platform Intelligence governance; and zero unresolved material documentation contradiction.

Closure means the target can be implemented without material semantic guessing. It does **not** mean CFIP is already production-ready.

## 12. Current decision

**GATE 0: OPEN**  
**PRODUCTION PROMOTION: LOCKED**  
**LIVE/HIGH-IMPACT IRREVERSIBLE ACTIONS: LOCKED**

The project may continue with controlled, evidence-backed implementation and documentation reconciliation. Parity and production readiness remain separate evidence gates.
