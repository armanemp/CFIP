# CFIP Ecosystem Architecture Matrix

## مرجع نهایی معماری، اکوسیستم OSS و تصمیم‌گیری CFIP

**Baseline:** 2026-09-16  
**Scope:** 30 حوزه مادر، بیش از 400 capability/subdomain عملیاتی  
**Architecture:** Composable Platform  
**Target:** CFIP — Financial Intelligence Platform  
**Status:** Architecture Reference Baseline + OSS Ecosystem Audit Catalog

---

## 1. هدف

CFIP قرار نیست همه‌چیز را از صفر بازنویسی کند. راهبرد این پروژه:

> **CFIP owns Domain + Core IP + Contracts + Governance; OSS supplies reusable capabilities behind explicit adapters.**

بنابراین repository حاضر «لیست ابزار» نیست؛ یک سیستم تصمیم‌گیری معماری است که مشخص می‌کند هر capability:

`BUILD / INTEGRATE / ADAPT / EVALUATE / BENCHMARK / REFERENCE / FORK / REJECT`

چرا و تحت چه شواهدی انتخاب می‌شود.

---

## 2. دامنه مرجع

30 حوزه مادر:

1. Forex / Trading / Quant Core
2. Market & Financial Data
3. Trading Engine / Execution
4. AI / LLM / Agent
5. Research Intelligence / Deep Research
6. Search / Retrieval
7. Web Acquisition
8. Document Intelligence
9. Knowledge Graph / Memory
10. Evidence / Provenance / Trust
11. Machine Learning
12. MLOps / LLMOps
13. Data Platform
14. Streaming / Event Infrastructure
15. Workflow / Distributed Execution
16. Evaluation / Intelligence QA
17. Observability
18. Security / Identity / Governance
19. Autonomous Elyrava / Self-Development
20. Frontend / Terminal / Visualization
21. Realtime
22. Payments / Subscription
23. Testing / Reliability
24. DevOps / Infrastructure
25. Developer Platform
26. Financial Intelligence
27. Decision Intelligence
28. Governance of Intelligence
29. Research Dataset / Knowledge Lifecycle
30. Globalization / Accessibility

جزئیات capabilityها در `data/domains.json` و ownership در `data/capabilities.json` قرار دارد.

---

## 3. قانون OSS

محبوبیت، star count، نام بزرگ یا وجود یک README جذاب evidence محسوب نمی‌شود.

هر پروژه باید از نظر موارد زیر بررسی شود:

- functional fit
- maturity و production-readiness
- activity و release discipline
- contributor/maintainer risk
- license و transitive licenses
- security/CVE practice
- Python compatibility در صورت ارتباط
- performance/latency/throughput
- scalability
- self-hosting
- data ownership
- SaaS dependency
- vendor lock-in
- API/extension quality
- documentation/tests
- CPU/RAM/GPU/storage cost
- migration risk
- CFIP fit

هیچ پروژه‌ای قبل از عبور از adoption gate وارد runtime نمی‌شود.

---

## 4. Core IP

CFIP به‌صورت صریح مالک این بخش‌هاست:

- Evidence Contract
- Claim/Source semantics
- Research Intelligence Fabric
- Research Decision Model
- Market Structure semantics
- FVG / Order Block intelligence
- Signal Fusion
- Consensus semantics
- Confidence / Calibration
- Outcome Attribution
- Risk / Decision semantics
- PIT / reproducibility policy
- canonical event semantics
- Elyrava governance
- self-improvement gates
- domain contracts

در مقابل، قابلیت‌های عمومی مثل OCR، PDF parsing، crawling، browser automation، search، vector retrieval، graph storage، workflow، generic trading engines، authentication، observability و testing ابتدا OSS-first هستند.

---

## 5. معماری کلان

```text
Experience / Terminal
        │
        ▼
CFIP API / BFF
        │
        ▼
Elyrava Core
        │
        ▼
CFIP Canonical Contracts
        │
        ▼
Capability Fabric
 ┌──────┼────────┬────────┐
 AI   Research   Quant    Platform
 │       │         │        │
 OSS   OSS/CFIP   OSS      OSS
 adapters behind stable ports
        │
        ▼
Data Plane
PostgreSQL / ClickHouse / Redis / Object Storage
DuckDB / Arrow / Parquet
        │
        ▼
Event Plane
NATS JetStream
        │
        ▼
Observability + Governance
        │
        ▼
Elyrava Lab
Research → Experiment → Sandbox → Benchmark → Gate
→ Approval → Promotion → Health Guard → Rollback
```

---

## 6. Anti-sprawl

- یک implementation اصلی برای هر capability production مگر با ADR.
- یک event plane baseline؛ NATS JetStream فعلاً مرجع است.
- workflow engine با event broker اشتباه گرفته نمی‌شود.
- graph database پیش‌فرض نیست.
- چند vector/search engine همزمان وارد runtime نمی‌شوند مگر benchmark/ADR.
- چند trading engine همزمان وارد production نمی‌شوند.
- domain به vendor SDK وابسته نمی‌شود.
- agent به database یا infrastructure دسترسی مستقیم ندارد.
- microservice فقط با evidence استخراج می‌شود.
- Fork آخرین انتخاب است.

---

## 7. فایل‌ها

- `index.html` — نمای مادر
- `matrix.html` — ماتریس capability/OSS
- `projects.html` — کاتالوگ repositoryها
- `graph.html` — dependency/capability/OSS boundary graph
- `contracts.html` — ports و event contracts
- `adoption.html` — lifecycle انتخاب OSS
- `deployment.html` — deployment profiles
- `governance.html` — governance و decision freeze
- `domains.html` — 30 حوزه
- `research.html` — Research Intelligence
- `trading.html` — Trading/Quant
- `ai.html` — Elyrava/AI
- `data.html` — Data Platform
- `security.html` — Security/Identity
- `observability.html` — OTel/monitoring
- `frontend.html` — Terminal UX
- `payments.html` — subscription/payment
- `testing.html` — reliability/testing
- `autonomy.html` — autonomous development
- `architecture-decisions.html` — ADR registry
- `data/*.json` — source of truth ماشین‌خوان

---

## 8. وضعیت ممیزی OSS

این catalog با جست‌وجوی حوزه‌ای ساخته می‌شود، نه با ادعای بررسی تک‌تک repositoryهای GitHub. در حوزه‌هایی با ده‌ها هزار repository، ابتدا ecosystem coverage و سپس shortlist و evidence-level audit انجام می‌شود.

هر موردی که هنوز benchmark یا audit کامل ندارد، عمداً با وضعیت `candidate` یا `BENCHMARK` ثبت می‌شود و به‌عنوان dependency قطعی معرفی نمی‌شود.

---

## 9. قانون تصمیم نهایی

```text
Upstream
   ↓
Adapter
   ↓
Extension
   ↓
Patch upstream
   ↓
Fork
   ↓
Build ourselves
```

Build زمانی مجاز است که capability واقعاً Core IP/Domain-specific باشد یا evidence نشان دهد هیچ implementation قابل‌قبول با هزینه و ریسک منطقی وجود ندارد.

این سند جایگزین کتاب معماری قبلی است و مرجع فعلی تصمیم‌های معماری و OSS CFIP محسوب می‌شود.
