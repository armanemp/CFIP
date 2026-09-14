# ADR-004 — Dataset, Replay and Point-in-Time Integrity

**Status:** Accepted for target architecture; implementation blocked by Gate 0  
**Date:** 2026-09-14  
**Scope:** dataset identity, point-in-time integrity, replay/backtest reproducibility and historical reconstruction

## Context

CForex contains durable schema evidence for dataset fingerprints and replay cases, while the current source study has not yet established a complete authoritative producer/consumer/executor lifecycle for those records. The learning worker also derives a deterministic revision from ordered journal outcomes. These are useful mechanisms, but they represent different domains and must not be conflated.

CFIP requires a stronger explicit contract so that a dataset fingerprint, a point-in-time market-data revision, a replay case and a learning revision cannot accidentally become interchangeable identifiers.

## Decision

CFIP separates four concepts:

1. **Dataset identity** — identifies a concrete dataset artifact/version and its content/schema/feature integrity.
2. **PIT market-data identity** — identifies the historically valid market-data view available at a defined event/observation boundary.
3. **Replay case identity** — identifies an executable replay scenario, including input snapshot/reference, expected invariants and engine/version context.
4. **Learning revision identity** — identifies the deterministic outcome corpus used by a learning/evaluation cycle.

These identities MAY reference one another, but one must never be substituted for another merely because both are represented by hashes or revisions.

## Integrity requirements

A production-grade replayable analytical path MUST be able to establish, directly or through durable references:

- dataset version and content integrity;
- schema/feature integrity where applicable;
- rights/licensing verification where required;
- point-in-time verification status;
- exact or content-addressed input snapshot/reference;
- market-data revision or reconstruction boundary;
- engine identity and version;
- parameter identity/fingerprint;
- dependency/runtime version information where reproducibility requires it;
- provenance references;
- expected invariants and verification outcome;
- deterministic ordering semantics;
- replay execution result and failure state.

## PIT rules

PIT correctness is defined by the information available at the selected historical boundary, not merely by replaying rows in timestamp order. The reconstruction contract must account for event time, ingestion/availability time, revisions, corrections, late events and provider-specific history semantics where those dimensions exist.

Future information MUST NOT enter an historical feature, decision, engine input or evaluation result unless the capability explicitly models that information as available at the selected boundary.

## Replay rules

Replay is an executable verification capability, not just a database row. A replay implementation claiming live semantic equivalence MUST preserve or explicitly declare its behavior for:

- ordering/partition semantics;
- event-time and watermark progression;
- deduplication;
- late-event policy;
- checkpoint/recovery boundaries;
- engine version and dependency identity;
- input snapshot/PIT identity;
- output verification and expected invariants.

Backtest is a distinct workload but must reuse the canonical market, engine and decision contracts. A simplified historical loop must not silently be labeled equivalent to the live runtime.

## Dataset fingerprint rules

Dataset fingerprints are immutable evidence records. A fingerprint should be content-addressed or otherwise uniquely tied to the exact dataset artifact/version it describes. Recomputing a fingerprint for the same immutable artifact must produce the same identity under the same canonicalization rules.

A fingerprint does not prove PIT correctness by itself. `point_in_time_verified` is an explicit verification property and must have a traceable basis.

## Learning revision rules

A learning revision derived from ordered journal outcomes is a valid revision for that outcome corpus only. It is not a market-data revision and does not establish historical market-data availability.

Learning/evaluation records must retain the relevant dataset/PIT references when market data contributes to the evaluation.

## Target improvement beyond current source evidence

CFIP will introduce a consistency gate that detects:

- dataset fingerprint without a resolvable artifact/reference;
- PIT verification without evidence basis;
- replay case without resolvable input/PIT identity;
- replay execution using an engine/version not present in the canonical catalog;
- learning revision incorrectly used as market-data PIT identity;
- missing provenance or expected-invariant verification;
- replay/backtest paths that silently diverge from live event-time semantics.

This is a target architecture improvement, not a claim that CForex already provides the complete lifecycle.

## Performance and scale

Large immutable datasets and replay artifacts should use object storage or another content-addressed artifact boundary when justified, while transactional metadata remains in the system-of-record store. Analytical scans should be isolated from latency-sensitive transactional workloads.

Fingerprinting and verification should be incremental where possible and must not require repeatedly re-reading massive datasets synchronously on the trading path.

## Verification obligations before Gate 1

- establish authoritative CForex producer/consumer evidence for dataset fingerprints;
- establish replay-case producer/loader/executor evidence;
- trace market-data PIT reconstruction and revision semantics;
- distinguish all known revision/fingerprint identifiers;
- map replay/backtest tests and fixtures;
- define target artifact/reference contracts;
- add consistency and leakage tests;
- document intentional source-to-target divergences.

This ADR does not authorize CFIP runtime implementation. Gate 0 remains OPEN and runtime implementation remains LOCKED.
