# CFIP CForex Training Dataset Source Inventory

**Source baseline:** `armanemp/CForex` `main` / v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** source inventory; not materialization approval

## Purpose

This inventory prevents mature CForex training/evaluation artifacts from being lost during clean-room migration. It records what exists in the source repository before CFIP decides what may be copied, transformed, evaluated or promoted.

## Enumerated source artifacts

The CForex `data/training` directory currently exposes the following seed manifest sequence:

- `SEED-DATASET-MANIFEST-v0.10.json`
- `SEED-DATASET-MANIFEST-v0.11.json`
- `SEED-DATASET-MANIFEST-v0.12.json`
- `SEED-DATASET-MANIFEST-v0.13.json`
- `SEED-DATASET-MANIFEST-v0.14.json`
- `SEED-DATASET-MANIFEST-v0.15.json`
- `SEED-DATASET-MANIFEST-v0.16.json`
- `SEED-DATASET-MANIFEST-v0.17.json`
- `SEED-DATASET-MANIFEST-v0.18.json`
- `SEED-DATASET-MANIFEST-v0.19.json`
- `SEED-DATASET-MANIFEST-v0.20.json`
- `SEED-DATASET-MANIFEST-v0.21.json`
- `OBSERVED-RELEASE-EVIDENCE-MANIFEST-v0.1.json`

This enumeration is directory evidence. It is not a claim that every manifest has been individually reconciled yet.

## Governed carry-forward status

| Artifact family | Source status | CFIP action | Promotion |
|---|---|---|---|
| Seed manifests v0.10–v0.18 | Enumerated | Preserve source evidence; inspect manifests/datasets before materialization | Blocked until evidence review |
| Seed v0.19 | Manifest indexed | Preserve source evidence | Blocked until dataset hash/count verification |
| Seed v0.20 | Manifest indexed | Preserve source evidence | Blocked until dataset hash/count verification |
| Seed v0.21 | Manifest + dataset evidence inspected | Preserve; explicit integrity blocker | **Blocked** |
| Observed release evidence v0.1 | Manifest + dataset evidence inspected | Preserve as governed educational/release evidence | **Blocked pending direct hash/count verification** |

## v0.21 integrity finding

The v0.21 source manifest declares:

- dataset: `governed_platform_knowledge_v0.21.jsonl`
- record count: `330`
- source SHA-256: `2970683a5f7d860ec2841ed52e6063e10cb7bded3533c1c6dd9eba29d552bd38`
- source type: `synthetic_seed`
- point-in-time: `2026-09-12T00:00:00+00:00`
- synthetic only: `true`
- promotion allowed: `false`
- model mutation allowed: `false`
- evaluation required: `true`

Direct source-blob evidence currently exposes 108 JSONL records. The difference is unresolved. CFIP therefore does not materialize the partial blob and does not replace the manifest count with the observed count.

## Observed release evidence v0.1

The source manifest declares 20 records and identifies the material as educational governance examples derived from verified local release evidence. It is not market truth and is not a production training set. Its declared domains include analysis, calibration, drift, market data, operations, outcome, self-development, self-healing, signal and UX.

## Materialization protocol

For every source artifact:

`source path → source ref → manifest SHA → declared count → dataset SHA → direct record count → provenance/rights → temporal scope → evaluation → materialization status`

No artifact advances to `MATERIALIZED_VERIFIED` until all required evidence agrees.

Synthetic records remain explicitly synthetic and cannot silently become market truth. Observed release evidence remains evidence about engineering/release behavior, not a substitute for market observations.

## Next closure work

1. Reconcile v0.19 and v0.20 manifest metadata with their dataset blobs.
2. Resolve v0.21 record-count/SHA discrepancy from authoritative source evidence.
3. Directly verify the observed-release dataset count and SHA.
4. Inspect v0.10–v0.18 manifests and classify whether their datasets are superseded, complementary or historical evidence.
5. Build a deduplication/content-addressed relationship across versions before any bulk materialization.
6. Feed only verified evidence into the governed Intelligence Training Lifecycle.
