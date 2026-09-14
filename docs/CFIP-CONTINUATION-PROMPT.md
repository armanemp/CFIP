# CFIP Continuation Prompt

Continue the **CForex → CFIP** migration/source-closure and engineering workflow from the current GitHub state.

## Non-negotiable rules

- Canonical target: `armanemp/CFIP`; source of behavioral truth: `armanemp/CForex`.
- Never use the discarded `cforex-platform`/Laravel architecture as the target.
- Before every batch: inspect current `CFIP/main` and `CForex/main`; read `docs/CFIP-MIGRATION-CONTROL-INDEX.md`, `docs/CFIP-MIGRATION-MASTER-PLAN.md`, `docs/capabilities/source-study-integration.md`, Gate-0 control and latest progress/contradiction sweep.
- Directly apply useful changes to GitHub `main` when permitted; do not wait for approval.
- Do real engineering and verification alongside documentation; avoid report-only batches.
- Preserve history. Do not delete or overwrite source evidence. Do not create duplicate corrective migration/documentation artifacts.
- For an existing mutable target logical migration, correct the original owner; create a new migration only for a genuinely new schema evolution.
- Do not create fake/marker-only runtime files to improve status.
- Gate 0 stays OPEN until executable source-closure evidence is complete. CFIP production runtime stays LOCKED until then.
- Never promote code-search no-result to verified absence.
- Never claim parity, production readiness, test success or CI green without executable evidence.

## Required workflow

1. Re-check current GitHub heads and repository health.
2. Read canonical migration workflow/control docs first.
3. Study CForex source deeply and use the strongest evidence precedence: executable implementation/tests > schema/contracts/migrations > composition/entrypoints > CI/config > prose.
4. Run/extend source-closure tooling in parallel where safe, then reconcile results serially to avoid contradictory canonical docs.
5. Fix actual defects and structural inconsistencies discovered across the whole project, not only the requested item.
6. Keep architecture modern, modular, dependency-directed, globally scalable, observable, secure, i18n/RTL/LTR/accessibility-ready and provider-neutral; avoid novelty-only dependencies and premature microservices.
7. Maintain one canonical `(engine_id, version)` identity and one semantic implementation per engine version; runtime/durable/replay are execution projections, not duplicate engines.
8. Preserve PIT correctness, provenance, lineage, causal ordering, live/replay/backtest semantic compatibility, durable outbox, idempotency, event-time/watermark semantics, governed learning and controlled autonomy.
9. Prefer OpenTelemetry semantic conventions before custom attributes; agent/autonomy controls must remain inspectable, traceable and instrumentable with explicit policy hooks.
10. After changes: verify files, run available tests/CI evidence, update canonical manifest/matrices, perform contradiction sweep, and write a precise progress report.

## Current known baseline

- Source: CForex `main` v0.9.154.
- Target: CFIP `main`.
- Current target inventory: **34 bounded contexts**, **14 engine namespaces**, **15 concrete runtime engine classes**.
- Gate 0: **OPEN**.
- CFIP runtime implementation: **0% / LOCKED**.
- Active architecture/source-closure tooling includes target-contract validation, API/WS census, event census, migration graph validation, engine registry reconciliation and worker lifecycle validation.
- The next priority is to **execute these tools against the complete CForex checkout**, reconcile actual evidence, then add PIT/replay, dependency-direction, frontend, policy/config, adapter and operations closure tooling as needed.

## Required progress report

Every continuation must end with:

- exact current CFIP HEAD;
- exact source baseline;
- actual GitHub changes and files;
- verification evidence and any unverified claims;
- overall progress table;
- detailed D1–D11 Gate-0 table;
- blockers and remaining evidence gaps;
- next engineering actions;
- explicit statement whether Gate 0/runtime status changed.

Use this prompt as the operating contract, then continue from the repository's actual current state rather than assuming any older commit/report is current.
