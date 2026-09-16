const page=document.body.dataset.page||location.pathname.split('/').pop().replace('.html','')||'index';
const labels={
index:['مرجع نهایی CFIP','Composable Platform؛ مالکیت Domain/Contract/Core IP در CFIP و implementation capability در OSS'],
matrix:['ماتریس تصمیم‌گیری OSS','Capability → candidate → evidence → adoption decision'],
projects:['کاتالوگ OSS','کاتالوگ repositoryها، نقش، license، تناسب و ریسک'],
graph:['گراف معماری','Dependency Graph + Capability Graph + CFIP ↔ OSS Boundary'],
contracts:['Canonical Contracts','Ports، Domain Contracts و Event Contracts'],
adoption:['چرخه پذیرش OSS','Discover → Audit → Benchmark → Decision → Pilot → Production'],
deployment:['Deployment Profiles','Development محدود تا production مقیاس‌پذیر'],
governance:['Governance','ADR، decision freeze، policy-as-code و approval gates'],
domains:['۳۰ حوزه مادر','Master scope و 400+ capability عملیاتی'],
research:['Research Intelligence Fabric','Deep Research، acquisition، retrieval، evidence و verification'],
trading:['Trading / Quant Core','Market data، structure، signal، backtest، risk و execution'],
ai:['Elyrava / AI','Agent، model، memory، tool، planning و governed autonomy'],
data:['Data Platform','OLTP، analytics، object storage، embedded analytics و interchange'],
security:['Security / Identity','AuthN/AuthZ، secrets، supply chain، sandbox و policy'],
observability:['Observability','OpenTelemetry، logs، metrics، traces، SLO و AI telemetry'],
frontend:['Terminal UX','Chart-first، realtime، accessibility، i18n و RTL/LTR'],
payments:['Payments / Entitlements','Crypto subscription، settlement، reconciliation و entitlement'],
testing:['Testing / Reliability','Unit، property، contract، E2E، load، security و simulation'],
autonomy:['Autonomous Elyrava','Research → sandbox → benchmark → gate → promotion → rollback'],
'architecture-decisions':['Architecture Decision Records','تصمیم‌های frozen و قواعد تغییر معماری']
};
const details={
research:['Research Planner','Query Decomposition','Search / Retrieval','Web Acquisition','Document Intelligence','Evidence & Provenance','Claim Verification','Contradiction Analysis','Citation Validation','Freshness / Trust','Research Memory','Reproducibility'],
trading:['Canonical Market Data','Technical Analysis','Market Structure','Liquidity','FVG / Order Blocks','MTF','Signal Engines','Consensus','Backtest / Replay','Risk / Position Sizing','Execution Boundary','Reconciliation','Outcome Attribution'],
ai:['Elyrava Core','Agent Contract','Model Contract','Tool Contract','Memory Contract','Research Contract','Model Routing','Structured Output','Cost Governance','Evaluation','Calibration','Drift','Approval / Promotion'],
data:['PostgreSQL: system of record','ClickHouse: analytical workloads','Redis: bounded cache/ephemeral state','Object Storage: immutable artifacts','DuckDB: local/research analytics','Arrow/Parquet: interchange','Feature/Data Lineage','Dataset Versioning'],
security:['OIDC/OAuth','RBAC / ABAC','OpenFGA / OPA boundary','Secrets isolation','SBOM','SAST','Dependency/container scanning','SSRF controls','Prompt-injection controls','Agent sandbox','Audit trail','Policy-as-code'],
observability:['OpenTelemetry','Metrics','Logs','Traces','Profiling','SLO/SLA evidence','Alerting','LLM/agent telemetry','Cost observability','Correlation across request→decision→outcome'],
frontend:['Next.js + React + TypeScript','Tailwind','TradingView Lightweight Charts adapter','Chart semantics owned by CFIP','WebSocket/SSE','Command palette','Drawing/overlay model','Responsive terminal','PWA','Accessibility','i18n','RTL/LTR'],
payments:['Free/Pro plans','Entitlement model','Checkout','Payment intent','Verification','Settlement','Webhook idempotency','Reconciliation','Expiry/Renewal','Refund','Audit','BTCPay evaluation'],
testing:['pytest','Hypothesis','Schemathesis','Playwright','k6/Locust','Contract tests','Property tests','E2E critical journeys','PIT/replay tests','Financial simulation tests','Security tests','Chaos/soak tests'],
autonomy:['Observe','Research','Propose','Risk classify','Checkpoint','Isolated sandbox','Independent verification','Benchmark','Release gates','Human approval when required','Promotion','Health guard','Rollback'],
};
async function loadJSON(name){try{const r=await fetch(`data/${name}.json`);return await r.json();}catch(e){return null;}}
function section(title,html){const s=document.createElement('section');s.innerHTML=`<h2>${title}</h2>${html}`;document.querySelector('main')?.appendChild(s);}
function list(items){return `<ul>${items.map(x=>`<li>${x}</li>`).join('')}</ul>`;}
function table(headers,rows){return `<div class="table-wrap"><table><thead><tr>${headers.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;}
async function render(){
 document.documentElement.lang='fa';document.documentElement.dir='rtl';
 const [domains,projects,contracts,architecture,decisions,gates,capabilities]=await Promise.all(['domains','projects','contracts','architecture','decisions','gates','capabilities'].map(loadJSON));
 const l=labels[page]||labels.index; document.title=`${l[0]} — CFIP`;
 section(l[0],`<p class="lead">${l[1]}</p>`);
 if(details[page]) section('قابلیت‌های مرجع',list(details[page]));
 if(page==='domains'&&domains) section('Scope مرجع',domains.domains.map(d=>`<article class="card"><h3>${d.id} — ${d.name}</h3>${list(d.capabilities)}</article>`).join(''));
 if(page==='projects'&&projects) section('OSS Shortlist',table(['پروژه','حوزه','نقش','License','Fit / وضعیت'],projects.projects.map(p=>[`<a href="${p.url}" target="_blank" rel="noreferrer">${p.name}</a>`,p.domains.join(', '),p.roles.join(', '),p.license||'—',`${p.fit||'—'} · ${p.status||''}`])));
 if(page==='matrix'&&projects&&capabilities) section('Decision Matrix',table(['Project','Role','Domains','License','Status'],projects.projects.map(p=>[p.name,p.roles.join(' / '),p.domains.join(', '),p.license||'—',p.status||'candidate'])));
 if(page==='contracts'&&contracts){section('Canonical Ports',list(contracts.ports.map(p=>`<strong>${p.name}</strong> — ${p.purpose}`)));section('Core Domain Contracts',list(contracts.core_domain_contracts));section('Event Envelope',`<pre>${contracts.event_envelope.join('\n')}</pre>`);section('Contract Rules',list(contracts.contract_rules));}
 if(page==='graph'&&architecture){section('Layer Graph',`<pre>Experience → API/BFF → Elyrava Core → CFIP Contracts → Capability Fabric → Data/Event Plane → Observability/Governance → Elyrava Lab</pre>`);section('Boundaries',`<p>${architecture.oss_boundary}</p><pre>${JSON.stringify(architecture.anti_sprawl,null,2)}</pre>`);}
 if(page==='architecture-decisions'&&decisions) section('ADR Registry',table(['ID','عنوان','وضعیت','تصمیم'],decisions.decisions.map(d=>[d.id,d.title,d.status,d.decision])));
 if(page==='governance'&&decisions&&gates){section('Decision Freeze',`<p>${decisions.decision_freeze}</p>`);section('Promotion Flow',`<pre>${gates.promotion_flow.join(' → ')}</pre>`);section('Risk Classes',list(Object.entries(gates.risk_classes).map(([k,v])=>`<strong>${k}</strong>: ${v}`)));}
 if(page==='adoption'&&projects){section('Adoption Lifecycle',`<pre>Discover → Deduplicate → Classify → Technical Audit → Security/License Audit → Benchmark → CFIP Fit → Decision → Pilot → Production</pre>`);section('Decision Ladder',`<pre>Use upstream → Adapter → Extension → Patch upstream → Fork → Build ourselves</pre>`);section('Mandatory evidence',list(['functional fit','maturity/activity','license/transitive license','security','Python compatibility','performance/scalability','self-hosting/data ownership','lock-in','API/extensibility','resource cost','documentation/tests','migration risk','CFIP fit']));}
 if(page==='deployment') section('Profiles',table(['Profile','Characteristics','Allowed complexity'],[['Developer / 8GB RAM','Compose + modular monolith + PostgreSQL/Redis/NATS','Minimal'],['Research Lab','Add ClickHouse/Object Storage/DuckDB and evaluation workers','Moderate'],['Production Single Region','Horizontally scaled API/workers, durable backups, OTel, health guards','High'],['Production Multi-Region','Region-aware data/event topology, residency and DR','Only with evidence']])));
 if(page==='index') section('Architecture Law',list(['CFIP owns domain and canonical contracts.','OSS implementations terminate at adapters.','No runtime dependency by popularity.','One production implementation per capability unless ADR.','Fork is last resort.','Research and autonomy cannot bypass governance.','PIT/provenance/reproducibility are mandatory.']));
 if(page==='research') section('Reference Pipeline',`<pre>Question → Research Plan → Query Decomposition → Search → Acquisition → Retrieval → Extraction → Evidence → Verification → Contradiction → Synthesis → Citation Validation → Confidence → Reproducible Answer</pre>`);
 if(page==='trading') section('Reference Pipeline',`<pre>Market Data → Normalize → Validate → Deduplicate → Event-Time → Quality → Canonical → Features/Structure → Evidence → Consensus → Decision → Risk → Order Intent → Execution → Reconciliation → Outcome</pre>`);
 if(page==='ai') section('Elyrava boundary',`<pre>Elyrava
 ├─ Agent Contract
 ├─ Model Contract
 ├─ Tool Contract
 ├─ Memory Contract
 └─ Research Contract
       ↓
 adapters: LangGraph / Haystack / PydanticAI / future implementations</pre>`);
 if(page==='autonomy') section('Governed Autonomy',`<pre>Observe → Research → Propose → Classify → Checkpoint → Sandbox → Verify → Benchmark → Gates → Approval* → Promote → Health Guard → Rollback
* approval depends on risk class</pre>`);
 if(page==='testing') section('Release rule',`<p>هر capability مهم باید domain/application/adapter/integration/contract/E2E/performance/security tests مناسب خود را داشته باشد. failure در gate اجباری promotion را متوقف می‌کند.</p>`);
 if(page==='security') section('Security rule',`<p>هیچ agent، UI یا domain مستقیماً به database، broker یا vendor SDK دسترسی ندارد. secrets، authorization، tool permissions و governance paths باید از runtime agent مستقل و قابل audit باشند.</p>`);
 if(page==='observability') section('Trace model',`<pre>request → use case → domain → persistence/event → consumer → analysis → consensus → risk → execution → outcome</pre>`);
 if(page==='frontend') section('UX law',`<p>CFIP یک chart-first terminal است، نه dashboard معمولی. Intelligence و drawing semantics به renderer قفل نمی‌شوند.</p>`);
 if(page==='payments') section('Payment state machine',`<pre>Checkout → Intent → Address/Invoice → Verify → Settle → Subscription → Entitlement → Activation → Expiry/Renewal → Reconciliation</pre>`);
 if(page==='data') section('Data ownership',`<ul><li>PostgreSQL: authoritative transactional state</li><li>ClickHouse: analytical/time-series workloads</li><li>Redis: cache/ephemeral state</li><li>Object Storage: immutable artifacts</li><li>DuckDB: local/research analytics</li><li>Arrow/Parquet: interchange</li></ul>`);
 if(page==='deployment') section('Anti-sprawl',list(['No redundant datastore','No redundant broker','No competing workflow engines','No competing search/vector engines without benchmark','No service extraction without measurable justification']));
 if(page==='matrix'||page==='projects') section('قانون وضعیت',`<p>candidate/benchmark/reference به معنی «وارد production شده» نیست. adoption نهایی فقط بعد از عبور از OSS Adoption Gate معتبر است.</p>`);
}
render();
