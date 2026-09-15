# CFIP Intelligence Memory Contract

**Status:** Accepted Gate-0-compatible contract; runtime implementation remains gated.
**Purpose:** define the durable place where Platform Intelligence can write, retrieve, evaluate, supersede and retire learned knowledge without turning mutable model state into an uncontrolled source of truth.

## 1. Design decision

CFIP uses a **durable intelligence-memory evidence layer** rather than free-form model memory. The canonical pattern is:

`evidence → normalized lesson → provenance → validity window → evaluation → memory record → retrieval index → governed use → outcome → revision`

The memory layer is not a domain authority. Market, risk, execution, security and other bounded contexts remain authoritative for their own invariants.

## 2. Storage model

The target architecture separates three concerns:

1. **Immutable evidence objects** — source observations, release evidence, evaluation artifacts and large immutable datasets; object storage may be used at scale.
2. **Transactional memory metadata** — PostgreSQL owns identity, provenance links, validity, lifecycle, authorization, revision and audit metadata.
3. **Derived retrieval indexes** — search/vector/analytical indexes are rebuildable projections and never the only authoritative copy.

MongoDB is not required for intelligence memory. It may be introduced only if a measured document workload justifies it and an ADR defines ownership, consistency, retention, backup and recovery semantics.

## 3. Memory record contract

Every durable memory record must have, at minimum:

- stable `memory_id`;
- schema version;
- knowledge class/domain/aspects;
- normalized lesson or structured knowledge payload;
- source/evidence references;
- content digest;
- observed/created timestamp;
- point-in-time validity when applicable;
- provenance and rights classification;
- confidence and uncertainty metadata;
- evaluation/baseline references;
- applicability and contraindications;
- lifecycle state;
- revision/supersession links;
- retention/sensitivity classification;
- creator/process identity;
- verification evidence;
- retrieval policy metadata.

Free-form notes without provenance, validity and lifecycle metadata are not durable intelligence memory.

## 4. Lifecycle

`CANDIDATE → VERIFIED → ACTIVE → SUPERSEDED → RETIRED`

A candidate may be retained for research without becoming active. An active record may be superseded only by a new verified revision. Retirement preserves historical evidence and reason.

## 5. Temporal correctness

For market, research and operational knowledge, retrieval must respect the caller's `as_of` time. A record created after the requested historical decision point must not leak into that decision. Validity windows and source vintage are first-class fields.

Engineering knowledge also uses temporal scope for dependency, architecture and release-specific lessons so later fixes cannot rewrite historical explanations.

## 6. Retrieval semantics

Retrieval ranking must consider, at minimum:

- semantic relevance;
- temporal validity;
- provenance quality;
- verification state;
- domain/tenant authorization;
- confidence/uncertainty;
- contradiction/supersession state;
- freshness where the knowledge class requires it.

Ties must be deterministic. Future knowledge is excluded from point-in-time retrieval. Contradictory active records are surfaced rather than silently collapsed.

## 7. Learning boundary

The intelligence training lifecycle may generate candidate memory records from verified evidence. It may not silently mutate production domain behavior. Promotion requires the same evidence gates defined by `CFIP-INTELLIGENCE-TRAINING-LIFECYCLE.md`.

A memory record can improve retrieval, diagnosis, planning or recommendations without becoming a new domain rule. Domain-rule changes require the owning capability contract, tests and release governance.

## 8. Security and privacy

Memory retrieval is authorization-aware and tenant/workspace scoped where applicable. Secrets, credentials, raw sensitive prompts and unnecessary personal data are excluded by default. Sensitive memory classes require explicit retention and access policy.

Agents cannot directly write arbitrary memory through SQL or infrastructure access. Memory writes occur through governed application tools that validate schema, provenance, authorization and lifecycle transitions.

## 9. Reproducibility

Every production decision that materially uses intelligence memory should be reconstructable from:

`memory_id + revision + retrieval policy/version + as_of + evidence references + caller/agent identity`

This permits audit, replay, attribution and rollback of intelligence behavior.

## 10. Gate-0 implementation boundary

The contract, schema/index format, validators and evidence records may be implemented during Gate 0. Runtime retrieval, persistence and production learning remain subject to the migration gates and parity evidence.

The canonical machine-readable index is `data/training/CFIP-INTELLIGENCE-MEMORY-INDEX-v0.1.json`.
