# مرجع مادر معماری و اکوسیستم CFIP

**وضعیت:** Baseline مرجع معماری — Frozen for decision-making until an explicit ADR changes it  
**تاریخ baseline:** 2026-09-16  
**هدف:** ساخت CFIP به‌عنوان یک Composable Financial Intelligence Platform، نه بازنویسی صفر تا صد  
**اصل محوری:** `CFIP owns Domain + Contracts + Governance + proprietary intelligence; OSS owns reusable capabilities.`

> این سند جایگزین کامل «کتاب معماری قبلی» است. هدف آن فهرست ابزار نیست؛ بلکه مرجع تصمیم‌گیری برای Build/Integrate/Adapt/Evaluate/Benchmark/Reference/Fork است.

---

## 1. تصمیم مادر

CFIP از صفر همه‌چیز را نمی‌سازد. ابتدا اکوسیستم Open Source در کل حوزه‌های موردنیاز ممیزی می‌شود، قابلیت‌های mature شناسایی و غربال می‌شوند و سپس CFIP با قراردادها و Domain Model اختصاصی خود، بهترین implementationهای موجود را پشت مرزهای استاندارد قرار می‌دهد.

فرآیند اجباری:

`Discover → Deduplicate → Classify → Technical Audit → Security/License Audit → Benchmark Evidence → CFIP Fit → Adoption Decision`

هیچ پروژه OSS فقط به دلیل شهرت وارد runtime نمی‌شود.

---

## 2. دامنه مادر

Baseline فعلی شامل **30 حوزه مادر** و بیش از **400 capability/subdomain عملیاتی** است:

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

در نسخه‌های آینده فقط با ADR می‌توان حوزه مادر را حذف، ادغام یا تغییر داد.

---

## 3. مدل انتخاب OSS

هر repository در کاتالوگ ماشین‌خوان ثبت می‌شود و حداقل این فیلدها را دارد:

- نام و URL رسمی
- حوزه و capability
- نقش: `BUILD | INTEGRATE | ADAPT | EVALUATE | BENCHMARK | REFERENCE | FORK | REJECT`
- دلیل تصمیم
- license و compatibility
- وضعیت نگهداری و آخرین release
- تعداد/تنوع مشارکت‌کنندگان و ریسک single-maintainer
- maturity و production evidence
- Python compatibility، در صورت مرتبط بودن
- architecture و integration surface
- self-hosting و deployment
- امنیت و سابقه آسیب‌پذیری
- performance و scalability
- CPU/RAM/GPU/storage cost
- data ownership
- SaaS/vendor lock-in
- extensibility/plugin/adapter model
- documentation و testing
- migration risk
- CFIP boundary
- evidence/reference برای تصمیم

**Fork آخرین انتخاب است:**

`Upstream → Adapter → Extension → Upstream Patch → Fork → Build`

---

## 4. مرز Core IP و OSS

### CFIP Core IP

موارد Domain-specific و governed که مالکیت طراحی آنها باید نزد CFIP بماند:

- Evidence Contract
- Claim/Evidence/Source مدل
- Research Decision Model
- Research Intelligence Fabric
- FVG/Order Block intelligence
- Market Structure/Liquidity semantics اختصاصی
- Signal Fusion
- Consensus و contradiction semantics
- Confidence و calibration policy
- Outcome Attribution
- Financial Decision Intelligence
- Elyrava governance
- self-improvement gates
- domain contracts و canonical event semantics
- PIT/reproducibility policy
- risk decision policy و CFIP execution boundary

### قابلیت‌هایی که ابتدا OSS بررسی می‌شوند

PDF parsing، OCR، crawling، browser automation، search engine، vector search، graph database، workflow engine، generic trading engine، authentication، authorization، observability، ML frameworks، experiment tracking، testing و infrastructure.

---

## 5. معماری کلان

```text
┌─────────────────────────────────────────────────────────────┐
│                         CFIP                                │
│              Financial Intelligence Platform                │
├─────────────────────────────────────────────────────────────┤
│ EXPERIENCE                                                  │
│ Trading Terminal │ Research │ AI │ Journal │ Admin          │
├─────────────────────────────────────────────────────────────┤
│ CFIP API / BFF                                              │
├─────────────────────────────────────────────────────────────┤
│ ELYRAVA CORE                                                │
│ Planning │ Reasoning │ Research │ Decision │ Memory          │
├─────────────────────────────────────────────────────────────┤
│ CFIP CONTRACT LAYER                                         │
│ Search │ MarketData │ Evidence │ Agent │ Tool │ Model        │
│ Document │ Signal │ Risk │ Order │ Research │ Evaluation     │
├─────────────────────────────────────────────────────────────┤
│ CAPABILITY FABRIC                                           │
│ AI/Agent │ Search │ Web │ Documents │ Graph │ Quant           │
│ ML │ Evaluation │ Workflow │ Data │ Streaming │ Security      │
├─────────────────────────────────────────────────────────────┤
│ DATA PLANE                                                  │
│ PostgreSQL │ ClickHouse │ Redis │ Object Storage │ Search     │
├─────────────────────────────────────────────────────────────┤
│ EVENT PLANE                                                 │
│ NATS JetStream                                              │
├─────────────────────────────────────────────────────────────┤
│ OBSERVABILITY / GOVERNANCE                                  │
│ OpenTelemetry │ Metrics │ Logs │ Traces │ Audit │ Policy      │
├─────────────────────────────────────────────────────────────┤
│ ELYRAVA LAB                                                 │
│ Research → Experiment → Sandbox → Benchmark → Gate           │
│ → Promotion → Health Guard → Rollback                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Elyrava

Elyrava یک framework vendor-specific نیست. هسته آن باید مستقل از مدل، agent framework و provider باقی بماند.

```text
Elyrava
├── Agent Contract
├── Tool Contract
├── Model Contract
├── Memory Contract
├── Research Contract
└── Governance Contract
        │
        ├── adapter: LangGraph
        ├── adapter: Haystack
        ├── adapter: PydanticAI
        └── future adapters
```

Agentها حق دسترسی مستقیم به DB، broker credential یا HTTP نامحدود ندارند؛ تمام عملیات از application ports و policy checks عبور می‌کند.

---

## 7. Research Intelligence Fabric

CFIP نباید به chatbot + RAG تقلیل پیدا کند.

```text
Question
 ↓
Research Planner
 ↓
Query Decomposition
 ↓
Search / Acquisition
 ↓
Retrieval
 ↓
Evidence Extraction
 ↓
Verification
 ↓
Contradiction Analysis
 ↓
Synthesis
 ↓
Citation Validation
 ↓
Confidence / Freshness / Trust
 ↓
Answer + Evidence Graph
```

تحقیق خارجی تا زمان ثبت source identity، freshness، provenance، rights و evidence قابل اعتماد تلقی نمی‌شود.

---

## 8. Search و Retrieval

Capabilityها:

- Web/meta search
- full-text
- BM25
- dense/sparse retrieval
- hybrid retrieval
- vector search
- reranking
- query expansion
- temporal retrieval
- faceting
- ranking analytics

نامزدهای اصلی برای ممیزی شامل Vespa، OpenSearch، Elasticsearch، Qdrant، Weaviate، Milvus، pgvector، Typesense، Meilisearch، Tantivy، LanceDB و FAISS هستند.

هیچ‌کدام از پیش انتخاب‌شده نیستند؛ benchmark و architecture-fit تعیین‌کننده است.

---

## 9. Web Acquisition

Crawling، scraping، browser automation، JS rendering، deduplication، canonicalization، RSS، sitemap، crawl scheduling، politeness و source monitoring باید پشت `WebAcquisitionPort` قرار گیرند.

نامزدهای بررسی: Playwright، Selenium، Scrapy، Browser-use، Firecrawl، trafilatura، newspaper4k، readability، BeautifulSoup و httpx ecosystem.

---

## 10. Document Intelligence

PDF، HTML، DOCX، XLSX، PPTX، OCR، table/layout extraction، chart و multilingual document handling باید capabilityهای مستقل باشند.

نامزدها: Docling، MinerU، Unstructured، Marker، PyMuPDF، PaddleOCR، Tesseract، Surya، Camelot و Tabula.

---

## 11. Knowledge / Memory

CFIP مدل خود را برای Claim Graph، Evidence Graph، Temporal Graph، Entity Resolution و Agent Memory مالک می‌شود؛ database implementation قابل تعویض است.

نامزدهای بررسی: Neo4j، Kuzu، Apache AGE، Memgraph، NetworkX و پروژه‌های فعال GraphRAG/Memory.

اصل: Graph DB تا زمانی که benchmark و workload واقعی نیاز آن را ثابت نکند، جزء الزامی runtime نیست.

---

## 12. Evidence / Provenance / Trust

این لایه Core IP است.

هر Evidence باید تا حد نیاز دارای source، retrieval timestamp، event-time، content hash، provenance، citation span، supporting/contradicting claims، confidence و freshness باشد.

اصل بنیادی: **historical truth قابل بازسازی و PIT-safe باشد.** یک revision جدید نباید بدون trace کردن lineage، تصمیم تاریخی را تغییر دهد.

---

## 13. Trading / Quant

قابلیت‌های بررسی:

Market Data، Tick/OHLCV، Order Book، Microstructure، Technical Analysis، Price Action، Market Structure، Liquidity، FVG، Order Blocks، MTF، Pattern Detection، Indicators، Signals، Strategy Engine، Backtest، Walk-forward، Replay، Paper/Live Trading، Execution، Slippage، Transaction Cost، Portfolio، Position Sizing، Risk، Leverage، Margin، SL/TP، Journal و Performance Attribution.

### Trading engine

NautilusTrader و LEAN باید عمیقاً بررسی و benchmark شوند. Qlib نیز برای research/AI/quant workflow بررسی می‌شود.

FVG/OB و semantics اختصاصی CFIP از engine عمومی جدا می‌مانند.

**چند trading engine همزمان وارد runtime نمی‌شوند.** یک execution boundary استاندارد ساخته می‌شود و فقط یک implementation عملیاتی در هر deployment profile انتخاب می‌شود.

---

## 14. Market Data

Provider نباید وارد Domain شود.

```text
Provider
 ↓
Raw
 ↓
Normalize
 ↓
Validate
 ↓
Deduplicate
 ↓
Event-Time
 ↓
Quality
 ↓
Canonical Observation
 ↓
Transactional Outbox
 ↓
NATS JetStream
```

تمام providerها پشت `MarketDataProvider`، `EconomicDataProvider` و `NewsProvider` قرار می‌گیرند.

نامزدها شامل OpenBB، yfinance ecosystem، Nasdaq Data Link tooling، Stooq، Alpha Vantage integrations، FMP integrations، Polygon/Massive integrations، ccxt، pandas-datareader، fredapi، sec-edgar-downloader، edgartools، Arelle/XBRL و exchange-specific clients هستند.

---

## 15. Data Plane

Baseline:

- **PostgreSQL:** system of record و transactional invariants
- **ClickHouse:** analytical/high-volume time-series workloads
- **Redis:** cache و ephemeral bounded state
- **Object Storage:** datasets، immutable artifacts و model/evidence bundles
- **DuckDB:** local/research analytical execution
- **Arrow/Parquet:** columnar interchange و datasets

Vespa، graph DB، lakehouse engines و سایر datastoreها فقط با evidence و benchmark اضافه می‌شوند.

---

## 16. Event Plane و Workflow

NATS JetStream baseline event infrastructure است.

Kafka، Redpanda، Pulsar و Redis Streams باید به‌عنوان benchmark/reference بررسی شوند، نه اینکه همزمان وارد runtime شوند.

### Event envelope

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

### NATS vs Workflow Engine

NATS JetStream مسئول durable messaging/event streams است؛ workflow engine مسئول durable execution، timers، retries، compensation و workflow state است.

Temporal، Prefect، Dagster، Airflow، Celery، Dramatiq، Arq و Hatchet باید بر اساس workload واقعی benchmark شوند. استفاده همزمان از چند workflow engine ممنوع است مگر با ADR صریح.

---

## 17. ML / LLMOps

نامزدها:

PyTorch، scikit-learn، XGBoost، LightGBM، CatBoost، Hugging Face، PyTorch Forecasting، Darts، Nixtla، Ray، JAX، MLflow، Feast، DVC، Kubeflow، Optuna و Evidently.

قابلیت‌های اجباری:

- dataset versioning
- experiment lineage
- train/holdout temporal separation
- leakage detection
- model registry
- evaluation
- calibration
- drift
- reproducibility
- promotion/rollback

---

## 18. Evaluation

معیارها و capabilityها:

RAG recall/precision، MRR، nDCG، citation precision/recall، groundedness، faithfulness، contradiction، freshness، latency، token cost، calibration و financial outcome evaluation.

نامزدها: Ragas، DeepEval، TruLens، Arize Phoenix، Langfuse، promptfoo، OpenAI Evals ecosystem و ابزارهای مشابه.

Reference implementation با production dependency یکی نیست.

---

## 19. Security / Identity

Identity: Keycloak، ZITADEL، Authentik، OAuth/OIDC.  
Authorization: OpenFGA، OPA، Casbin و Zanzibar-style designs.  
Secrets: Vault، Infisical، SOPS، age.  
Supply chain: Trivy، Semgrep، Bandit، CodeQL، Gitleaks، Syft، Grype و SBOM tooling.

Agent permissions باید با همان authorization policyهای governed platform یکپارچه شوند.

---

## 20. Autonomous Elyrava

چرخه استاندارد:

`Observe → Propose → Checkpoint → Isolate → Risk Check → Sandbox → Independent Verification → Gates → Approval if required → Promote → Health Guard → Rollback`

Risk classes:

- LOW: تغییر محدود و reversible؛ automatic promotion فقط پس از تمام gates
- MEDIUM: human approval اجباری
- HIGH: authorization صریح و کنترل‌های تقویت‌شده

Self-healing با self-development یکی نیست؛ اولی operational recovery است و دومی تغییر پیشنهادی و governed.

نامزدهای بررسی: OpenHands، SWE-agent، Aider، Continue، Roo Code ecosystem، Cline ecosystem، OpenCode و ابزارهای repository/code intelligence.

---

## 21. Frontend / Terminal

Target:

Next.js + React + TypeScript + Tailwind + TradingView Lightweight Charts یا renderer جایگزین که contract را حفظ کند.

CFIP dashboard سنتی نیست؛ chart-first terminal است:

```text
┌─────────────────────────────────────────────┐
│                 CFIP TERMINAL               │
│                                             │
│ Tools       CHART / MARKET / RESEARCH       │
│ Rail        Intelligence Workspace          │
│                                             │
│ ─────────────────────────────────────────   │
│ Timeline / Signals / Evidence / AI          │
└─────────────────────────────────────────────┘
```

Accessibility، keyboard navigation، responsive، PWA، SEO، i18n و RTL/LTR از ابتدا جزء architecture هستند.

---

## 22. Realtime

Market streaming، signals، research progress، agent events و notifications از event plane تغذیه می‌شوند.

NATS → realtime gateway → WebSocket/SSE → typed client state.

Backpressure، reconnect، ordering، idempotency و stale-state handling اجباری است.

---

## 23. Payments / Entitlements

چرخه:

`Checkout → Intent → Address/Invoice → Verify → Settle → Subscription → Entitlement → Activation → Expiry/Renewal → Reconciliation`

تمام عملیات payment باید idempotent، auditable و قابل reconciliation باشند.

BTCPay Server و crypto payment ecosystem باید از نظر license، operational model، self-hosting و lifecycle audit شوند؛ انتخاب آن پیش‌فرض نیست.

---

## 24. Testing / Reliability

حداقل:

1. unit/domain
2. application/use-case
3. adapter contract
4. integration با infrastructure واقعی
5. event contract
6. PIT/replay
7. authorization/security
8. frontend/accessibility
9. E2E critical journeys
10. load/performance
11. property-based با Hypothesis
12. API contract با Schemathesis
13. browser با Playwright
14. load با k6/Locust
15. mutation/chaos در workloadهای مناسب

Architecture tests باید dependency direction و boundaryها را enforce کنند.

---

## 25. Observability

OpenTelemetry baseline است.

Trace باید در صورت امکان مسیر زیر را قابل مشاهده کند:

`request → use case → domain → persistence/event → consumer → analysis → decision → risk → outcome`

برای Elyrava:

`candidate → research/context → sandbox → verification → promotion → health guard`

Logs، metrics، traces، profiling، SLO، alerting و AI cost telemetry باید correlation و provenance مناسب داشته باشند.

---

## 26. Deployment Profiles

### Profile A — Development / محدود
یک deployment ساده با API، worker، web و زیرساخت حداقلی.

### Profile B — Single-node production
تفکیک processها، persistence durable، backup، monitoring و health gates.

### Profile C — Scaled production
Horizontal API/workers، partitioning، ClickHouse scaling، event-stream partitioning، object storage و workload isolation.

### Profile D — Global
Region-aware routing، data residency policy، regional workers، disaster recovery و SLOهای منطقه‌ای؛ فقط زمانی که workload واقعی توجیه کند.

Microservice extraction فقط با evidence برای scale/fault/security/team ownership انجام می‌شود.

---

## 27. Anti-sprawl

ممنوع:

- چند vector DB بدون workload مشخص
- چند graph DB همزمان
- چند agent framework در runtime بدون boundary
- چند workflow engine
- چند event broker
- چند auth provider عملیاتی
- datastoreهای redundant
- service فقط برای «تمیزتر شدن diagram»
- dependency صرفاً به خاطر popularity

هر capability باید یک owner، یک canonical contract و یک operational reason داشته باشد.

---

## 28. Release Gates

### Architecture Gate
Boundary، dependency direction، contracts و ADRها معتبر باشند.

### Functional Gate
Capability و regression tests کامل باشند.

### Security Gate
AuthN/AuthZ، secrets، supply chain، SBOM، scanning و threat controls پاس شوند.

### Performance Gate
Latency، throughput، memory، CPU، startup، query cost و frontend budgets پاس شوند.

### Data Gate
PIT، lineage، revision، quality و reproducibility پاس شوند.

### AI Gate
Evaluation، groundedness، citation، calibration، drift و policy checks پاس شوند.

### Licensing Gate
License و transitive dependency compatibility تأیید شده باشد.

### Migration Gate
Backward compatibility، reconciliation، rollback و evidence ثبت شده باشد.

### Operational Gate
Health/readiness، backup/restore، observability و runbook آماده باشد.

---

## 29. ADR و Decision Freeze

هر تصمیمی که runtime، contract، data ownership، license، security boundary یا operational topology را تغییر دهد، ADR لازم دارد.

Decision freeze زمانی فعال است که:

- capability catalog ممیزی شده باشد؛
- alternatives اصلی بررسی شده باشند؛
- benchmark evidence ثبت شده باشد؛
- contract و boundary تثبیت شده باشند؛
- gates تعریف شده باشند.

پس از freeze، تغییر فقط با ADR جدید و impact analysis انجام می‌شود.

---

## 30. Graphهای مرجع

سه graph مستقل باید نگهداری شوند:

### Architecture Dependency Graph
چه component/contextی به چه contract یا infrastructure متکی است.

### Capability Dependency Graph
برای هر capability، prerequisites و downstream consumers چیست.

### CFIP ↔ OSS Boundary Graph
هر OSS دقیقاً پشت کدام port/adapter قرار دارد و آیا runtime dependency، optional dependency، benchmark یا reference است.

---

## 31. قراردادهای Canonical

حداقل contractهای موردنیاز:

`MarketDataProvider`  
`EconomicDataProvider`  
`NewsProvider`  
`SearchProvider`  
`Retriever`  
`Reranker`  
`WebAcquisitionPort`  
`DocumentParser`  
`OCRProvider`  
`EvidenceStore`  
`KnowledgeGraphPort`  
`MemoryProvider`  
`ModelProvider`  
`AgentRuntime`  
`ToolRegistry`  
`ResearchPlanner`  
`ResearchExecutor`  
`SignalEngine`  
`ConsensusService`  
`RiskEngine`  
`OrderGateway`  
`ExecutionGateway`  
`BacktestEngine`  
`ReplayEngine`  
`EvaluationProvider`  
`FeatureStore`  
`WorkflowPort`  
`IdentityProvider`  
`AuthorizationProvider`  
`PaymentProvider`  
`NotificationProvider`

این contractها از implementation مستقل هستند.

---

## 32. Adoption Lifecycle

```text
DISCOVERED
   ↓
SHORTLISTED
   ↓
AUDITED
   ↓
BENCHMARKED
   ↓
CFIP-FIT REVIEW
   ↓
DECISION
   ├── REFERENCE
   ├── EVALUATE
   ├── BENCHMARK
   ├── INTEGRATE
   ├── ADAPT
   ├── FORK
   ├── BUILD
   └── REJECT
   ↓
PILOT
   ↓
PRODUCTION
   ↓
CONTINUOUS REVIEW
```

وضعیت upstream، license، security و compatibility باید در releaseهای بعدی دوباره ارزیابی شود.

---

## 33. Baseline repository

CForex منبع رفتاری و مهاجرتی است؛ CFIP مقصد معماری جدید است. `cforex-platform` مقصد معماری محسوب نمی‌شود.

هیچ بخش CForex صرفاً به‌صورت filename migration منتقل نمی‌شود؛ مسیر صحیح:

`CForex implementation → behavioral evidence → domain contract → CFIP capability → port → adapter → verification`

---

## 34. اصل نهایی

CFIP نباید یک انبار سرویس‌های OSS باشد.

مدل صحیح:

```text
                 CFIP DOMAIN / IP
                        │
                CFIP CONTRACTS
                        │
              CAPABILITY BOUNDARY
                 /       |       \
                /        |        \
             OSS-A     OSS-B     CFIP-BUILD
                \        |        /
                 \       |       /
                   ADAPTERS
                       │
                   RUNTIME
```

**هر dependency باید دلیلی داشته باشد. هر capability باید owner داشته باشد. هر تصمیم باید evidence داشته باشد. هر تغییر معماری باید قابل بازبینی و rollback باشد.**
