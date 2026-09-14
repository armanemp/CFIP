# CFIP Evidence-Driven Speed and Closure Protocol

**Date:** 2026-09-15  
**Status:** Canonical operating protocol for Gate 0 continuation

## Purpose

Increase migration throughput without reducing evidence quality. Speed comes from parallel source investigation, bounded work units, deterministic reconciliation and immediate verification—not from skipping closure gates.

## 1. Work-unit model

The atomic work unit is a **closure packet**:

`question → source evidence → interpretation → target implication → evidence state → documentation change → verification`

A closure packet must be independently reviewable and must identify unresolved assumptions.

## 2. Parallel lanes

The following lanes may run concurrently:

1. API/HTTP/WS
2. events and messaging
3. data ownership/PIT/replay
4. analytical engines
5. workers/runtime
6. frontend/workflows
7. tests/fixtures
8. policy/config/entitlements
9. external adapters/providers
10. operations/security/observability

Each lane writes evidence to its own batch artifact first. Shared canonical matrices are updated only after reconciliation.

## 3. Reconciliation barrier

Before changing a canonical register, compare:

`source evidence ↔ capability registry ↔ target file manifest ↔ parity matrix ↔ Gate 0 register ↔ ADRs`

If a contradiction is found:

1. stop propagation of the conflicting claim;
2. identify evidence precedence;
3. correct the canonical artifact;
4. mark historical reports as historical snapshots where needed;
5. record the contradiction sweep;
6. continue only after the canonical state is coherent.

## 4. Evidence states

Use only these states:

- `CONFIRMED` — direct executable/schema/entrypoint/test evidence.
- `PARTIAL` — meaningful evidence exists but closure links remain missing.
- `UNVERIFIED` — not enough evidence yet.
- `NEGATIVE-SEARCH` — no indexed search result; never proof of absence.
- `TARGET-REQUIRED` — source evidence is insufficient or the target requires an intentional architectural addition.
- `VERIFIED-ABSENCE` — exhaustive source inspection supports absence.

## 5. Fast-path rules

The following are safe accelerators:

- inspect related source files in parallel;
- reuse previously verified evidence instead of repeating identical searches;
- group related capabilities into one closure packet;
- use source-tree and direct-file evidence before broad prose searches;
- maintain stable evidence IDs;
- run contradiction checks after each batch rather than waiting for a large release;
- verify every GitHub write immediately;
- maintain a single canonical owner for each decision;
- batch independent GitHub documentation changes where the repository write mechanism permits it.

The following are not allowed accelerators:

- declaring parity from documentation;
- treating search no-results as absence;
- copying a source module without tracing its consumers;
- creating target runtime files solely to satisfy a tree shape;
- closing a Gate dimension because an inventory exists;
- duplicating an analytical implementation to satisfy two execution paths;
- introducing a dependency only because it is fashionable;
- fragmenting into microservices before measured need;
- creating corrective migration files for schema work that belongs to an existing, not-yet-frozen target migration;
- creating duplicate documentation artifacts when an existing canonical document owns the decision.

## 6. Evidence compression

For repeated evidence, store a canonical source reference and summarize the behavioral conclusion rather than copying source prose into multiple documents. Cross-reference the canonical evidence artifact. This reduces documentation drift and review cost.

## 7. Migration and schema change discipline

Migration files are treated as part of the canonical target schema history, not as disposable implementation patches.

### 7.1 Canonical migration ownership

When CFIP runtime implementation is authorized and a schema change belongs to an existing target migration that has not been released/applied as an immutable production contract, **modify the original migration file itself**. Do not create a second corrective migration merely to repair, complete or optimize the same logical schema change.

The same rule applies to equivalent schema artifacts: indexes, constraints, defaults, ownership metadata and migration-linked data contracts must be corrected at their canonical owner rather than duplicated in a follow-up patch artifact.

### 7.2 No duplicate migration history

A new migration is not a substitute for a missing edit to an existing canonical migration. Before creating any new migration, the continuation must first prove that the change is genuinely a new schema evolution rather than a correction or completion of an existing migration. During the current pre-Gate-1 phase, target migrations are not yet frozen, so related schema corrections must be consolidated into their original migration files.

### 7.3 Source migrations are evidence

CForex migrations remain source evidence and must not be rewritten as part of CFIP migration work. Source migration files such as `0008_event_replay_provenance` and `0012_dataset_integrity_intelligence_memory` are behavioral/schema evidence; CFIP may improve their target design, but must preserve the source facts and explicitly document intentional divergence.

### 7.4 Verification

Any migration modification must be followed by:

`migration graph check → upgrade/downgrade review → schema/contract check → affected repository/adapter review → integration test → rollback verification`

No migration correction is considered complete merely because the file parses.

## 8. Runtime lock discipline

While Gate 0 is OPEN, target runtime implementation remains locked. Architecture contracts, evidence tools, manifests, ADRs and governance documents may be improved. Runtime code may not be counted as Gate 1 implementation until the formal Gate 0 exit decision.

## 9. Definition of closure

A dimension is closed only when its evidence graph has no unresolved material link, or every remaining bounded risk has an explicit owner, impact, mitigation and Gate 0 exit disposition.

## 10. Release/continuation sequence

```text
inspect current heads
→ read control documents
→ select highest-value evidence gap
→ parallel source investigation
→ normalize evidence
→ reconcile canonical artifacts
→ apply GitHub changes
→ fetch changed artifacts
→ contradiction sweep
→ update Gate 0 status
→ progress report
```

## 11. Quality invariant

**Completeness beats speed; parallelism provides speed without reducing completeness.** The process should optimize elapsed time while preserving the same evidence threshold for every capability.
