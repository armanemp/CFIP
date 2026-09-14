# CFIP Documentation Contradiction Sweep — Batch 49

## Scope

This sweep covers the controlled migration index, continuation contract references, architecture/global-scale/Platform Intelligence contracts, capability registry/matrix, latest progress evidence, and the Architecture Contracts CI definition after Batch 49.

## Findings and resolutions

### 1. CI test-framework mismatch — resolved

The platform-intelligence coverage test module contained pytest-style top-level test functions while the canonical workflow invokes `python -m unittest <module>`. This was an execution-contract contradiction between test implementation and CI orchestration, not an architecture-rule failure.

Resolution: the test module now uses `unittest.TestCase` methods and a `unittest.main()` entrypoint. The workflow remains deterministic and dependency-light.

### 2. Platform Intelligence hook semantics — consistent

The capability matrix defines `observe`, `context` and `audit` as universal hooks. `reason`, `act`, `verify`, `learn` and `safety` remain domain-specific. The validator and tests now enforce this distinction instead of requiring every hook on every capability.

### 3. Gate 0 status — consistent

The migration control index, continuation contract and progress evidence continue to state that Gate 0 is open and business runtime implementation is locked. Architecture tooling and safe evidence work remain allowed in parallel.

### 4. Source baseline — consistent

The current behavioral source remains `armanemp/CForex` `main` / v0.9.154. CFIP remains a controlled reimplementation rather than a source-file copy.

### 5. Global-scale claims — bounded correctly

Global-scale documentation describes architectural requirements and evidence obligations, not measured production capacity. Capacity, SLO, DR/RPO/RTO, residency and failure-domain claims remain open until measured evidence exists.

### 6. Intelligence claims — bounded correctly

Platform Intelligence coverage is treated as an architecture/control contract. No document treats the coverage matrix as proof that runtime intelligence has already been implemented or production-verified.

### 7. Documentation/engineering sequencing — consistent

Amendment 47 remains the controlling rule: documentation, source evidence, reconciliation and safe engineering proceed in parallel. Neither documentation completeness nor implementation work is used to block independent closure work.

## Residual open items

- Final green status of the latest Architecture Contracts run must still be observed after the Batch 49 commits.
- D1–D10 executable/source evidence gaps remain open as recorded in the latest progress report.
- Gate 0 closure remains a formal governance decision and is not implied by CI success.

## Sweep result

**No new documentation contradiction requiring an architecture change was found. One CI/test-framework contradiction was found and corrected at the test boundary.**
