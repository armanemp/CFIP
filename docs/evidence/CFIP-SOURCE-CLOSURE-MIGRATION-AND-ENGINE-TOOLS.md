# Source-Closure Migration and Engine Tooling

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate 0:** OPEN

## Purpose

This document records the executable verification primitives added for two high-risk source-closure surfaces: database migration topology and analysis-engine registration/test evidence.

## Migration graph validator

`tools/architecture/validate_migration_graph.py` parses Python migration files using only the standard library and checks:

- unique revision identifiers;
- referenced `down_revision` parents;
- referenced `depends_on` revisions;
- static migration metadata;
- logical schema-object reuse as a **warning**, not an automatic failure.

The warning classification is intentional: a later migration legitimately may evolve an existing table. The tool therefore does not encode the unsafe rule "an object appearing twice means duplicate migration". The canonical migration-hygiene policy remains: if a mutable target logical change already has an owner, correct that owner rather than creating a second corrective migration; a genuinely new schema evolution may receive a new migration.

The tool does not prove:

- migration execution in production;
- current live database schema;
- rollback safety;
- data migration correctness;
- deployment ordering;
- zero-downtime compatibility.

Those require runtime/database evidence later in the migration lifecycle.

## Engine registry reconciliation

`tools/architecture/reconcile_engine_registry.py` scans a CForex Python checkout for the 15 currently identified concrete runtime engine classes and records three evidence dimensions:

1. class definition;
2. registration/name evidence;
3. test-file evidence.

This is deliberately a first-pass static reconciler. It must not be interpreted as proof of:

- unique `(engine_id, version)` registration;
- semantic implementation uniqueness;
- descriptor/runtime consistency;
- PIT correctness;
- deterministic behavior;
- replay equivalence;
- durable execution persistence;
- production entrypoint wiring.

Those remain explicit Gate-0 closure requirements.

## Why both tools are necessary

Migration topology and engine topology are coupled to replay and historical correctness. A schema graph can be structurally valid while its runtime producer is missing; an engine can be registered while its durable execution path is disconnected. The migration chain therefore remains:

`source artifact → static evidence → composition → executable test → runtime/telemetry evidence → parity evidence`.

## CI integration

The existing `Architecture Contracts` workflow remains the single architecture/source-closure quality gate. It now runs the architecture validator and the complete architecture-tool test suite. If a target migration runtime tree is materialized later, the same workflow validates it automatically.

No second workflow was introduced.
