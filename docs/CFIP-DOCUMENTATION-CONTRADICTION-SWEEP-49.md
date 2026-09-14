# CFIP Documentation Contradiction Sweep — Batch 49

## Scope

This sweep covers the controlled migration index, continuation contract references, architecture/global-scale/Platform Intelligence contracts, capability registry/matrix, latest progress evidence, and the Architecture Contracts CI definition after Batch 49.

## Findings and resolutions

### 1. CI test-framework mismatch — resolved

The platform-intelligence coverage test module contained pytest-style top-level test functions while the canonical workflow invokes `python -m unittest <module>`. This was an execution-contract contradiction between test implementation and CI orchestration, not an architecture-rule failure.

Resolution: the test module now uses `unittest.TestCase` methods and a `unittest.main()` entrypoint. The workflow remains deterministic and dependency-light.

### 2. PIT evidence-path mismatch — resolved

The Architecture Contracts workflow referenced `docs/evidence/CFIP-SOURCE-CLOSURE-TRACEABILITY-RULES.md`, but that file does not exist in the target repository. The canonical D3 evidence boundary is already present at `docs/capabilities/CFIP-D3-PIT-REPLAY-EVIDENCE-CONTRACT.md` and contains the required PIT/replay evidence vocabulary.

Resolution: the workflow now validates the canonical D3 contract instead of a stale/non-existent path. This is a CI wiring correction, not a weakening of the PIT gate.

### 3. Platform Intelligence hook semantics — consistent

The capability matrix defines `observe`, `context` and `audit` as universal hooks. `reason`, `act`, `verify`, `learn` and `safety` remain domain-specific. The validator and tests now enforce this distinction instead of requiring every hook on every capability.

### 4. Gate 0 status — consistent

The migration control index, continuation contract and progress evidence continue to state that Gate 0 is open and business runtime implementation is locked. Architecture tooling and safe evidence work remain allowed in parallel.

### 5. Source baseline — consistent

The current behavioral source remains `armanemp/CForex` `main` / v0.9.154. CFIP remains a controlled reimplementation rather than a source-file copy.

### 6. Global-scale claims — bounded correctly

Global-scale documentation describes architectural requirements and evidence obligations, not measured production capacity. Capacity, SLO, DR/RPO/RTO, residency and failure-domain claims remain open until measured evidence exists.

### 7. Intelligence claims — bounded correctly

Platform Intelligence coverage is treated as an architecture/control contract. No document treats the coverage matrix as proof that runtime intelligence has already been implemented or production-verified.

### 8. Documentation/engineering sequencing — consistent

Amendment 47 remains the controlling rule: documentation, source evidence, reconciliation and safe engineering proceed in parallel. Neither documentation completeness nor implementation work is used to block independent closure work.

## Verification result

Architecture Contracts CI run **#129 completed PASS** on `96862a4ed2d4c3b45ceff3168eddc89edf26c4ea`. The run passed all named test modules and final verification steps, including PIT/replay, global-scale, Platform Intelligence contracts and capability-wide coverage.

## Residual open items

- D1–D10 executable/source evidence gaps remain open as recorded in the latest progress report.
- Gate 0 closure remains a formal governance decision and is not implied by CI success.

## Sweep result

**No remaining contradiction requiring an architecture change was found in the controlled documentation/CI surface reviewed in Batch 49. Two execution-boundary defects were found and corrected: test-framework discoverability and a stale PIT evidence path.**
