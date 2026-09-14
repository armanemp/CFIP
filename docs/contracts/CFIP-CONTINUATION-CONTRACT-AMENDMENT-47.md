# CFIP Continuation Contract — Amendment 47

**Status:** canonical contract amendment; read with `docs/CFIP-CONTINUATION-PROMPT.md`.

## Parallel documentation + engineering is mandatory

The previous sequencing restriction that required documentation to be completed before engineering is **removed permanently**.

From Amendment 47 onward, the authoritative continuation workflow is:

`source study ↔ evidence closure ↔ contract evolution ↔ documentation ↔ architecture tooling ↔ safe engineering ↔ tests ↔ verification ↔ reconciliation`

These tracks must advance together whenever they can be independently progressed without violating Gate 0 or evidence rules. Documentation is not a prerequisite gate for safe architecture/evidence engineering, and engineering is not permission to bypass documentation reconciliation.

## Global intelligence requirement

Every registered capability is a platform-intelligence integration boundary. Each capability must be evaluated for the applicable:

`observe → context → reason → act → verify → learn → audit → safety`

hooks. The canonical matrix remains `docs/capabilities/CFIP-PLATFORM-INTELLIGENCE-COVERAGE-MATRIX.md`. Matrix coverage is an architecture obligation, not proof of runtime implementation.

The target operating model is bounded autonomous professional engineering, research, operations and trading-support. Human intervention should not be required for routine operation, but autonomy must remain policy-bounded, auditable, independently verified, isolated where needed, health-guarded and reversible. Agents cannot alter their own governor, safety controls or evidence history and cannot bypass domain authority boundaries.

## Gate 0 compatibility

This amendment does **not** authorize CFIP production business runtime before Gate 0 closure. Safe pre-Gate-0 work includes evidence tooling, source-study automation, validators, contract tests, architecture structures, documentation, CI, reconciliation and other runtime-independent engineering.
