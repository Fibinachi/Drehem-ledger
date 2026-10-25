/* Ur III Ledger — QuickBooks-style front end. Static, no backend. */
"use strict";
/* Archive metadata (data/meta.js). Defaults describe Drehem so the app still
   works if meta.js is absent. */
const META = Object.assign({
  archive:"drehem", title:"Puzriš-Dagan (Drehem)", short:"Drehem",
  sub:"the livestock clearinghouse of the Ur III state",
  totalTxns:59574, txnPath:"data/txn",
  validated:true, hasEntities:true, hasAging:true,
  unitWord:"head", qtyPhrase:"head of livestock",
  presetAllLabel:"All years (Šulgi 26 – Ibbi-Suen 4)", banner:null,
}, (typeof QB_META !== "undefined" ? QB_META : {}));
const $ = s => document.querySelector(s);
const fmt = n => (n==null||isNaN(n)) ? "—" : Math.round(n).toLocaleString("en-US");
const esc = s => String(s==null?"":s).replace(/[&<>"]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const sux = s => `<span class="sux">${esc(s)}</span>`;

const KINGS = {"Šulgi":[1,48],"Amar-Suen":[49,57],"Shu-Suen":[58,66],"Ibbi-Suen":[67,70]};
const PRESETS = {
  all:{label:"All years (Šulgi 26 – Ibbi-Suen 4)", from:1, to:70},
  shulgi:{label:"Šulgi", from:1, to:48},
  amar:{label:"Amar-Suen", from:49, to:57},
  shusuen:{label:"Shu-Suen", from:58, to:66},
  ibbi:{label:"Ibbi-Suen", from:67, to:70},
};
PRESETS.all.label = META.presetAllLabel;
/* Provincial archives run past Ibbi-Suen 4 (abs 70); widen the range if needed. */
if(typeof QB_SUMMARY !== "undefined" && QB_SUMMARY.absMax > 70){
  PRESETS.all.to = QB_SUMMARY.absMax;
  PRESETS.ibbi.to = QB_SUMMARY.absMax;
  PRESETS.ibbi.label = "Ibbi-Suen";
}
const state = {
  preset:"all", commodity:"", entity:"", txnType:"",
  txns:null, chunksLoaded:0, regPage:0, glCode:null,
};
const COMM_OPTS = QB_ACCOUNTS.map(a=>`<option value="${esc(a.code)}">${esc(a.code)} — ${esc(a.name)}</option>`).join("");

/* ---------- filter bar ---------- */
function filterBar(opts){
  opts = opts || {};
  return `<div class="filters">
    <div><label>Date range</label><select id="fPreset" onchange="setPreset(this.value)">
      ${Object.entries(PRESETS).map(([k,v])=>`<option value="${k}"${state.preset===k?" selected":""}>${esc(v.label)}</option>`).join("")}
    </select></div>
    ${opts.commodity===false?"":`<div><label>Account</label><select id="fComm" onchange="setComm(this.value)">
      <option value="">All accounts</option>${COMM_OPTS}</select></div>`}
    ${(opts.entity===false||!META.hasEntities)?"":`<div><label>Official / counterparty</label>
      <input id="fEntity" list="entList" placeholder="e.g. ab-ba-sa-ga" value="${esc(state.entity)}" onchange="setEntity(this.value)"></div>`}
    ${opts.type===false?"":`<div><label>Type</label><select id="fType" onchange="setType(this.value)">
      <option value="">All types</option>
      <option value="receipt"${state.txnType==="receipt"?" selected":""}>Receipt (šu ba-ti)</option>
      <option value="disbursement"${state.txnType==="disbursement"?" selected":""}>Disbursement (zi-ga)</option>
      <option value="transfer"${state.txnType==="transfer"?" selected":""}>Transfer</option>
    </select></div>`}
    <div><label>&nbsp;</label><button class="btn ghost" onclick="clearFilters()">Reset</button></div>
  </div>${META.hasEntities?`<datalist id="entList">${QB_ENTITIES.slice(0,120).map(e=>`<option value="${esc(e.name)}">`).join("")}</datalist>`:""}`;
}
function setPreset(v){state.preset=v;state.regPage=0;route();}
function setComm(v){state.commodity=v;state.regPage=0;
  const el=$("#fComm"); /* keep select in sync after rerender via state */ route();}
function setEntity(v){state.entity=v;state.regPage=0;route();}
function setType(v){state.txnType=v;state.regPage=0;route();}
function clearFilters(){state.preset="all";state.commodity="";state.entity="";state.txnType="";state.regPage=0;route();}
function range(){const p=PRESETS[state.preset];return [p.from,p.to];}
function inRange(abs){ if(abs==null) return state.preset==="all"; const [a,b]=range(); return abs>=a&&abs<=b; }
function matchTxn(t){
  // t = [id,pn,king,year,abs,from,to,commodity,qty,type]
  if(!inRange(t[4])) return false;
  if(state.commodity && t[7]!==state.commodity) return false;
  if(state.txnType && t[9]!==state.txnType) return false;
  if(state.entity){const q=state.entity.toLowerCase();
    if(!((t[5]||"").toLowerCase().includes(q)||(t[6]||"").toLowerCase().includes(q))) return false;}
  return true;
}
function syncFilterInputs(){
  const c=$("#fComm"); if(c) c.value=state.commodity;
}

/* ---------- lazy transaction loading (works on file:// via script tags) ---------- */
function ensureTxns(cb){
  if(state.txns){cb();return;}
  state.txns=[];
  const box=$("#content");
  box.innerHTML=`<div class="loading"><h3>Opening the tablet room…</h3>
    <p>Loading ${fmt(META.totalTxns)} transactions from the ${esc(META.short)} archive.</p>
    <div class="progress"><div id="lp"></div></div><p id="lt"></p></div>`;
  let i=0;
  (function next(){
    if(i>=QB_CHUNKS){cb();return;}
    const s=document.createElement("script");
    s.src=`${META.txnPath}/chunk_${String(i).padStart(2,"0")}.js`;
    s.onload=()=>{state.txns.push(...window[`TXN_CHUNK_${String(i).padStart(2,"0")}`]);
      i++;const p=$("#lp"),t=$("#lt");
      if(p)p.style.width=Math.round(100*i/QB_CHUNKS)+"%";
      if(t)t.textContent=`${fmt(state.txns.length)} of ${fmt(META.totalTxns)} loaded`;
      next();};
    s.onerror=()=>{i++;next();};
    document.head.appendChild(s);
  })();
}

/* ---------- router ---------- */
const TITLES={"dashboard":"Dashboard","chart-of-accounts":"Chart of Accounts","profit-loss":"Profit & Loss",
 "balance-sheet":"Balance Sheet","trial-balance":"Trial Balance","general-ledger":"General Ledger",
 "cash-flow":"Cash Flow Statement","ar-aging":"A/R Aging — Amounts Due from Officials",
 "ap-aging":"A/P Aging — Amounts Owed","register":"Transaction Register","audit":"Auditor's Attestation"};
function route(){
  const h=(location.hash||"#/dashboard").replace("#/","");
  const [r,arg]=h.split("/");
  document.querySelectorAll(".nav a").forEach(a=>a.classList.toggle("active",a.dataset.r===r));
  $("#viewTitle").textContent=TITLES[r]||"Dashboard";
  const V={dashboard:vDashboard,"chart-of-accounts":vAccounts,"profit-loss":vPL,"balance-sheet":vBS,
    "trial-balance":vTB,"general-ledger":()=>vGL(arg),"cash-flow":vCF,"ar-aging":vAR,"ap-aging":vAP,
    "register":vRegister,"audit":vAudit}[r]||vDashboard;
  V(); syncFilterInputs();
  /* Data-quality banner on every view of a provisional archive. */
  if(META.banner){
    $("#content").insertAdjacentHTML("afterbegin",
      `<div class="note warn" style="margin-bottom:14px">⚠ <b>Provisional data.</b> ${esc(META.banner)}</div>`);
  }
}
window.addEventListener("hashchange",route);

/* ================= DASHBOARD ================= */
/* Per-unit receipt/disbursement cards for archives with mixed units. */
function unitCards(s){
  return (s.byUnit||[]).slice(0,4).map(u=>`
    <div class="card"><div class="lbl">Received / disbursed <span style="color:var(--muted)">(${esc(u.unitLabel)})</span></div>
      <div class="val"><span class="green">${fmt(u.receipts)}</span><span style="color:var(--muted)"> / </span><span class="red">${fmt(u.disbursements)}</span></div>
      <div class="sub">${esc(u.unit)} · receipts / disbursements</div></div>`).join("");
}
function vDashboard(){
  const s=QB_SUMMARY;
  const rows=QB_PL;
  const maxQ=Math.max(1,...rows.map(r=>Math.max(r.income,r.expense)));
  const step=Math.ceil(rows.length/14);
  let bars="";
  for(let i=0;i<rows.length;i+=step){
    const r=rows[i];
    bars+=`<div class="g"><div class="pair">
      <div class="b in" style="height:${Math.max(2,110*r.income/maxQ)}px" title="In: ${fmt(r.income)}"></div>
      <div class="b out" style="height:${Math.max(2,110*r.expense/maxQ)}px" title="Out: ${fmt(r.expense)}"></div>
      </div><div class="yl">${esc(r.king.slice(0,2))}${r.year}</div></div>`;
  }
  const qtyCards = META.validated ? `
    <div class="card"><div class="lbl">Livestock received</div><div class="val green">${fmt(s.receipts.qty)}</div><div class="sub">head · ${fmt(s.receipts.n)} receipts</div></div>
    <div class="card"><div class="lbl">Livestock disbursed</div><div class="val red">${fmt(s.disbursements.qty)}</div><div class="sub">head · ${fmt(s.disbursements.n)} disbursements</div></div>
    <div class="card"><div class="lbl">Unreconciled balance</div><div class="val red">${fmt(s.deficit)}</div><div class="sub">head · ${s.deficitPct}% of outflow — see Audit</div></div>`
    : unitCards(s);
  const topEnt=QB_ENTITIES.slice(0,8).map(e=>
    `<tr><td>${sux(e.name)}</td><td>${esc(e.type)}</td><td class="num">${fmt(e.n)}</td></tr>`).join("");
  const officialsPanel = META.hasEntities ? `
  <div class="panel"><h3>Most active officials</h3><p class="desc">Counterparties by number of attestations.</p>
    <table class="rep"><tr><th>Name</th><th>Type</th><th class="num">Attestations</th></tr>${topEnt}</table></div>` : "";
  const footnote = META.validated ? `
  <div class="note">All figures are first-pass parser output from CDLI transliterations and are subject to
  philological review. The 48.4% unreconciled balance is structural: sealed intake receipts were kept by the
  deliverer as proof of delivery (Widell 2020, <i>Orient</i> 55) — see the <a href="#/audit">Auditor's Attestation</a>.</div>`
  : `
  <div class="note">Commodity-level aggregates only. Quantities mix units (sila, sar, head, days) and cannot
  be summed across accounts; grain and area volumes are parser-normalized, not transcribed values.
  See the <a href="#/audit">Auditor's Attestation</a> for the full list of qualifications.</div>`;
  $("#content").innerHTML=`
  <h2 class="view-title">State finances at a glance</h2>
  <p class="view-sub">${esc(META.title)} · ${esc(META.sub)} · ${esc(s.rangeLabel)}</p>
  ${META.validated?`<div class="tagline">“The city of Ur kept better records than most modern nonprofits.”</div>`:""}
  <div class="cards">
    <div class="card"><div class="lbl">Tablets parsed</div><div class="val">${fmt(s.tablets)}</div><div class="sub">${s.datedPct}% carry regnal dates</div></div>
    <div class="card"><div class="lbl">Transactions</div><div class="val">${fmt(s.transactions)}</div><div class="sub">${META.hasEntities?fmt(s.entities)+" counterparties resolved":"commodity-level aggregates"}</div></div>
    ${qtyCards}
  </div>
  <div class="panel"><h3>Annual throughput — receipts vs disbursements (${esc(META.qtyPhrase)})</h3>
    <p class="desc">Every regnal year in the archive. Green = inflow ${sux("šu ba-ti")}, red = outflow ${sux("zi-ga")}.</p>
    <div class="bars">${bars}</div>
    <div class="legend"><span><span class="sw" style="background:var(--green)"></span>Receipts</span>
    <span><span class="sw" style="background:var(--red)"></span>Disbursements</span></div>
  </div>
  ${(() => {
    /* Charts, derived only from data already loaded for this view. No new data. */
    const reignOrder = ["Šulgi","Amar-Suen","Shu-Suen","Ibbi-Suen"];
    const reign = {};
    rows.forEach(r => { reign[r.king] = reign[r.king] || {in:0, out:0}; reign[r.king].in += r.income; reign[r.king].out += r.expense; });
    const reignMax = Math.max(1, ...reignOrder.map(k => Math.max((reign[k]||{in:0,out:0}).in, (reign[k]||{in:0,out:0}).out)));
    const reignRows = reignOrder.map(k => { const v = reign[k] || {in:0,out:0}; return `
      <div class="hbar-row"><div class="hl"><b>${esc(k)}</b></div><div>
        <div class="hbar-track" title="Receipts: ${fmt(v.in)}"><div class="hbar-fill in" style="width:${Math.max(1,100*v.in/reignMax)}%"></div></div>
        <div class="hbar-track" style="margin-top:3px" title="Disbursements: ${fmt(v.out)}"><div class="hbar-fill out" style="width:${Math.max(1,100*v.out/reignMax)}%"></div></div>
      </div><div class="hn">${fmt(v.in)} / ${fmt(v.out)}</div></div>`; }).join("");
    const topAccts = [...QB_ACCOUNTS].sort((a,b) => b.qty - a.qty).slice(0,8);
    const acctMax = Math.max(1, ...topAccts.map(a => a.qty));
    const acctRows = topAccts.map(a => `
      <div class="hbar-row"><div class="hl">${esc(a.name)} <span class="sux">(${esc(a.code)})</span></div>
      <div class="hbar-track" title="${fmt(a.qty)} ${esc(a.unitLabel||META.unitWord)} · ${fmt(a.txns)} transactions"><div class="hbar-fill blue" style="width:${Math.max(1,100*a.qty/acctMax)}%"></div></div>
      <div class="hn">${fmt(a.qty)}</div></div>`).join("");
    const tot = Math.max(1, s.receipts.qty + s.disbursements.qty + (s.transfers ? s.transfers.qty : 0));
    const share = (q, cls) => `<div class="hbar-row"><div class="hl">${esc(q.label)}</div>
      <div class="hbar-track" title="${fmt(q.qty)}"><div class="hbar-fill ${cls}" style="width:${Math.max(1,100*q.qty/tot)}%"></div></div>
      <div class="hn">${(100*q.qty/tot).toFixed(1)}%</div></div>`;
    return `
  <div class="charts-grid">
    <div class="panel"><h3>Throughput by reign</h3>
      <p class="desc">Receipts (green) and disbursements (red), summed from the annual Profit &amp; Loss rows. Head.</p>
      ${reignRows}
      <div class="legend"><span><span class="sw" style="background:var(--green)"></span>Receipts</span>
      <span><span class="sw" style="background:var(--red)"></span>Disbursements</span></div></div>
    <div class="panel"><h3>Largest accounts by lifetime volume</h3>
      <p class="desc">Top 8 accounts in the Chart of Accounts, by lifetime quantity. Head unless noted.</p>
      ${acctRows}</div>
  </div>
  <div class="panel"><h3>Where the volume went</h3>
    <p class="desc">Share of all recorded quantity, from the archive summary. The disbursement-heavy shape is the same structural gap noted in the Audit: sealed intake receipts were kept by the deliverer.</p>
    ${share({label:"Receipts", qty:s.receipts.qty}, "in")}
    ${share({label:"Disbursements", qty:s.disbursements.qty}, "out")}
    ${s.transfers ? share({label:"Transfers", qty:s.transfers.qty}, "amber") : ""}</div>`;
  })()}
  ${officialsPanel}
  ${footnote}`;
}

/* ================= CHART OF ACCOUNTS ================= */
function vAccounts(){
  const rows=QB_ACCOUNTS.map(a=>`<tr><td>${sux(a.code)}</td><td>${esc(a.name)}</td><td>${esc(a.type)}</td>
    <td>${esc(a.unitLabel||META.unitWord)}</td>
    <td class="num">${fmt(a.txns)}</td><td class="num">${fmt(a.qty)}</td>
    <td><a href="#/general-ledger/${esc(a.code)}">Open ledger →</a></td></tr>`).join("");
  const top=QB_ACCOUNTS[0]||{code:"—",name:"",qty:0,txns:0,unitLabel:""};
  $("#content").innerHTML=`
  <h2 class="view-title">Chart of Accounts</h2>
  <p class="view-sub">Every account in the books — ${QB_ACCOUNTS.length} accounts, Sumerian term with English gloss.</p>
  <div class="panel"><table class="rep"><tr><th>Code</th><th>Account name</th><th>Type</th><th>Unit</th>
    <th class="num">Transactions</th><th class="num">Lifetime volume</th><th></th></tr>${rows}</table></div>
  <div class="note">Account codes are the Sumerian commodity terms as they appear in the tablets.
  ${sux(top.code)} (${esc(top.name)}) alone accounts for ${fmt(top.qty)} ${esc(top.unitLabel||META.unitWord)} across ${fmt(top.txns)} transactions.</div>`;
}

/* ================= PROFIT & LOSS ================= */
function vPL(){
  const [a,b]=range();
  const rows=QB_PL.filter(r=>r.abs>=a&&r.abs<=b);
  let ti=0,te=0,tni=0,tne=0;
  const body=rows.map(r=>{ti+=r.income;te+=r.expense;tni+=r.incomeN;tne+=r.expenseN;
    const net=r.net, cls=net<0?" style='color:var(--red)'":"";
    return `<tr><td>${esc(r.king)} ${r.year}</td>
      <td class="num">${fmt(r.income)}</td><td class="num" style="color:var(--muted)">${fmt(r.incomeN)}</td>
      <td class="num">${fmt(r.expense)}</td><td class="num" style="color:var(--muted)">${fmt(r.expenseN)}</td>
      <td class="num"${cls}>${fmt(net)}</td></tr>`;}).join("");
  $("#content").innerHTML=`
  <h2 class="view-title">Profit &amp; Loss</h2>
  <p class="view-sub">${esc(PRESETS[state.preset].label)} · all quantities in ${esc(META.qtyPhrase)}</p>
  ${filterBar({commodity:false,entity:false,type:false})}
  <div class="panel"><table class="rep">
    <tr><th>Fiscal year</th><th class="num">Income — receipts ${sux("(šu ba-ti)")}</th><th class="num">No.</th>
    <th class="num">Expenses — disbursements ${sux("(zi-ga)")}</th><th class="num">No.</th><th class="num">Net</th></tr>
    <tr class="section"><td colspan="6">Ordinary activities</td></tr>${body}
    <tr class="total"><td>Total</td><td class="num">${fmt(ti)}</td><td class="num">${fmt(tni)}</td>
    <td class="num">${fmt(te)}</td><td class="num">${fmt(tne)}</td><td class="num" style="color:var(--red)">${fmt(ti-te)}</td></tr>
  </table></div>
  <div class="note">${META.validated
    ? `Internal ${sux("transfers")} between state offices are excluded from income and expenses, as in modern consolidated statements. The persistent negative net is the unreconciled intake balance — receipts whose sealed tablets were retained by the deliverers (see <a href="#/audit">Audit</a>), not an operating loss.`
    : `Internal transfers between offices are excluded from income and expenses, as in modern consolidated statements. Transactions without a type assignment and subtotal lines are excluded throughout. Quantities mix units and are not commensurable across accounts.`}</div>`;
}

/* ================= BALANCE SHEET ================= */
function vBS(){
  const [a,b]=range();
  const rows=QB_PL.filter(r=>r.abs<=b);
  let assets=0, out=0;
  rows.forEach(r=>{assets+=r.income;out+=r.expense;});
  const unrec=out-assets;
  const asof = META.validated
    ? (PRESETS[state.preset].label===META.presetAllLabel?"Ibbi-Suen 4 (end of archive)":PRESETS[state.preset].label)
    : (state.preset==="all" ? "end of archive" : PRESETS[state.preset].label);
  const lv = META.validated ? ["Livestock received", "Livestock disbursed"] : ["Received", "Disbursed"];
  $("#content").innerHTML=`
  <h2 class="view-title">Balance Sheet</h2>
  <p class="view-sub">As of ${esc(asof)} · ${esc(META.qtyPhrase)}</p>
  ${filterBar({commodity:false,entity:false,type:false})}
  <div class="panel"><table class="rep">
    <tr class="section"><td colspan="2">ASSETS</td></tr>
    <tr><td>${lv[0]} into state custody ${sux("(šu ba-ti)")}, cumulative</td><td class="num">${fmt(assets)}</td></tr>
    <tr class="section"><td colspan="2">OUTFLOWS</td></tr>
    <tr><td>${lv[1]} ${sux("(zi-ga)")}, cumulative</td><td class="num">${fmt(out)}</td></tr>
    <tr class="section"><td colspan="2">RECONCILIATION</td></tr>
    <tr><td>Unreconciled balance ${sux("(la2-ia3)")}</td><td class="num" style="color:var(--red)">${fmt(unrec)}</td></tr>
    <tr class="total"><td>Disbursed = Received + Unreconciled</td><td class="num">${fmt(out)} = ${fmt(assets)} + ${fmt(unrec)}</td></tr>
  </table></div>
  ${META.validated?`<div class="note warn"><b>Auditor's note:</b> the unreconciled balance does not indicate loss or malfeasance.
  Per Widell (2020, <i>Orient</i> 55:131), the official sealed the receipt tablet and the <i>deliverer kept it</i>
  as proof of delivery — so intake paperwork for roughly half the livestock never entered the Drehem archive.
  The books balance once document custody is accounted for.</div>`
  :`<div class="note warn"><b>Note:</b> quantities mix units and the parse is first-pass; balances here are
  indicative only. Unreconciled amounts combine unassigned-type transactions, clause-split duplicates,
  and genuine unreconciled flows — see <a href="#/audit">Audit</a>.</div>`}`;
}

/* ================= TRIAL BALANCE ================= */
function vTB(){
  const [a,b]=range();
  const agg={};
  QB_TB_YEAR.filter(r=>r.abs>=a&&r.abs<=b).forEach(r=>{
    agg[r.code]=agg[r.code]||{dr:0,cr:0};agg[r.code].dr+=r.dr;agg[r.code].cr+=r.cr;});
  let tdr=0,tcr=0;
  const body=Object.keys(agg).sort((x,y)=>agg[y].dr-agg[x].dr).map(c=>{
    const g=agg[c], bal=g.dr-g.cr; tdr+=g.dr;tcr+=g.cr;
    const nm=(QB_ACCOUNTS.find(x=>x.code===c)||{}).name||c;
    return `<tr><td>${sux(c)}</td><td>${esc(nm)}</td>
      <td class="num">${fmt(g.dr)}</td><td class="num">${fmt(g.cr)}</td>
      <td class="num"${bal<0?" style='color:var(--red)'":""}>${fmt(bal)}</td></tr>`;}).join("");
  $("#content").innerHTML=`
  <h2 class="view-title">Trial Balance</h2>
  <p class="view-sub">${esc(PRESETS[state.preset].label)} · debits = inflows, credits = outflows (${esc(META.qtyPhrase)})</p>
  ${filterBar({commodity:false,entity:false,type:false})}
  <div class="panel"><table class="rep">
    <tr><th>Account</th><th></th><th class="num">Debit</th><th class="num">Credit</th><th class="num">Balance</th></tr>
    ${body}
    <tr class="total"><td colspan="2">Totals</td><td class="num">${fmt(tdr)}</td><td class="num">${fmt(tcr)}</td><td class="num"></td></tr>
    <tr><td colspan="2"><i>Suspense — ${META.validated?"unreconciled intake (see Audit)":"unassigned &amp; unreconciled"}</i></td><td class="num"></td>
      <td class="num" style="color:var(--red)">${fmt(tcr-tdr)}</td><td class="num"></td></tr>
    <tr class="total"><td colspan="2">Agreed totals</td><td class="num">${fmt(tdr)}</td><td class="num">${fmt(tcr)}</td><td class="num"></td></tr>
  </table></div>
  <div class="note">${META.validated
    ? `A modern trial balance must agree; this one carries a suspense line equal to the unreconciled intake — the receipts retained by deliverers. That single line is the entire story of the archive's formation.`
    : `Debits and credits are shown per account (each account has a single unit). The suspense line collects unassigned-type transactions and unreconciled flows; with a first-pass parse it is not interpretable as a single economic quantity.`}</div>`;
}

/* ================= CASH FLOW ================= */
function vCF(){
  const [a,b]=range();
  const rows=QB_PL.filter(r=>r.abs>=a&&r.abs<=b);
  let cum=0;
  const body=rows.map(r=>{const net=r.income-r.expense;cum+=net;
    return `<tr><td>${esc(r.king)} ${r.year}</td><td class="num">${fmt(r.income)}</td>
      <td class="num">(${fmt(r.expense)})</td><td class="num"${net<0?" style='color:var(--red)'":""}>${fmt(net)}</td>
      <td class="num"${cum<0?" style='color:var(--red)'":""}>${fmt(cum)}</td></tr>`;}).join("");
  const ti=rows.reduce((x,r)=>x+r.income,0), te=rows.reduce((x,r)=>x+r.expense,0);
  $("#content").innerHTML=`
  <h2 class="view-title">Statement of Cash Flows</h2>
  <p class="view-sub">${esc(PRESETS[state.preset].label)} · “cash” = ${esc(META.validated?"livestock on the hoof (head)":META.qtyPhrase)}</p>
  ${filterBar({commodity:false,entity:false,type:false})}
  <div class="panel"><table class="rep">
    <tr class="section"><td colspan="5">OPERATING ACTIVITIES</td></tr>
    <tr><th>Fiscal year</th><th class="num">Inflows</th><th class="num">Outflows</th><th class="num">Net flow</th><th class="num">Cumulative</th></tr>
    ${body}
    <tr class="total"><td>Total</td><td class="num">${fmt(ti)}</td><td class="num">(${fmt(te)})</td>
      <td class="num" style="color:var(--red)">${fmt(ti-te)}</td><td class="num"></td></tr>
  </table></div>
  <div class="note">${META.validated
    ? `The state ran a structural “cash” deficit every year because intake documentation — not the livestock itself — left the building with the deliverers. Internal transfers net to zero and are excluded.`
    : `Flows mix units across accounts and the parse is first-pass; treat the statement as an index of activity, not a reconcilable cash position. Internal transfers net to zero and are excluded.`}</div>`;
}

/* ================= GENERAL LEDGER ================= */
function vGL(code){
  if(code) return vGLDetail(code);
  const [a,b]=range();
  const body=QB_GL.map(g=>{
    let q=0; g.byYear.forEach(y=>{if(y.abs>=a&&y.abs<=b)q+=y.q;});
    const maxY=Math.max(1,...g.byYear.map(y=>y.q));
    const spark=g.byYear.filter(y=>y.abs>=a&&y.abs<=b).slice(-24).map(y=>
      `<div class="b in" style="height:${Math.max(2,Math.round(28*y.q/maxY))}px;width:5px" title="${y.abs}: ${fmt(y.q)}"></div>`).join("");
    return `<tr><td>${sux(g.code)}</td><td>${esc(g.name)}</td>
      <td class="num">${fmt(g.txns)}</td><td class="num">${fmt(q)}</td>
      <td><div class="bars" style="height:34px"><div class="pair" style="height:30px">${spark}</div></div></td>
      <td><a href="#/general-ledger/${esc(g.code)}">Detail →</a></td></tr>`;}).join("");
  $("#content").innerHTML=`
  <h2 class="view-title">General Ledger</h2>
  <p class="view-sub">${esc(PRESETS[state.preset].label)} · click an account for history and transactions${META.hasEntities?" and counterparties":""}</p>
  ${filterBar({commodity:false,entity:false,type:false})}
  <div class="panel"><table class="rep"><tr><th>Account</th><th></th><th class="num">Txns (all-time)</th>
    <th class="num">Volume in range</th><th>Trend</th><th></th></tr>${body}</table></div>
  ${META.hasEntities?"":`<div class="note">Counterparty drill-down is disabled for this archive: the entity tables are corrupted (forensic screening).</div>`}`;
}
function vGLDetail(code){
  const g=QB_GL.find(x=>x.code===code);
  if(!g){location.hash="#/general-ledger";return;}
  const [a,b]=range();
  const yrs=g.byYear.filter(y=>y.abs>=a&&y.abs<=b);
  const q=yrs.reduce((x,y)=>x+y.q,0);
  const maxY=Math.max(1,...yrs.map(y=>y.q));
  const bars=yrs.map(y=>`<div class="g"><div class="pair"><div class="b in" style="height:${Math.max(2,Math.round(100*y.q/maxY))}px" title="${fmt(y.q)}"></div></div><div class="yl">${y.abs}</div></div>`).join("");
  const li=(arr,t)=>arr.map(x=>`<tr><td>${sux(x.n||"—")}</td><td class="num">${fmt(x.q)}</td></tr>`).join("");
  const unitLbl = g.unitLabel||META.unitWord;
  const cpPanels = (g.topTo&&g.topTo.length) ? `
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div class="panel"><h3>Top sources ${sux("(ki …-ta)")}</h3><table class="rep"><tr><th>From</th><th class="num">${esc(unitLbl)}</th></tr>${li(g.topFrom)}</table></div>
    <div class="panel"><h3>Top destinations</h3><table class="rep"><tr><th>To</th><th class="num">${esc(unitLbl)}</th></tr>${li(g.topTo)}</table></div>
  </div>` : "";
  $("#content").innerHTML=`
  <h2 class="view-title">Ledger: ${sux(g.code)} <span style="font-weight:400;font-size:15px">(${esc(g.name)})</span></h2>
  <p class="view-sub">${esc(PRESETS[state.preset].label)} · <a href="#/general-ledger">← all accounts</a></p>
  ${filterBar({commodity:false,entity:false,type:false})}
  <div class="cards">
    <div class="card"><div class="lbl">Transactions (all-time)</div><div class="val">${fmt(g.txns)}</div></div>
    <div class="card"><div class="lbl">Volume in range</div><div class="val blue">${fmt(q)}</div><div class="sub">${esc(unitLbl)}</div></div>
  </div>
  <div class="panel"><h3>Volume by year</h3><div class="bars">${bars}</div></div>
  ${cpPanels}
  <button class="btn" onclick="state.commodity='${esc(g.code)}';state.regPage=0;location.hash='#/register'">View transactions in Register</button>`;
}

/* ================= A/R & A/P AGING ================= */
function vAging(list,title,desc,cls){
  const q=(state.entity||"").toLowerCase();
  const rows=list.filter(x=>!q||x.name.toLowerCase().includes(q));
  const tot=list.reduce((x,r)=>x+Math.abs(r.net),0);
  const body=rows.map(x=>`<tr><td>${sux(x.name)}</td><td>${esc(x.type)}</td><td>${esc(x.commodity)}</td>
    <td>${esc(x.vintage)}</td><td class="num" style="color:${cls}">${fmt(Math.abs(x.net))}</td></tr>`).join("");
  $("#content").innerHTML=`
  <h2 class="view-title">${title}</h2><p class="view-sub">${desc}</p>
  ${filterBar({commodity:false,type:false})}
  <div class="cards"><div class="card"><div class="lbl">Counterparties</div><div class="val">${fmt(list.length)}</div></div>
  <div class="card"><div class="lbl">Total outstanding</div><div class="val" style="color:${cls}">${fmt(tot)}</div><div class="sub">${esc(META.qtyPhrase)}</div></div></div>
  <div class="panel"><table class="rep"><tr><th>Official</th><th>Type</th><th>Main commodity</th><th>Vintage</th><th class="num">Balance (head)</th></tr>${body}</table></div>
  <div class="note">Vintage = age of the counterparty's most recent activity relative to Ibbi-Suen 4 (end of archive).
  Balances net each official's lifetime inflows against outflows across all livestock accounts.</div>`;
}
function vAR(){
  if(!META.hasAging) return vNoAging("A/R Aging");
  vAging(QB_AR,"A/R Aging — Amounts Due from Officials",
  "Officials holding state livestock or owing an accounting (inflow exceeding outflow).","var(--green-dark)");}
function vAP(){
  if(!META.hasAging) return vNoAging("A/P Aging");
  vAging(QB_AP,"A/P Aging — Amounts Owed",
  "Officials who disbursed more than they received — the state owes them livestock or documentation.","var(--red)");}
function vNoAging(title){
  $("#content").innerHTML=`
  <h2 class="view-title">${esc(title)}</h2>
  <p class="view-sub">${esc(META.title)} · not available</p>
  <div class="panel"><h3>Disabled for this archive</h3>
  <p class="desc">Official-level balances are not shown: forensic screening found the entity tables
  corrupted (units of measure such as ${sux("ban2")} and ${sux("bur3")} appear as "officials"), and
  21–65% of transactions have no recorded counterparty. Any aging built on this data would be invalid.
  Commodity-level aggregates remain available throughout.</p></div>`;
}

/* ================= TRANSACTION REGISTER ================= */
function vRegister(){
  ensureTxns(()=>{
    const list=state.txns.filter(matchTxn);
    const per=50, pages=Math.max(1,Math.ceil(list.length/per));
    if(state.regPage>=pages)state.regPage=pages-1;
    const seg=list.slice(state.regPage*per,(state.regPage+1)*per);
    const badge=t=>t==="receipt"?'<span class="badge receipt">receipt</span>':t==="disbursement"?'<span class="badge disbursement">disbursement</span>':'<span class="badge transfer">transfer</span>';
    const body=seg.map(t=>`<tr><td style="color:var(--muted)">${t[0]}</td><td>${esc(t[1]||"—")}</td>
      <td>${t[2]?esc(t[2])+" "+t[3]:"<i>undated</i>"}</td>
      <td>${sux(t[5]||"—")}</td><td>${sux(t[6]||"—")}</td>
      <td>${sux(t[7])} <span style="color:var(--muted)">(${(QB_ACCOUNTS.find(a=>a.code===t[7])||{}).name||""})</span></td>
      <td class="num">${fmt(t[8])}</td><td>${badge(t[9])}</td></tr>`).join("");
    $("#content").innerHTML=`
    <h2 class="view-title">Transaction Register</h2>
    <p class="view-sub">${fmt(list.length)} of ${fmt(META.totalTxns)} transactions match · ${esc(PRESETS[state.preset].label)}${META.validated?"":" · subtotal lines excluded"}</p>
    ${filterBar({})}
    <div class="panel" style="overflow-x:auto"><table class="rep">
      <tr><th>#</th><th>Tablet</th><th>Date</th><th>From</th><th>To</th><th>Account</th><th class="num">Qty</th><th>Type</th></tr>
      ${body||'<tr><td colspan="8" style="text-align:center;color:var(--muted);padding:24px">No transactions match these filters.</td></tr>'}
    </table></div>
    <div class="pager">
      <button class="btn ghost" ${state.regPage===0?"disabled":""} onclick="regGo(0)">« First</button>
      <button class="btn ghost" ${state.regPage===0?"disabled":""} onclick="regGo(state.regPage-1)">‹ Prev</button>
      <span>Page ${state.regPage+1} of ${fmt(pages)}</span>
      <button class="btn ghost" ${state.regPage>=pages-1?"disabled":""} onclick="regGo(state.regPage+1)">Next ›</button>
      <button class="btn ghost" ${state.regPage>=pages-1?"disabled":""} onclick="regGo(${pages-1})">Last »</button>
    </div>
    <div class="note">Tablet IDs (e.g. P100189) are CDLI identifiers — every line is traceable to its source tablet.</div>`;
    syncFilterInputs();
  });
}
function regGo(p){state.regPage=p;route();}

/* ================= AUDIT ================= */
function vAudit(){
  if(!META.validated) return vAuditProv();
  const s=QB_SUMMARY;
  $("#content").innerHTML=`
  <h2 class="view-title">Auditor's Attestation</h2>
  <p class="view-sub">Independent examination of the reconstructed books of Puzriš-Dagan</p>
  <div class="attest">
    <div class="sux-block">nig2-ka9-ak mu-un-si-sa2<br>dub-ba si-sa2-am3<br>kiszib lu2-di-dam</div>
    <div class="trans">“The balanced account has been verified. The tablets are correct. Sealed by the auditor.”</div>
  </div>
  <div class="panel"><h3>Scope</h3><p class="desc">Full transaction-level reconstruction of the Drehem (Puzriš-Dagan) livestock
  administration, ${esc(s.rangeLabel)}, from CDLI transliterations of ${fmt(s.tablets)} tablets.</p>
  <ul class="checklist">
    <li><span class="ok">✓</span><span><b>Completeness of dating</b> — ${s.datedPct}% of ${fmt(s.transactions)} transactions carry regnal dates; undated items are flagged, never assumed.</span></li>
    <li><span class="ok">✓</span><span><b>Entity resolution</b> — ${fmt(s.entities)} counterparties resolved; 1,114 crosswalked against the Berkeley Sumerian Network authority.</span></li>
    <li><span class="ok">✓</span><span><b>Physical conservation</b> — every receipt is a physical inflow, every disbursement a physical outflow; the books are tested against the no-negative-livestock constraint.</span></li>
    <li><span class="ok">✓</span><span><b>Provenance</b> — every transaction traces to its source tablet (CDLI P-number); original entity spellings preserved.</span></li>
  </ul></div>
  <div class="panel"><h3>Material finding — the unreconciled balance</h3>
    <p class="desc">Disbursements exceed recorded receipts by ${fmt(s.deficit)} head (${s.deficitPct}% of outflow).</p>
    <p style="font-size:13.5px">This is <b>not</b> evidence of loss, fraud, or fiscal collapse. It is an artifact of <b>document custody</b>:
    per Widell (2020, <i>Orient</i> 55:117–154), the receiving official sealed the receipt tablet and the
    <b>deliverer kept it</b> as proof of delivery. Intake paperwork therefore left Drehem with the provincial
    officials who made the deliveries — it survives, if at all, in the Umma and Girsu archives, currently under audit.</p></div>
  <div class="panel"><h3>Limitations</h3>
  <ul class="checklist">
    <li><span style="color:var(--amber);font-weight:700">!</span><span>Umma and Girsu provincial archives are first-pass parses under refinement — inter-archive reconciliation is pending.</span></li>
    <li><span style="color:var(--amber);font-weight:700">!</span><span>Namesakes are not fully disambiguated; shared name strings across archives are not proven identities.</span></li>
    <li><span style="color:var(--amber);font-weight:700">!</span><span>All figures derive from published transliterations, taken as given; no independent philological verification has been performed on individual readings.</span></li>
  </ul></div>
  <div class="note">Opinion: the reconstructed books present fairly, in all material respects, the livestock
  administration of Puzriš-Dagan — <i>subject to the document-custody qualification above</i>. The city of Ur
  kept better records than most modern nonprofits.</div>`;
}

/* Provisional attestation for the provincial archives (forensic verdict: CAUTION). */
function vAuditProv(){
  const s=QB_SUMMARY;
  const unPct = s.transactions ? Math.round(100*s.unassigned.n/s.transactions) : 0;
  $("#content").innerHTML=`
  <h2 class="view-title">Auditor's Attestation — provisional</h2>
  <p class="view-sub">${esc(META.title)} · first-pass parse · forensic verdict: CAUTION</p>
  <div class="panel"><h3>Scope</h3><p class="desc">Transaction-level reconstruction of the ${esc(META.title)}
  provincial administration, ${esc(s.rangeLabel)}, from CDLI transliterations of ${fmt(s.tablets)} tablets.
  This is a <b>first-pass parse</b>, not an audited book. It has been forensically screened
  (Benford, round-number, duplicate, chronology, entity-sanity, totals-vs-line-items checks), and the
  screening found material data-quality issues listed below. Nothing here should be quoted as a validated figure.</p>
  <ul class="checklist">
    <li><span class="ok">✓</span><span><b>Dating</b> — ${s.datedPct}% of ${fmt(s.transactions)} transactions carry regnal dates (BDTNS catalog join); undated items are flagged, never assumed.</span></li>
    <li><span class="ok">✓</span><span><b>Livestock precision</b> — livestock commodities show Drehem-like round-number precision (3.6–16.3% round), the strongest genuineness signal available.</span></li>
    <li><span class="ok">✓</span><span><b>Chronology</b> — no impossible months, days, or years in the dated subset.</span></li>
  </ul></div>
  <div class="panel"><h3>Material findings</h3>
  <ul class="checklist">
    <li><span style="color:var(--red);font-weight:700">✗</span><span><b>Entity tables corrupted</b> — the most-connected "official" is a unit of measure (${esc(META.archive==="umma"?"ban2 (volume)":"bur3 (area)")}). Official-level balances, A/R and A/P aging are disabled in this build; only commodity-level aggregates are shown.</span></li>
    <li><span style="color:var(--amber);font-weight:700">!</span><span><b>${unPct}% of transactions lack a type assignment</b> (${fmt(s.unassigned.n)} of ${fmt(s.transactions)}) and are excluded from income/expense figures.</span></li>
    <li><span style="color:var(--amber);font-weight:700">!</span><span><b>Subtotal lines excluded</b> — ${fmt(s.excludedTotals)} total-lines do not reconcile with line items and are excluded from every aggregate and from the register.</span></li>
    <li><span style="color:var(--amber);font-weight:700">!</span><span><b>Clause-split duplicates</b> — ~7–10% of rows are duplicate parse outputs from related clauses; collapsing them requires clause-level judgment the parser does not yet make.</span></li>
    <li><span style="color:var(--amber);font-weight:700">!</span><span><b>Converted commodities</b> — grain and field-area volumes are parser-normalized (e.g. bur₃ → sar ×64,800); treat them as normalized, not transcribed, values.</span></li>
    ${s.excludedPreUr3?`<li><span style="color:var(--amber);font-weight:700">!</span><span><b>Period filter</b> — ${fmt(s.excludedPreUr3)} pre-Ur-III transactions excluded; this view covers Ur III kings only.</span></li>`:""}
  </ul></div>
  <div class="panel"><h3>What would upgrade this to an audited book</h3>
  <ul class="checklist">
    <li><span style="color:var(--muted)">○</span><span>Purge units of measure from entity roles and re-run entity resolution.</span></li>
    <li><span style="color:var(--muted)">○</span><span>Reduce unassigned transaction types below 10%.</span></li>
    <li><span style="color:var(--muted)">○</span><span>Resolve or document the clause-splitting duplicates.</span></li>
    <li><span style="color:var(--muted)">○</span><span>Fix or drop the non-reconciling totals.</span></li>
  </ul></div>
  <div class="note">Opinion: <b>withheld.</b> The commodity-level aggregates present a usable first-pass picture
  of the ${esc(META.title)} administration — subject to every qualification above. Do not cite these figures
  as validated.</div>`;
}

/* ---------- init ---------- */
/* Entity tables are corrupted in the provincial archives (forensic screening):
   hide the A/R and A/P aging views there. */
if(!META.hasAging){
  document.querySelectorAll('[data-r="ar-aging"],[data-r="ap-aging"]').forEach(a=>{a.style.display="none";});
}
route();
