# CFIP ECP and Training-Evidence Data Contract

**Status:** Accepted governance contract; Gate 0 compatible

## Purpose

CFIP needs a machine-readable project-control boundary so the future autonomous engineering system can work with Git/GitHub without turning the application into a second version-control system. The same evidence discipline applies to training datasets: source material is identified, hashed and governed before it can become eligible learning input.

## Internal Git relationship

Git/GitHub remains canonical for source history, branches, commits, trees and pull requests. The future Evolution Control Plane (ECP) records project-level intent, checkpoints, verification and outcomes above Git.

The minimum immutable technical anchor for an ECP checkpoint is:

`repository + revision_sha + target_ref + evidence_fingerprints`

An ECP record may reference Git objects, but it may not rewrite or conceal them.

## ECP evidence record minimum

Every persisted ECP event/checkpoint must be able to identify:

- `event_id`
- `change_id`
- `parent_event_id` when applicable
- `event_type`
- `actor_id`
- `actor_kind`
- `repository`
- `revision`
- `target_ref`
- `timestamp`
- `risk_class`
- `capability_ids`
- `evidence_refs`
- `policy_decision`
- `result`
- `correlation_id`

Checkpoint evidence must additionally identify the exact source/target baseline and the verification set used to authorize the next transition.

## Training/evaluation evidence minimum

A dataset or training record is eligible only when its identity, provenance, rights, temporal scope and evaluation status are reconstructable. Synthetic material must remain explicitly synthetic and cannot be interpreted as real market truth.

For source carry-forward datasets, CFIP records:

`source repository → source ref → source path → source manifest SHA → source dataset SHA → declared count → verified count → materialization status`

A missing or conflicting count is a **blocker**, not a pass.

## Current source-integrity finding

The CForex v0.9.154 training baseline contains seed manifests for governed platform knowledge. The v0.21 manifest declares 330 records, while the currently retrievable source dataset blob evidence exposes 108 JSONL records. This is intentionally preserved as a source-integrity discrepancy in `data/training/CFIP-CFOREX-TRAINING-DATASET-INDEX-v0.1.json`.

CFIP therefore does **not** copy a partial dataset, invent the missing records, or silently trust the declared count. The source discrepancy must be reconciled before the dataset is marked materialized/verified.

## Promotion rules

- Retrieval is not promotion.
- Materialization is not training eligibility.
- Training eligibility is not model mutation.
- Evaluation success is not production promotion.
- Production mutation remains separately governed.
- Failed or incomplete evidence remains visible and auditable.

## Future ECP implementation boundary

When the migration gate authorizes runtime implementation, ECP persistence should use append-oriented records with deterministic identifiers, optimistic version/freshness checks, explicit ownership/leases for concurrent work, and immutable evidence references. Git operations remain delegated to a bounded adapter/tool boundary rather than direct unrestricted infrastructure authority from an agent.
