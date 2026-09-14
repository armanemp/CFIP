# CFIP Target Cross-Cutting Capability Register

**Status:** Target architecture requirement; implementation blocked by Gate 0.

The latest CForex migration evidence requires explicit target ownership for these cross-cutting capabilities:

| Capability | Target ownership | Current source evidence | Gate 0 status |
|---|---|---|---|
| Dataset fingerprint lifecycle | `contexts/data_lineage` | `0012_dataset_integrity_intelligence_memory.py` | producer/verification open |
| PIT reconstruction authority | `contexts/data_lineage` + `contexts/market_data` | dataset fingerprint and revision fields; runtime reconstruction still being traced | open |
| Replay case registry/executor | `contexts/replay` | `0008_event_replay_provenance.py` | producer/loader/executor open |
| Replay invariant verification | `contexts/replay` | `replay_cases.expected_invariants` | executable verifier open |
| Realtime event ledger | `contexts/realtime` | `0014_realtime_runtime.py` | retention/scale closure open |
| Realtime restart state | `contexts/realtime` | `0015_realtime_runtime_state.py` | ownership/failover closure open |
| Partition ownership/checkpoint | `contexts/realtime`, `contexts/operations` | target requirement; persisted state exists | source implementation tracing open |
| Durable evolution control | `contexts/governance` | `0023_governed_evolution_control_plane.py` | end-to-end promotion/rollback closure open |
| Independent verification evidence | `contexts/governance` | `evolution_change_verifications` | lifecycle closure open |
| Immutable cross-domain evidence | `packages/contracts`, `contexts/data_lineage` | provenance/content hashes and evidence refs | target contract open |

## Architectural rule

These are not duplicate implementations of existing domains. They are explicit ownership boundaries for lifecycle concerns that otherwise become hidden responsibilities inside workers, repositories or generic utilities.

They must be materialized only when the associated source lifecycle is sufficiently evidenced and the Gate 0 lock permits runtime implementation.

## Global-scale rule

Durable correctness state must not depend solely on process-local memory. Horizontal realtime execution requires explicit partition ownership, checkpoint/recovery and idempotency semantics. Large immutable dataset/replay artifacts may use object storage when justified, while transactional metadata remains in the system of record.
