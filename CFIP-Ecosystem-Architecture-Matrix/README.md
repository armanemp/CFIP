# CFIP Ecosystem Architecture Matrix

## مرجع تصمیم‌گیری معماری CFIP

این مجموعه مرجع ماشین‌خوان و انسانی معماری CFIP است. هدف آن انتخاب کورکورانه ابزار نیست؛ هدف، ساخت یک پلتفرم Composable است که در آن **Domain، Contract، Governance و Intelligence اختصاصی متعلق به CFIP** و capabilityهای عمومی تا حد امکان از OSS mature تأمین شوند.

### Scope

Baseline شامل 30 حوزه مادر و بیش از 400 capability عملیاتی است. کاتالوگ OSS هر پروژه را با نقش BUILD/INTEGRATE/ADAPT/EVALUATE/BENCHMARK/REFERENCE/FORK/REJECT و شواهد تصمیم ثبت می‌کند.

### اصول

1. هیچ OSS صرفاً به دلیل محبوبیت وارد runtime نمی‌شود.
2. Fork آخرین انتخاب است.
3. چند implementation رقیب برای یک capability بدون ADR وارد production نمی‌شوند.
4. CFIP مالک canonical contracts است.
5. Providerها از Domain جدا و پشت port/adapter قرار می‌گیرند.
6. Evidence، provenance، PIT، calibration و governance جزو Core IP هستند.
7. microservice، datastore، broker و framework جدید فقط با evidence وارد می‌شوند.

### ساختار

- `index.html`: نمای مادر
- `matrix.html`: ماتریس capability و OSS
- `projects.html`: کاتالوگ پروژه‌ها
- `graph.html`: graphهای معماری
- `contracts.html`: canonical ports/events
- `adoption.html`: lifecycle انتخاب OSS
- `deployment.html`: deployment profiles
- `governance.html`: governance و decision freeze
- `domains.html`: 30 حوزه مادر
- صفحات تخصصی: research/trading/ai/data/security/observability/frontend/payments/testing/autonomy
- `data/*.json`: source of truth ماشین‌خوان

این مجموعه جایگزین کتاب معماری قبلی است و باید همراه با ADRهای جدید نگهداری شود.
