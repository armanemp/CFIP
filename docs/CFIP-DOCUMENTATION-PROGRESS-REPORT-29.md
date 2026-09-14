# CFIP Documentation Progress Report 29

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Runtime implementation:** **0% / LOCKED**

## 1. Executive result

Batch 29 continued the migration using the required control-first workflow. The current migration index and master plan were re-read before source work. CForex API/realtime evidence was refreshed directly from `apps/api/src/fi_api/realtime.py`, and the target documentation was hardened against current OpenTelemetry and OWASP agent-control guidance.

No speculative runtime implementation was introduced. No capability was retired. No source or target history was rewritten.

## 2. Direct source evidence added

### API / WebSocket / realtime

`docs/evidence/CFIP-SOURCE-CLOSURE-BATCH-29-API-WS-AND-REALTIME-CENSUS.md`

Direct source evidence confirms:

- `/realtime/metrics` authenticated metrics endpoint;
- `/ws/market` authenticated WebSocket;
- principal resolution through bearer/session mechanisms;
- typed client/server commands and events;
- subscription authorization;
- subscription registry;
- historical snapshot before incremental updates;
- cursor propagation;
- ping/pong;
- unsubscribe;
- explicit validation/auth/timeline error outcomes;
- forwarding tasks and disconnect cleanup.

This is strong transport evidence, but it does not by itself prove complete durable event replay, global subscription ownership, or end-to-end recovery.

## 3. Target architecture hardening

`docs/evidence/CFIP-TARGET-OBSERVABILITY-AND-AGENT-CONTROL-REFRESH-2026-09.md`

The target was refreshed against current OpenTelemetry Semantic Conventions 1.44.0 and current OWASP Agent Control Standard guidance.

The target now explicitly requires:

- reuse of established OTel semantic conventions before bespoke attributes;
- stable event naming with dynamic identifiers represented as attributes;
- explicit semantic-convention migration/version handling for messaging;
- client session correlation for frontend telemetry;
- agent identity and capability boundaries;
- policy hooks before sensitive tool actions;
- scoped credentials;
- high-impact human/approval boundaries where required;
- immutable action evidence;
- memory/data provenance;
- post-action verification;
- revocation/circuit-breaker controls;
- explicit coverage for prompt injection, tool abuse, data exfiltration and memory poisoning.

These are target improvements, not retroactive claims about CForex.

## 4. Documentation quality control

`docs/CFIP-DOCUMENTATION-CONTRADICTION-SWEEP-29.md` records a PASS WITH OPEN EVIDENCE GAPS result.

The sweep confirms that the new standards material does not change Gate 0 semantics, does not introduce a new runtime dependency, and does not create a second source of truth.

## 5. Speed and accuracy protocol

The workflow is now explicitly split into:

`parallel evidence tracks → evidence normalization → serialized canonical reconciliation → contradiction sweep → progress report`.

Parallel tracks reduce idle time; serialized canonical writes prevent contradictory architecture decisions. No-result searches remain bounded negative evidence unless exhaustive source inspection proves absence.

## 6. Gate status

| Dimension | Status | Main remaining closure |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | exhaustive route/caller/side-effect/test registry |
| D2 Events | ADVANCED / OPEN | exhaustive producer/consumer lifecycle |
| D3 Data/PIT | ADVANCED / OPEN | authoritative reconstruction + PIT/replay execution |
| D4 Engines | ADVANCED / OPEN | exhaustive registration/test/fixture/dependency mapping |
| D5 Workers | ADVANCED / OPEN | checkpoint/lease/recovery/scaling evidence |
| D6 Frontend | ADVANCED / OPEN | recursive component/hook/state/API/realtime/test census |
| D7 Tests | IN PROGRESS / OPEN | capability-to-test + negative/security/PIT/replay matrix |
| D8 Policy/config | IN PROGRESS / OPEN | hardcode/config/flag/entitlement census |
| D9 Adapters | IN PROGRESS / OPEN | provider/broker/model/research/identity/billing/storage matrix |
| D10 Operations | IN PROGRESS / OPEN | SLO/capacity/retention/DR/residency/recovery evidence |
| D11 Reconciliation | IN PROGRESS / OPEN | final cross-matrix consistency + documentation freeze |

## 7. Inventory checkpoint

The canonical target inventory remains:

- 7 app roots;
- 33 bounded contexts;
- 8 package boundaries;
- 4 inbound adapter families;
- 10 outbound adapter families;
- 14 engine namespaces;
- 15 source runtime engine classes;
- 5 data areas;
- 9 frontend areas;
- 4 infrastructure areas;
- 9 test categories;
- 6 script categories.

These counts describe the architecture/evidence inventory and are not implementation percentages.

## 8. Important architectural decisions retained

1. CForex source behavior remains authoritative until parity closure.
2. CFIP is a controlled reimplementation, not a file-copy migration.
3. One canonical `(engine_id, version)` identity per semantic engine version.
4. Runtime and durable execution may be separate projections without duplicate analytical implementations.
5. Durable event streams and client WebSocket sessions remain distinct.
6. Market-data revision, dataset fingerprint, replay case and learning revision remain separate identities.
7. MongoDB remains conditional rather than default.
8. Microservices remain evidence-driven rather than directory-driven.
9. Frontend domain semantics remain outside presentation components.
10. Agent authority remains explicitly separate from analytical and infrastructure authority.

## 9. Next work

The next high-value closure pass should execute these tracks concurrently:

1. exhaustive API/WS caller and side-effect census;
2. event producer/consumer/subject/schema registry;
3. engine registration/test/fixture dependency graph;
4. worker checkpoint/lease/recovery graph;
5. PIT/replay reconstruction ownership;
6. frontend recursive component/state graph;
7. hardcode/config/entitlement classification;
8. external adapter/provider graph;
9. final cross-matrix reconciliation.

Gate 0 remains OPEN and CFIP runtime remains 0% / LOCKED.
