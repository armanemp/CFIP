# CFIP Documentation / Engineering Progress Report — Batch 51

## Evidence snapshot

- CForex source: `main` / v0.9.154.
- CFIP current HEAD at report creation: `462cd38a81cb27d967f8bb366a0f58ff7a498d7d`.
- Gate 0: **OPEN**.
- CFIP production business runtime: **0% / LOCKED**.
- Documentation + Gate-0-compatible engineering: **ACTIVE IN PARALLEL**.
- The GitHub connector currently exposes no workflow-run/status result for the new push commits, so this batch does **not** claim a fresh green CI run. The last confirmed Architecture Contracts green run remains #135 on its recorded commit; current HEAD requires fresh CI evidence.

## Batch 51 engineering/governance work

1. Added `data/training/CFIP-CFOREX-TRAINING-DATASET-INDEX-v0.1.json` as a governed carry-forward index for the CForex training/evaluation dataset family. It records source paths, source hashes, declared record counts, synthetic status, promotion restrictions and materialization state.
2. Added `docs/governance/CFIP-ECP-DATA-CONTRACT.md` to make ECP checkpoint/evidence identity and training-dataset provenance/materialization rules machine-auditable and explicit.
3. Added `tools/governance/validate_training_dataset_index.py` and architecture tests for the new dataset-governance boundary.
4. Extended `.github/workflows/architecture-contracts.yml` so training-data governance is tested and validated together with the existing architecture contracts.
5. Updated the canonical migration control index so source training/evaluation manifests must be reconciled against dataset blobs before materialization.
6. During source inspection, found a material integrity discrepancy that must remain visible: the CForex v0.9.154 source baseline's v0.21 training manifest declares 330 records, while the directly retrieved source dataset blob evidence exposes 108 JSONL records. CFIP deliberately does **not** copy a partial dataset or trust the declared count without reconciliation.
7. Preserved the source discrepancy as a governed blocker rather than hiding it or converting it into a false dataset-completeness claim.

## Source dataset evidence discovered

| Source artifact | Declared records | Direct blob evidence | CFIP status |
|---|---:|---:|---|
| `SEED-DATASET-MANIFEST-v0.19.json` | 204 | not yet materialized | SOURCE_EVIDENCE_ONLY |
| `SEED-DATASET-MANIFEST-v0.20.json` | 222 | not yet materialized | SOURCE_EVIDENCE_ONLY |
| `SEED-DATASET-MANIFEST-v0.21.json` | 330 | 108 currently exposed records | BLOCKED_PENDING_SOURCE_INTEGRITY_RECONCILIATION |

The source v0.21 manifest also explicitly marks the dataset synthetic-only, not promotion-eligible and requiring evaluation. This is treated as training/evaluation evidence, never as real market truth.

## Verification performed

- Repository state re-read from GitHub after each mutation.
- Dataset index contains explicit source identity and governance restrictions.
- New validator enforces required fields, unique manifests, positive declared counts, synthetic-data restrictions, blocked-entry evidence notes and governance invariants.
- New unittest suite covers valid blocked-source entries, synthetic promotion rejection, missing integrity notes and duplicate manifest detection.
- Workflow was updated to execute the new tests/validator.
- No Gate-1 business runtime was introduced.

Fresh CI status for current HEAD is **UNVERIFIED** because the available GitHub status/run interface returned no run/status record for the new push commits. This is intentionally reported as unverified rather than assumed green.

## Progress

| Dimension | Batch 50 | Batch 51 | Change | State |
|---|---:|---:|---:|---|
| Source inventory & architecture | 93% | 93% | 0 | Advanced / Open |
| API/WebSocket (D1) | 78% | 78% | 0 | Advanced+ / Open |
| Event topology (D2) | 73% | 73% | 0 | Advanced+ / Open |
| Data/PIT/replay (D3) | 79% | 80% | +1 | Advanced++ / Open |
| Analysis engines (D4) | 79% | 79% | 0 | Advanced+ / Open |
| Workers/realtime (D5) | 79% | 79% | 0 | Advanced+ / Open |
| Frontend (D6) | 62% | 62% | 0 | Advanced / Open |
| Tests/verification (D7) | 84% | 85% | +1 | Advanced / Open |
| Policy/config (D8) | 81% | 81% | 0 | Advanced+ / Open |
| External adapters (D9) | 63% | 63% | 0 | Advanced / Open |
| Observability/governance/intelligence | 88% | 89% | +1 | Advanced++ / Open |
| Operations/global scale (D10) | 61% | 61% | 0 | In Progress+ / Open |
| Cross-matrix reconciliation (D11) | 76% | 77% | +1 | Advanced / Open |
| **Overall source closure / architecture readiness** | **~79%** | **~79–80%** | **evidence-weighted incremental advance** | **OPEN** |

These percentages are evidence/architecture closure estimates, not production runtime-code completion. They are deliberately conservative because the newly discovered dataset discrepancy remains unresolved.

## D1–D11 detailed status

| Domain | % | Current evidence state | Highest-value remaining closure |
|---|---:|---|---|
| D1 API/WS | 78% | source census/control contract remains strong | exhaustive lifecycle graph + controlled parity cases |
| D2 Events | 73% | event graph/control foundation | complete producer → outbox → subject → consumer → retry/idempotency → replay evidence |
| D3 Data/PIT | 80% | PIT/replay contract plus governed dataset identity and integrity blocker | deterministic reconstruction, full fingerprints, leakage/availability evidence, source dataset reconciliation |
| D4 Engines | 79% | canonical identity/composition model | all concrete source engines mapped to deterministic fixtures and controlled composition |
| D5 Workers | 79% | lifecycle contract + realtime semantics | partition ownership, leases/checkpoints, recovery and scale evidence |
| D6 Frontend | 62% | architecture/census baseline | workflow parity, intelligence UX, accessibility, i18n/RTL/LTR and performance evidence |
| D7 Tests | 85% | architecture governance suite expanded | fresh CI evidence + end-to-end/PIT/recovery/capacity/independent verification |
| D8 Policy | 81% | policy/config census + governance | exhaustive hardcode, entitlement, feature-flag and deployment reconciliation |
| D9 Adapters | 63% | target boundaries defined | provider/broker/model/research lifecycle, health, rights and failure evidence |
| D10 Operations | 61% | global-scale obligations validated | measured capacity/SLO, DR/RPO/RTO, residency and failure-domain evidence |
| D11 Reconciliation | 77% | control index + carry-forward + intelligence + dataset identity integrated | source ↔ capability ↔ parity ↔ target ↔ ADR ↔ ECP ↔ dataset evidence ↔ Gate-0 closure |

## Current blockers

1. Gate 0 remains open; production business runtime remains locked.
2. Fresh CI evidence for current HEAD is not exposed by the current connector status/run interface and must not be assumed.
3. D1/D2/D5/D6/D9/D10 executable/source evidence gaps remain.
4. D3 has a concrete source dataset integrity discrepancy: v0.21 declares 330 records while the directly retrieved source blob exposes 108 records; materialization is therefore blocked.
5. Platform Intelligence and continuous training are governed by architecture/contracts, but runtime intelligence implementation/readiness remains unverified.
6. ECP is currently a governance architecture contract; runtime persistence/workflow implementation belongs to the appropriate later gate.
7. Global scale remains architecture-ready but not capacity-proven; measured load, SLO, DR and residency evidence remain required.

## Next parallel tracks

- Reconcile the CForex v0.21 dataset manifest/blob discrepancy from authoritative source evidence before materialization.
- Inspect all remaining CForex training/research/autonomy data directories and manifests and build a complete carry-forward inventory.
- Continue D3 deterministic PIT/replay reconstruction and dataset fingerprints.
- Close D1/D2 lifecycle graphs and D5 worker ownership/checkpoint/recovery evidence.
- Continue D10 measured scale/SLO/DR/residency evidence.
- Keep ECP runtime implementation gated to its authorized migration phase while strengthening its evidence schema now.
- Run the governed intelligence-learning/evaluation loop on each newly verified evidence set; do not promote synthetic or unverified material.
