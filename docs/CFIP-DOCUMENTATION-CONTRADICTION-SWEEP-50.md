# CFIP Documentation Contradiction Sweep — Batch 50

## Scope

Reviewed the canonical migration control index, continuation contract references, Gate-0 state, ADR-005 Platform Intelligence contract, global-scale contracts, capability matrix, CForex carry-forward baseline, Evolution Control Plane, Intelligence Training Lifecycle and latest progress evidence.

## Findings

### 1. Internal Git semantics — normalized

The project previously referred to an Evolution Control Plane but did not have a single explicit contract describing its relationship to Git. Batch 50 establishes the rule that Git/GitHub remains the canonical VCS and ECP is an evidence/governance layer above it. ECP cannot rewrite history or conceal failed changes.

### 2. Autonomous development lifecycle — normalized

ADR-005 already required checkpoint, isolated change, verification, promotion, health guard and rollback. The ECP now provides the project-control entities and state model that operationalize those concepts without claiming that the runtime implementation already exists.

### 3. Intelligence learning — normalized

ADR-005 and existing source evidence required governed learning, calibration and drift. The new Intelligence Training Lifecycle makes the continuous process explicit and covers engineering, market/trading, research and operations. It preserves temporal/leakage-aware evaluation and governed promotion.

### 4. CForex carry-forward — strengthened

The source contains material capabilities that could otherwise be lost between release notes and the CFIP capability registry. The new carry-forward baseline converts these into explicit obligations classified as `PRESERVE`, `IMPROVE`, `REPLACE` or `INTENTIONALLY-DIVERGE` during closure.

### 5. Gate 0 — unchanged and consistent

No new document or governance feature claims Gate 0 closure. Business runtime remains 0% / LOCKED. Governance, evidence, validators, documentation and other runtime-independent quality infrastructure remain permitted.

### 6. Scale claims — bounded

Global-scale architecture requirements remain requirements/evidence obligations, not capacity claims. ECP and intelligence workloads are explicitly required to use bounded concurrency, policy, verification and resource isolation before production readiness.

## Verification

Architecture Contracts CI run **#135 PASS** on `09e71f6e7074bb44c8a2406f9d34a9deee123416`, including global-scale, Platform Intelligence, PIT/replay, worker lifecycle and migration-control checks.

## Result

**No unresolved contradiction requiring an architecture reversal was found. Batch 50 closes the documentation gap around internal project-control semantics, continuous intelligence training governance and CForex capability carry-forward.**
