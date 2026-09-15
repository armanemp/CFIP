# CFIP Documentation & Engineering Progress Report — Batch 71

Date: 2026-09-15  
Source: `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
Target: `armanemp/CFIP` `main` — Batch 71

## Executive result

Batch 71 converts repository hygiene from a path-limited architecture check into an always-on repository control. The validator now inspects every current-tree path and every file's raw bytes, while excluding only repository/runtime cache internals. Tests cover text, filenames and extensionless artifacts. A dedicated GitHub Actions workflow executes the hygiene test and validator on every pull request and every push to `main`.

The continuation contract and migration control index were reconciled with this stronger enforcement model. No business semantics were changed. This batch still does not claim source closure, parity, runtime capacity, disaster-recovery readiness or production readiness.

## Exact evidence snapshot

- Source HEAD rechecked: `900882154cab3b9b74d0543b9bbf72a708a08134`.
- CFIP repository metadata confirms `main` is the default branch and the connected GitHub integration has write permission.
- Batch 71 writes were applied directly to `main` through the connected GitHub integration.
- Final executable CI status is **not claimed** until GitHub exposes a fresh workflow result for the final head.

## Engineering changes

### 1. Complete-tree hygiene validator

`tools/architecture/validate_target_contracts.py` now:

- scans path names as well as file contents;
- scans raw bytes instead of relying on a text-extension allow-list;
- catches extensionless artifacts and new file types automatically;
- keeps repository/runtime cache directories excluded to avoid scanning generated internals;
- keeps detection markers encoded so the validator cannot reproduce the strings it is designed to reject;
- preserves the existing canonical-file, bounded-context and migration-ownership checks.

### 2. Stronger validator tests

`tests/architecture/test_validate_target_contracts.py` now covers:

- clean current repository;
- obsolete content in a normal text file;
- obsolete content in a filename/path;
- obsolete content in an extensionless file;
- canonical contract inventory.

### 3. Always-on CI gate

Added `.github/workflows/repository-hygiene.yml`:

- triggers on every pull request;
- triggers on every push to `main`;
- uses read-only `contents` permissions;
- runs the focused validator test;
- runs the complete-tree hygiene validator;
- has a bounded five-minute job timeout.

This closes the previous trigger-path gap where a hygiene failure in an unrelated file type could bypass the architecture workflow simply because the change did not touch an architecture-sensitive path.

## Documentation changes

- `docs/CFIP-CONTINUATION-PROMPT.md` now makes the always-on hygiene workflow an explicit verification requirement.
- `docs/CFIP-MIGRATION-CONTROL-INDEX.md` registers Batch 71 and records the stronger hygiene control.
- This report records the actual engineering/documentation changes and verification boundary.

## Standards alignment

The workflow uses explicit read-only token permissions and a bounded job, consistent with GitHub Actions' permission model; GitHub documents that explicitly setting permissions restricts unspecified scopes to none and that job-level permissions can further narrow access. citeturn0search0

The focused Python tests use `unittest`, whose documented command-line discovery/execution model supports direct module execution used by the repository workflow. citeturn0search4

## D1–D11 progress

| Dimension | Batch 71 impact | Current status | Main open closure |
|---|---|---|---|
| D1 API/WS | governance-only | ADVANCED | exhaustive route/channel registry and lifecycle evidence |
| D2 Events | governance-only | ADVANCED | producer→outbox→consumer→recovery closure |
| D3 Data/PIT | governance-only | ADVANCED / OPEN | authoritative ownership and executable reconstruction evidence |
| D4 Engines | governance-only | ADVANCED / BOUNDED | PIT/replay/fixture/telemetry closure |
| D5 Workers | governance-only | ADVANCED | checkpoint/lease/recovery/scale lifecycle evidence |
| D6 Frontend | no semantic change | IN PROGRESS | route/feature/workflow/i18n/accessibility evidence |
| D7 Tests | stronger repository-wide hygiene coverage | IN PROGRESS | integration/E2E/security/recovery/performance closure |
| D8 Policy/config | stronger repository hygiene | IN PROGRESS | exhaustive hardcode/policy/config classification |
| D9 Adapters | no transport invention | IN PROGRESS | broker/provider/model/research lifecycle closure |
| D10 Operations | stronger always-on CI control | IN PROGRESS | SLO/capacity/DR/residency/security evidence |
| D11 Reconciliation | stronger current-tree enforcement | IN PROGRESS | whole-repo contradiction/duplicate ownership closure |

## Overall progress

| Area | Status | Evidence / boundary |
|---|---|---|
| Repository governance | **STRONGER** | always-on hygiene workflow + validator |
| Documentation integrity | **STRONGER** | canonical contract/index reconciled |
| Obsolete-reference hygiene | **ENFORCED** | complete-tree/path-aware scan + tests + every-change CI |
| Source study | **OPEN / ADVANCING** | source HEAD rechecked; capability closure ongoing |
| Source closure | **OPEN** | material evidence gaps remain |
| Target engineering | **ADVANCING** | Gate-0-compatible implementation continues |
| Realtime foundation | **ADVANCING / UNVERIFIED INTEGRATION** | contracts/runtime/migrations exist; live DB/broker evidence open |
| PostgreSQL integration | **OPEN** | executable upgrade/downgrade and runtime integration evidence required |
| PIT/replay | **ADVANCED / OPEN** | contracts/tooling exist; full lifecycle closure remains |
| Analytical engines | **ADVANCED / BOUNDED** | registry/implementation evidence exists; parity fixtures/telemetry closure open |
| Workers | **ADVANCED / OPEN** | lifecycle contracts exist; repository/recovery evidence remains |
| Frontend | **IN PROGRESS** | workflow and evidence census incomplete |
| Policy/config | **IN PROGRESS** | hardcode/config classification incomplete |
| Adapters | **IN PROGRESS** | source-derived provider/broker/model/research closure incomplete |
| Observability | **IN PROGRESS** | realtime lag/lateness/watermark/backpressure evidence open |
| Security | **IN PROGRESS** | Admin Git write-path/test census remains open |
| Platform Intelligence | **CROSS-CUTTING** | governed boundary established; capability-wide closure ongoing |
| Global-scale architecture | **CONTRACTED** | architecture requirements explicit |
| Global-scale capacity | **UNPROVEN** | representative load/failure-domain evidence required |
| DR/RPO/RTO | **UNPROVEN** | executable recovery evidence required |
| Data residency | **REQUIRED / UNPROVEN** | regional/jurisdiction evidence required where applicable |
| Production readiness | **LOCKED** | intentionally not claimed |
| Gate 0 | **OPEN** | source-closure exit evidence incomplete |

## Open evidence blockers

1. Source-derived broker/transport census sufficient for an evidence-backed adapter.
2. Executable PostgreSQL migration upgrade/downgrade integration evidence.
3. Durable checkpoint/lease repository integration and transactional fencing evidence.
4. Consumer restart/recovery and replay integration.
5. Realtime lag/lateness/watermark/backpressure telemetry.
6. Current-head Admin Git write-path and test census.
7. Raw-byte hash/count reconciliation for outstanding training datasets.
8. Whole-repository dependency, hardcode, duplicate ownership and contradiction closure.
9. Representative global-scale capacity/load/failure-domain/DR evidence.

## Verification boundary

Verified by repository read-back:

- current canonical continuation contract was updated;
- control index was updated;
- validator was updated;
- validator tests were updated;
- always-on hygiene workflow was created.

Not yet claimed:

- a green GitHub Actions run for the final head;
- local full-suite execution (direct external network access from the execution environment remains unavailable);
- source parity;
- PostgreSQL runtime integration;
- broker/runtime recovery;
- global-scale capacity;
- production readiness.

## Next parallel tracks

### Track A — source/broker evidence
Perform a source census of broker/transport abstractions, concrete integrations, configuration, failure semantics, tests and operational entrypoints before implementing any transport-specific target adapter.

### Track B — durable realtime state
Close repository implementations for checkpoints/leases, fencing, transactional ownership and recovery, then connect them to executable integration tests.

### Track C — PIT/replay
Trace dataset identity, revisions, event-time ordering, reconstruction, replay loading and integrity checks end-to-end.

### Track D — realtime telemetry
Implement/verify queue depth, consumer lag, event-time watermark, lateness, processing latency and backpressure/degradation telemetry without making telemetry authoritative state.

### Track E — PostgreSQL evidence
Run executable migration and integration evidence in CI, including upgrade/downgrade, transactional behavior and failure/recovery boundaries.

### Track F — Admin Git
Complete the current-head write-path/test census and reconcile the governance adapter with target policy and audit boundaries.

### Track G — whole-repository audit
Parallelize dependency direction, hardcode inventory, duplicate ownership, dead artifacts, documentation contradiction and CI coverage scans; serialize canonical fixes.

### Track H — global scale
Build measurable capacity, isolation, regional consistency, recovery and cost evidence before making any scale-readiness claim.

## Gate / runtime status

- **Gate 0:** OPEN.
- **Controlled target engineering:** PERMITTED when source-evidenced, contract-first, reversible, testable and independently verifiable as required.
- **Production promotion:** LOCKED.
- **Live trading / irreversible high-impact mutation:** LOCKED behind applicable gates.
- **Autonomous unrestricted mutation:** NOT PERMITTED.
- **Global-scale readiness:** NOT CLAIMED.

Batch 71 is a real engineering/control improvement, not a progress-metric change. It strengthens the repository's ability to prevent reintroduction of obsolete material while leaving business semantics untouched and preserving the evidence gates for all higher-risk claims.
