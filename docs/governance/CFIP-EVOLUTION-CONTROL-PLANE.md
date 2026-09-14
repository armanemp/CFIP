# CFIP Evolution Control Plane (ECP)

**Status:** Accepted governance architecture; Gate 0 compatible

## Purpose

The Evolution Control Plane (ECP) is CFIP's internal project-control and governed-evolution layer above Git. Git/GitHub remains the canonical version-control system; ECP adds structured project state, evidence, checkpoints, reviews, verification, promotion, health guards, rollback and audit semantics so autonomous development can operate like a disciplined professional engineering organization.

ECP is not a replacement VCS, not a second Git implementation and not a hidden mutable state store.

## Core model

```text
Intent / Issue
    ↓
Change Proposal
    ↓
Risk + Scope + Ownership
    ↓
Checkpoint
    ↓
Isolated Change Set
    ↓
Automated Checks
    ↓
Independent Verification
    ↓
Review / Policy Decision
    ↓
Promotion
    ↓
Post-Promotion Health Guard
    ↓
Verified Outcome
    ↓
Learn / Reconcile / Close
```

Every transition is attributable to a principal, timestamp, repository revision and evidence set.

## Git relationship

- Git commit/tree is the immutable technical revision anchor.
- Git branch/worktree/PR is the implementation isolation mechanism.
- ECP change ID is the project-level identity spanning proposal, evidence, checks and outcome.
- A checkpoint records the exact Git revision plus relevant evidence fingerprints.
- Promotion records the source revision, target ref, policy decision and verification evidence.
- Rollback points to a known-good Git revision; it does not rewrite history.
- ECP never edits Git history to hide an outcome.

## Project-control entities

### Change Proposal

A change proposal describes why a change exists, affected capabilities, expected behavior, risk class, owner, dependencies, acceptance criteria and rollback plan.

### Work Unit

A bounded implementation/evidence task linked to one or more capabilities and a parent change proposal. Work units can be parallelized when they do not share mutable canonical state.

### Checkpoint

An immutable snapshot containing repository revision, source/target evidence snapshot, relevant configuration identity, test/check results and a human/agent-readable summary.

### Verification Run

A machine-generated record of checks, tool versions, inputs, outputs, status, duration and evidence references. A passing run cannot be claimed when a check was skipped or unexecuted.

### Review Decision

A policy decision recording reviewer/agent identity, scope, findings, disposition and required follow-up. Independent verification must be attributable separately from the change author where the risk class requires it.

### Promotion

A controlled transition of a verified revision to a target branch/environment/release channel. Promotion is allowed only when required gates and evidence exist.

### Health Guard

A bounded post-promotion observation window with predefined failure signals, rollback criteria and termination conditions.

### Rollback

A reversible return to a known-good revision or configuration state. Rollback preserves all evidence and never deletes the failed change history.

### Incident / Outcome

The observed result after promotion, including regressions, user/market impact, performance impact, security findings, recovery actions and learning inputs.

## State machine

Change lifecycle:

`PROPOSED → TRIAGED → PLANNED → CHECKPOINTED → IMPLEMENTING → VERIFYING → REVIEWED → APPROVED → PROMOTED → GUARDED → VERIFIED → CLOSED`

Exceptional transitions:

- `VERIFYING → REJECTED`
- `REVIEWED → CHANGES_REQUESTED`
- `PROMOTED → ROLLBACK_PENDING`
- `GUARDED → ROLLBACK_PENDING`
- `ROLLBACK_PENDING → ROLLED_BACK`
- `ROLLED_BACK → REOPENED`
- `CLOSED → SUPERSEDED` only when a replacement change preserves the historical record.

No transition may delete prior evidence.

## Risk classes

- **R0 — Documentation/evidence only:** no runtime behavior impact.
- **R1 — Low-risk reversible engineering:** bounded, testable, reversible and independently verifiable.
- **R2 — Material runtime/configuration change:** stronger integration, security and rollback evidence required.
- **R3 — High-impact/security/data/risk/execution change:** explicit policy gate, independent verification and stronger health guard required.
- **R4 — Irreversible/high-consequence action:** requires explicit governance authorization and must never be auto-promoted solely by model confidence.

Risk classification is evidence-driven and may be escalated automatically when scope expands.

## Autonomous operation

Low-risk reversible changes may be promoted automatically only after:

1. checkpoint exists;
2. source/target HEADs are stable;
3. required tests and static checks pass;
4. independent verification passes;
5. security/policy checks pass;
6. acceptance criteria are satisfied;
7. rollback target exists;
8. health-guard criteria are registered.

R2–R4 actions require progressively stronger policy controls. The autonomy system cannot change the policy that governs its own action, cannot modify its own evidence ledger, and cannot suppress a failed verification result.

## Internal audit ledger

The ledger is append-oriented and records at least:

`event_id, change_id, parent_event_id, event_type, actor_id, actor_kind, repository, revision, target_ref, timestamp, risk_class, capability_ids, evidence_refs, policy_decision, result, correlation_id`

The ledger is evidence, not domain truth. It must be reconstructable from Git plus ECP records and must not become an implicit business database.

## Concurrency and locking

- Parallel read/evidence work is encouraged.
- Canonical state transitions are serialized per change ID.
- Shared mutable artifacts have explicit ownership.
- Conflicting changes require reconciliation before promotion.
- Stale checkpoints cannot authorize promotion of a changed revision.
- Distributed agents must use version/freshness checks and bounded leases rather than assuming local state is globally authoritative.

## Project board semantics

The ECP board is capability/evidence driven rather than ticket-count driven. Each work unit exposes:

- current state;
- capability IDs;
- gate/domain;
- source evidence status;
- implementation status;
- verification status;
- blockers;
- dependencies;
- latest checkpoint;
- latest CI/verification run;
- promotion/rollback state;
- owner/agent identity;
- next deterministic action.

## Release semantics

A release is a signed/identified collection of Git revisions and ECP evidence, not merely a tag. It must include:

- source/target baseline;
- included change IDs;
- capability deltas;
- schema/data evolution identity;
- dependency identity;
- CI and independent verification results;
- security/policy result;
- known limitations;
- rollback target;
- health-guard policy;
- release outcome.

## Safety invariants

- No history rewriting to conceal failures.
- No silent deletion of capabilities or evidence.
- No autonomous modification of governance roots.
- No direct agent SQL/infrastructure authority.
- No promotion without required evidence.
- No claim of parity from static presence alone.
- No rollback without preserving the failed revision and its evidence.
- No unbounded self-healing loop.
- No cross-agent shared-state mutation without ownership/version checks.

## Gate 0 relationship

ECP governance contracts, validators, tests, documentation and audit tooling are permitted while Gate 0 is open. Production business runtime implementation remains locked until Gate 0 closes.

The ECP is therefore usable from the migration/evidence phase without prematurely implementing the target trading runtime.
