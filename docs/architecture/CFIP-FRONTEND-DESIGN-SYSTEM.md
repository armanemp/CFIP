# CFIP Frontend Design System — Product Visual Language

**Status:** Target architecture/design contract; Gate 0 compatible  
**Scope:** public web + authenticated terminal + admin/governance surfaces

## 1. Design objective

CFIP should look and behave like a purpose-built global market-intelligence platform: dense enough for professional analysis, calm enough for sustained use, and visually distinctive without relying on novelty effects.

The visual language is a platform-level contract. It must not encode market semantics that belong to domain contracts.

## 2. Signature palette

The palette is intentionally dark-first and semantic, with a restrained luminous accent system:

| Token family | Intended role |
|---|---|
| `cfip-ink` | deepest application canvas and navigation background |
| `cfip-graphite` | primary panels, cards and terminal chrome |
| `cfip-slate` | secondary surfaces, borders and structural separation |
| `cfip-cloud` | primary text and high-emphasis content |
| `cfip-mist` | secondary text, metadata and subdued labels |
| `cfip-cyan` | primary CFIP signature accent, active controls and data focus |
| `cfip-teal` | healthy/realtime/confirmed operational state |
| `cfip-violet` | intelligence/AI/research distinction |
| `cfip-amber` | caution, degraded confidence and attention states |
| `cfip-coral` | bearish/negative/error semantics where a market semantic requires it |
| `cfip-mint` | bullish/positive/success semantics where a market semantic requires it |

The signature identity is **cyan + teal + violet illumination over ink/graphite**, with amber/coral/mint reserved for semantic status. Saturation must be controlled; glow is an accent, not a permanent background effect.

## 3. Semantic separation

Visual tokens have two categories:

1. **brand/UI tokens** — CFIP identity, surfaces, typography and interaction focus;
2. **semantic tokens** — market direction, confidence, warning, error, health and entitlement state.

Market direction must never be inferred from the brand accent alone. Bullish/bearish colors remain configurable through accessible semantic tokens and must always have non-color cues such as icons, labels or numeric direction.

## 4. Terminal composition

The authenticated terminal should be organized around:

- global command/search rail;
- workspace navigation;
- instrument/context header;
- chart canvas;
- analysis/evidence panels;
- decision/risk panel;
- watchlist/scanner surfaces;
- event/realtime status strip;
- contextual inspector/drawer;
- optional AI/research assistant panel.

Panels should be resizable and collapsible where practical. The system must retain keyboard-first workflows while supporting pointer/touch interaction.

## 5. Typography and density

Use a modern variable sans-serif for application text and a tabular/monospaced numeric treatment for prices, quantities, timestamps and identifiers where it improves scanability. Typography must support Latin, Persian/Arabic and other product locales without changing semantic layout.

Density is adaptive rather than fixed: professional desktop mode may be information-dense; tablet/mobile mode prioritizes context, focus and task completion.

## 6. Motion

Motion communicates state transitions, not decoration. Realtime updates, chart crosshair/selection, panel transitions and AI/tool activity may use short bounded transitions. Respect reduced-motion preferences. Avoid animations that imply certainty or prediction.

## 7. Chart visual contract

The chart layer must preserve domain semantics independently from the renderer:

- correct timeframe boundaries;
- candle open/high/low/close lifecycle;
- timezone/session display rules;
- historical snapshot versus incremental update state;
- cursor/reconnect continuity;
- overlays and drawings with stable IDs;
- analysis evidence provenance;
- replay cursor and deterministic state;
- accessible non-chart summaries for critical decisions.

No visual treatment may make an unverified signal look authoritative.

## 8. Accessibility

Target WCAG-aligned interaction quality with keyboard navigation, visible focus, semantic landmarks, screen-reader labels, sufficient contrast, reduced motion and non-color status cues. Complex charts require textual/structured alternatives for important values and decisions.

## 9. Internationalization

Locale is a first-class application state. Layouts must support LTR and RTL without duplicating domain components. Dates, numbers, prices, percentages and timezones use locale-aware formatting. Translation keys are data/configuration, not scattered hardcoded UI strings.

## 10. Performance contract

Frontend performance is part of product correctness. Target architecture requires route-level code splitting, bounded client state, memoized high-frequency market views, incremental rendering where appropriate, controlled realtime update batching and explicit performance telemetry. Chart updates must not force unrelated application-wide renders.

## 11. SEO and public/private boundary

Public pages use semantic metadata, canonical URLs, robots/sitemap policy and server-rendered content where beneficial. Authenticated terminal state is not exposed through public indexing paths. Public marketing/education content and private workspace data use separate security and caching boundaries.

## 12. Component ownership

Components own presentation and interaction orchestration. Domain semantics belong to contracts/contexts. Feature modules may compose capabilities but must not duplicate analytical calculations, risk formulas, PIT reconstruction or event ordering logic.

## 13. Design-system acceptance

Before frontend implementation is considered production-ready:

- all major workflows have empty/loading/error/degraded states;
- RTL/LTR and locale formatting are verified;
- keyboard/touch/accessibility behavior is tested;
- realtime snapshot/incremental/reconnect behavior is tested;
- chart timeframe/candle semantics are tested;
- semantic colors have non-color alternatives;
- visual regression coverage exists for critical surfaces;
- performance budgets and telemetry are verified;
- public/private SEO boundaries are tested.
