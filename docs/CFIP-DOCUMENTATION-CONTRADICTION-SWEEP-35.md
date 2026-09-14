# CFIP Documentation Contradiction Sweep 35

**Target HEAD:** `2aeee86b18e6dab5abb05229be62b8bda08bf92a`  
**Gate 0:** OPEN

## Scope

This sweep covers the documentation and executable-verification changes introduced in Batch 35, with emphasis on stale status claims, CI truth, source-closure semantics and migration hygiene.

## Findings and dispositions

| Area | Finding | Disposition |
|---|---|---|
| Architecture validator | Existing validator already reports the 34-context inventory and migration ownership correctly | CONFIRMED; no duplicate validator created |
| CI | First Batch-35 CI run failed in the new test harness | RESOLVED in a follow-up commit |
| CI | Second Batch-35 CI run exposed a fixture/heuristic mismatch | RESOLVED in a follow-up commit |
| CI | Third run completed successfully | CURRENT TRUTH = GREEN |
| API/WS census | Static route extraction could otherwise be mistaken for complete semantic closure | Explicitly documented as bounded static evidence; Gate 0 remains open |
| Dynamic routing | Static analysis cannot safely resolve all runtime composition | Explicit `UNRESOLVED` statuses retained; no guessing |
| Event hints | Generic names such as `publisher` are not treated as proof of event semantics | Conservative heuristic retained and test fixture corrected |
| Migration ownership | No migration files were added or duplicated | CONFIRMED |
| Runtime implementation | New tools are evidence infrastructure, not CFIP production runtime | CONFIRMED; runtime remains locked |
| Context inventory | 34-context correction remains canonical | CONFIRMED; no new context added |

## CI evidence

The current GitHub Actions `Architecture Contracts` run for commit `2aeee86b18e6dab5abb05229be62b8bda08bf92a` completed successfully. The validator and source-closure test suite both passed.

Earlier failed runs are preserved as immutable history and are not erased or rewritten. The corrected run is the current operational truth.

## Remaining documentation reconciliation

The API/WS census now has executable extraction support, but the canonical Gate 0 register should only be promoted from `ADVANCED` to a stronger status after the extractor has been used against the actual CForex checkout and its output has been reconciled against service, event, auth, entitlement, frontend and test evidence.

The same rule applies to all future source-closure extractors: tool presence and green self-tests are evidence of tooling correctness, not evidence that the source capability itself is closed.

## Decision

**Sweep 35: PASS — no unresolved material contradiction introduced by Batch 35.**
