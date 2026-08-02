#!/usr/bin/env python3
"""Build the two companion pages for the skill-tree site:

  viewer/labs.html   - Find & contact a community lab (data: src/data/labs.json,
                       sourced from the Global Biolab Atlas)
  viewer/costs.html  - Interactive lab-cost calculator (data: src/data/cost_model.json)

Both share the main viewer's Inter + light/dark theme. No dependencies.
Run:  python build_pages.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
LABS = ROOT / "src" / "data" / "labs.json"
COSTS = ROOT / "src" / "data" / "cost_model.json"
OUT = ROOT / "viewer"

SHARED_HEAD = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>
(function(){try{var t=localStorage.getItem('synbio-theme');
if(t!=='light'&&t!=='dark'){t=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches)?'light':'dark';}
document.documentElement.setAttribute('data-theme',t);}catch(e){document.documentElement.setAttribute('data-theme','dark');}})();
</script>
<style>
  :root{
    --sans:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;
    --bg:#0a0b0a; --ink:#e9f0e2; --dim:#8a9683; --green:#c6f24e; --green-dim:#7f9a3a;
    --orange:#ff7a2f; --line:#2a3226; --panel:#14170f; --edge:#3a4531;
    --surface:#12150e; --surface-2:#0e110c; --on-accent:#0a0b0a; --track:#1c2018;
    --info:#8fd3ff; --info-edge:#3a5566; --scrim:rgba(4,5,4,.72); --shadow:rgba(0,0,0,.5);
    --ok:#8fd36a; --warn:#ffb454; --bad:#ff6f6f; --scheme:dark;
  }
  :root[data-theme="light"]{
    --bg:#fcfcfb; --ink:#16191c; --dim:#5f6a72; --green:#4d7c0f; --green-dim:#7ba32f;
    --orange:#c2410c; --line:#e4e6e1; --panel:#ffffff; --edge:#cfd4c9;
    --surface:#ffffff; --surface-2:#fafbf8; --on-accent:#ffffff; --track:#e6e8e2;
    --info:#1e6fa8; --info-edge:#b8d4e8; --scrim:rgba(22,25,28,.42); --shadow:rgba(16,20,24,.12);
    --ok:#3f7d20; --warn:#a86412; --bad:#c0392b; --scheme:light;
  }
  :root{color-scheme:var(--scheme)}
  *{box-sizing:border-box}
  html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
  a{color:var(--green)}
  header{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:14px;flex-wrap:wrap;
    padding:12px 20px;border-bottom:1px solid var(--line);background:var(--surface-2)}
  .brand{font-weight:800;font-size:17px;letter-spacing:-.02em;color:var(--green);white-space:nowrap}
  .brand small{display:block;font-weight:400;font-size:10px;color:var(--dim);letter-spacing:.12em;text-transform:uppercase}
  .grow{flex:1}
  .nav{display:flex;gap:6px}
  .nav a{font-size:12px;padding:7px 12px;border:1px solid var(--edge);border-radius:7px;color:var(--dim);text-decoration:none}
  .nav a:hover{border-color:var(--green);color:var(--green)}
  .nav a.on{background:var(--green);color:var(--on-accent);border-color:var(--green);font-weight:700}
  .themeBtn{width:34px;height:34px;border-radius:8px;border:1px solid var(--edge);background:var(--surface);color:var(--ink);font-size:15px;cursor:pointer}
  .themeBtn:hover{border-color:var(--green);color:var(--green)}
  main{max-width:1120px;margin:0 auto;padding:26px 20px 70px}
  h1.page{font-size:26px;font-weight:800;letter-spacing:-.025em;margin:6px 0 6px}
  p.lead{color:var(--dim);font-size:14px;line-height:1.6;max-width:760px;margin:0 0 22px}
</style>
"""

THEME_JS = r"""
  var themeBtn=document.getElementById('themeBtn');
  function theme(){return document.documentElement.getAttribute('data-theme')==='light'?'light':'dark';}
  function setTheme(t){document.documentElement.setAttribute('data-theme',t);try{localStorage.setItem('synbio-theme',t);}catch(e){}
    themeBtn.textContent=t==='light'?'☾':'☀';themeBtn.title='Switch to '+(t==='light'?'dark':'light')+' mode';}
  themeBtn.addEventListener('click',function(){setTheme(theme()==='light'?'dark':'light');});
  setTheme(theme());
"""


def nav(active):
    def a(href, label, key):
        cls = ' class="on"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    return ('<div class="nav">'
            + a("index.html", "◆ skill tree", "map")
            + a("costs.html", "$ cost calculator", "costs")
            + a("labs.html", "⌖ find a lab", "labs")
            + '</div>')


# ------------------------------------------------------------------ LABS PAGE
LABS_BODY = r"""
</head>
<body>
<header>
  <div class="brand">find a lab<small>get hands-on access near you</small></div>
  <div class="grow"></div>
  __NAV__
  <button class="themeBtn" id="themeBtn" type="button" aria-label="Toggle theme">◐</button>
</header>
<main>
  <h1 class="page">Find a community lab &mdash; and reach out</h1>
  <p class="lead">The skills in the tree need a bench. These are community &amp; DIY biolabs worldwide (from the
  <a href="https://global-biolab-atlas.netlify.app/" target="_blank" rel="noopener">Global Biolab Atlas</a>) where you can
  often get access to equipment and space to learn. Find one near you, then <strong>send your own message</strong> via their
  site &mdash; this tool drafts it for you but never contacts anyone on your behalf.</p>

  <div class="controls">
    <label class="search"><span>&#x2315;</span><input id="q" placeholder="search by lab, city, or country&hellip;" autocomplete="off"></label>
    <button class="geo" id="geoBtn" type="button">&#x1F4CD; sort by distance to me</button>
  </div>
  <div class="chips" id="regionChips"></div>
  <div class="filters">
    <label class="chk"><input type="checkbox" id="activeOnly" checked> active labs only</label>
    <span class="count" id="count"></span>
  </div>

  <div id="results" class="results"></div>
</main>

<div id="scrim" class="scrim"><div id="pop" class="pop"></div></div>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
  "use strict";
  var DATA=JSON.parse(document.getElementById('data').textContent);
  var LABS=DATA.labs.slice();
  __THEME_JS__

  var STATUS={active:{c:'ok',t:'active'},dormant:{c:'warn',t:'dormant'},uncertain:{c:'dim',t:'unverified'},dead:{c:'bad',t:'closed'}};
  var regionSel=null, myPos=null, q='';
  var activeOnly=document.getElementById('activeOnly');

  // region chips
  var regions={}; LABS.forEach(function(l){regions[l.region]=(regions[l.region]||0)+1;});
  var order=Object.keys(regions).sort();
  document.getElementById('regionChips').innerHTML='<span class="chip'+(regionSel?'':' on')+'" data-r="">all regions</span>'+
    order.map(function(r){return '<span class="chip" data-r="'+esc(r)+'">'+esc(r)+' ('+regions[r]+')</span>';}).join('');
  document.querySelectorAll('#regionChips .chip').forEach(function(c){
    c.addEventListener('click',function(){regionSel=c.getAttribute('data-r')||null;
      document.querySelectorAll('#regionChips .chip').forEach(function(x){x.classList.toggle('on',x===c);});render();});
  });

  document.getElementById('q').addEventListener('input',function(e){q=e.target.value.trim().toLowerCase();render();});
  activeOnly.addEventListener('change',render);

  document.getElementById('geoBtn').addEventListener('click',function(){
    if(!navigator.geolocation){alert('Geolocation not available in this browser.');return;}
    var b=document.getElementById('geoBtn'); b.textContent='… locating';
    navigator.geolocation.getCurrentPosition(function(p){
      myPos={lat:p.coords.latitude,lng:p.coords.longitude};
      b.textContent='✓ nearest first';b.classList.add('active');render();
    },function(){b.textContent='✕ location denied';setTimeout(function(){b.textContent='📍 sort by distance to me';},2500);});
  });

  function hav(a,b){var R=6371,dl=(b.lat-a.lat)*Math.PI/180,dg=(b.lng-a.lng)*Math.PI/180,
    x=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a.lat*Math.PI/180)*Math.cos(b.lat*Math.PI/180)*Math.sin(dg/2)*Math.sin(dg/2);
    return R*2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x));}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  function render(){
    var list=LABS.filter(function(l){
      if(activeOnly.checked && l.status!=='active')return false;
      if(regionSel && l.region!==regionSel)return false;
      if(q){var hay=(l.name+' '+l.city+' '+l.country+' '+(l.desc||'')).toLowerCase();if(hay.indexOf(q)<0)return false;}
      return true;
    });
    if(myPos){list.forEach(function(l){l._d=hav(myPos,l);});list.sort(function(a,b){return a._d-b._d;});}
    else{list.sort(function(a,b){var o={active:0,dormant:1,uncertain:2,dead:3};return (o[a.status]-o[b.status])||a.name.localeCompare(b.name);});}
    document.getElementById('count').textContent=list.length+' lab'+(list.length===1?'':'s')+(activeOnly.checked?' active':'')+(regionSel?' in '+regionSel:'');
    document.getElementById('results').innerHTML=list.map(card).join('')||'<p class="empty">No labs match. Try clearing filters or unchecking &ldquo;active only.&rdquo;</p>';
    document.querySelectorAll('[data-compose]').forEach(function(b){b.addEventListener('click',function(){compose(b.getAttribute('data-compose'));});});
  }

  function card(l){
    var st=STATUS[l.status]||STATUS.uncertain;
    var dist=(myPos&&l._d!=null)?'<span class="dist">'+Math.round(l._d).toLocaleString()+' km</span>':'';
    var tags=(l.sources||[]).map(function(s){return '<span class="src">'+esc(s)+'</span>';}).join('');
    var visit=l.url?'<a class="lab-a" href="'+esc(l.url)+'" target="_blank" rel="noopener">visit site ↗</a>':'';
    return '<div class="lab">'
      +'<div class="lab-top"><div><div class="lab-name">'+esc(l.name)+'</div>'
      +'<div class="lab-loc">'+esc(l.city?l.city+', ':'')+esc(l.country||'')+dist+'</div></div>'
      +'<span class="badge '+st.c+'">'+st.t+'</span></div>'
      +(l.desc?'<div class="lab-desc">'+esc(l.desc)+'</div>':'')
      +'<div class="lab-tags">'+tags+(l.founded?'<span class="src">est. '+l.founded+'</span>':'')+'</div>'
      +'<div class="lab-acts">'+visit
      +(l.url?'<button class="lab-b" data-compose="'+esc(l.name)+'∷'+esc(l.url)+'">compose outreach →</button>':'')
      +'</div></div>';
  }

  // outreach composer (drafts a message; user sends it themselves)
  var scrim=document.getElementById('scrim'),pop=document.getElementById('pop');
  function compose(key){
    var i=key.indexOf('∷'); var name=key.slice(0,i), url=key.slice(i+1);
    var msg='Hi '+name+' team,\n\n'
      +'I’m learning synthetic biology through an open curriculum (the Biotech Skill Tree, '
      +'biotech-skill-tree.netlify.app) and I’m looking for hands-on bench time to practise the wet-lab skills.\n\n'
      +'Could you tell me about:\n'
      +'  • how to visit or become a member\n'
      +'  • open hours / intro sessions for newcomers\n'
      +'  • what equipment and space is available to learners\n'
      +'  • any safety training or onboarding I’d need first\n\n'
      +'A little about me: [your background + what you want to work on].\n\n'
      +'Thanks so much!\n[your name]';
    pop.innerHTML='<div class="pop-top"><b>Reach out to '+esc(name)+'</b><button class="x" id="px">✕</button></div>'
      +'<div class="pop-body"><p class="pop-note">Edit this, copy it, then send it yourself via their site or contact form. '
      +'We don’t send anything for you.</p>'
      +'<textarea id="msg" spellcheck="false">'+esc(msg)+'</textarea>'
      +'<div class="pop-acts"><button class="cp" id="cp">⎘ copy message</button>'
      +'<a class="go" href="'+esc(url)+'" target="_blank" rel="noopener">open their site ↗</a></div></div>';
    scrim.classList.add('show');
    document.getElementById('px').addEventListener('click',close);
    document.getElementById('cp').addEventListener('click',function(){
      var ta=document.getElementById('msg');ta.select();
      try{navigator.clipboard.writeText(ta.value);}catch(e){document.execCommand('copy');}
      var b=document.getElementById('cp');b.textContent='✓ copied';setTimeout(function(){b.textContent='⎘ copy message';},1800);
    });
  }
  function close(){scrim.classList.remove('show');}
  scrim.addEventListener('click',function(e){if(e.target===scrim)close();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});

  render();
})();
</script>
</body>
</html>
"""

LABS_CSS = r"""
<style>
  .controls{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px}
  .search{flex:1 1 280px;min-width:200px;display:flex;align-items:center;gap:8px;border:1px solid var(--edge);border-radius:8px;padding:8px 12px;background:var(--surface)}
  .search span{color:var(--dim)}
  .search input{flex:1;background:transparent;border:0;outline:0;color:var(--ink);font-family:var(--sans);font-size:14px}
  .geo{border:1px solid var(--edge);border-radius:8px;background:var(--surface);color:var(--ink);font-family:var(--sans);font-size:13px;padding:8px 14px;cursor:pointer}
  .geo:hover{border-color:var(--green)}
  .geo.active{border-color:var(--green);color:var(--green)}
  .chips{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:12px}
  .chip{border:1px solid var(--edge);border-radius:20px;padding:6px 12px;font-size:12px;color:var(--dim);cursor:pointer;background:transparent}
  .chip.on{background:var(--green);color:var(--on-accent);border-color:var(--green);font-weight:700}
  .filters{display:flex;align-items:center;gap:16px;margin-bottom:18px;flex-wrap:wrap}
  .chk{font-size:13px;color:var(--ink);display:flex;align-items:center;gap:7px;cursor:pointer}
  .chk input{accent-color:var(--green)}
  .count{font-size:12px;color:var(--dim);font-variant-numeric:tabular-nums}
  .results{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
  .lab{border:1px solid var(--line);border-radius:11px;background:var(--surface);padding:15px 16px;display:flex;flex-direction:column}
  .lab-top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
  .lab-name{font-size:15px;font-weight:700;line-height:1.25}
  .lab-loc{font-size:12px;color:var(--dim);margin-top:3px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
  .dist{color:var(--green);font-weight:600;font-variant-numeric:tabular-nums}
  .badge{font-size:9px;letter-spacing:.06em;text-transform:uppercase;padding:4px 8px;border-radius:20px;border:1px solid currentColor;white-space:nowrap;flex:0 0 auto}
  .badge.ok{color:var(--ok)}.badge.warn{color:var(--warn)}.badge.bad{color:var(--bad)}.badge.dim{color:var(--dim)}
  .lab-desc{font-size:12.5px;color:var(--dim);line-height:1.5;margin:10px 0}
  .lab-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:8px}
  .src{font-size:9.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--dim);border:1px solid var(--edge);border-radius:4px;padding:2px 6px}
  .lab-acts{display:flex;gap:8px;align-items:center;margin-top:12px;flex-wrap:wrap}
  .lab-a{font-size:12px;color:var(--green);text-decoration:none}
  .lab-a:hover{text-decoration:underline}
  .lab-b{margin-left:auto;font-size:12px;border:1px solid var(--edge);border-radius:7px;background:transparent;color:var(--ink);font-family:var(--sans);padding:7px 11px;cursor:pointer}
  .lab-b:hover{border-color:var(--green);color:var(--green)}
  .empty{color:var(--dim);font-size:14px;padding:30px 0}
  .scrim{position:fixed;inset:0;background:var(--scrim);backdrop-filter:blur(3px);z-index:40;display:none;align-items:center;justify-content:center;padding:20px}
  .scrim.show{display:flex}
  .pop{width:min(560px,100%);max-height:88vh;overflow:auto;background:var(--panel);border:1px solid var(--edge);border-radius:13px;box-shadow:0 24px 70px var(--shadow)}
  .pop-top{display:flex;justify-content:space-between;align-items:center;padding:15px 17px;border-bottom:1px solid var(--edge)}
  .pop-top b{font-size:15px}
  .x{background:transparent;border:1px solid var(--edge);color:var(--ink);width:30px;height:30px;border-radius:7px;cursor:pointer}
  .pop-body{padding:15px 17px}
  .pop-note{font-size:12px;color:var(--dim);line-height:1.5;margin:0 0 10px}
  #msg{width:100%;height:230px;resize:vertical;background:var(--surface-2);color:var(--ink);border:1px solid var(--edge);border-radius:9px;padding:12px;font-family:var(--sans);font-size:12.5px;line-height:1.55}
  .pop-acts{display:flex;gap:9px;margin-top:12px;flex-wrap:wrap}
  .cp{border:0;border-radius:8px;background:var(--green);color:var(--on-accent);font-family:var(--sans);font-weight:700;font-size:13px;padding:10px 15px;cursor:pointer}
  .go{border:1px solid var(--edge);border-radius:8px;color:var(--ink);text-decoration:none;font-size:13px;padding:10px 15px}
  .go:hover{border-color:var(--green);color:var(--green)}
  @media(max-width:600px){.lab-b{margin-left:0}}
</style>
"""

# ------------------------------------------------------------------ COSTS PAGE
COSTS_BODY = r"""
</head>
<body>
<header>
  <div class="brand">lab cost calculator<small>what a training program costs</small></div>
  <div class="grow"></div>
  __NAV__
  <button class="themeBtn" id="themeBtn" type="button" aria-label="Toggle theme">◐</button>
</header>
<main>
  <h1 class="page">What would a hands-on program cost?</h1>
  <p class="lead">Equipment is a one-time, shared cost; consumables scale per student. Pick who it&rsquo;s for, how you&rsquo;ll
  buy, and which tracks to teach &mdash; the estimate updates live. Planning figures only (&plusmn;~30%); see the
  <a href="https://crablaboratory.com/" target="_blank" rel="noopener">lab-in-a-box</a> end of the spectrum too.</p>

  <div class="calc">
    <div class="panel inputs">
      <div class="grp">
        <div class="glabel">Who is it for?</div>
        <div class="seg" id="mode">
          <button data-mode="individual" class="on">Individual</button>
          <button data-mode="group">Group / cohort</button>
        </div>
      </div>
      <div class="grp" id="groupInputs" style="display:none">
        <label class="fld"><span>Cohort size <b id="nOut">12</b></span>
          <input type="range" id="n" min="1" max="32" value="12"></label>
        <label class="fld"><span>How many cohorts <b id="cOut">1</b></span>
          <input type="range" id="cohorts" min="1" max="10" value="1"></label>
      </div>
      <div class="grp">
        <div class="glabel">How will you get the gear?</div>
        <div class="seg wide" id="proc">
          <button data-proc="retail" class="on">Buy retail</button>
          <button data-proc="diy">DIY-build</button>
          <button data-proc="share">Share / rent</button>
        </div>
        <div class="phint" id="procHint"></div>
      </div>
      <div class="grp">
        <div class="glabel">Which tracks?</div>
        <div id="tracks" class="tracks"></div>
      </div>
    </div>

    <div class="panel out">
      <div class="big"><div class="big-num" id="perStudent">$0</div><div class="big-lbl">per student</div></div>
      <div class="rows">
        <div class="orow"><span>One-time equipment</span><b id="capex">$0</b></div>
        <div class="orow"><span>Consumables (all students)</span><b id="cons">$0</b></div>
        <div class="orow total"><span>Total program cost</span><b id="total">$0</b></div>
      </div>
      <div class="students" id="students"></div>
      <div class="notes" id="notes"></div>
    </div>
  </div>
</main>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
  "use strict";
  var M=JSON.parse(document.getElementById('data').textContent);
  __THEME_JS__

  var EQ={}; M.equipment.forEach(function(e){EQ[e.id]=e;});
  var mode='individual', proc='retail';
  var selected={}; M.tracks.forEach(function(t){selected[t.id]=!!t.recommended;});

  // build track checkboxes
  document.getElementById('tracks').innerHTML=M.tracks.map(function(t){
    return '<label class="trk"><input type="checkbox" data-t="'+t.id+'"'+(t.recommended?' checked':'')+'>'
      +'<span class="tk-name">'+esc(t.name)+(t.facility?' <em class="fac">facility</em>':'')+'</span>'
      +'<span class="tk-desc">'+esc(t.desc)+'</span></label>';
  }).join('');
  document.querySelectorAll('#tracks input').forEach(function(c){
    c.addEventListener('change',function(){selected[c.getAttribute('data-t')]=c.checked;calc();});
  });

  document.querySelectorAll('#mode button').forEach(function(b){b.addEventListener('click',function(){
    mode=b.getAttribute('data-mode');document.querySelectorAll('#mode button').forEach(function(x){x.classList.toggle('on',x===b);});
    document.getElementById('groupInputs').style.display=mode==='group'?'':'none';calc();});});
  document.querySelectorAll('#proc button').forEach(function(b){b.addEventListener('click',function(){
    proc=b.getAttribute('data-proc');document.querySelectorAll('#proc button').forEach(function(x){x.classList.toggle('on',x===b);});calc();});});
  var nEl=document.getElementById('n'),cEl=document.getElementById('cohorts');
  nEl.addEventListener('input',function(){document.getElementById('nOut').textContent=nEl.value;calc();});
  cEl.addEventListener('input',function(){document.getElementById('cOut').textContent=cEl.value;calc();});

  var PROC_HINT={retail:'Off-the-shelf education kits & instruments.',
    diy:'Open-hardware builds where they exist (still-air box, DIY centrifuge, OpenPCR…) — cheaper, but ~40-100h of build time.',
    share:'Big instruments (Opentrons, qPCR, sequencer) are rented at a community lab / core instead of bought.'};
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function money(x){return '$'+Math.round(x).toLocaleString();}

  function eqPrice(e){
    if(proc==='diy')return e.diy!=null?e.diy:e.retail;
    return e.retail;
  }

  function calc(){
    document.getElementById('procHint').textContent=PROC_HINT[proc];
    var tracks=M.tracks.filter(function(t){return selected[t.id];});
    // union of equipment
    var eqset={}; tracks.forEach(function(t){t.equipment.forEach(function(id){eqset[id]=1;});});
    var capex=0,bigCapex=0,retailCapex=0,diyCapex=0,anyFacility=false;
    Object.keys(eqset).forEach(function(id){
      var e=EQ[id]; if(!e)return;
      var share_excluded=(proc==='share'&&e.big);
      if(!share_excluded){capex+=eqPrice(e); if(e.big)bigCapex+=eqPrice(e);}
      retailCapex+=e.retail; diyCapex+=(e.diy!=null?e.diy:e.retail);
    });
    tracks.forEach(function(t){if(t.facility)anyFacility=true;});

    var perStudentCons=0; tracks.forEach(function(t){perStudentCons+=t.perStudent;});
    if(proc==='share')perStudentCons+=M.shareModel.benchFeePerStudent;

    var N=mode==='group'?parseInt(nEl.value,10):1;
    var cohorts=mode==='group'?parseInt(cEl.value,10):1;
    var students=Math.max(1,N*cohorts);
    var consTotal=perStudentCons*students;
    var total=capex+consTotal;
    var per=total/students;

    document.getElementById('capex').textContent=money(capex);
    document.getElementById('cons').textContent=money(consTotal);
    document.getElementById('total').textContent=money(total);
    document.getElementById('perStudent').textContent=money(per);
    document.getElementById('students').textContent=(mode==='group'
      ? N+' × '+cohorts+' cohort'+(cohorts>1?'s':'')+' = '+students+' learners'
      : 'a single learner');

    // guidance
    var notes=[];
    if(!tracks.length){notes.push(['warn','Pick at least one track to see an estimate.']);}
    if(bigCapex>0){
      var perBig=bigCapex/students;
      if(perBig>150){
        var need=Math.ceil(bigCapex/150);
        notes.push(['warn','Big instruments add '+money(perBig)+'/student here. They only get cheap when shared — you’d need ~'+need+' learners to bring that under ~$150/student. Below that, use <b>Share / rent</b>.']);
      } else {
        notes.push(['ok','At this scale the big instruments amortise to '+money(perBig)+'/student — owning them is reasonable.']);
      }
    }
    if(proc!=='diy'){
      var save=retailCapex-diyCapex;
      if(save>300)notes.push(['ok','DIY-building the gear would cut equipment by ~'+money(save)+' (trading ~40-100h of build time). Try the <b>DIY-build</b> option.']);
    }
    if(proc==='share'){notes.push(['info',M.shareModel.note]);}
    if(anyFacility){notes.push(['warn','A selected track (cell culture / flow) realistically needs a shared <b>BSL-2 / core facility</b> — budget bench-time there rather than a home setup.']);}
    if(mode==='individual'&&capex>1500){notes.push(['info','For one learner this much equipment rarely pays off — consider a <a href="https://crablaboratory.com/" target="_blank" rel="noopener">lab-in-a-box</a> ($40-170) or a community lab instead.']);}

    document.getElementById('notes').innerHTML=notes.map(function(n){
      return '<div class="nt '+n[0]+'">'+n[1]+'</div>';}).join('');
  }
  calc();
})();
</script>
</body>
</html>
"""

COSTS_CSS = r"""
<style>
  .calc{display:grid;grid-template-columns:1.15fr 0.85fr;gap:18px;align-items:start}
  .panel{border:1px solid var(--line);border-radius:12px;background:var(--surface);padding:18px}
  .grp{margin-bottom:18px}
  .grp:last-child{margin-bottom:0}
  .glabel{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-bottom:9px}
  .seg{display:inline-flex;border:1px solid var(--edge);border-radius:8px;overflow:hidden;flex-wrap:wrap}
  .seg.wide{display:flex}
  .seg button{background:transparent;border:0;color:var(--dim);font-family:var(--sans);font-size:13px;padding:9px 15px;cursor:pointer;flex:1}
  .seg button.on{background:var(--green);color:var(--on-accent);font-weight:700}
  .phint{font-size:11.5px;color:var(--dim);line-height:1.5;margin-top:8px}
  .fld{display:block;margin-bottom:14px}
  .fld span{display:block;font-size:12.5px;color:var(--ink);margin-bottom:6px}
  .fld b{color:var(--green);font-variant-numeric:tabular-nums}
  .fld input[type=range]{width:100%;accent-color:var(--green)}
  .tracks{display:flex;flex-direction:column;gap:8px}
  .trk{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;align-items:baseline;border:1px solid var(--line);border-radius:9px;padding:10px 12px;cursor:pointer}
  .trk:hover{border-color:var(--edge)}
  .trk input{grid-row:span 2;align-self:center;accent-color:var(--green);width:16px;height:16px}
  .tk-name{font-size:13px;font-weight:600}
  .tk-desc{grid-column:2;font-size:11px;color:var(--dim);line-height:1.4}
  .fac{font-style:normal;font-size:8.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--warn);border:1px solid var(--warn);border-radius:4px;padding:1px 5px;margin-left:5px}
  .out{position:sticky;top:70px}
  .big{text-align:center;padding:8px 0 16px;border-bottom:1px solid var(--line);margin-bottom:14px}
  .big-num{font-size:44px;font-weight:800;letter-spacing:-.03em;color:var(--green);line-height:1;font-variant-numeric:tabular-nums}
  .big-lbl{font-size:12px;color:var(--dim);margin-top:5px}
  .rows{display:flex;flex-direction:column;gap:9px}
  .orow{display:flex;justify-content:space-between;font-size:13px;color:var(--dim)}
  .orow b{color:var(--ink);font-variant-numeric:tabular-nums}
  .orow.total{border-top:1px solid var(--line);padding-top:9px;margin-top:2px;color:var(--ink);font-weight:600}
  .orow.total b{color:var(--green);font-size:15px}
  .students{font-size:11.5px;color:var(--dim);text-align:center;margin:12px 0}
  .notes{display:flex;flex-direction:column;gap:8px}
  .nt{font-size:11.5px;line-height:1.5;padding:9px 11px;border-radius:8px;border-left:3px solid var(--edge);background:var(--surface-2)}
  .nt b{color:var(--ink)} .nt a{color:var(--green)}
  .nt.ok{border-left-color:var(--ok)} .nt.warn{border-left-color:var(--warn)} .nt.info{border-left-color:var(--info)}
  @media(max-width:860px){.calc{grid-template-columns:1fr}.out{position:static}}
</style>
"""


def build_page(head_title, desc, css, body, active, data_obj):
    head = SHARED_HEAD.replace("__TITLE__", head_title).replace("__DESC__", desc)
    html = head + css + body
    html = html.replace("__NAV__", nav(active))
    html = html.replace("__THEME_JS__", THEME_JS)
    blob = json.dumps(data_obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = html.replace("__DATA__", blob)
    # unescape the \uXXXX we wrote as literal button glyphs in the body templates
    return html


def main():
    labs = json.loads(LABS.read_text(encoding="utf-8"))
    costs = json.loads(COSTS.read_text(encoding="utf-8"))

    labs_html = build_page(
        "Find a Community Lab — Biotech Skill Tree",
        "Find community & DIY biolabs worldwide and draft an outreach message to get hands-on access to equipment and space.",
        LABS_CSS, LABS_BODY, "labs", labs,
    )
    costs_html = build_page(
        "Lab Cost Calculator — Biotech Skill Tree",
        "Estimate what a hands-on biotech training program costs for an individual or a cohort - equipment, consumables, and break-even.",
        COSTS_CSS, COSTS_BODY, "costs", costs,
    )

    # the button glyph placeholders ◐ were written literally in the body strings
    labs_html = labs_html.replace("\\u25d0", "◐")
    costs_html = costs_html.replace("\\u25d0", "◐")

    (OUT / "labs.html").write_text(labs_html, encoding="utf-8")
    (OUT / "costs.html").write_text(costs_html, encoding="utf-8")
    print(f"wrote viewer/labs.html  ({len(labs_html)//1024} KB, {len(labs['labs'])} labs)")
    print(f"wrote viewer/costs.html ({len(costs_html)//1024} KB, {len(costs['tracks'])} tracks)")


if __name__ == "__main__":
    main()
