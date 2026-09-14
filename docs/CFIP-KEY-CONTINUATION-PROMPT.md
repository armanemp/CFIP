# CFIP Key Continuation Prompt

This is the **short chat-level entrypoint**. It intentionally contains no duplicate operating contract. Its only job is to direct the next session to the authoritative prompt inside the repository.

## Copy/paste prompt

> ادامه پروژه **CForex → CFIP** را مستقیماً از وضعیت فعلی GitHub ادامه بده. ابتدا HEAD هر دو repo (`armanemp/CForex` و `armanemp/CFIP`) را بررسی کن، سپس **حتماً `docs/CFIP-KEY-CONTINUATION-PROMPT.md` و بعد `docs/CFIP-CONTINUATION-PROMPT.md` را از GitHub بخوان و کل قرارداد داخل آن را اجرا کن**. CForex منبع رفتاری و CFIP مقصد است؛ `cforex-platform`/Laravel کنار گذاشته شده؛ Gate 0 باز و CFIP runtime برابر `0% / LOCKED` است. هم‌زمان source study و evidence closure را با engineering واقعی پیش ببر: API/WS، events، data/PIT/replay، engines، workers/realtime، frontend، tests، policy/config، adapters، security، observability، AI/governance، performance و **global-scale architecture از همین الان**. برای مقیاس جهانی از ابتدا stateless regional APIs، partition/ownership/checkpoint semantics، multi-region/data-residency boundaries، workload isolation، retention/partitioning، bounded caches، backpressure، capacity/SLO، DR/rollback و cost-aware scaling را به‌عنوان معماری و evidence requirement در نظر بگیر؛ هیچ ادعای scale را صرفاً از روی directory یا configuration قبول نکن. هر نقص واقعی، contradiction، hardcode، dependency-direction problem، duplicate file/migration، test/CI failure یا architectural weakness را ریشه‌ای بررسی و در صورت مجاز بودن مستقیماً روی GitHub اصلاح کن؛ گزارش‌نویسی جای engineering را نگیرد و runtime business implementation قبل از Gate 0 انجام نشود. از evidence اجرایی و منابع رسمی/به‌روز استفاده کن، هیچ parity/readiness/absence/scale claim را بدون evidence نکن، documentation را هر بار با repository reality reconcile کن، و در پایان exact HEADها، تغییرات واقعی و commitها، verification/CI، موارد unverified، جدول پیشرفت کلی، جدول D1–D11، blockers/evidence gaps، next parallel tracks، Gate 0 و runtime status را دقیق گزارش بده.

## Rule

If this pointer conflicts with another chat prompt, **this repository contract wins**: read and follow `docs/CFIP-CONTINUATION-PROMPT.md`.
