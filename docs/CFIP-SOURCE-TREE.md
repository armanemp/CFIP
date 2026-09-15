# CFIP Canonical Source Tree

**Status:** canonical target structure; controlled runtime implementation is permitted under Gate 0, while production promotion remains locked.

This document defines the logical target ownership tree and rules for materializing it. Gate 0 permits controlled implementation when the applicable source evidence, contract, ownership, tests and rollback/change controls exist. Empty production folders and fake placeholder modules are prohibited.

**File-level implementation contract:** `docs/evidence/CFIP-TARGET-FILE-MANIFEST.md` is the authoritative file-by-file materialization manifest. This tree defines ownership and boundaries; the manifest defines concrete target artifacts and acceptance status.

## 1. Canonical target tree

```text
cfip/
├── apps/
│   ├── api/
│   ├── realtime/
│   ├── market_data_worker/
│   ├── analysis_worker/
│   ├── learning_worker/
│   ├── autonomy_worker/
│   └── web/
├── contexts/
├── packages/
│   ├── contracts/
│   ├── domain-kernel/
│   ├── application-kernel/
│   ├── eventing-dispatcher/
│   ├── eventing-postgres/
│   ├── eventing-nats/
│   ├── analysis-runtime/
│   └── intelligence-runtime/
├── adapters/
├── engines/
│   └── technical/
├── data/
├── frontend/
├── infrastructure/
├── tests/
├── scripts/
└── tools/
```

## 2. Materialization rule

The tree is a logical architecture map, not a requirement to create every directory immediately. A physical target namespace is created only when it has an explicit contract/ownership purpose or executable implementation. Source census names alone are insufficient.

## 3. Engine ownership rule

`engines/technical/` is currently the executable analytical-engine family. Its canonical indicator implementation is physically owned by the four family modules under `engines/technical/src/cfip_technical/indicators/` and the versioned metadata registry. Other source engine identities remain migration obligations/evidence until a concrete target owner and implementation contract are established; they must not be represented by empty or README-only placeholders.

## 4. Shared package rule

Packages are bounded capabilities, not a miscellaneous utility bucket. Cross-cutting contracts and infrastructure adapters must remain dependency-direction safe. `analysis-runtime` owns evidence-to-consensus composition; `intelligence-runtime` owns governed lifecycle tracing and must not become a second domain authority.

## 5. Global-scale boundary

The tree must support regional stateless API deployment, partition/lease/checkpoint ownership, bounded event flow, tenant isolation, data residency, workload isolation, retention/partitioning, cache bounds, SLO/capacity measurement and DR/rollback. These are architectural obligations, not claims that capacity has already been proven.

## 6. Verification

Structural presence is not parity. Each materialized runtime capability follows:

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

Only executable evidence may advance a capability between stages.
