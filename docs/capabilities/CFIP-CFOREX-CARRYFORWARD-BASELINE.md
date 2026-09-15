# CFIP CForex Carry-Forward Baseline

**Purpose:** prevent loss of material capabilities and engineering decisions accumulated in CForex while keeping CFIP clean-room and evidence-driven.

The historical source baseline is `armanemp/CForex` `main` / v0.9.154. The current observed CForex HEAD is `900882154cab3b9b74d0543b9bbf72a708a08134`. This document remains a carry-forward obligation index, not proof that CFIP already implements these capabilities. Current-head deltas are recorded separately and must be reconciled before Gate 0 closure.

## Carry-forward principles

1. Preserve meaningful behavior and contracts, not source-file structure.
2. Re-evaluate every dependency and implementation under CFIP's current architecture and standards.
3. Preserve mature governance controls even when implementation boundaries change.
4. Do not carry forward contradictory, obsolete or technically unsafe behavior merely because it existed in CForex; record intentional divergence with evidence/ADR.
5. Treat source implementation/tests/migrations/contracts as stronger evidence than release prose.
6. Historical source baselines never override the current CForex HEAD; source drift must produce an explicit evidence record before parity decisions.

## Material capabilities already established in CForex that CFIP must account for

### Platform and product surface

- Python-first modular realtime market-intelligence architecture.
- Professional chart-first trading terminal/workspace rather than a generic dashboard.
- Chart intelligence, drawing/workspace layers and responsive/touch-oriented UX.
- Terminal command surfaces for intelligence, analysis, risk, learning, journal, tutor and control functions.
- Public/private surface separation, SEO foundations and multilingual route metadata.
- Accessibility and RTL/LTR requirements.

### Market/data/realtime

- Canonical market observations with durable outbox before event publication.
- PostgreSQL-backed durable realtime state and runtime events.
- NATS JetStream durable pull consumption and explicit ACK-after-critical-processing semantics.
- Correlation/causation metadata.
- Realtime state hydration/recovery.
- Sequence/ordering, bounded dedupe and in-flight suppression.
- Watermarks, event-time semantics, late-event policies and bounded backpressure.
- Provider/source health, data quality and freshness intelligence.

### Analytics and trading intelligence

- Deterministic analytical engines with explicit engine identity/versioning.
- Technical, structure, liquidity, FVG, order-block, regime and multi-timeframe evidence.
- Confluence, contradiction and consensus boundaries.
- Strategy/research/backtest/replay workflows.
- Account-aware risk, leverage, position sizing and entry/exit guidance.
- Single reproducible decision package rather than disconnected analyzer answers.
- Fail-closed live execution boundary.
- Journal, MAE/MFE and outcome attribution.

### Learning and intelligence

- Temporal learning attribution and contextual memory.
- Leakage controls and train/holdout temporal boundaries.
- Attribution by instrument/timeframe/setup/regime/provider.
- Governed learning memory and bounded recommendations.
- Platform knowledge fabric with provenance-bound records, temporal/aspect filtering and content hashing.
- AI context grounding in governed knowledge and market evidence.
- Governed Platform Academy / Tutor with bilingual translation-key based curriculum.
- Safe Code Editing Lab and engineering education.
- Autonomous development readiness with sandbox-first behavior.
- Evidence-driven Research → Development bridge.
- Persisted intelligence performance evidence.
- Performance-regression release gate.
- Tool allowlisting and local-model capability probing where relevant.
- Fail-closed autonomous promotion.
- Independent post-gate verification.
- Rollback manifests and least-privilege agent governance.
- Excessive-agency controls.
- Continuous research, learning, self-development and verification loops with high-impact actions fail-closed.

### Research intelligence

- Governed source registry and point-in-time research evidence.
- Source identity, freshness, rights/licensing and vintage verification.
- Release-watch discovery/staging.
- Training permission disabled until rights and vintage verification are satisfied.
- Research-to-development adoption workflow.

### Product governance

- Authentication/authorization and workspace boundaries.
- Usage and entitlement controls.
- Admin settings, autonomy and intelligence governance.
- Provider/model capability boundaries.
- Security posture, health/readiness and operational diagnostics.
- Billing and product entitlement surfaces.
- Notifications and user/workspace controls.
- Governed Admin Git as an application capability, explicitly separated from shell/terminal authority.
- Git input/ref validation, bounded execution, credential-safe output, operation identity and telemetry.

### Operations and quality

- Production composition boundaries separated from unit tests.
- Opt-in live-integration smoke tests.
- Release gate orchestration.
- Independent verification.
- Runtime process smoke checks.
- Observability through OpenTelemetry.
- Performance-governed terminal refresh and rendering behavior.
- Hidden-tab polling suppression and visibility-aware refresh.
- Single-flight/cancellation patterns to reduce duplicate work and stale responses.

## Current-head delta obligation

CForex current HEAD `900882154cab3b9b74d0543b9bbf72a708a08134` adds hardened governed Admin Git behavior. The delta is classified as `PRESERVE + IMPROVE` for the governance boundary, with explicit reconciliation still required for all write operations and source tests. Detailed evidence: `docs/architecture/CFIP-SOURCE-DELTA-59-ADMIN-GIT.md`.

## Known source evidence caveat

The v0.9.154 evidence records 330 governed synthetic point-in-time platform-knowledge records across 18 AI aspects, 42 authoritative research/data sources, 69 release gates in the continuity update, and 15/15 independent verification checks. These are **source-side evidence**, not CFIP implementation claims.

The source README also records an earlier release history with evolving versions and temporary validation constraints. Those historical details are useful for capability discovery but must not be copied blindly into CFIP configuration or dependency policy.

## CFIP carry-forward rule

For each material source capability above, Gate-0 closure evidence must classify it as:

`PRESERVE → IMPROVE → REPLACE → INTENTIONALLY-DIVERGE`

with:

- source evidence reference;
- capability ID;
- behavioral contract;
- target owner;
- verification plan;
- parity status;
- divergence ADR when applicable.

No capability is considered safely carried forward merely because a similarly named file or feature exists in CFIP.