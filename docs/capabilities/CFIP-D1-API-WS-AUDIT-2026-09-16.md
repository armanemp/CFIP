# CFIP D1 API / WebSocket Audit — 2026-09-16

## Purpose

This audit closes the current **target-repository** D1 question: what HTTP and WebSocket surface is actually executable in `armanemp/CFIP` on `main`?

The audit deliberately separates three things:

1. **CFIP target implementation evidence** — executable API/WebSocket code physically present in `CFIP`.
2. **CForex source evidence** — historical capability/behavior evidence used for discovery and parity requirements.
3. **Architecture/documentation targets** — planned contracts or directory placeholders that do not prove runtime behavior.

`cforex-platform` is excluded.

## Repository snapshot

- Repository: `armanemp/CFIP`
- Branch: `main`
- Snapshot observed: commit `89d7d94339d934997a8753e0247e41e39c155c55`
- Audit date: 2026-09-16

## Executive result

**Target API/WS runtime closure is not present yet.**

The repository contains an `apps/api` directory, but its current materialized content is only an application README stating that it is the inbound HTTP/API composition root. No `apps/api/src/cfip_api/*` runtime module, FastAPI application object, router implementation, HTTP endpoint, or WebSocket endpoint is present in the audited tree.

Therefore:

| Dimension | Result | Evidence class |
|---|---|---|
| Target FastAPI application | `TARGET-REQUIRED` | no executable `apps/api/src` tree |
| Target HTTP routes | `TARGET-REQUIRED` / **0 evidenced** | no target route decorators found |
| Target WebSocket routes | `TARGET-REQUIRED` / **0 evidenced** | no target WebSocket implementation found |
| Target router composition | `TARGET-REQUIRED` | no target `include_router` composition found |
| Target API schemas | `TARGET-REQUIRED` | no API runtime schema surface found |
| Target auth dependency wiring | `TARGET-REQUIRED` | no API dependency graph found |
| Target entitlement enforcement | `TARGET-REQUIRED` | no API enforcement surface found |
| Target event side effects | `TARGET-REQUIRED` | no API handlers exist to establish side effects |
| Target route tests | `TARGET-REQUIRED` | no target API/WS route tests found |
| CForex source census tooling | `IMPLEMENTED` as source-study tooling | `tools/architecture/census_api_ws.py` |
| CForex route evidence | available as source evidence | source-study documents/tooling |

## Important correction

Earlier documentation contains statements such as “API composition root directly mounts” historical CForex routers. Those statements describe **CForex source evidence**, not executable CFIP API behavior. They must not be interpreted as evidence that the corresponding CFIP routes already exist.

The existing source-census tool is intentionally a source-study tool: it uses Python AST parsing and does not import the source application. Its own documentation explicitly describes the output as bounded static evidence rather than a runtime OpenAPI dump.

## Target repository route census

A target-repository route census must be based on executable CFIP source, not the CForex census output.

Current target tree evidence shows:

- `apps/api/README.md` exists.
- `apps/api/src/cfip_api/main.py` does **not** exist.
- `apps/api/src/cfip_api/router.py` does **not** exist.
- `apps/api/src/cfip_api/dependencies.py` does **not** exist.
- `apps/api/src/cfip_api/middleware.py` does **not** exist.
- `apps/api/src/cfip_api/error_handlers.py` does **not** exist.
- No target API route module was found in the repository tree.
- No target WebSocket route module was found in the repository tree.

Consequently, an exhaustive target route table is currently empty because there are **no executable target routes to enumerate**, not because route closure is complete.

## Source-study evidence versus target evidence

The repository does contain:

- `tools/architecture/census_api_ws.py` — static source-study extractor for FastAPI HTTP/WebSocket declarations, router prefixes and `include_router` edges.
- `tests/architecture/test_census_api_ws.py` — tests for that extractor.
- multiple `docs/evidence/CFIP-SOURCE-CLOSURE-*API*` documents describing historical CForex API/WS evidence.

These artifacts prove that the **study mechanism** exists and that CForex API/WS evidence has been investigated. They do not prove that CFIP exposes the same endpoints.

## Required D1 target contract

Before any target endpoint is implemented, every route must be registered with at least:

| Field | Required |
|---|---|
| Route ID | yes |
| Capability ID / bounded context | yes |
| HTTP method or WebSocket channel | yes |
| Canonical path/channel | yes |
| Request schema/version | yes |
| Response/event schema/version | yes |
| Error contract | yes |
| Authentication requirement | yes |
| Authorization/policy requirement | yes |
| Entitlement/usage rule, if applicable | yes |
| Idempotency semantics, if mutating | yes |
| PIT/replay semantics, if market-data/analysis related | yes |
| Event/outbox side effects | yes, or explicit none |
| Observability requirements | yes |
| Rate/abuse limits | yes where applicable |
| Implementation reference | required after implementation |
| Automated test reference | required for verification |
| Evidence state | yes |

## Security closure requirements

No API/WS route should be considered verified merely because the handler returns the expected payload. D1 closure requires explicit evidence for:

- authentication and principal extraction;
- authorization and capability/role checks;
- tenant/workspace isolation where applicable;
- entitlement/usage enforcement where applicable;
- input validation and bounded payloads;
- WebSocket origin/session/channel controls where applicable;
- replay/idempotency protection for mutating operations;
- secret isolation and absence of credential leakage;
- auditability for administrative or high-impact actions;
- fail-closed behavior on policy/dependency failure.

## Observability closure requirements

Each implemented route/channel must define:

- stable route/channel identifier;
- trace/span boundary;
- request/correlation identifier propagation;
- latency/error metrics;
- structured outcome logging without secrets/PII leakage;
- dependency failure classification;
- WebSocket connection/message lifecycle metrics where applicable.

## D1 status

**D1 target implementation: OPEN / TARGET-REQUIRED.**

This is intentionally stricter than the historical CForex source-study status. The current CFIP repository has the architectural destination and source-study machinery, but it does not yet contain the executable API/WS application needed to close D1.

## Next controlled action

Do not fabricate or bulk-create endpoints from CForex. The next implementation slice should be a **single CFIP-native vertical contract** selected from the capability registry, with:

`contract → application service → domain/context behavior → adapter boundary → API route → test → observability → evidence`

The route should only be added after its capability contract and target ownership are explicit.

## Evidence references

- `apps/api/README.md`
- `tools/architecture/census_api_ws.py`
- `tests/architecture/test_census_api_ws.py`
- `docs/capabilities/CFIP-CAPABILITY-REGISTRY.md`
- `docs/capabilities/source-evidence-matrix.md`
- `docs/evidence/CFIP-SOURCE-CLOSURE-API-CENSUS-TOOL.md`
- `docs/evidence/CFIP-SOURCE-CLOSURE-BATCH-29-API-WS-AND-REALTIME-CENSUS.md`

