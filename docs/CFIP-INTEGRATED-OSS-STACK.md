# CFIP — Integrated OSS Stack & Contract Boundary

**Baseline:** 2026-09-16  
**Status:** Canonical target decision document (implementation plan; not a claim that every item is already runtime-integrated)

## 1. تصمیم اصلی

CFIP قرار نیست کاتالوگ صدها پروژه باشد و قرار نیست همه پروژه‌های کاتالوگ هم‌زمان نصب شوند.

هدف این سند دقیقاً مشخص می‌کند **چه پروژه‌هایی برای runtime / platform واقعاً وارد CFIP می‌شوند**، کدام‌ها فقط به‌عنوان optional/research باقی می‌مانند و کدام capabilityها باید توسط خود CFIP ساخته شوند.

اصل:

> **Python-first + maximum reuse + minimum custom code + explicit contracts + one authoritative semantic owner per capability.**

معماری اجرایی:

`Experience → API/BFF → Application → CFIP Contracts/Domain → OSS Adapters → Data/Event/Operations`

OSS هرگز domain authority نیست. هر OSS project فقط پشت Port/Adapter مجاز است.

---

## 2. Runtime Baseline — پروژه‌های منتخب برای ادغام

| حوزه | پروژه | نقش در CFIP | زبان/رویکرد | تصمیم |
|---|---|---|---|---|
| Trading/Execution | `NautilusTrader` | trading engine، event-driven research/simulation/live execution boundary | Rust core + Python control plane | **INTEGRATE via Adapter** |
| AI/Agents | `PydanticAI` | agent runtime، typed tools، structured outputs، MCP/tool capabilities | Python-first | **INTEGRATE** |
| Research/Orchestration | `LangGraph` | stateful research/agent graph فقط در orchestration layer | Python | **INTEGRATE selectively** |
| Research/RAG | `Haystack` | modular retrieval/RAG pipelines و components | Python | **INTEGRATE selectively** |
| Deep Research | `STORM` | research methodology/reference components، نه domain authority | Python | **ADAPT / REFERENCE** |
| Document Intelligence | `Docling` | PDF/DOCX/PPTX/XLSX/HTML parsing، layout/table/chart understanding | Python | **INTEGRATE** |
| Web Acquisition | `Playwright` | browser automation و JS-rendered acquisition | Python API | **INTEGRATE** |
| Vector Retrieval | `Qdrant` | vector/semantic retrieval backend در صورت عبور از benchmark | Rust server + Python client | **INTEGRATE via Adapter** |
| Event Plane | `NATS JetStream` + `nats-py` | durable eventing، pub/sub، replay و worker communication | server + Python client | **INTEGRATE** |
| Durable Workflow | `Temporal` | long-running/retryable workflows و recovery | Python SDK + service | **INTEGRATE selectively** |
| Authorization | `OpenFGA` | fine-grained authorization / relationship-based access | Go service + Python SDK | **INTEGRATE** |
| Observability | `OpenTelemetry` | traces/metrics/logging contracts و context propagation | Python SDK + ecosystem | **INTEGRATE** |
| MLOps/LLMOps | `MLflow` | experiment/model/prompt/evaluation lifecycle | Python-first ecosystem | **INTEGRATE selectively** |
| DataFrame/Research | `Polars` | high-performance research/data transformations | Rust core + Python API | **INTEGRATE** |
| Local Analytics | `DuckDB` | local/research/PIT reconstruction/Parquet analytics | embedded + Python | **INTEGRATE** |
| Columnar Data | `Apache Arrow/Parquet` | canonical interchange/artifact format | multi-language + Python | **INTEGRATE** |

### Storage baseline

- `PostgreSQL`: authoritative transactional/control-plane state.
- `ClickHouse`: analytical/time-series workloads where workload evidence supports it.
- `Redis`: bounded cache/ephemeral coordination only; never source of truth.
- Object storage: immutable datasets, documents, model/evaluation artifacts when justified.
- `DuckDB + Parquet + Arrow`: research/local analytics plane.

### Frontend baseline

- `Next.js + React + TypeScript + Tailwind` for the terminal.
- `TradingView Lightweight Charts` for chart-first market UI.
- Python remains the domain/application/agent/research control-plane language.

---

## 3. چیزهایی که عمداً ادغام نمی‌کنیم

### Trading engines
`LEAN`, `Backtrader`, `vectorbt`, `AAT` و سایر engineها در runtime اصلی هم‌زمان نصب نمی‌شوند. آنها برای benchmark/reference یا migration evidence باقی می‌مانند. اگر benchmark نشان دهد NautilusTrader برای یک workload خاص کافی نیست، تصمیم با ADR و boundary جدید انجام می‌شود.

### Agent frameworks
LangChain/LangGraph، Haystack، CrewAI، AutoGen/Microsoft Agent Framework، Semantic Kernel، Agno، OpenAI Agents SDK و غیره هم‌زمان به‌عنوان چند runtime مستقل وارد محصول نمی‌شوند. `PydanticAI` لایه typed agent/tool contract است؛ `LangGraph` فقط در orchestrationهای stateful که واقعاً به graph semantics نیاز دارند استفاده می‌شود؛ Haystack برای pipeline/retrieval components در موارد لازم استفاده می‌شود.

### Search engines
Vespa، OpenSearch، Elasticsearch، Qdrant، Weaviate، Milvus، pgvector، Typesense، Meilisearch و غیره همگی backend هم‌زمان نیستند. ابتدا PostgreSQL/ClickHouse و سپس Qdrant در صورت نیاز واقعی؛ search backend فقط پشت `SearchProvider/Retriever/Reranker` قرار می‌گیرد.

### Workflow engines
Temporal، Prefect، Dagster، Airflow، Celery، Dramatiq و Arq هم‌زمان deploy نمی‌شوند. `NATS JetStream` event plane است و `Temporal` فقط durable workflow plane؛ این دو جای یکدیگر نیستند.

### Document parsers
Docling baseline parser است. MinerU/Unstructured/Marker/PyMuPDF/Camelot/Tabula/PaddleOCR/Surya/Tesseract به‌عنوان fallback یا benchmark نگه داشته می‌شوند و فقط در صورت evidence وارد adapter set می‌شوند.

---

## 4. چیزهایی که باید خود CFIP بسازد

اینها generic framework نیستند و نباید با OSS جایگزین شوند:

1. `Evidence Contract`
2. Claim/Source/Evidence semantics
3. PIT / available-at semantics و reproducibility policy
4. Market Structure semantics
5. FVG lifecycle و intelligence
6. Order Block semantics و intelligence
7. MTF evidence semantics
8. Signal Fusion
9. Consensus semantics
10. Confidence / uncertainty / calibration
11. Outcome Attribution
12. Decision Intelligence / final decision contract
13. Risk/position-sizing semantics و broker-account constraints
14. Canonical engine identity/version/descriptor contract
15. Canonical event semantics
16. Research Decision Model
17. Research evidence/provenance graph semantics
18. Elyrava governance، safety، promotion/rollback و self-improvement gates
19. Agent authorization/tool policy boundary
20. Dataset identity/revision/PIT lineage
21. Cross-engine replay/backtest compatibility contract
22. Domain/application contracts

---

## 5. قرارداد بین پروژه‌ها

تمام ارتباطات زیر از contract عبور می‌کند و direct dependency ممنوع است:

```text
                 ┌─────────────────────┐
                 │ CFIP Canonical      │
                 │ Contracts           │
                 └─────────┬───────────┘
                           │
       ┌───────────────────┼────────────────────┐
       ▼                   ▼                    ▼
 Market/Quant          Research/AI         Platform
       │                   │                    │
 Nautilus           PydanticAI/LangGraph   Temporal/NATS
       │             Haystack/STORM        PostgreSQL/CH
       ▼                   ▼                    ▼
  Market Events      Evidence Objects      Workflow Events
       └───────────────────┼────────────────────┘
                           ▼
                    Evidence/Outcome
                           │
                           ▼
                         Elyrava
```

### Core ports

- `MarketDataProvider`
- `HistoricalDataProvider`
- `EconomicDataProvider`
- `NewsProvider`
- `SearchProvider`
- `Retriever`
- `Reranker`
- `WebAcquisitionPort`
- `DocumentParser`
- `OCRProvider`
- `EvidenceStore`
- `KnowledgeGraphPort`
- `MemoryProvider`
- `ModelProvider`
- `AgentRuntime`
- `ToolRegistry`
- `ResearchPlanner`
- `ResearchExecutor`
- `SignalEngine`
- `ConsensusService`
- `RiskEngine`
- `OrderGateway`
- `ExecutionGateway`
- `BacktestEngine`
- `ReplayEngine`
- `EvaluationProvider`
- `FeatureStore`
- `WorkflowPort`
- `IdentityProvider`
- `AuthorizationProvider`
- `PaymentProvider`
- `NotificationProvider`
- `ArtifactStore`

---

## 6. Canonical Event Contract

Every durable event uses a versioned envelope:

```text
id
schema_version
event_type
occurred_at
observed_at
producer
aggregate_type
aggregate_id
correlation_id
causation_id
partition_key
sequence
payload
metadata
```

Rules:

- durable outbox before durable fan-out;
- idempotent consumers;
- explicit ordering/partition semantics;
- replayability where required;
- schema compatibility/versioning;
- audit correlation;
- no business correctness based solely on Redis/cache state.

---

## 7. Canonical Evidence Contract

Every research/AI/market conclusion must be representable as:

```text
Evidence
 ├─ evidence_id
 ├─ source_id
 ├─ source_type
 ├─ source_uri
 ├─ provider
 ├─ retrieved_at
 ├─ published_at
 ├─ available_at
 ├─ content_hash
 ├─ locator/span
 ├─ claim_id
 ├─ support_type
 ├─ freshness
 ├─ authority
 ├─ confidence
 └─ provenance
```

AI frameworks may create candidates, but CFIP owns evidence semantics and citation validation.

---

## 8. Research contract

Canonical pipeline:

`Question → Planner → Decomposition → Acquisition → Retrieval → Evidence → Verification → Contradiction → Synthesis → Citation Validation → Confidence → Answer`

- `PydanticAI`: typed agent/tool execution.
- `LangGraph`: stateful orchestration where required.
- `Haystack`: retrieval/pipeline components where useful.
- `STORM`: research methodology/reference patterns.
- `Playwright`: browser acquisition.
- `Docling`: document extraction.
- `Qdrant`: semantic retrieval when benchmarked.
- CFIP: research state, evidence semantics, contradiction rules, confidence and final answer contract.

---

## 9. Trading contract

Canonical pipeline:

`Provider → Normalization → Market Truth/PIT → Structure → Features → Signal → Consensus → Risk → Execution Gateway`

- `NautilusTrader` owns reusable engine/runtime mechanics only behind CFIP adapter.
- CFIP owns FVG/OB/MTF/structure semantics, signal fusion, consensus, risk semantics and final decision contract.
- Backtest/replay/live paths must share the same canonical engine identity and execution semantics where applicable.

Final analytical decision schema:

`direction, entry_zone/trigger, stop_loss, targets, invalidation, risk_budget, position_size, leverage_constraint, confidence, evidence, timeframe, generated_at, data_freshness`

Execution authority is separate from analytical recommendation.

---

## 10. Minimum-custom-code rule

Before writing a new CFIP implementation:

1. Check whether an adopted project already provides the capability.
2. If yes, use it behind an existing port.
3. If API mismatch exists, write a thin adapter.
4. If semantics mismatch, add a CFIP translation layer—not duplicated domain logic.
5. Only build from scratch when the capability is CFIP core IP or no acceptable OSS implementation exists.
6. Every new dependency requires owner, failure mode, license, security, resource, upgrade and rollback analysis.

هدف عملی: **کدنویسی اختصاصی فقط جایی که ارزش/قرارداد/مالکیت معنایی CFIP ایجاد می‌کند.**

---

## 11. Integration status semantics

- `INTEGRATE`: planned runtime dependency after adoption gates.
- `INTEGRATE via Adapter`: runtime capability, but isolated behind CFIP port.
- `INTEGRATE selectively`: only specific components/features are used.
- `ADAPT / REFERENCE`: methodology/components inform CFIP but are not a runtime authority.
- `BENCHMARK`: evaluated before runtime choice.
- `OPTIONAL`: deployment/profile dependent.
- `REJECT`: explicitly unsuitable for target constraints.
- `BUILD`: CFIP-owned implementation.

**Inventory ≠ runtime dependency.**

---

## 12. Evidence snapshot

Current primary-source checks confirm, among others:

- NautilusTrader currently documents a Rust-native production trading engine with Python 3.12–3.14 support and a Python control plane. 
- PydanticAI is a Python agent framework with typed capabilities/tooling; its repository shows active 2026 releases. 
- Haystack 3.x is a Python production-oriented orchestration/RAG framework and its package metadata lists Python 3.14. 
- Docling provides broad document parsing and advanced PDF/layout/table/chart understanding with Python APIs. 
- Playwright provides a Python API for Chromium/Firefox/WebKit and current package metadata lists Python 3.14. 
- NATS Python provides asyncio Core NATS and JetStream support. 
- Temporal provides a durable workflow engine with a Python SDK. 
- OpenFGA provides fine-grained authorization with Python SDK support and PostgreSQL-backed production deployment options. 
- OpenTelemetry Python provides stable tracing and metrics APIs/SDKs and tracks current Python compatibility. 
- Qdrant is a vector search/database service with Python client support. 
- MLflow covers model/agent/LLM evaluation, observability and lifecycle capabilities. 

These facts support candidate selection; final production adoption still requires CFIP-specific integration, security, performance and failure-recovery gates.

---

## 13. Non-negotiable boundary

No adopted OSS project may:

- define CFIP domain truth;
- bypass authorization/policy;
- write directly to authoritative databases outside its adapter contract;
- mutate production intelligence governance;
- silently change PIT/replay semantics;
- become an unversioned hidden dependency;
- introduce an alternative canonical implementation of the same semantic engine.

The intended end state is a **composable Python-first platform assembled primarily from mature OSS capabilities, with a small and explicit CFIP-owned semantic/core-IP layer and machine-verifiable contracts between every major subsystem.**
