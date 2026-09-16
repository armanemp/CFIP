# CHANGELOG

## 2026-09-16 — Final Composable Architecture + OSS Audit Baseline

### Architecture
- مرجع قبلی از حالت کتاب معماری مستقل خارج و با مرجع Composable Platform جایگزین شد.
- Scope روی 30 حوزه مادر و بیش از 400 capability/subdomain تثبیت شد.
- CFIP به‌عنوان مالک Domain، Core IP، Contracts و Governance تعریف شد.
- OSS به‌عنوان implementation capability پشت adapter تعریف شد.
- Modular Monolith First و استخراج سرویس فقط با evidence تثبیت شد.

### OSS Ecosystem
- catalog از نمونه اولیه به ecosystem catalog گسترده ارتقا یافت.
- نقش‌های BUILD/INTEGRATE/ADAPT/EVALUATE/BENCHMARK/REFERENCE/FORK/REJECT تعریف شدند.
- معیارهای functional fit، maturity، activity، license، security، Python compatibility، performance، scalability، self-hosting، lock-in، resource cost، tests، docs و migration risk ثبت شدند.
- پروژه‌های trading، market data، agent، research، search، crawling، document intelligence، graph/memory، ML/MLOps، data، streaming، workflow، evaluation، observability، security، autonomy، frontend، payments، testing و infrastructure کاتالوگ شدند.
- پروژه‌هایی که license یا maturity آنها نیازمند بررسی بیشتر است عمداً dependency قطعی اعلام نشده‌اند.

### Contracts
- canonical ports ثبت و مالک آنها CFIP مشخص شد.
- Evidence/Claim/Source/Research/Signal/Consensus/Risk/Order/Outcome/Dataset/Model/Proposal/Promotion contracts به‌عنوان domain contracts ثبت شدند.
- canonical event envelope و قواعد versioning/idempotency/outbox/order/retry/quarantine ثبت شدند.

### Governance
- 18 ADR پایه ثبت شد.
- decision freeze rule تعریف شد.
- Fork Last و Popularity Is Not Evidence به‌صورت تصمیم معماری ثبت شدند.
- Graph DB، Search Stack، Workflow Engine و Trading Engine به‌عنوان تصمیم‌های benchmark-driven تعریف شدند.

### Gates
- Architecture
- Functional
- Security
- Performance
- Data/PIT
- AI/Evaluation
- Licensing
- Migration
- Operations
- OSS Adoption

همه به‌عنوان release/adoption gates ثبت شدند.

### Autonomy / Elyrava
- proposal → classification → checkpoint → sandbox → verification → gates → approval → promotion → health guard → rollback تثبیت شد.
- Elyrava framework-neutral باقی ماند.

### Evidence policy
این baseline ادعا نمی‌کند تک‌تک repositoryهای GitHub بررسی شده‌اند. حوزه‌ها به‌صورت ecosystem-level پوشش داده شده‌اند و shortlist/evidence audit برای نامزدها ثبت می‌شود. موارد فاقد evidence کافی در وضعیت candidate/benchmark/reference باقی می‌مانند.

## Previous baseline
نسخه‌های قبلی این مجموعه صرفاً به‌عنوان تاریخچه Git حفظ شده‌اند؛ محتوای فعلی مرجع معماری فعال است.
