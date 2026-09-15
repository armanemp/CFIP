# CFIP Documentation Contradiction Sweep 53

**Gate 0:** OPEN
**Scope:** canonical control, intelligence training, source-dataset governance and newly added intelligence-memory artifacts.

## Findings

| Check | Result | Action |
|---|---|---|
| Gate-0 runtime lock | Consistent | Preserved |
| CForex v0.9.154 source baseline | Consistent | Preserved |
| Training lifecycle vs memory lifecycle | Consistent | Memory is a governed output, not an authority |
| Synthetic-data promotion policy | Consistent | Production/model mutation remains forbidden |
| PIT/temporal retrieval semantics | Consistent | `as_of` validity is mandatory |
| PostgreSQL authority rule | Consistent | Memory metadata targets PostgreSQL |
| MongoDB rule | Consistent | Optional only with measured document workload + ADR |
| Derived retrieval index authority | Consistent | Rebuildable projection only |
| Domain authority | Consistent | Memory cannot replace bounded-context authority |
| Autonomous operation | Consistent | Governed tools/policies/verification/rollback remain mandatory |
| CI verification claim | Consistent | New gate is wired; green result is not claimed without observed run evidence |

## New controlled references

- `docs/governance/CFIP-INTELLIGENCE-MEMORY-CONTRACT.md`
- `data/training/CFIP-INTELLIGENCE-MEMORY-INDEX-v0.1.json`
- `tools/governance/validate_intelligence_memory_index.py`
- `tests/architecture/test_validate_intelligence_memory_index.py`
- `.github/workflows/intelligence-memory-contracts.yml`
- `docs/governance/CFIP-ECP-CHECKPOINT-53.md`

## Open contradiction / evidence items

No new architectural contradiction was introduced. Existing source-data integrity discrepancies remain open and are intentionally not normalized away:

- v0.19 declared count/hash require direct dataset verification.
- v0.20 declared count/hash require direct dataset verification.
- v0.21 manifest/blob count/SHA discrepancy remains unresolved.
- observed-release evidence requires direct hash/count verification.
- v0.10–v0.18 remain pending manifest/dataset classification.

These are evidence gaps, not documentation contradictions.
