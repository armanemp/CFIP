# CFIP Shared Packages

Cross-cutting contracts, kernels and infrastructure adapters with explicit ownership. Packages must not become generic dumping grounds.

Gate 0 status: controlled implementation is permitted when source-evidenced, contract-first, reversible and testable; production promotion remains locked.

## Current eventing boundary

- `contracts` — transport-neutral event and realtime contracts.
- `eventing-dispatcher` — bounded, lease-fenced durable dispatch orchestration.
- `eventing-nats` — concrete NATS JetStream transport adapter behind `EventTransport`.

Concrete infrastructure dependencies stay behind adapter packages; domain and contract packages remain technology-neutral.
