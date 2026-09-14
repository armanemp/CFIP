# CFIP Engine Census — D4 Continuation 02

**Source:** `armanemp/CForex` `main` v0.9.154
**Source commit:** `900882154cab3b9b74d0543b9bbf72a708a08134`
**Target:** `armanemp/CFIP` `main`
**Status:** evidence advanced; D4 remains OPEN

## Purpose

This document freezes the currently proven runtime-engine census without inventing coverage where the source inspection is incomplete. It distinguishes source namespace, executable implementation, and runtime registration.

## Proven runtime census

| Runtime engine | Runtime source family | Version evidence | Direct behavior/test evidence | Status |
|---|---|---|---|---|
| `technical.momentum` | `fi_application.analysis_engine.builtin` | `1.0.0` | runtime + deterministic/provenance tests | proven |
| `technical.volatility` | `fi_application.analysis_engine.builtin` | `1.0.0` | runtime + health/deterministic tests | proven |
| `backtest.replay` | `fi_engine_backtest` | `1.1.0` | modular catalog/behavior tests | proven |
| `confluence.score` | `fi_engine_confluence` | `1.1.0` | modular catalog/behavior tests | proven |
| `contradiction.detect` | `fi_engine_contradiction` | `1.1.0` | modular catalog/behavior tests | proven |
| `fvg.causal` | `fi_engine_fvg` | `1.2.0` | modular behavior + causality/parity tests | proven |
| `intelligence.score` | `fi_engine_intelligence_score` | `1.1.0` | modular catalog/behavior tests | proven |
| `liquidity.map` | `fi_engine_liquidity` | `1.1.0` | modular catalog/behavior tests | proven |
| `mtf.alignment` | `fi_engine_mtf` | `1.1.0` | modular catalog/behavior tests | proven |
| `order_block.causal` | `fi_engine_order_block` | `1.1.0` | modular catalog/behavior tests | proven |
| `regime.classify` | `fi_engine_regime` | `1.1.0` | modular catalog/behavior tests | proven |
| `signal.scoring` | `fi_engine_signal` | `1.1.0` | modular catalog/behavior tests | proven |
| `signal.trigger` | `fi_engine_signal` | `1.1.0` | namespace/implementation evidence requires further per-descriptor census | open |
| `strategy.baseline` | `fi_engine_strategy` | `1.1.0` | modular catalog/behavior tests | proven |
| `structure.swing` | `fi_engine_structure` | `1.1.0` | modular catalog/behavior tests | proven |
| `scoring` runtime family | `fi_engine_scoring` | `1.1.0` | modular catalog/behavior tests | proven |

## Important reconciliation

The API runtime composition contains 15 Python engine instances. The descriptor-level census contains a larger logical surface because a single implementation namespace can expose more than one versioned descriptor/capability. Therefore counts must never be compared as if they represented the same unit.

In particular, the source evidence identifies both `signal.scoring@1.1.0` and `signal.trigger@1.1.0` as engine descriptors, while the runtime composition names a single `SignalEngine` instance. Exact descriptor enumeration and whether both descriptors are exposed by that instance or only one is the runtime-authoritative path remains an explicit closure task.

Likewise, the `scoring` namespace must not be reduced to a directory-name count: its executable implementation and descriptor identity require direct enumeration.

## Test evidence

The modular catalog test instantiates 13 dedicated engine classes and verifies deterministic, bounded output, provenance and evidence. The modular behavior test additionally verifies FVG semantic parity and no future-fill reclassification. The Fabric failure-policy test verifies explicit `FAIL_CLOSED` enforcement. The Fabric test verifies independent engine execution and normalized evidence.

These tests establish executable behavior for the inspected classes but do not by themselves prove that every descriptor exposed by a namespace is independently runtime-registered.

## Negative evidence / unresolved items

The following are deliberately unresolved:

1. complete descriptor enumeration for every engine package;
2. exact mapping from every descriptor to a runtime instance;
3. all alternate registration/composition paths outside the known API composition root;
4. per-engine parameter schema and canonical serialization/fingerprint;
5. upstream data dependency contract for every engine;
6. PIT dataset reconstruction/fingerprint per engine;
7. replay/backtest equivalence for every engine that participates in replay;
8. engine-specific golden/regression fixture inventory;
9. engine telemetry/event production and persistent health projections;
10. complete capability-registry/parity-matrix reconciliation;
11. executable engine-like components outside `engines/`, `fi_application.analysis_engine.builtin`, and the known `fi_engine_*` packages.

## Migration invariants

CFIP migration must preserve:

- namespace, implementation and runtime registration as separate inventories;
- stable engine identity/version;
- descriptor-to-runtime mapping;
- deterministic semantics where declared;
- causal `data_revision` and `as_of` context;
- evidence/provenance propagation;
- explicit failure policy;
- replay/backtest semantic compatibility;
- operational health visibility without conflating transient health with durable business truth.

**Conclusion:** the executable runtime census is now materially stronger, but D4 remains OPEN and Gate 0 remains OPEN. No CFIP runtime implementation is authorized by this evidence document.
