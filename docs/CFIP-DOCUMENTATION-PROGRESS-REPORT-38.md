# CFIP Documentation Progress Report 38

**Date:** 2026-09-15  
**Target:** `armanemp/CFIP` `main`  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Gate 0:** OPEN  
**CFIP production runtime:** 0% / LOCKED

## Executive result

**BATCH 38 — ENGINEERING PASS WITH VERIFICATION RUN IN PROGRESS AT COMMIT TIME.**

This batch did not merely add documentation. It investigated the actual GitHub Actions failure from the previous architecture gate, isolated two classes of defects, and corrected them in the repository.

## Defects found and fixed

### 1. Dynamic test-module loading defect

The architecture tests dynamically load validator modules. Several tests did not register the dynamically created module in `sys.modules`, which can break Python `dataclasses` during module execution. The affected tests were corrected to register the module before executing it.

### 2. PIT/replay contract validator was too schema-column-specific

The validator required source migration column names such as `point_in_time_verified` and `provenance_nodes` to appear literally in target architectural documents. This was too strict because the target ADR intentionally uses domain-level concepts such as "point-in-time verification", "provenance references", and "engine identity and version".

The validator now accepts canonical source terms and documented architectural aliases while retaining deterministic failure when a required concept is absent.

## Verification evidence

Before the fixes, the latest architecture workflow failed specifically at the PIT/replay contract step after the complete architecture-tool test suite had passed.

After the dynamic-test loading fixes, the architecture test suite, target architecture validation, migration graph validation, worker lifecycle validation, and dependency-direction validation were observed as successful in GitHub Actions. The PIT/replay step was then corrected to recognize the target ADR's canonical domain terminology.

The next GitHub Actions run is the authoritative verification of the final corrected HEAD. No green result is claimed until that run is observed as completed successfully.

## Architecture integrity

- 34 bounded contexts remain canonical.
- 14 engine namespaces / 15 concrete runtime engines remain canonical.
- One canonical engine identity per `(engine_id, version)` remains required.
- Migration ownership rule remains: correct an existing mutable logical migration at its original owner; do not create a duplicate corrective migration.
- CForex source migrations remain immutable evidence.
- Static source-closure tooling remains evidence support, not parity proof.
- Gate 0 remains OPEN.
- CFIP runtime remains 0% / LOCKED.

## Speed and quality improvement

The failure investigation reduced future debugging time by making architecture-test module loading deterministic and by preventing target documentation vocabulary from being incorrectly coupled to source database column naming. The architecture CI remains consolidated into one workflow.

## Remaining source-closure work

The highest-value next work remains execution of the census tools against the actual CForex source checkout and reconciliation of their output with the canonical Source Evidence Matrix, Capability Registry, Parity Matrix and Gate-0 dimensions D1–D11.

## Decision

Batch 38 is a **real engineering remediation batch**. Final CI status must be rechecked after the last corrective commit before the batch is promoted from `IN PROGRESS` to `PASS`.
