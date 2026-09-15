# CFIP Documentation & Engineering Progress Report — Batch 76

**Date:** 2026-09-15  
**Source:** `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main` — current HEAD is the commit containing this report.  
**Gate 0:** OPEN — controlled implementation permitted; production promotion locked.

## 1. Root-cause result

The first materialized target migration graph exposed a validator defect that was hidden while the revision directory was empty. The validator scanned the entire migration root and incorrectly treated Alembic infrastructure files such as `env.py` as migration revisions.

The fix is now implemented and tested:

- migration graph scanning scopes to `versions/` when that directory exists;
- `__init__.py` is ignored inside revision directories;
- tests explicitly cover `env.py`, template files and package initializers being excluded;
- actual revision files remain fully parsed and validated for duplicate revisions, missing parents/dependencies and logical-object reuse warnings.

This is a genuine CI/control-plane root-cause fix, not a workflow bypass.

## 2. Verification evidence

On the affected run, every architecture-contract test through the migration graph unit tests passed. The only failure was the materialized migration-graph execution step. The new commit triggered a fresh Architecture Contracts run; its early steps and the new migration-graph unit test were observed passing while the workflow was still running. Final green status is therefore **not claimed until the run completes**.

Repository Hygiene on the preceding current HEAD passed.

## 3. Engineering state after Batch 76

### Durable event path

`source durable outbox → async claim contract → PostgreSQL atomic claim → monotonic fencing → async transport publish → fenced durable transition`

The PostgreSQL adapter remains runtime-unverified. Its deterministic tests are not substituted for live concurrency evidence.

### Governance

Gate 0 remains open for controlled implementation. Production promotion remains locked.

### Migration ownership

Fencing remains consolidated into canonical migration `0001_analysis_execution_outbox`; no duplicate corrective migration is retained.

## 4. D1–D11

| Domain | Status | Current evidence | Remaining highest-value closure |
|---|---|---|---|
| D1 API/WS | ADVANCED | architecture census | lifecycle/auth/entitlement closure |
| D2 Events | ADVANCED / INTEGRATION OPEN | async contracts + PostgreSQL adapter + fencing | JetStream topology + E2E |
| D3 Data/PIT | ADVANCED / OPEN | migration contracts | PIT reconstruction + revision identity |
| D4 Engines | ADVANCED / BOUNDED | registry/contracts | PIT/replay/fixture closure |
| D5 Workers | ADVANCED / OPEN | async storage boundary | recovery/ownership/capacity |
| D6 Frontend | IN PROGRESS | census/contracts | product workflow/i18n/a11y |
| D7 Tests | IN PROGRESS | architecture + adapter unit coverage | live integration/race/performance |
| D8 Policy/config | IN PROGRESS | governance validators | exhaustive hardcode/config closure |
| D9 Adapters | ADVANCED / OPEN | NATS + PostgreSQL adapters | live lifecycle integration |
| D10 Operations | IN PROGRESS | global-scale contracts | capacity/DR/residency/telemetry |
| D11 Reconciliation | STRONGER / OPEN | docs/code/CI root-cause reconciliation | whole-repo closure |

## 5. Overall status

| Area | Status |
|---|---|
| Repository governance | STRONGER |
| Documentation integrity | STRONGER |
| Source study | ADVANCING / OPEN |
| Target engineering | ADVANCING |
| Eventing | ADVANCED / INTEGRATION OPEN |
| PostgreSQL durability | IMPLEMENTED / RUNTIME UNVERIFIED |
| Realtime | ADVANCED / INTEGRATION OPEN |
| PIT/replay | ADVANCED / OPEN |
| Frontend | IN PROGRESS |
| Security | IN PROGRESS |
| Platform Intelligence | CROSS-CUTTING |
| Global-scale architecture | CONTRACTED |
| Global-scale capacity | UNPROVEN |
| DR/RPO/RTO | UNPROVEN |
| Data residency | REQUIRED / UNPROVEN |
| Production readiness | LOCKED |

## 6. Next parallel tracks

1. **PostgreSQL live integration:** concurrent claimers, stale-owner race, isolation, pool and timeout budgets.
2. **JetStream lifecycle:** stream/consumer registry, retention/replay, end-to-end dispatch.
3. **Realtime recovery:** checkpoint/lease repository, restart/reassignment, watermark/lateness telemetry.
4. **Source census:** event families, consumers, providers/brokers/models/research and Admin Git write path.
5. **PIT/data:** reconstruction, revision identity and dataset byte/hash/count reconciliation.
6. **Global operations:** tenant isolation, regional consistency, capacity/failure-domain testing and DR.

## 7. Gate status

- Gate 0: **OPEN**.
- Controlled implementation: **PERMITTED**.
- Production promotion: **LOCKED**.
- Live trading: **NOT PERMITTED**.
- Unrestricted autonomous mutation: **NOT PERMITTED**.
- Global-scale readiness: **NOT CLAIMED**.
