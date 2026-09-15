# CFIP Shared Packages

Cross-cutting contracts, kernels and infrastructure adapters with explicit ownership. Packages must not become generic dumping grounds.

Gate 0 status: controlled implementation is permitted when source-evidenced, contract-first, reversible and testable; production promotion remains locked.

## Current eventing boundary

- `contracts` — transport-neutral event and realtime contracts.
- `eventing-dispatcher` — bounded, lease-fenced durable dispatch orchestration.
- `eventing-postgres` — async PostgreSQL durability adapter with atomic `SKIP LOCKED` claim and monotonic fencing.
- `eventing-nats` — concrete NATS JetStream transport adapter behind `EventTransport`.

## Analysis boundary

- `analysis-runtime` — deterministic specialist-evidence composition, indicator semantic translation and the single consensus aggregation boundary.

## Platform Intelligence boundary

- `intelligence-runtime` — dependency-free lifecycle trace contracts for `observe → context → reason → act → verify → learn → audit → safety`. It records governed intelligence state but never executes domain operations, SQL, infrastructure mutations, trades or model calls. `act` requires an explicit prior safety event in the same trace.

Concrete infrastructure dependencies stay behind adapter packages; domain and contract packages remain technology-neutral.

The PostgreSQL adapter currently has deterministic contract/SQL compilation coverage. Live database concurrency, stale-owner races and end-to-end broker composition remain explicit integration evidence requirements.
