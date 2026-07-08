<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>폴더블 3총사! 골든 라인을 찾아라 — 2026 UNPACKED 기구개발팀 감사제</title>
<style>
  :root{
    --navy:#0B1026; --navy2:#131A3A; --blue:#3B82F6; --cyan:#22D3EE;
    --violet:#8B93E8; --card:#F2F3F6; --ink:#EAF0FF; --dim:#8E9AC4;
    --gold:#FFD166; --ok:#34D399; --bad:#F87171;
    --font:'Segoe UI','Malgun Gothic','Apple SD Gothic Neo',sans-serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%}
  body{
    font-family:var(--font); color:var(--ink);
    background:radial-gradient(1200px 700px at 50% -10%, #1B2C6B 0%, var(--navy2) 45%, var(--navy) 100%);
    min-height:100vh; overflow-x:hidden;
  }

  /* ── 상단 고정 타이틀 ─────────────────────────── */
  header{
    position:fixed; top:0; left:0; right:0; z-index:50;
    text-align:center; padding:14px 10px 12px;
    background:linear-gradient(180deg, rgba(11,16,38,.96) 60%, rgba(11,16,38,0));
    backdrop-filter:blur(4px);
  }
  .event-name{font-size:12px; letter-spacing:.22em; color:var(--dim); text-transform:uppercase}
  .game-title{
    position:relative; display:inline-block; margin-top:4px;
    font-size:clamp(20px,4.5vw,34px); font-weight:800; letter-spacing:-0.02em;
    background:linear-gradient(92deg,#7DB2FF 0%, var(--cyan) 45%, #A78BFA 100%);
    background-size:200% 100%;
    -webkit-background-clip:text; background-clip:text; color:transparent;
    animation:shine 4s linear infinite;
  }
  @keyframes shine{to{background-position:200% 0}}
  .game-title .spark{
    position:absolute; font-size:.55em; animation:twinkle 1.6s ease-in-out infinite;
    -webkit-text-fill-color:var(--gold);
  }
  .spark.s1{top:-12px; left:-26px}
  .spark.s2{top:-16px; right:-24px; animation-delay:.5s}
  .spark.s3{bottom:-10px; right:-38px; animation-delay:1s; font-size:.4em}
  @keyframes twinkle{0%,100%{transform:scale(.6) rotate(0deg);opacity:.4}50%{transform:scale(1.25) rotate(20deg);opacity:1}}
  .fold-emoji{display:inline-block; animation:flip 3s ease-in-out infinite}
  @keyframes flip{0%,100%{transform:rotateY(0)}50%{transform:rotateY(180deg)}}
  @media (prefers-reduced-motion:reduce){ *{animation:none!important;transition:none!important} }

  main{max-width:760px; margin:0 auto; padding:112px 16px 60px}

  .panel{
    background:rgba(255,255,255,.05); border:1px solid rgba(139,147,232,.25);
    border-radius:20px; padding:26px 22px; box-shadow:0 18px 50px rgba(0,0,0,.35);
  }
  h2{font-size:19px; margin-bottom:14px}
  p.desc{color:var(--dim); font-size:14px; line-height:1.6}

  label{display:block; font-size:13px; color:var(--dim); margin:16px 0 6px}
  input[type=text]{
    width:100%; padding:13px 14px; font-size:16px; border-radius:12px;
    border:1px solid rgba(139,147,232,.35); background:rgba(11,16,38,.6); color:var(--ink);
    outline:none;
  }
  input[type=text]:focus{border-color:var(--cyan); box-shadow:0 0 0 3px rgba(34,211,238,.18)}

  .btn{
    display:inline-flex; align-items:center; justify-content:center; gap:8px;
    padding:13px 22px; border:none; border-radius:14px; cursor:pointer;
    font-size:16px; font-weight:700; font-family:var(--font); color:#fff;
    background:linear-gradient(92deg,var(--blue),var(--cyan)); 
    transition:transform .12s, filter .12s;
  }
  .btn:hover{transform:translateY(-1px); filter:brightness(1.08)}
  .btn:disabled{opacity:.35; cursor:not-allowed; transform:none}
  .btn.ghost{background:rgba(139,147,232,.16); color:var(--ink); border:1px solid rgba(139,147,232,.4)}
  .btn.warn{background:linear-gradient(92deg,#EF4444,#F97316)}
  .btn.block{width:100%; margin-top:20px}
  .btn-row{display:flex; gap:10px; margin-top:14px}
  .btn-row .btn{flex:1}

  .msg{margin-top:14px; font-size:14px; min-height:20px}
  .msg.error{color:var(--bad); font-weight:700}
  .msg.info{color:var(--ok)}

  .hidden{display:none!important}

  /* ── 게임 화면 ────────────────────────────────── */
  .stage-head{display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:6px}
  .stage-chip{
    font-size:12px; font-weight:800; letter-spacing:.08em; color:#06283D;
    background:linear-gradient(92deg,var(--gold),#FCA5A5); border-radius:999px; padding:4px 12px;
  }
  .stage-name{font-size:20px; font-weight:800}
  .progress{display:flex; gap:6px; margin:10px 0 18px}
  .progress i{flex:1; height:5px; border-radius:99px; background:rgba(139,147,232,.25)}
  .progress i.on{background:linear-gradient(92deg,var(--blue),var(--cyan))}

  .game-grid{display:grid; grid-template-columns:1fr 1fr; gap:18px}
  @media (max-width:640px){ .game-grid{grid-template-columns:1fr} }
  .img-label{font-size:12px; color:var(--dim); margin-bottom:6px; text-align:center}
  .frame{
    background:rgba(11,16,38,.5); border:1px solid rgba(139,147,232,.25);
    border-radius:14px; padding:12px; display:flex; align-items:center; justify-content:center;
  }
  .frame svg, .frame canvas{max-width:100%; height:auto; display:block}
  #gameCanvas{cursor:crosshair; touch-action:none; border-radius:6px}
  .hint{font-size:13px; color:var(--dim); text-align:center; margin-top:8px}

  /* ── 결과 / 순위 ─────────────────────────────── */
  .big-score{font-size:56px; font-weight:900; text-align:center;
    background:linear-gradient(92deg,#7DB2FF,var(--cyan));-webkit-background-clip:text;background-clip:text;color:transparent}
  #thanksOverlay{
    position:fixed; inset:0; z-index:200; display:flex; align-items:center; justify-content:center;
    background:rgba(11,16,38,.92); backdrop-filter:blur(6px);
  }
  .thanks-big{
    font-size:clamp(44px,11vw,96px); font-weight:900; text-align:center; line-height:1.25; padding:0 16px;
    background:linear-gradient(92deg,#FFD166,#7DB2FF,var(--cyan));
    -webkit-background-clip:text; background-clip:text; color:transparent;
    animation:thanksPop .6s cubic-bezier(.2,1.4,.4,1);
  }
  @keyframes thanksPop{0%{transform:scale(.3);opacity:0}70%{transform:scale(1.08)}100%{transform:scale(1);opacity:1}}
  .thanks{text-align:center; font-size:22px; font-weight:800; margin-top:8px}
  .sub-scores{display:flex; justify-content:center; gap:18px; margin-top:14px; color:var(--dim); font-size:14px}
  .sub-scores b{color:var(--ink)}

  table{width:100%; border-collapse:collapse; margin-top:14px; font-size:14px}
  th,td{padding:10px 8px; text-align:left; border-bottom:1px solid rgba(139,147,232,.18)}
  th{color:var(--dim); font-size:12px; letter-spacing:.06em}
  tr.me{background:rgba(34,211,238,.12)}
  tr.me td{font-weight:800}
  td.rank{font-weight:800; width:52px}
  .medal{font-size:16px}
  .list-wrap{max-height:420px; overflow-y:auto; margin-top:6px; border-radius:10px}
  .count-line{margin-top:16px; color:var(--dim); font-size:13px}
</style>
</head>
<body>

<header>
  <div class="event-name">2026 UNPACKED 기구개발팀 감사제</div>
  <div class="game-title">
    <span class="spark s1">✦</span>
    <span class="fold-emoji">📱</span> 폴더블 3총사! 골든 라인을 찾아라
    <span class="spark s2">✦</span><span class="spark s3">✧</span>
  </div>
</header>

<main>

  <!-- ── 시작 화면 ─────────────────────────────── -->
  <section id="screen-start" class="panel">
    <p class="desc">갤럭시 폴더블 3총사 언팩을 기념하는 3단계 챌린지!<br>
    기구인의 눈썰미로 <b>골든 라인</b>을 정확히 그려보세요. 단계당 100점, 총 300점 만점.</p>
    <label for="inpId">Knox ID</label>
    <input type="text" id="inpId" placeholder="예) gildong.hong" autocomplete="off">
    <label for="inpName">이름</label>
    <input type="text" id="inpName" placeholder="예) 홍길동" autocomplete="off">
    <button class="btn block" id="btnStart">게임 시작</button>
    <button class="btn ghost block hidden" id="btnAdmin" style="margin-top:10px">🛠 운영자 화면</button>
    <div class="msg error" id="startMsg"></div>
  </section>

  <!-- ── 게임 화면 ─────────────────────────────── -->
  <section id="screen-game" class="panel hidden">
    <div class="stage-head">
      <span class="stage-chip" id="stageChip">1단계</span>
      <span class="stage-name" id="stageName"></span>
    </div>
    <div class="progress"><i id="p1"></i><i id="p2"></i><i id="p3"></i></div>
    <p class="desc" id="stageDesc"></p>
    <div class="game-grid" style="margin-top:16px">
      <div>
        <div class="frame" id="exampleBox"></div>
      </div>
      <div>
        <div class="img-label">여기에 라인을 직접 그리세요</div>
        <div class="frame"><canvas id="gameCanvas"></canvas></div>
        <div class="hint" id="drawHint">마우스 또는 손가락으로 라인을 직접 그려주세요. 라인이 충분히 길어야 제출 버튼이 활성화되며, 제출 전까지 지우고 다시 그릴 수 있어요.</div>
      </div>
    </div>
    <div class="btn-row">
      <button class="btn ghost" id="btnErase">🧽 지우기</button>
      <button class="btn" id="btnSubmit" disabled>제출</button>
    </div>
  </section>

  <!-- ── 결과 화면 ─────────────────────────────── -->
  <section id="screen-result" class="panel hidden" style="text-align:center">
    <p class="desc">나의 총점</p>
    <div class="big-score" id="totalScore">0점</div>
    <div class="sub-scores" id="subScores"></div>
    <button class="btn block" id="btnFinish">게임완료</button>
  </section>

  <!-- ── 감사합니다 오버레이 ───────────────────── -->
  <div id="thanksOverlay" class="hidden">
    <div class="thanks-big">🎉 감사합니다! 🎉</div>
  </div>

  <!-- ── 순위 화면 ─────────────────────────────── -->
  <section id="screen-rank" class="panel hidden">
    <h2>🏆 실시간 순위</h2>
    <p class="desc" id="myRankLine"></p>
    <div class="list-wrap">
      <table>
        <thead><tr><th>순위</th><th>Knox ID</th><th>이름</th><th>점수</th></tr></thead>
        <tbody id="rankBody"></tbody>
      </table>
    </div>
    <button class="btn ghost block" id="btnRankRefresh">순위 새로고침</button>
  </section>

  <!-- ── 운영자 화면 ───────────────────────────── -->
  <section id="screen-admin" class="panel hidden">
    <h2>🛠 운영자 화면</h2>
    <p class="desc" id="adminSummary"></p>
    <div class="btn-row">
      <button class="btn ghost" id="btnAdminRefresh">목록 새로고침</button>
      <button class="btn warn" id="btnReset">게임 초기화</button>
    </div>
    <div class="list-wrap">
      <table>
        <thead><tr><th>순위</th><th>Knox ID</th><th>이름</th><th>점수</th></tr></thead>
        <tbody id="adminBody"></tbody>
      </table>
    </div>
    <button class="btn ghost block" id="btnAdminBack">← 시작 화면으로</button>
    <div class="msg info" id="adminMsg"></div>
  </section>

</main>

<script>
/* ═══════════════ 공통 ═══════════════ */
const $ = s => document.querySelector(s);
const screens = ['start','game','result','rank','admin'];
function show(name){ screens.forEach(s => $('#screen-'+s).classList.toggle('hidden', s!==name)); window.scrollTo(0,0); }

const ADMIN_ID='jhwan1.choi', ADMIN_NAME='최종환';
let me = { id:'', name:'' };
let scores = [0,0,0];

/* ═══════════════ API + 체험 모드(서버 미연결 시 자동 전환) ═══════════════
   실제 이벤트에서는 server.js가 응답하므로 이 모드는 동작하지 않음.
   서버 없이 HTML만 열었을 때(미리보기/리허설)도 전체 흐름을 체험 가능. */
let demoMode = false;
const mock = { players: new Map() }; // knox_id → {name, total, s1,s2,s3, finished, t}
function mockBoard(){
  return [...mock.players.entries()].filter(([,v])=>v.finished)
    .sort((a,b)=> b[1].total-a[1].total || a[1].playMs-b[1].playMs || a[1].t-b[1].t)
    .map(([id,v],i)=>({rank:i+1,id,name:v.name,total:v.total}));
}
function mockApi(path, body){
  body = body||{};
  const id=(body.id||'').trim().toLowerCase(), name=(body.name||'').trim();
  if(path==='/api/register'){
    if(mock.players.has(id)) return {ok:false,duplicate:true,message:'중복 참여자 입니다. (체험 모드)'};
    mock.players.set(id,{name,finished:0}); return {ok:true};
  }
  if(path==='/api/score'){
    const p=mock.players.get(id); if(!p) return {ok:false};
    const total = Math.round((body.s1+body.s2+body.s3)*100)/100;
    Object.assign(p,{s1:body.s1,s2:body.s2,s3:body.s3,total,playMs:body.playMs||0,finished:1,t:Date.now()});
    const b=mockBoard(); return {ok:true,total:p.total,rank:b.find(x=>x.id===id)?.rank||null,count:b.length};
  }
  if(path==='/api/leaderboard') return {list:mockBoard()};
  if(path==='/api/admin/participants'){
    const done=mockBoard();
    const playing=[...mock.players.entries()].filter(([,v])=>!v.finished).map(([id,v])=>({id,name:v.name}));
    return {ok:true,done,playing,totalCount:done.length+playing.length};
  }
  if(path==='/api/admin/reset'){ mock.players.clear(); return {ok:true,message:'게임이 초기화되었습니다. (체험 모드)'}; }
  return {ok:false};
}
function showDemoBadge(){
  if($('#demoBadge')) return;
  const b=document.createElement('div'); b.id='demoBadge';
  b.style.cssText='position:fixed;bottom:12px;left:50%;transform:translateX(-50%);z-index:99;background:rgba(255,209,102,.15);border:1px solid rgba(255,209,102,.5);color:#FFD166;font-size:12px;font-weight:700;padding:6px 14px;border-radius:999px';
  b.textContent='⚡ 체험 모드 — 서버 미연결 상태입니다. 실제 이벤트는 사내 서버(server.js) 실행 후 사용하세요.';
  document.body.appendChild(b);
}
async function api(path, body){
  if(demoMode) return mockApi(path, body);
  try{
    const opt = body!==undefined
      ? {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}
      : undefined;
    const r = await fetch(path, opt);
    return await r.json();
  }catch(e){
    demoMode = true; showDemoBadge();
    return mockApi(path, body);
  }
}

/* ═══════════════ 카드 그래픽 (예시사진의 깔끔한 재구성 버전) ═══════════════
   캡쳐 원본의 구성(스파클 + 선물상자 카드)은 유지하되,
   음영·배경을 제거한 삼성닷컴 수준의 클린 벡터 이미지로 렌더링 */
function star4(cx,cy,r,fill,rot=0){
  const k=r*0.28;
  return `<path transform="rotate(${rot} ${cx} ${cy})" fill="${fill}"
    d="M ${cx} ${cy-r} C ${cx+k*0.3} ${cy-k} ${cx+k} ${cy-k*0.3} ${cx+r} ${cy}
       C ${cx+k} ${cy+k*0.3} ${cx+k*0.3} ${cy+k} ${cx} ${cy+r}
       C ${cx-k*0.3} ${cy+k} ${cx-k} ${cy+k*0.3} ${cx-r} ${cy}
       C ${cx-k} ${cy-k*0.3} ${cx-k*0.3} ${cy-k} ${cx} ${cy-r} Z"/>`;
}
function cardArtSVG(w,h){ // 카드 내부 아트(스파클+선물상자), 좌표는 w×h 기준
  const cx=w/2, gy=h*0.60, gw=Math.min(w,h)*0.34;
  return `
  <defs>
    <linearGradient id="gStar" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="gBox" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#C7CDF4"/><stop offset="1" stop-color="#8B93E8"/>
    </linearGradient>
  </defs>
  <!-- 선물 상자 -->
  <g opacity="0.95">
    <polygon points="${cx-gw},${gy} ${cx},${gy+gw*0.5} ${cx+gw},${gy} ${cx},${gy-gw*0.5}" fill="#DDE1F8"/>
    <polygon points="${cx-gw},${gy} ${cx},${gy+gw*0.5} ${cx},${gy+gw*1.15} ${cx-gw},${gy+gw*0.6}" fill="url(#gBox)"/>
    <polygon points="${cx+gw},${gy} ${cx},${gy+gw*0.5} ${cx},${gy+gw*1.15} ${cx+gw},${gy+gw*0.6}" fill="#A6ADEF"/>
    <polygon points="${cx-gw*0.16},${gy-gw*0.42} ${cx},${gy-gw*0.34} ${cx+gw*0.16},${gy-gw*0.42} ${cx},${gy-gw*0.5}" fill="#fff" opacity=".7"/>
  </g>
  <!-- 스파클 3총사 -->
  ${star4(cx+w*0.06, gy-gw*1.35, gw*0.62, 'url(#gStar)')}
  ${star4(cx-w*0.17, gy-gw*1.75, gw*0.30, '#2DD4BF', 15)}
  ${star4(cx+w*0.20, gy-gw*0.85, gw*0.22, '#38BDF8', -10)}`;
}
/* 예시 이미지 SVG: ratio = 장/폭, guide = {type:'h'|'v', pct}
   displayW = 화면 표시 폭(px) — 실제 게임 이미지의 절반 크기로 표시 */
function exampleSVG(ratio, guide, displayW){
  const w=300, cardH=w*ratio, topPad=16, svgH = cardH + topPad + 16;
  const cy = topPad;
  let perf=''; for(let px=10; px<w-10; px+=9) perf+=`<circle cx="${px}" cy="${cy}" r="1.6" fill="#C9CEDA"/>`;
  let guideLine='';
  if(guide){
    if(guide.type==='h'){ const y=cy+cardH*guide.pct;
      guideLine=`<line x1="-8" y1="${y}" x2="${w+8}" y2="${y}" stroke="#111827" stroke-width="4" stroke-dasharray="10 7"/>`; }
    else{ const x=w*guide.pct;
      guideLine=`<line x1="${x}" y1="${cy-10}" x2="${x}" y2="${cy+cardH+10}" stroke="#111827" stroke-width="4" stroke-dasharray="10 7"/>`; }
  }
  return `<svg viewBox="-10 -6 ${w+20} ${svgH}" xmlns="http://www.w3.org/2000/svg" style="width:${displayW}px">
    <g>
      <rect x="0" y="${cy}" width="${w}" height="${cardH}" rx="10" fill="#F2F3F6" stroke="#E2E5EC"/>
      ${perf}
      <svg x="0" y="${cy}" width="${w}" height="${cardH}" viewBox="0 0 ${w} ${cardH}">${cardArtSVG(w,cardH)}</svg>
    </g>
    ${guideLine}
  </svg>`;
}

/* ═══════════════ 단계 정의 ═══════════════ */
const STAGES = [
  { name:'최적의 비율을 찾아라', ratio:2, dir:'h', targetPct:0.25,
    desc:'최적의 비율을 위해 상단에서 25% 지점에 직선 라인을 그려주세요~',
    example:w=>exampleSVG(2,{type:'h',pct:0.25},w) },
  { name:'가로 방향 센터 라인을 찾아라', ratio:2.25, dir:'h', targetPct:0.5,
    desc:'최적의 폴딩을 위해 세로 절반 지점에 직선 라인을 그려주세요~',
    example:w=>exampleSVG(2.25,{type:'h',pct:0.5},w) },
  { name:'세로 센터 라인을 찾아라', ratio:1.1, dir:'v', targetPct:0.5,
    desc:'최적의 폴딩을 위해 가로 절반 지점에 직선 라인을 그려주세요~',
    example:w=>exampleSVG(1.1,{type:'v',pct:0.5},w) },
];
let stageIdx = 0;
let strokes = [];      // 손으로 그린 선: [[{x,y},...], ...] (0~1 정규화 좌표)
let curStroke = null;  // 현재 그리는 중인 선

/* ═══════════════ 캔버스 (프리핸드 드로잉) ═══════════════ */
const canvas = $('#gameCanvas'), ctx = canvas.getContext('2d');
function setupCanvas(){
  const st = STAGES[stageIdx];
  const cssW = Math.min(300, (canvas.parentElement.clientWidth||300)-8);
  const dpr = window.devicePixelRatio||1;
  canvas.style.width = cssW+'px'; canvas.style.height = (cssW*st.ratio)+'px';
  canvas.width = cssW*dpr; canvas.height = cssW*st.ratio*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  strokes = []; curStroke = null; $('#btnSubmit').disabled = true;
  drawCanvas();
}
function drawCanvas(){
  const st = STAGES[stageIdx];
  const w = canvas.width/(window.devicePixelRatio||1), h = w*st.ratio;
  ctx.clearRect(0,0,w,h);
  // 카드 배경
  ctx.fillStyle = '#F2F3F6';
  roundRect(ctx,0,0,w,h,10); ctx.fill();
  ctx.strokeStyle = '#E2E5EC'; ctx.lineWidth = 1.5; ctx.stroke();
  // 아트 (SVG와 동일 구성을 캔버스로)
  drawCardArt(w,h);
  // 사용자가 직접 그린 선(프리핸드)
  ctx.strokeStyle = '#EF4444'; ctx.lineWidth = 4;
  ctx.lineCap='round'; ctx.lineJoin='round';
  for(const s of strokes){
    if(s.length < 2) continue;
    ctx.beginPath();
    ctx.moveTo(s[0].x*w, s[0].y*h);
    for(let i=1;i<s.length;i++) ctx.lineTo(s[i].x*w, s[i].y*h);
    ctx.stroke();
  }
}
function roundRect(c,x,y,w,h,r){ c.beginPath(); c.moveTo(x+r,y); c.arcTo(x+w,y,x+w,y+h,r); c.arcTo(x+w,y+h,x,y+h,r); c.arcTo(x,y+h,x,y,r); c.arcTo(x,y,x+w,y,r); c.closePath(); }
function drawStar(cx,cy,r,color,rot=0){
  const k=r*0.28; ctx.save(); ctx.translate(cx,cy); ctx.rotate(rot*Math.PI/180);
  ctx.fillStyle=color; ctx.beginPath(); ctx.moveTo(0,-r);
  ctx.bezierCurveTo(k*0.3,-k, k,-k*0.3, r,0); ctx.bezierCurveTo(k,k*0.3, k*0.3,k, 0,r);
  ctx.bezierCurveTo(-k*0.3,k, -k,k*0.3, -r,0); ctx.bezierCurveTo(-k,-k*0.3, -k*0.3,-k, 0,-r);
  ctx.closePath(); ctx.fill(); ctx.restore();
}
function drawCardArt(w,h){
  const cx=w/2, gy=h*0.60, gw=Math.min(w,h)*0.34;
  const poly=(pts,fill)=>{ ctx.fillStyle=fill; ctx.beginPath(); ctx.moveTo(pts[0][0],pts[0][1]); pts.slice(1).forEach(p=>ctx.lineTo(p[0],p[1])); ctx.closePath(); ctx.fill(); };
  poly([[cx-gw,gy],[cx,gy+gw*0.5],[cx+gw,gy],[cx,gy-gw*0.5]],'#DDE1F8');
  const grad=ctx.createLinearGradient(0,gy,0,gy+gw*1.15); grad.addColorStop(0,'#C7CDF4'); grad.addColorStop(1,'#8B93E8');
  poly([[cx-gw,gy],[cx,gy+gw*0.5],[cx,gy+gw*1.15],[cx-gw,gy+gw*0.6]],grad);
  poly([[cx+gw,gy],[cx,gy+gw*0.5],[cx,gy+gw*1.15],[cx+gw,gy+gw*0.6]],'#A6ADEF');
  const sg=ctx.createLinearGradient(cx-gw*0.6,gy-gw*2,cx+gw*0.6,gy-gw*0.8); sg.addColorStop(0,'#22D3EE'); sg.addColorStop(1,'#2563EB');
  drawStar(cx+w*0.06, gy-gw*1.35, gw*0.62, sg);
  drawStar(cx-w*0.17, gy-gw*1.75, gw*0.30, '#2DD4BF', 15);
  drawStar(cx+w*0.20, gy-gw*0.85, gw*0.22, '#38BDF8', -10);
}
function pointerPos(e){
  const r = canvas.getBoundingClientRect();
  const t = e.touches ? e.touches[0] : e;
  return { x:(t.clientX-r.left)/r.width, y:(t.clientY-r.top)/r.height };
}
let dragging=false;
function onDraw(e){
  e.preventDefault();
  const p = pointerPos(e);
  const pt = { x:Math.min(1,Math.max(0,p.x)), y:Math.min(1,Math.max(0,p.y)) };
  if(curStroke) curStroke.push(pt);
  updateSubmitState();
  drawCanvas();
}
// 그린 선이 카드의 주요 방향으로 충분히(40% 이상) 이어져야 제출 가능
function strokeSpan(){
  const st = STAGES[stageIdx];
  const pts = strokes.flat();
  if(pts.length < 2) return 0;
  const vals = pts.map(p => st.dir==='h' ? p.x : p.y);
  return Math.max(...vals) - Math.min(...vals);
}
function updateSubmitState(){ $('#btnSubmit').disabled = strokeSpan() < 0.4; }

canvas.addEventListener('pointerdown', e=>{ dragging=true; curStroke=[]; strokes.push(curStroke); onDraw(e); });
canvas.addEventListener('pointermove', e=>{ if(dragging) onDraw(e); });
window.addEventListener('pointerup', ()=>{ dragging=false; curStroke=null; });
window.addEventListener('resize', ()=>{
  if($('#screen-game').classList.contains('hidden')) return;
  const keep = strokes;               // 정규화 좌표라 리사이즈 후에도 유지 가능
  setupCanvas(); strokes = keep; updateSubmitState(); drawCanvas();
  renderExample();
});

/* ═══════════════ 단계 진행 ═══════════════ */
function renderExample(){
  const st = STAGES[stageIdx];
  const halfW = (parseFloat(canvas.style.width)||300) / 2; // 실제 게임 이미지의 절반 크기
  $('#exampleBox').innerHTML = st.example(halfW);
}
function loadStage(){
  const st = STAGES[stageIdx];
  $('#stageChip').textContent = (stageIdx+1)+'단계';
  $('#stageName').textContent = st.name;
  $('#stageDesc').innerHTML = st.desc;
  for(let i=1;i<=3;i++) $('#p'+i).classList.toggle('on', i<=stageIdx+1);
  setupCanvas();
  renderExample();
}
$('#btnErase').onclick = ()=>{ strokes=[]; curStroke=null; $('#btnSubmit').disabled=true; drawCanvas(); };
$('#btnSubmit').onclick = async ()=>{
  const st = STAGES[stageIdx];
  const pts = strokes.flat();
  const coords = pts.map(p => st.dir==='h' ? p.y : p.x);
  // ① 위치 정확도: 목표 라인 대비 평균 편차 (1%p당 5점 감점)
  const devs = coords.map(v => Math.abs(v - st.targetPct));
  const avgDev = devs.reduce((a,b)=>a+b,0) / devs.length;
  // ② 직진도: 선 자체의 출렁임(표준편차, 1%p당 2점 감점) — 동점 방지용 추가 변별 축
  const mean = coords.reduce((a,b)=>a+b,0) / coords.length;
  const std = Math.sqrt(coords.reduce((a,v)=>a+(v-mean)**2,0) / coords.length);
  // 소수점 2자리 정밀 채점 (1,100명 동점 방지)
  const raw = 100 - avgDev*100*5 - std*100*2;
  scores[stageIdx] = Math.max(0, Math.round(raw*100)/100);
  if(stageIdx < 2){ stageIdx++; loadStage(); }
  else await finishGame();
};
async function finishGame(){
  const total = Math.round((scores[0]+scores[1]+scores[2])*100)/100;
  $('#totalScore').textContent = fmt(total)+'점';
  $('#subScores').innerHTML = scores.map((s,i)=>`${i+1}단계 <b>${fmt(s)}점</b>`).join(' · ');
  show('result');
  // 점수는 결과 화면 진입 시 즉시 저장 (버튼을 안 눌러도 기록 보존)
  const d = await api('/api/score',{id:me.id, s1:scores[0], s2:scores[1], s3:scores[2], playMs: Date.now()-playStart});
  myFinalRank = (d && d.ok) ? d.rank : null;
}
let myFinalRank = null;
let playStart = 0;
const fmt = v => (Math.round(v*100)/100).toFixed(2);
$('#btnFinish').onclick = ()=>{
  $('#thanksOverlay').classList.remove('hidden');   // 감사합니다! 크게 표시
  setTimeout(()=>{                                   // 1초 후 순위 화면으로 전환
    $('#thanksOverlay').classList.add('hidden');
    showRank(myFinalRank);
  }, 1000);
};

/* ═══════════════ 순위 ═══════════════ */
async function showRank(myRank){
  await renderRank(myRank);
  show('rank');
}
async function renderRank(myRank){
  try{
    const d = await api('/api/leaderboard');
    const list = d.list||[];
    $('#rankBody').innerHTML = list.map(row=>{
      const medal = row.rank===1?'🥇':row.rank===2?'🥈':row.rank===3?'🥉':row.rank;
      return `<tr class="${row.id===me.id?'me':''}"><td class="rank medal">${medal}</td><td>${esc(row.id)}</td><td>${esc(row.name)}</td><td>${fmt(row.total)}점</td></tr>`;
    }).join('') || '<tr><td colspan="4">아직 완료한 참가자가 없습니다.</td></tr>';
    const meRow = list.find(x=>x.id===me.id);
    $('#myRankLine').innerHTML = meRow
      ? `<b>${esc(me.name)}</b>님은 현재 참가자 ${list.length}명 중 <b style="color:var(--gold)">${meRow.rank}위</b> 입니다!`
      : `현재까지 ${list.length}명이 참여했습니다.`;
  }catch(e){ $('#myRankLine').textContent='순위를 불러오지 못했습니다.'; }
}
$('#btnRankRefresh').onclick = ()=>renderRank();
const esc = s => String(s).replace(/[&<>"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* ═══════════════ 시작 / 등록 ═══════════════ */
function checkAdminBtn(){
  const id = $('#inpId').value.trim().toLowerCase(), nm = $('#inpName').value.trim();
  $('#btnAdmin').classList.toggle('hidden', !(id===ADMIN_ID && nm===ADMIN_NAME));
}
$('#inpId').addEventListener('input', checkAdminBtn);
$('#inpName').addEventListener('input', checkAdminBtn);

$('#btnStart').onclick = async ()=>{
  const id = $('#inpId').value.trim(), name = $('#inpName').value.trim();
  const msg = $('#startMsg'); msg.textContent='';
  if(!id || !name){ msg.textContent='Knox ID와 이름을 모두 입력해 주세요.'; return; }
  const d = await api('/api/register',{id,name});
  if(!d || !d.ok){ msg.textContent = (d && d.message) || '등록에 실패했습니다.'; return; }
  me = { id:id.toLowerCase(), name };
  scores=[0,0,0]; stageIdx=0;
  playStart = Date.now();   // 동점자 처리용 플레이 시간 측정 시작
  show('game'); loadStage();
};

/* ═══════════════ 운영자 ═══════════════ */
$('#btnAdmin').onclick = ()=>{ me={id:ADMIN_ID,name:ADMIN_NAME}; show('admin'); loadAdmin(); };
$('#btnAdminBack').onclick = ()=> show('start');
$('#btnAdminRefresh').onclick = loadAdmin;
$('#btnReset').onclick = async ()=>{
  if(!confirm('정말 게임을 초기화할까요?\n모든 참가 기록과 점수가 삭제됩니다.')) return;
  const d = await api('/api/admin/reset',{id:ADMIN_ID,name:ADMIN_NAME});
  $('#adminMsg').textContent = (d && d.message) || '';
  loadAdmin();
};
async function loadAdmin(){
  try{
    const d = await api('/api/admin/participants',{id:ADMIN_ID,name:ADMIN_NAME});
    if(!d || !d.ok) return;
    $('#adminSummary').innerHTML = `총 참여 <b>${d.totalCount}명</b> · 완료 <b>${d.done.length}명</b> · 진행 중 <b>${d.playing.length}명</b>`;
    const doneRows = d.done.map(x=>`<tr><td class="rank">${x.rank}</td><td>${esc(x.id)}</td><td>${esc(x.name)}</td><td>${fmt(x.total)}점</td></tr>`).join('');
    const playRows = d.playing.map(x=>`<tr style="opacity:.55"><td class="rank">—</td><td>${esc(x.id)}</td><td>${esc(x.name)}</td><td>진행 중</td></tr>`).join('');
    $('#adminBody').innerHTML = (doneRows+playRows) || '<tr><td colspan="4">참가자가 없습니다.</td></tr>';
  }catch(e){}
}
setInterval(()=>{ if(!$('#screen-admin').classList.contains('hidden')) loadAdmin(); }, 5000);
</script>
</body>
</html>
