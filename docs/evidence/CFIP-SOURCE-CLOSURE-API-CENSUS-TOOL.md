# Source-Closure API/WebSocket Census Tool

## Purpose

`tools/architecture/census_api_ws.py` is the first executable source-closure extractor for Gate 0. It statically parses a CForex checkout with Python's standard-library `ast` module and records FastAPI HTTP/WebSocket route declarations without importing CForex or requiring its runtime dependencies.

FastAPI models HTTP path operations and WebSocket operations through `FastAPI`/`APIRouter` decorators, router prefixes and `include_router`; the extractor records those constructs as source evidence.

## What it records

- HTTP route vs WebSocket route.
- Source file and source line.
- Decorator/owner and handler function.
- Declared route path.
- Statically known router prefix.
- Effective path when the local router prefix is statically resolvable.
- Explicit unresolved-path status when static composition is insufficient.
- `Depends`/`Security` dependency names.
- Conservative evidence hints for event publishing, outbox references, authentication/principal symbols, entitlement/usage symbols and repository references.
- `include_router` edges and their static include prefixes.
- Files that could not be parsed/read.

## Deliberate non-inferences

The tool does **not** claim that a route's caller, service owner, authorization policy, entitlement, event side effect, repository, telemetry, or tests are proven merely by names. Those are separate Gate 0 evidence dimensions.

This is important for migration correctness: a static census should maximize coverage while preserving an explicit `UNRESOLVED` state rather than turning incomplete analysis into false certainty.

## Usage

```text
python tools/architecture/census_api_ws.py --source-root ../CForex --format json --output /tmp/cforex-api-ws.json
python tools/architecture/census_api_ws.py --source-root ../CForex --format markdown --output /tmp/cforex-api-ws.md
```

The output is deterministic for the same source tree. JSON is intended for later machine reconciliation; Markdown is intended for evidence review.

## Verification

The companion standard-library `unittest` suite exercises route extraction, WebSocket extraction, local router prefixes, dependency discovery, include edges and deterministic serialization:

```text
python -m unittest discover -s tests/architecture -p 'test_*.py'
```

The tool is migration/evidence infrastructure and does **not** close Gate 0 or authorize CFIP runtime implementation.
