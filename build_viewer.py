#!/usr/bin/env python3
"""Build a self-contained, interactive viewer for the synthetic-biology skill tree.

Reads the tree graph (src/data/trees/synthetic-biology.json) and every per-node
detail file (src/data/skill_nodes/*.json), embeds them inline as JSON, and emits
viewer/index.html -- a single file that renders the dependency graph with
click-to-open popups, search, progress tracking, and a mobile list view.

No third-party dependencies. Run:  python build_viewer.py
Then serve:  python -m http.server 8000  (open http://localhost:8000/viewer/)
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
TREE = ROOT / "src" / "data" / "trees" / "synthetic-biology.json"
NODES_DIR = ROOT / "src" / "data" / "skill_nodes"
QUESTIONS = ROOT / "src" / "data" / "interview_questions.json"
HTGAA = ROOT / "src" / "data" / "htgaa_companion.json"
OUT = ROOT / "viewer" / "index.html"


def load_data():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    details = {}
    for f in sorted(NODES_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        details[d["id"]] = d
    questions = []
    if QUESTIONS.exists():
        questions = json.loads(QUESTIONS.read_text(encoding="utf-8")).get("questions", [])
    htgaa = {}
    if HTGAA.exists():
        htgaa = json.loads(HTGAA.read_text(encoding="utf-8"))
    return {"tree": tree, "details": details, "questions": questions, "htgaa": htgaa}


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
<title>Synthetic Biology Skill Tree</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>
/* Set the theme before first paint so there is no flash of the wrong scheme.
   An explicit choice wins; otherwise follow the OS preference. */
(function(){try{
  var t=localStorage.getItem('synbio-theme');
  if(t!=='light'&&t!=='dark'){
    t=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches)?'light':'dark';
  }
  document.documentElement.setAttribute('data-theme',t);
}catch(e){document.documentElement.setAttribute('data-theme','dark');}})();
</script>
<style>
  /* Inter: an open, Helvetica-style neo-grotesque. --mono/--disp are kept as
     names so every existing rule keeps working; both now resolve to Inter. */
  :root{
    --sans:'Inter','Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif;
    --mono:var(--sans);
    --disp:var(--sans);

    /* ---- dark (default) ---- */
    --bg:#0a0b0a; --bg2:#111311; --ink:#e9f0e2; --dim:#8a9683;
    --green:#c6f24e; --green-dim:#7f9a3a; --orange:#ff7a2f; --line:#2a3226;
    --panel:#14170f; --edge:#3a4531; --edge-hot:#c6f24e;
    --on-accent:#0a0b0a;
    --surface:var(--surface); --surface-2:var(--surface-2); --surface-3:var(--surface-3);
    --node-a:#171b13; --node-b:#0f120c;
    --head-a:#101210; --head-b:#0c0e0c;
    --panel-top-a:#191d12; --panel-top-b:#14170f;
    --track:var(--track); --expl-bg:var(--expl-bg); --tier:var(--tier);
    --info:var(--info); --info-edge:var(--info-edge); --info-a:#0d1620; --info-b:#0b1118;
    --scrim:rgba(4,5,4,.72); --scanline:rgba(255,255,255,.015);
    --shadow:rgba(0,0,0,.5); --shadow-lg:rgba(0,0,0,.7);
    --ok-tint:rgba(198,242,78,.10); --warn-tint:rgba(255,122,47,.10); --warn-ring:rgba(255,122,47,.5);
    --scheme:dark;
  }
  /* ---- light ---- */
  :root[data-theme="light"]{
    --bg:#fcfcfb; --bg2:#f4f5f2; --ink:#16191c; --dim:#5f6a72;
    --green:#4d7c0f; --green-dim:#7ba32f; --orange:#c2410c; --line:#e4e6e1;
    --panel:#ffffff; --edge:#cfd4c9; --edge-hot:#4d7c0f;
    --on-accent:#ffffff;
    --surface:#ffffff; --surface-2:#fafbf8; --surface-3:#ffffff;
    --node-a:#ffffff; --node-b:#f7f8f5;
    --head-a:#ffffff; --head-b:#f6f7f4;
    --panel-top-a:#f7f8f5; --panel-top-b:#ffffff;
    --track:#e6e8e2; --expl-bg:#f5f8ee; --tier:#c9cfc2;
    --info:#1e6fa8; --info-edge:#b8d4e8; --info-a:#f2f8fc; --info-b:#eaf3fa;
    --scrim:rgba(22,25,28,.42); --scanline:rgba(0,0,0,.012);
    --shadow:rgba(16,20,24,.10); --shadow-lg:rgba(16,20,24,.18);
    --ok-tint:rgba(77,124,15,.10); --warn-tint:rgba(194,65,12,.10); --warn-ring:rgba(194,65,12,.45);
    --scheme:light;
  }
  :root{color-scheme:var(--scheme)}
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);font-family:var(--mono);
    -webkit-font-smoothing:antialiased;overflow:hidden}
  body{background-image:repeating-linear-gradient(0deg,var(--scanline) 0 1px,transparent 1px 3px)}
  a{color:var(--green)}
  #app{position:fixed;inset:0;display:flex;flex-direction:column}

  header{flex:0 0 auto;padding:12px 16px;border-bottom:1px solid var(--line);
    background:linear-gradient(180deg,var(--head-a),var(--head-b));z-index:20}
  .hrow{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
  .brand{font-family:var(--disp);font-weight:800;font-size:18px;letter-spacing:-.021em;color:var(--green);
    text-transform:lowercase;white-space:nowrap}
  .brand small{display:block;font-family:var(--mono);font-weight:400;font-size:10px;color:var(--dim);letter-spacing:.14em;text-transform:uppercase}
  .grow{flex:1 1 auto}
  .toggle{display:flex;border:1px solid var(--edge);border-radius:6px;overflow:hidden}
  .toggle button{background:transparent;color:var(--dim);border:0;padding:7px 12px;font-family:var(--mono);
    font-size:12px;cursor:pointer}
  .toggle button.on{background:var(--green);color:var(--on-accent);font-weight:600}
  .themeBtn{flex:0 0 auto;width:34px;height:34px;border-radius:8px;border:1px solid var(--edge);
    background:var(--surface);color:var(--ink);font-size:15px;line-height:1;cursor:pointer}
  .themeBtn:hover{border-color:var(--green);color:var(--green)}
  .pagenav{display:flex;gap:6px}
  .pagenav a{font-size:12px;padding:7px 11px;border:1px solid var(--edge);border-radius:7px;color:var(--dim);text-decoration:none;white-space:nowrap}
  .pagenav a:hover{border-color:var(--green);color:var(--green)}
  .search{flex:1 1 220px;min-width:140px;display:flex;align-items:center;gap:8px;
    border:1px solid var(--edge);border-radius:6px;padding:6px 10px;background:var(--surface-3)}
  .search input{flex:1;background:transparent;border:0;outline:0;color:var(--ink);font-family:var(--mono);font-size:13px}
  .search span{color:var(--dim)}
  .stats{display:flex;gap:14px;font-size:11px;color:var(--dim);margin-top:8px;flex-wrap:wrap}
  .stats b{color:var(--green)}
  .legend{display:flex;gap:14px;font-size:10px;color:var(--dim);margin-top:6px;flex-wrap:wrap}
  .legend i{font-style:normal}
  .dot{display:inline-block;width:9px;height:9px;border-radius:50%;vertical-align:middle;margin-right:4px}

  main{flex:1 1 auto;position:relative;overflow:hidden}

  /* ---------- MAP ---------- */
  #map{position:absolute;inset:0;cursor:grab;touch-action:none}
  #map.drag{cursor:grabbing}
  #canvas{position:absolute;top:0;left:0;transform-origin:0 0;will-change:transform}
  svg.edges{position:absolute;top:0;left:0;overflow:visible;pointer-events:none}
  .node{position:absolute;transform:translate(-50%,-50%);width:150px;padding:9px 11px;border-radius:9px;
    border:1px solid var(--edge);background:linear-gradient(180deg,var(--node-a),var(--node-b));cursor:pointer;
    transition:border-color .15s,box-shadow .15s,transform .1s;user-select:none}
  .node:hover{border-color:var(--green);box-shadow:0 0 0 1px var(--green),0 6px 24px var(--shadow);z-index:5}
  .node .nt{font-size:11.5px;line-height:1.25;letter-spacing:.01em}
  .node .nm{font-size:9px;color:var(--dim);margin-top:5px;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
  .node .glyphs{font-size:10px;letter-spacing:2px}
  /* every node is open/navigable - 'open' is a soft de-emphasis, never a lock */
  .node.open{opacity:.92}
  .node.next{border-color:var(--orange);box-shadow:0 0 0 1px var(--warn-ring)}
  .node.next::after{content:"";position:absolute;inset:-3px;border-radius:11px;border:1px solid var(--orange);
    animation:pulse 1.6s ease-in-out infinite;pointer-events:none}
  @keyframes pulse{0%,100%{opacity:.15}50%{opacity:.8}}
  .node.done{border-color:var(--green-dim)}
  .node.done .nt{color:var(--green)}
  .node.main{border-left:3px solid var(--green)}
  .node.dim{opacity:.12;filter:grayscale(1)}
  .tierlab{position:absolute;left:8px;font-family:var(--disp);font-weight:800;font-size:11px;color:var(--tier);
    letter-spacing:.2em;writing-mode:vertical-rl;text-transform:uppercase;pointer-events:none}

  .ctl{position:absolute;right:14px;bottom:14px;display:flex;flex-direction:column;gap:6px;z-index:10}
  .ctl button{width:38px;height:38px;border-radius:8px;border:1px solid var(--edge);background:var(--surface);
    color:var(--ink);font-size:17px;cursor:pointer}
  .ctl button:hover{border-color:var(--green)}
  .hint{position:absolute;left:14px;bottom:12px;font-size:10px;color:var(--dim);z-index:10}

  /* ---------- LIST ---------- */
  #list{position:absolute;inset:0;overflow:auto;padding:16px;display:none}
  .tiergrp{margin-bottom:20px}
  .tiergrp h3{font-family:var(--disp);font-weight:800;font-size:12px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--dim);border-left:3px solid var(--green);padding-left:9px;margin:0 0 10px}
  .li{display:flex;align-items:center;gap:12px;padding:13px 12px;border:1px solid var(--line);border-radius:9px;
    margin-bottom:8px;cursor:pointer;background:var(--surface-2);min-height:54px}
  .li:hover{border-color:var(--green)}
  .li .bar{width:4px;align-self:stretch;border-radius:3px;background:var(--edge)}
  .li.main .bar{background:var(--green)}
  .li .txt{flex:1;min-width:0}
  .li .txt b{font-size:13px;font-weight:400;display:block}
  .li .txt small{color:var(--dim);font-size:10.5px;display:block;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .li .glyphs{font-size:11px;letter-spacing:2px;color:var(--dim)}
  .pill{font-size:9px;padding:3px 7px;border-radius:20px;border:1px solid var(--edge);color:var(--dim);white-space:nowrap}
  .pill.next{color:var(--orange);border-color:var(--orange)}
  .pill.done{color:var(--green);border-color:var(--green-dim)}
  .pill.open{color:var(--dim);border-color:var(--edge)}

  /* ---------- INTERVIEW ---------- */
  #interview{position:absolute;inset:0;overflow:auto;padding:22px 18px 60px;display:none}
  .iv-wrap{max-width:760px;margin:0 auto}
  .iv-h{font-family:var(--disp);font-weight:800;font-size:22px;letter-spacing:-.024em;margin:4px 0 4px}
  .iv-sub{color:var(--dim);font-size:12.5px;line-height:1.5;margin-bottom:20px}
  .iv-card{border:1px solid var(--edge);border-radius:12px;background:var(--surface-2);padding:18px;margin-bottom:16px}
  .iv-card h3{font-family:var(--disp);font-weight:800;font-size:13px;letter-spacing:.12em;text-transform:uppercase;
    color:var(--green);margin:0 0 12px}
  .roles{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  .role{border:1px solid var(--edge);border-radius:11px;padding:16px;cursor:pointer;background:var(--surface);transition:border-color .15s}
  .role:hover,.role.sel{border-color:var(--green);box-shadow:0 0 0 1px var(--green)}
  .role b{display:block;font-family:var(--disp);font-weight:800;font-size:15px;letter-spacing:-.018em;margin-bottom:6px}
  .role small{color:var(--dim);font-size:11.5px;line-height:1.45;display:block}
  .role .ic{font-size:22px;margin-bottom:8px;display:block}
  .fld{margin-bottom:14px}
  .fld label{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-bottom:7px}
  .chips{display:flex;gap:7px;flex-wrap:wrap}
  .chip{border:1px solid var(--edge);border-radius:20px;padding:7px 13px;font-size:12px;cursor:pointer;color:var(--dim);background:transparent}
  .chip.on{background:var(--green);color:var(--on-accent);border-color:var(--green);font-weight:700}
  .iv-start{width:100%;padding:14px;border:0;border-radius:10px;background:var(--green);color:var(--on-accent);
    font-family:var(--mono);font-weight:700;font-size:14px;cursor:pointer;margin-top:4px}
  .iv-start:disabled{background:var(--surface);color:var(--dim);cursor:not-allowed}

  .qbar{display:flex;align-items:center;gap:12px;margin-bottom:14px}
  .qbar .prog{flex:1;height:6px;border-radius:6px;background:var(--track);overflow:hidden}
  .qbar .prog i{display:block;height:100%;background:var(--green);width:0;transition:width .25s}
  .qbar .cnt{font-size:11px;color:var(--dim);white-space:nowrap}
  .qbar .sc{font-size:11px;color:var(--green);white-space:nowrap}
  .qmeta{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
  .badge{font-size:9px;letter-spacing:.08em;text-transform:uppercase;padding:4px 9px;border-radius:20px;border:1px solid var(--edge);color:var(--dim)}
  .badge.f{color:var(--info);border-color:var(--info-edge)}
  .badge.c{color:var(--green);border-color:var(--green-dim)}
  .badge.a{color:var(--orange);border-color:var(--orange)}
  .qprompt{font-size:16px;line-height:1.5;margin:0 0 16px;font-weight:700}
  .opt{display:block;width:100%;text-align:left;border:1px solid var(--edge);border-radius:10px;padding:13px 14px;
    margin-bottom:9px;background:var(--surface);color:var(--ink);font-family:var(--mono);font-size:13px;line-height:1.45;cursor:pointer;transition:border-color .12s}
  .opt:hover:not(:disabled){border-color:var(--green)}
  .opt .k{display:inline-block;width:20px;color:var(--dim);font-weight:700}
  .opt.correct{border-color:var(--green);background:var(--ok-tint);color:var(--green)}
  .opt.wrong{border-color:var(--orange);background:var(--warn-tint);color:var(--orange)}
  .opt:disabled{cursor:default}
  .expl{border-left:3px solid var(--green);background:var(--expl-bg);padding:12px 14px;border-radius:0 8px 8px 0;margin:6px 0 14px}
  .expl b{color:var(--green);font-size:11px;letter-spacing:.1em;text-transform:uppercase;display:block;margin-bottom:6px}
  .expl p{font-size:12.5px;line-height:1.55;margin:0 0 8px}
  .expl .probe{color:var(--dim);font-size:11.5px;font-style:italic}
  .expl a{font-size:11.5px}
  .qnext{width:100%;padding:13px;border:0;border-radius:10px;background:var(--green);color:var(--on-accent);font-family:var(--mono);font-weight:700;font-size:13px;cursor:pointer}
  .qskip{width:100%;padding:11px;border:1px solid var(--edge);border-radius:10px;background:transparent;color:var(--dim);font-family:var(--mono);font-size:12px;cursor:pointer;margin-top:8px}

  .score-big{font-family:var(--disp);font-weight:800;font-size:52px;letter-spacing:-.03em;color:var(--green);line-height:1}
  .score-lbl{color:var(--dim);font-size:12px;margin-top:6px}
  .brk{display:flex;flex-direction:column;gap:8px;margin:14px 0}
  .brk-row{display:flex;align-items:center;gap:10px;font-size:12px}
  .brk-row .nm{flex:0 0 150px;color:var(--dim)}
  .brk-row .bar2{flex:1;height:8px;border-radius:6px;background:var(--track);overflow:hidden}
  .brk-row .bar2 i{display:block;height:100%;background:var(--green)}
  .brk-row .v{flex:0 0 52px;text-align:right;color:var(--ink)}
  .miss{border:1px solid var(--line);border-radius:10px;padding:13px;margin-bottom:10px}
  .miss .mq{font-size:13px;font-weight:700;margin-bottom:8px}
  .miss .ma{font-size:12px;margin:3px 0}
  .miss .ma.good{color:var(--green)}
  .miss .ma.bad{color:var(--orange)}
  .miss .mx{font-size:11.5px;color:var(--dim);line-height:1.5;margin-top:6px}

  /* interviewer kit */
  .kit-q{border:1px solid var(--line);border-radius:10px;padding:14px;margin-bottom:10px}
  .kit-q .kp{font-size:13.5px;font-weight:700;margin-bottom:9px}
  .kit-q .ko{font-size:12px;color:var(--dim);margin:3px 0;padding-left:6px}
  .kit-q .ko.ans{color:var(--green);font-weight:700}
  .kit-q .kx{font-size:12px;color:var(--ink);line-height:1.55;margin-top:9px;border-top:1px solid var(--line);padding-top:9px}
  .kit-q .kprobe{font-size:11.5px;color:var(--orange);margin-top:7px;font-style:italic}
  .kit-topic{font-family:var(--disp);font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin:18px 0 10px}
  @media print{
    header,.iv-controls{display:none!important}
    #interview{position:static;overflow:visible}
    body{background:#fff;color:#000}
    .kit-q{border-color:#ccc;break-inside:avoid}
    .kit-q .ko.ans{color:#060}
  }
  @media (max-width:720px){.roles{grid-template-columns:1fr}.brk-row .nm{flex-basis:110px}}

  /* ---------- POPUP ---------- */
  #scrim{position:fixed;inset:0;background:var(--scrim);backdrop-filter:blur(3px);z-index:40;
    display:none;align-items:center;justify-content:center;padding:20px}
  #scrim.show{display:flex}
  #pop{width:min(640px,100%);max-height:88vh;overflow:auto;background:var(--panel);border:1px solid var(--edge);
    border-radius:14px;box-shadow:0 24px 80px var(--shadow-lg);animation:pin .18s ease}
  @keyframes pin{from{transform:scale(.96);opacity:0}to{transform:scale(1);opacity:1}}
  #pop .top{position:sticky;top:0;background:linear-gradient(180deg,var(--panel-top-a),var(--panel-top-b));padding:16px 18px;
    border-bottom:1px solid var(--edge);display:flex;gap:12px;align-items:flex-start}
  #pop .top .x{margin-left:auto;background:transparent;border:1px solid var(--edge);color:var(--ink);
    width:30px;height:30px;border-radius:7px;cursor:pointer;font-size:15px;flex:0 0 auto}
  #pop h2{font-family:var(--disp);font-weight:800;font-size:20px;margin:0;letter-spacing:-.022em}
  #pop .meta{font-size:10px;color:var(--dim);letter-spacing:.1em;text-transform:uppercase;margin-top:6px}
  #pop .body{padding:16px 18px}
  #pop section{margin-bottom:18px}
  #pop h4{font-family:var(--disp);font-weight:800;font-size:11px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--green);margin:0 0 8px}
  #pop p{font-size:13px;line-height:1.55;color:var(--ink);margin:0 0 8px}
  #pop ul{margin:0;padding-left:18px}
  #pop li{font-size:12.5px;line-height:1.5;margin-bottom:5px}
  .req{display:flex;align-items:center;gap:8px;font-size:12.5px;margin-bottom:5px}
  .req .m{font-size:13px}
  .req.ok{color:var(--green)}.req.no{color:var(--dim)}
  .req a.jump{color:inherit;text-decoration:none;border-bottom:1px dotted currentColor}
  .req a.jump:hover{color:var(--green);border-bottom-color:var(--green)}
  .freenote{font-size:11px;color:var(--dim);font-style:italic;margin-top:8px;padding-left:2px}
  .steps{counter-reset:s}
  .step{display:flex;gap:11px;margin-bottom:9px}
  .step .n{flex:0 0 auto;width:22px;height:22px;border-radius:50%;border:1px solid var(--edge);
    display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--green)}
  .step b{font-size:12.5px;font-weight:700}
  .step small{display:block;font-size:11.5px;color:var(--dim);margin-top:2px}
  .vid{position:relative;aspect-ratio:16/9;border-radius:9px;overflow:hidden;border:1px solid var(--edge);background:#000}
  .vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
  .watch{display:inline-flex;align-items:center;gap:8px;padding:11px 14px;border:1px solid var(--edge);
    border-radius:9px;color:var(--green);text-decoration:none;font-size:12.5px}
  .watch:hover{border-color:var(--green)}
  .res a{display:block;padding:9px 11px;border:1px solid var(--line);border-radius:8px;margin-bottom:6px;
    font-size:12px;text-decoration:none;color:var(--ink)}
  .res a:hover{border-color:var(--green);color:var(--green)}
  .res a span{color:var(--dim);font-size:10px}
  .kits{display:flex;flex-direction:column;gap:8px}
  .kit{display:block;padding:11px 12px;border:1px solid var(--line);border-radius:9px;text-decoration:none;
    color:var(--ink);background:var(--surface-2);transition:border-color .12s}
  .kit:hover{border-color:var(--green)}
  .kit .kn{font-size:12.5px;font-weight:600;line-height:1.3}
  .kit .ktag{font-style:normal;font-size:9px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
    color:var(--info);border:1px solid var(--info-edge);border-radius:20px;padding:1px 6px;margin-left:5px;vertical-align:middle}
  .kit .km{display:flex;justify-content:space-between;gap:8px;margin:4px 0 5px;font-size:11px;color:var(--dim)}
  .kit .km b{color:var(--green);font-weight:700;white-space:nowrap}
  .kit .kd{font-size:11.5px;line-height:1.45;color:var(--dim)}
  .htgaa{border:1px solid var(--info-edge);border-radius:10px;background:linear-gradient(180deg,var(--info-a),var(--info-b));padding:13px 15px}
  .htgaa .hh{display:flex;align-items:center;gap:8px;font-family:var(--disp);font-weight:800;font-size:11px;
    letter-spacing:.12em;text-transform:uppercase;color:var(--info);margin-bottom:8px}
  .htgaa .wk{font-size:13px;font-weight:700;margin-bottom:3px}
  .htgaa .mod{font-size:12.5px;color:var(--ink);margin-bottom:6px}
  .htgaa .who{font-size:11.5px;color:var(--dim);margin-bottom:9px}
  .htgaa a{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;color:var(--info);text-decoration:none;
    border:1px solid var(--info-edge);border-radius:7px;padding:6px 10px}
  .htgaa a:hover{border-color:var(--info)}
  .cta{width:100%;padding:12px;border-radius:9px;border:0;font-family:var(--mono);font-weight:700;font-size:13px;cursor:pointer}
  .cta.go{background:var(--green);color:var(--on-accent)}
  .cta.done{background:transparent;color:var(--green);border:1px solid var(--green-dim)}
  .cta.wait{background:var(--surface);color:var(--dim);cursor:not-allowed}

  @media (max-width:720px){
    .stats,.legend{display:none}
    #scrim{padding:0;align-items:flex-end}
    #pop{width:100%;max-height:90vh;border-radius:16px 16px 0 0}
    .brand{font-size:16px}
  }
</style>
</head>
<body>
<div id="app">
  <header>
    <div class="hrow">
      <div class="brand">synbio skill tree<small>sterile bench → purified protein</small></div>
      <div class="grow"></div>
      <div class="toggle" id="modeToggle">
        <button data-mode="map" class="on">◆ map</button>
        <button data-mode="list">☰ list</button>
        <button data-mode="interview">◇ interview</button>
      </div>
      <div class="pagenav"><a href="costs.html">$ cost</a><a href="labs.html">⌖ labs</a></div>
      <button class="themeBtn" id="themeBtn" type="button" aria-label="Toggle light or dark theme">◐</button>
    </div>
    <div class="hrow" style="margin-top:10px">
      <label class="search"><span>⌕</span><input id="q" placeholder="search techniques, objectives, projects…" autocomplete="off"></label>
    </div>
    <div class="stats" id="stats"></div>
    <div class="legend">
      <i><span class="dot" style="background:var(--green)"></span>main path</i>
      <i><span class="dot" style="background:var(--orange)"></span>next up (suggested)</i>
      <i><span class="dot" style="background:var(--edge)"></span>open — take in any order</i>
      <i>★ main · ⚙ equipment · ▶ has video · ⬢ HTGAA</i>
    </div>
  </header>
  <main>
    <div id="map">
      <svg class="edges" id="edges"></svg>
      <div id="canvas"></div>
      <div class="ctl">
        <button id="zin">+</button><button id="zout">−</button><button id="zfit">⤢</button><button id="zreset">⟲</button>
      </div>
      <div class="hint" id="hint">drag to pan · scroll to zoom · click a node</div>
    </div>
    <div id="list"></div>
    <div id="interview"></div>
  </main>
</div>

<div id="scrim"><div id="pop"></div></div>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
  "use strict";
  var DATA = JSON.parse(document.getElementById('data').textContent);
  var TREE = DATA.tree, DETAILS = DATA.details;
  var QUESTIONS = DATA.questions || [];
  var HTGAA = DATA.htgaa || {};
  var HMAP = HTGAA.map || {};
  var NODES = TREE.nodes;
  var MAIN = new Set(TREE.mainPathNodes||[]);
  var byId = {}; NODES.forEach(function(n){byId[n.id]=n;});

  // equipment nodes: optional reference cards (depend only on intro, gate nothing)
  var gatesSomething = {};
  NODES.forEach(function(n){(n.dependencies||[]).forEach(function(d){gatesSomething[d]=true;});});
  function isEquip(n){
    var det = DETAILS[n.id]||{};
    var proj = (det.project||'').toLowerCase();
    return proj.indexOf('equip')>=0;
  }

  // ---- progress (localStorage) ----
  var KEY='synbio-progress-v1';
  var done = {};
  try{done = JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){done={};}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(done));}catch(e){}}
  function isDone(id){return !!done[id];}
  function prereqsMet(id){
    var n=byId[id]; if(!n)return true;
    return (n.dependencies||[]).every(isDone);
  }
  // NOTHING IS EVER LOCKED. Every node is open, openable, and completable in any
  // order. Dependencies are shown as suggested trajectory, never as a gate --
  // 'next' merely flags the natural next step along the path.
  function status(id){return isDone(id)?'done':prereqsMet(id)?'next':'open';}
  // reverse index: what each node leads to (for trajectory navigation)
  var childrenOf={};
  NODES.forEach(function(n){
    (n.dependencies||[]).forEach(function(d){(childrenOf[d]=childrenOf[d]||[]).push(n.id);});
  });

  // ---- layout from initialPosition ----
  var xs=NODES.map(function(n){return n.initialPosition[0];});
  var ys=NODES.map(function(n){return n.initialPosition[1];});
  var minX=Math.min.apply(0,xs),maxX=Math.max.apply(0,xs);
  var minY=Math.min.apply(0,ys),maxY=Math.max.apply(0,ys);
  var SX=175, SY=125, PAD=120;
  function px(n){return (n.initialPosition[0]-minX)*SX+PAD;}
  function py(n){return (n.initialPosition[1]-minY)*SY+PAD;}
  var worldW=(maxX-minX)*SX+PAD*2;
  var worldH=(maxY-minY)*SY+PAD*2;

  var canvas=document.getElementById('canvas');
  var edges=document.getElementById('edges');
  var mapEl=document.getElementById('map');

  // ---- render map ----
  var nodeEls={};
  function glyphs(n){
    var g='';
    if(MAIN.has(n.id))g+='★';
    if(isEquip(n))g+='⚙';
    var det=DETAILS[n.id]||{};
    if(det.video&&det.video.url)g+='▶';
    if(HMAP[n.id])g+='⬢';
    return g;
  }
  function buildMap(){
    canvas.style.width=worldW+'px'; canvas.style.height=worldH+'px';
    edges.setAttribute('width',worldW); edges.setAttribute('height',worldH);
    // edges
    var ep='';
    NODES.forEach(function(n){
      (n.dependencies||[]).forEach(function(d){
        var p=byId[d]; if(!p)return;
        var x1=px(p),y1=py(p),x2=px(n),y2=py(n);
        var my=(y1+y2)/2;
        var hot=MAIN.has(n.id)&&MAIN.has(d);
        var equip=isEquip(n)||isEquip(p);
        ep+='<path d="M'+x1+','+y1+' C'+x1+','+my+' '+x2+','+my+' '+x2+','+y2+'" '
          +'fill="none" stroke="'+(hot?'var(--edge-hot)':'var(--edge)')+'" '
          +'stroke-width="'+(hot?2:1.3)+'" '+(equip?'stroke-dasharray="5 4" stroke="var(--orange)" opacity=".55"':'')+'/>';
      });
    });
    edges.innerHTML=ep;
    // nodes
    NODES.forEach(function(n){
      var el=document.createElement('div');
      el.className='node';
      el.style.left=px(n)+'px'; el.style.top=py(n)+'px';
      var det=DETAILS[n.id]||{};
      var proj=(det.project||'');
      el.innerHTML='<div class="nt">'+esc(n.title)+'</div>'
        +'<div class="nm"><span class="glyphs">'+glyphs(n)+'</span>'+(proj?'<span>'+esc(proj)+'</span>':'')+'</div>';
      el.setAttribute('data-node',n.id);
      el.setAttribute('role','button');
      el.tabIndex=0;
      // Primary activation is the map's pointerup (tap-vs-drag aware). This click
      // handler is a belt-and-braces fallback for environments where pointer
      // events behave differently; openPop() is guarded so it can't double-fire.
      el.addEventListener('click',function(ev){
        ev.stopPropagation();
        if(Date.now()-lastTapOpen<500)return; // pointerup already handled this tap
        openPop(n.id);
      });
      el.addEventListener('keydown',function(ev){
        if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();openPop(n.id);}
      });
      canvas.appendChild(el);
      nodeEls[n.id]=el;
    });
    // tier labels down the left gutter, grouped by rounded y
    var tiers={};
    NODES.forEach(function(n){var k=Math.round(n.initialPosition[1]); (tiers[k]=tiers[k]||[]).push(n);});
  }
  function refreshMapStatus(){
    NODES.forEach(function(n){
      var el=nodeEls[n.id]; if(!el)return;
      el.classList.remove('open','next','done','main');
      el.classList.add(status(n.id));
      if(MAIN.has(n.id))el.classList.add('main');
    });
  }

  // ---- render list ----
  var listEl=document.getElementById('list');
  function buildList(){
    // group by tier (rounded y), ordered top→bottom
    var groups={}, order=[];
    NODES.forEach(function(n){
      var k=Math.round(n.initialPosition[1]);
      if(!groups[k]){groups[k]=[];order.push(k);}
      groups[k].push(n);
    });
    order.sort(function(a,b){return a-b;});
    var html='';
    order.forEach(function(k,i){
      var g=groups[k].slice().sort(function(a,b){return a.initialPosition[0]-b.initialPosition[0];});
      html+='<div class="tiergrp"><h3>tier '+(i+1)+'</h3>';
      g.forEach(function(n){
        var det=DETAILS[n.id]||{};
        html+='<div class="li'+(MAIN.has(n.id)?' main':'')+'" data-id="'+n.id+'">'
          +'<div class="bar"></div>'
          +'<div class="txt"><b>'+esc(n.title)+'</b><small>'+esc(n.description||'')+'</small></div>'
          +'<span class="glyphs">'+glyphs(n)+'</span>'
          +'<span class="pill" data-pill="'+n.id+'"></span></div>';
      });
      html+='</div>';
    });
    listEl.innerHTML=html;
    listEl.querySelectorAll('.li').forEach(function(li){
      li.addEventListener('click',function(){openPop(li.getAttribute('data-id'));});
    });
  }
  function refreshListStatus(){
    listEl.querySelectorAll('.pill').forEach(function(p){
      var id=p.getAttribute('data-pill'),s=status(id);
      p.className='pill '+s;
      p.textContent=s==='done'?'done':s==='next'?'next up':'open';
    });
  }

  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  // ---- popup ----
  var scrim=document.getElementById('scrim'),pop=document.getElementById('pop');
  function ytEmbed(url){
    var m=String(url).match(/(?:v=|youtu\.be\/|embed\/)([\w-]{11})/);
    return m?('https://www.youtube.com/embed/'+m[1]):null;
  }
  function openPop(id){
    var n=byId[id],det=DETAILS[id]||{};
    var title=(det.title&&det.title.name)||n.title;
    var ov=det.overview||{}, st=det.steps||{};
    var s=status(id);
    var html='';
    html+='<div class="top"><div><h2>'+esc(title)+'</h2><div class="meta">'
      +esc(det.project||'')+(det.level?' · '+esc(det.level):'')+(det.time?' · ~'+det.time+' min':'')
      +'</div></div><button class="x" id="popx">✕</button></div>';
    html+='<div class="body">';
    // overview
    html+='<section><h4>overview</h4><p>'+esc(ov.description||n.description||'')+'</p></section>';
    // HTGAA course companion
    var hc=HMAP[id];
    if(hc){
      var who=(hc.who&&hc.who.length)?hc.who.join(' · '):'';
      html+='<section><div class="htgaa"><div class="hh">⬢ HTGAA course companion</div>'
        +'<div class="wk">Week '+esc(hc.w)+(hc.date?' · '+esc(hc.date):'')+'</div>'
        +'<div class="mod">'+esc(hc.module)+'</div>'
        +(who?'<div class="who">'+esc(who)+'</div>':'')
        +'<a href="'+esc(HTGAA.link||'https://www.htgaa.org/')+'" target="_blank" rel="noopener">'+esc((HTGAA.course||'HTGAA')+(HTGAA.term?' · '+HTGAA.term:''))+' ↗</a>'
        +'</div></section>';
    }
    // trajectory: builds on / leads to (navigable, never a gate)
    var deps=n.dependencies||[];
    if(deps.length){
      html+='<section><h4>builds on</h4>';
      deps.forEach(function(d){
        var ok=isDone(d);
        html+='<div class="req '+(ok?'ok':'no')+'"><span class="m">'+(ok?'✓':'○')+'</span>'
          +'<a href="#" class="jump" data-jump="'+esc(d)+'">'+esc(byId[d]?byId[d].title:d)+'</a></div>';
      });
      html+='<div class="freenote">Guidance, not a gate — you can start this any time and take skills out of order.</div>';
      html+='</section>';
    }
    var kids=childrenOf[id]||[];
    if(kids.length){
      html+='<section><h4>leads to</h4>';
      kids.forEach(function(c){
        html+='<div class="req no"><span class="m">→</span><a href="#" class="jump" data-jump="'+esc(c)+'">'+esc(byId[c]?byId[c].title:c)+'</a></div>';
      });
      html+='</section>';
    }
    // objectives
    if(ov.objectives&&ov.objectives.length){
      html+='<section><h4>objectives</h4><ul>'+ov.objectives.map(function(o){return '<li>'+esc(o)+'</li>';}).join('')+'</ul></section>';
    }
    // protocol steps
    var ins=st.instructions||[];
    if(ins.length){
      html+='<section><h4>protocol</h4><div class="steps">';
      ins.forEach(function(step,i){
        html+='<div class="step"><div class="n">'+(i+1)+'</div><div><b>'+esc(step.title)+'</b><small>'+esc(step.description||'')+'</small></div></div>';
      });
      html+='</div></section>';
    }
    // video
    if(det.video&&det.video.url){
      var emb=ytEmbed(det.video.url);
      html+='<section><h4>technique video</h4>';
      if(emb){html+='<div class="vid"><iframe loading="lazy" src="'+emb+'" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe></div>'
        +'<div style="margin-top:8px"><a class="watch" href="'+esc(det.video.url)+'" target="_blank" rel="noopener">▶ open on YouTube ↗</a></div>';}
      else{html+='<a class="watch" href="'+esc(det.video.url)+'" target="_blank" rel="noopener">▶ watch ↗</a>';}
      html+='</section>';
    }
    // resources
    if(det.resources&&det.resources.length){
      html+='<section><h4>resources</h4><div class="res">'+det.resources.map(function(r){
        var host=''; try{host=new URL(r.url).hostname.replace('www.','');}catch(e){}
        return '<a href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.title)+' <span>'+esc(host)+' ↗</span></a>';
      }).join('')+'</div></section>';
    }
    // hands-on training kits
    if(det.kits&&det.kits.length){
      html+='<section><h4>🧰 hands-on kits</h4><div class="kits">'+det.kits.map(function(kt){
        return '<a class="kit" href="'+esc(kt.url)+'" target="_blank" rel="noopener">'
          +'<div class="kn">'+esc(kt.name)+(kt.diy?' <em class="ktag">online</em>':'')+'</div>'
          +'<div class="km"><span>'+esc(kt.vendor)+'</span><b>'+esc(kt.price)+'</b></div>'
          +'<div class="kd">'+esc(kt.note)+'</div></a>';
      }).join('')+'</div>'
        +'<div class="freenote">Prices approximate — confirm with the vendor. Do genetic-modification work only in a legal, registered space.</div>'
        +'</section>';
    }
    // CTA — always available; no node is ever locked
    if(s==='done'){
      html+='<button class="cta done" id="ctaBtn">✓ completed — mark not done</button>';
    }else{
      html+='<button class="cta go" id="ctaBtn">mark complete →</button>';
    }
    html+='</div>';
    pop.innerHTML=html;
    scrim.classList.add('show');
    document.getElementById('popx').addEventListener('click',closePop);
    // navigate the trajectory: clicking a prerequisite / downstream skill opens it
    pop.querySelectorAll('[data-jump]').forEach(function(a){
      a.addEventListener('click',function(e){e.preventDefault();openPop(a.getAttribute('data-jump'));});
    });
    var cta=document.getElementById('ctaBtn');
    if(cta&&!cta.disabled){
      cta.addEventListener('click',function(){
        done[id]=!done[id]; if(!done[id])delete done[id];
        save(); refreshAll(); openPop(id);
      });
    }
    pop.scrollTop=0;
  }
  function closePop(){scrim.classList.remove('show');}
  scrim.addEventListener('click',function(e){if(e.target===scrim)closePop();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closePop();});

  // ---- search ----
  function nodeText(n){
    var det=DETAILS[n.id]||{},ov=det.overview||{};
    return [n.title,n.description,det.project,(ov.objectives||[]).join(' ')].join(' ').toLowerCase();
  }
  var qEl=document.getElementById('q'),matchIds=null;
  qEl.addEventListener('input',function(){
    var q=qEl.value.trim().toLowerCase();
    if(!q){matchIds=null;}
    else{matchIds=new Set(NODES.filter(function(n){return nodeText(n).indexOf(q)>=0;}).map(function(n){return n.id;}));}
    applyFilter();
  });
  function applyFilter(){
    // map dim
    NODES.forEach(function(n){
      var el=nodeEls[n.id]; if(el)el.classList.toggle('dim',!!matchIds&&!matchIds.has(n.id));
    });
    // list hide
    listEl.querySelectorAll('.li').forEach(function(li){
      var id=li.getAttribute('data-id');
      li.style.display=(!matchIds||matchIds.has(id))?'':'none';
    });
    listEl.querySelectorAll('.tiergrp').forEach(function(g){
      var any=Array.prototype.some.call(g.querySelectorAll('.li'),function(li){return li.style.display!=='none';});
      g.style.display=any?'':'none';
    });
    if(matchIds&&matchIds.size&&mode==='map'){fitTo([].concat.apply([],[Array.from(matchIds)]).map(function(id){return byId[id];}));}
  }

  // ---- pan / zoom ----
  var tx=0,ty=0,scale=1;
  function applyTransform(){canvas.style.transform='translate('+tx+'px,'+ty+'px) scale('+scale+')';
    edges.style.transform=canvas.style.transform;}
  function clampScale(s){return Math.max(.25,Math.min(2.2,s));}
  function zoomAt(cx,cy,factor){
    var ns=clampScale(scale*factor);
    var k=ns/scale;
    tx=cx-(cx-tx)*k; ty=cy-(cy-ty)*k; scale=ns; applyTransform();
  }
  mapEl.addEventListener('wheel',function(e){e.preventDefault();
    var r=mapEl.getBoundingClientRect();
    zoomAt(e.clientX-r.left,e.clientY-r.top,e.deltaY<0?1.12:1/1.12);
  },{passive:false});
  // ---- pointer drag + pinch, WITHOUT breaking click-to-open ----
  // Calling setPointerCapture() on pointerdown retargets the resulting `click`
  // to #map, so a node's own click handler never fires for a real mouse (only
  // for a synthetic el.click()). So: capture ONLY once a real drag starts, and
  // decide "tap vs drag" ourselves on pointerup.
  var ptrs={},last=null,pinchD=0,downPt=null,dragged=false;
  var DRAG_SLOP=5;   // px of movement before it counts as a pan, not a tap
  var lastTapOpen=0; // timestamp: lets the fallback click handler stand down

  mapEl.addEventListener('pointerdown',function(e){
    ptrs[e.pointerId]={x:e.clientX,y:e.clientY};
    if(Object.keys(ptrs).length===1){
      last={x:e.clientX,y:e.clientY};
      downPt={x:e.clientX,y:e.clientY,id:e.pointerId,node:nodeAt(e.target)};
      dragged=false;
    }else{
      downPt=null; // second finger => gesture, never a tap
    }
  });

  mapEl.addEventListener('pointermove',function(e){
    if(!ptrs[e.pointerId])return;
    ptrs[e.pointerId]={x:e.clientX,y:e.clientY};
    var ids=Object.keys(ptrs);
    if(ids.length>=2){
      dragged=true;
      var a=ptrs[ids[0]],b=ptrs[ids[1]];
      var d=Math.hypot(a.x-b.x,a.y-b.y);
      var r=mapEl.getBoundingClientRect();
      var midx=(a.x+b.x)/2-r.left,midy=(a.y+b.y)/2-r.top;
      if(pinchD)zoomAt(midx,midy,d/pinchD);
      pinchD=d; last=null;
      return;
    }
    if(!dragged&&downPt&&Math.hypot(e.clientX-downPt.x,e.clientY-downPt.y)<=DRAG_SLOP)return; // still a tap
    if(!dragged){
      dragged=true;
      mapEl.classList.add('drag');
      // now that it is genuinely a drag, capture so panning survives leaving the window
      try{mapEl.setPointerCapture(e.pointerId);}catch(_){}
    }
    if(last){
      tx+=e.clientX-last.x; ty+=e.clientY-last.y; last={x:e.clientX,y:e.clientY}; applyTransform();
    }
  });

  mapEl.addEventListener('pointerup',function(e){
    // a tap that never moved past the slop opens the node under the pointer
    if(!dragged&&downPt&&downPt.id===e.pointerId){
      var id=downPt.node||nodeAt(e.target)||nodeAtPoint(e.clientX,e.clientY);
      if(id){lastTapOpen=Date.now();openPop(id);}
    }
    endPtr(e);
  });

  function nodeAt(target){
    var el=target&&target.closest?target.closest('.node'):null;
    return el?el.getAttribute('data-node'):null;
  }
  function nodeAtPoint(x,y){ // fallback if the event was retargeted
    return nodeAt(document.elementFromPoint(x,y));
  }
  function endPtr(e){
    try{if(mapEl.hasPointerCapture&&mapEl.hasPointerCapture(e.pointerId))mapEl.releasePointerCapture(e.pointerId);}catch(_){}
    delete ptrs[e.pointerId];
    if(Object.keys(ptrs).length<2)pinchD=0;
    if(Object.keys(ptrs).length===0){last=null;downPt=null;dragged=false;mapEl.classList.remove('drag');}
  }
  mapEl.addEventListener('pointercancel',endPtr);

  function fitTo(nodes){
    nodes=(nodes&&nodes.length)?nodes:NODES;
    var r=mapEl.getBoundingClientRect();
    var xmin=Math.min.apply(0,nodes.map(px))-90, xmax=Math.max.apply(0,nodes.map(px))+90;
    var ymin=Math.min.apply(0,nodes.map(py))-70, ymax=Math.max.apply(0,nodes.map(py))+70;
    var w=xmax-xmin,h=ymax-ymin;
    scale=clampScale(Math.min(r.width/w,r.height/h));
    tx=(r.width-w*scale)/2-xmin*scale;
    ty=(r.height-h*scale)/2-ymin*scale;
    applyTransform();
  }
  // Default/reset view: readable zoom, fit to WIDTH, anchored near the top so the
  // tall tree opens legible and the user scrolls down (fit-to-height made it a thread).
  function readableView(nodes){
    nodes=(nodes&&nodes.length)?nodes:NODES;
    var r=mapEl.getBoundingClientRect();
    var xmin=Math.min.apply(0,nodes.map(px))-90, xmax=Math.max.apply(0,nodes.map(px))+90;
    var ymin=Math.min.apply(0,nodes.map(py))-70;
    var w=xmax-xmin;
    scale=clampScale(Math.min(r.width/w, 1.05));
    tx=(r.width-w*scale)/2-xmin*scale;
    ty=40-ymin*scale;
    applyTransform();
  }
  document.getElementById('zin').addEventListener('click',function(){var r=mapEl.getBoundingClientRect();zoomAt(r.width/2,r.height/2,1.2);});
  document.getElementById('zout').addEventListener('click',function(){var r=mapEl.getBoundingClientRect();zoomAt(r.width/2,r.height/2,1/1.2);});
  document.getElementById('zfit').addEventListener('click',function(){fitTo(NODES);});
  document.getElementById('zreset').addEventListener('click',function(){readableView(NODES);});

  // ---- mode toggle ----
  var mode='map';
  function setMode(m){
    mode=m;
    document.getElementById('map').style.display=m==='map'?'':'none';
    listEl.style.display=m==='list'?'block':'none';
    ivEl.style.display=m==='interview'?'block':'none';
    document.querySelectorAll('#modeToggle button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-mode')===m);});
    document.getElementById('hint').style.display=m==='map'?'':'none';
    if(m==='map')setTimeout(function(){readableView(NODES);},30);
    if(m==='interview')ivSetup();
  }
  document.querySelectorAll('#modeToggle button').forEach(function(b){
    b.addEventListener('click',function(){setMode(b.getAttribute('data-mode'));});
  });

  // ---- light / dark theme ----
  var themeBtn=document.getElementById('themeBtn');
  var themeExplicit=false;
  try{themeExplicit=['light','dark'].indexOf(localStorage.getItem('synbio-theme'))>=0;}catch(e){}
  function theme(){return document.documentElement.getAttribute('data-theme')==='light'?'light':'dark';}
  function setTheme(t,persist){
    document.documentElement.setAttribute('data-theme',t);
    if(persist){themeExplicit=true;try{localStorage.setItem('synbio-theme',t);}catch(e){}}
    themeBtn.textContent=t==='light'?'☾':'☀';
    themeBtn.title='Switch to '+(t==='light'?'dark':'light')+' mode';
  }
  themeBtn.addEventListener('click',function(){setTheme(theme()==='light'?'dark':'light',true);});
  // follow the OS until the user makes an explicit choice
  if(window.matchMedia){
    var mq=window.matchMedia('(prefers-color-scheme: light)');
    var onScheme=function(e){if(!themeExplicit)setTheme(e.matches?'light':'dark',false);};
    if(mq.addEventListener)mq.addEventListener('change',onScheme);
    else if(mq.addListener)mq.addListener(onScheme);
  }
  setTheme(theme(),false);

  // ================= INTERVIEW MODE =================
  var ivEl=document.getElementById('interview');
  var DIFFS=['foundational','core','advanced'];
  var DIFFCLS={foundational:'f',core:'c',advanced:'a'};
  var ivCfg={role:'practice',diff:'all',len:10};

  function diffBadge(d){return '<span class="badge '+(DIFFCLS[d]||'')+'">'+d+'</span>';}
  function shuffle(a,seed){ // deterministic-ish shuffle using an index seed (no Math.random)
    a=a.slice();
    for(var i=a.length-1;i>0;i--){seed=(seed*1103515245+12345)&0x7fffffff;var j=seed%(i+1);var t=a[i];a[i]=a[j];a[j]=t;}
    return a;
  }
  function poolFor(diff){
    return QUESTIONS.filter(function(q){return diff==='all'||q.difficulty===diff;});
  }

  // ---- setup screen ----
  function ivSetup(){
    if(!QUESTIONS.length){ivEl.innerHTML='<div class="iv-wrap"><p class="iv-sub">No question bank loaded.</p></div>';return;}
    var topics=QUESTIONS.length, nodes={};QUESTIONS.forEach(function(q){nodes[q.nodeId]=1;});
    var html='<div class="iv-wrap">';
    html+='<div class="iv-h">interview mode</div>';
    html+='<div class="iv-sub">A practical bench-skills question bank built from this skill tree — '+topics+' questions across '+Object.keys(nodes).length+' techniques and pieces of equipment. Practice for a biotech technical screen, or use the interviewer kit to run one.</div>';
    // role
    html+='<div class="iv-card"><h3>1 · choose a mode</h3><div class="roles">';
    html+='<div class="role'+(ivCfg.role==='practice'?' sel':'')+'" data-role="practice"><span class="ic">🧪</span><b>Practice quiz</b><small>Interviewee mode. One question at a time, instant feedback + explanation, score and review at the end. Progress saved locally.</small></div>';
    html+='<div class="role'+(ivCfg.role==='kit'?' sel':'')+'" data-role="kit"><span class="ic">📋</span><b>Interviewer kit</b><small>Every question with the answer keyed, a model explanation, and a follow-up probe to ask. Printable to run a live technical screen.</small></div>';
    html+='</div></div>';
    // difficulty
    html+='<div class="iv-card"><h3>2 · difficulty</h3><div class="fld"><div class="chips" id="ivDiff">';
    html+='<span class="chip'+(ivCfg.diff==='all'?' on':'')+'" data-diff="all">all ('+QUESTIONS.length+')</span>';
    DIFFS.forEach(function(d){var n=poolFor(d).length;html+='<span class="chip'+(ivCfg.diff===d?' on':'')+'" data-diff="'+d+'">'+d+' ('+n+')</span>';});
    html+='</div></div>';
    // length (only for practice)
    if(ivCfg.role==='practice'){
      html+='<div class="fld"><label>number of questions</label><div class="chips" id="ivLen">';
      [5,10,20,'all'].forEach(function(n){html+='<span class="chip'+(String(ivCfg.len)===String(n)?' on':'')+'" data-len="'+n+'">'+n+'</span>';});
      html+='</div></div>';
    }
    html+='</div>';
    var avail=poolFor(ivCfg.diff).length;
    html+='<button class="iv-start" id="ivStart"'+(avail?'':' disabled')+'>'+(ivCfg.role==='kit'?'open interviewer kit ('+avail+' q) →':'start practice quiz →')+'</button>';
    html+='</div>';
    ivEl.innerHTML=html;
    ivEl.querySelectorAll('.role').forEach(function(r){r.addEventListener('click',function(){ivCfg.role=r.getAttribute('data-role');ivSetup();});});
    var dd=document.getElementById('ivDiff');if(dd)dd.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){ivCfg.diff=c.getAttribute('data-diff');ivSetup();});});
    var ll=document.getElementById('ivLen');if(ll)ll.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){var v=c.getAttribute('data-len');ivCfg.len=v==='all'?'all':parseInt(v,10);ivSetup();});});
    document.getElementById('ivStart').addEventListener('click',function(){ivCfg.role==='kit'?ivKit():ivStartQuiz();});
    ivEl.scrollTop=0;
  }

  // ---- quiz engine ----
  var quiz=null;
  function ivStartQuiz(){
    var pool=poolFor(ivCfg.diff);
    pool=shuffle(pool,pool.length*7+DIFFS.indexOf(ivCfg.diff)+3);
    var n=ivCfg.len==='all'?pool.length:Math.min(ivCfg.len,pool.length);
    quiz={items:pool.slice(0,n),i:0,score:0,answered:[]};
    ivRenderQ();
  }
  function ivRenderQ(){
    var q=quiz.items[quiz.i];
    var optOrder=shuffle([0,1,2,3],quiz.i*13+7); // vary option order per question
    var html='<div class="iv-wrap">';
    html+='<div class="qbar"><span class="cnt">Q '+(quiz.i+1)+'/'+quiz.items.length+'</span>'
      +'<div class="prog"><i style="width:'+(quiz.i/quiz.items.length*100)+'%"></i></div>'
      +'<span class="sc">'+quiz.score+' correct</span></div>';
    html+='<div class="qmeta">'+diffBadge(q.difficulty)+'<span class="badge">'+esc(q.topic)+'</span></div>';
    html+='<p class="qprompt">'+esc(q.prompt)+'</p>';
    html+='<div id="ivOpts">';
    optOrder.forEach(function(oi,pos){
      var letter=String.fromCharCode(65+pos);
      html+='<button class="opt" data-oi="'+oi+'"><span class="k">'+letter+'</span>'+esc(q.options[oi])+'</button>';
    });
    html+='</div><div id="ivFb"></div>';
    html+='</div>';
    ivEl.innerHTML=html;
    ivEl.querySelectorAll('.opt').forEach(function(b){
      b.addEventListener('click',function(){ivAnswer(parseInt(b.getAttribute('data-oi'),10));});
    });
    ivEl.scrollTop=0;
  }
  function ivAnswer(chosen){
    var q=quiz.items[quiz.i];
    var correct=chosen===q.answer;
    if(correct)quiz.score++;
    quiz.answered.push({q:q,chosen:chosen,correct:correct});
    ivEl.querySelectorAll('.opt').forEach(function(b){
      var oi=parseInt(b.getAttribute('data-oi'),10);b.disabled=true;
      if(oi===q.answer)b.classList.add('correct');
      else if(oi===chosen)b.classList.add('wrong');
    });
    var det=DETAILS[q.nodeId]||{}, nodeTitle=(det.title&&det.title.name)||(byId[q.nodeId]&&byId[q.nodeId].title)||q.nodeId;
    var fb='<div class="expl"><b>'+(correct?'✓ correct':'✗ not quite')+'</b><p>'+esc(q.explanation)+'</p>';
    if(q.probe)fb+='<p class="probe">Interviewer would probe: '+esc(q.probe)+'</p>';
    fb+='<a href="#" data-study="'+esc(q.nodeId)+'">▸ study "'+esc(nodeTitle)+'" in the tree</a></div>';
    var last=quiz.i>=quiz.items.length-1;
    fb+='<button class="qnext" id="ivNext">'+(last?'see results →':'next question →')+'</button>';
    document.getElementById('ivFb').innerHTML=fb;
    var st=ivEl.querySelector('[data-study]');
    if(st)st.addEventListener('click',function(e){e.preventDefault();studyNode(st.getAttribute('data-study'));});
    document.getElementById('ivNext').addEventListener('click',function(){
      if(last){ivResults();}else{quiz.i++;ivRenderQ();}
    });
    document.getElementById('ivFb').scrollIntoView({behavior:'smooth',block:'nearest'});
  }
  function ivResults(){
    var total=quiz.items.length, pct=Math.round(quiz.score/total*100);
    // breakdown by topic
    var byTopic={};
    quiz.answered.forEach(function(a){var t=a.q.topic;(byTopic[t]=byTopic[t]||{n:0,ok:0});byTopic[t].n++;if(a.correct)byTopic[t].ok++;});
    var verdict=pct>=85?'Interview-ready on these fundamentals.':pct>=65?'Solid — a few gaps to close before a screen.':'Keep drilling; review the misses below and their tree nodes.';
    var html='<div class="iv-wrap">';
    html+='<div class="iv-card" style="text-align:center"><div class="score-big">'+pct+'%</div>'
      +'<div class="score-lbl">'+quiz.score+' / '+total+' correct · '+esc(verdict)+'</div></div>';
    // topic breakdown
    html+='<div class="iv-card"><h3>by topic</h3><div class="brk">';
    Object.keys(byTopic).sort().forEach(function(t){
      var b=byTopic[t], p=Math.round(b.ok/b.n*100);
      html+='<div class="brk-row"><span class="nm">'+esc(t)+'</span><span class="bar2"><i style="width:'+p+'%"></i></span><span class="v">'+b.ok+'/'+b.n+'</span></div>';
    });
    html+='</div></div>';
    // misses
    var misses=quiz.answered.filter(function(a){return !a.correct;});
    if(misses.length){
      html+='<div class="iv-card"><h3>review your misses ('+misses.length+')</h3>';
      misses.forEach(function(a){
        var q=a.q, det=DETAILS[q.nodeId]||{}, nt=(det.title&&det.title.name)||q.nodeId;
        html+='<div class="miss"><div class="mq">'+diffBadge(q.difficulty)+' '+esc(q.prompt)+'</div>';
        html+='<div class="ma bad">your answer: '+esc(q.options[a.chosen])+'</div>';
        html+='<div class="ma good">correct: '+esc(q.options[q.answer])+'</div>';
        html+='<div class="mx">'+esc(q.explanation)+' <a href="#" data-study="'+esc(q.nodeId)+'">▸ '+esc(nt)+'</a></div></div>';
      });
      html+='</div>';
    }else{
      html+='<div class="iv-card"><h3>clean sweep 🎉</h3><p class="iv-sub" style="margin:0">No misses — every answer correct.</p></div>';
    }
    html+='<button class="iv-start" id="ivAgain">new quiz →</button>';
    if(misses.length)html+='<button class="qskip" id="ivRetry">retry only the '+misses.length+' missed →</button>';
    html+='</div>';
    ivEl.innerHTML=html;
    ivEl.querySelectorAll('[data-study]').forEach(function(s){s.addEventListener('click',function(e){e.preventDefault();studyNode(s.getAttribute('data-study'));});});
    document.getElementById('ivAgain').addEventListener('click',ivSetup);
    var rt=document.getElementById('ivRetry');
    if(rt)rt.addEventListener('click',function(){quiz={items:misses.map(function(m){return m.q;}),i:0,score:0,answered:[]};ivRenderQ();});
    ivEl.scrollTop=0;
  }

  // ---- interviewer kit ----
  function ivKit(){
    var pool=poolFor(ivCfg.diff);
    var groups={},order=[];
    pool.forEach(function(q){if(!groups[q.topic]){groups[q.topic]=[];order.push(q.topic);}groups[q.topic].push(q);});
    var html='<div class="iv-wrap"><div class="iv-controls" style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap">'
      +'<button class="qskip" id="ivBack" style="width:auto;margin:0">← back</button>'
      +'<button class="qskip" id="ivPrint" style="width:auto;margin:0">🖨 print / PDF</button></div>';
    html+='<div class="iv-h">interviewer kit</div>';
    html+='<div class="iv-sub">'+pool.length+' questions'+(ivCfg.diff==='all'?'':' ('+ivCfg.diff+')')+', answer-keyed with model explanations and a follow-up probe for each. Ask the question, listen, then use the probe to test depth.</div>';
    order.sort();
    order.forEach(function(t){
      html+='<div class="kit-topic">'+esc(t)+'</div>';
      groups[t].forEach(function(q){
        var det=DETAILS[q.nodeId]||{}, nt=(det.title&&det.title.name)||q.nodeId;
        html+='<div class="kit-q"><div class="kp">'+diffBadge(q.difficulty)+' '+esc(q.prompt)+'</div>';
        q.options.forEach(function(o,i){
          html+='<div class="ko'+(i===q.answer?' ans':'')+'">'+(i===q.answer?'✓ ':'○ ')+esc(o)+'</div>';
        });
        html+='<div class="kx">'+esc(q.explanation)+'</div>';
        if(q.probe)html+='<div class="kprobe">↳ probe: '+esc(q.probe)+'</div>';
        html+='<div class="kx" style="border:0;padding-top:6px;color:var(--dim)">tree node: '+esc(nt)+'</div></div>';
      });
    });
    html+='</div>';
    ivEl.innerHTML=html;
    document.getElementById('ivBack').addEventListener('click',ivSetup);
    document.getElementById('ivPrint').addEventListener('click',function(){window.print();});
    ivEl.scrollTop=0;
  }

  // jump from a question to its node detail in the map/list
  function studyNode(id){
    setMode(window.innerWidth<=720?'list':'map');
    document.querySelectorAll('#modeToggle button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-mode')===mode);});
    setTimeout(function(){openPop(id);},60);
  }

  // ---- stats ----
  function refreshStats(){
    var d=NODES.filter(function(n){return isDone(n.id);}).length;
    var r=NODES.filter(function(n){return status(n.id)==='next';}).length;
    document.getElementById('stats').innerHTML=
      '<span><b>'+NODES.length+'</b> nodes</span>'
      +'<span><b>'+d+'</b> completed</span>'
      +'<span><b>'+r+'</b> next up</span>'
      +'<span><b>'+MAIN.size+'</b> on main path</span>'
      +'<span style="color:var(--green)">all nodes unlocked — explore in any order</span>';
  }
  function refreshAll(){refreshMapStatus();refreshListStatus();refreshStats();}

  // touch hint
  if(window.matchMedia&&window.matchMedia('(pointer:coarse)').matches){
    document.getElementById('hint').textContent='drag to pan · pinch to zoom · tap a node';
  }

  // resize refit (debounced)
  var rt; window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){if(mode==='map')readableView(NODES);},160);});

  // boot
  buildMap(); buildList(); refreshAll();
  // default to list on narrow screens
  if(window.innerWidth<=720)setMode('list'); else {setMode('map');readableView(NODES);}
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){if(mode==='map')readableView(NODES);});
})();
</script>
</body>
</html>
"""


def main():
    data = load_data()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # guard against premature </script> termination inside the JSON blob
    blob = blob.replace("</", "<\\/")
    html = HTML.replace("__DATA__", blob)
    OUT.write_text(html, encoding="utf-8")
    n = len(data["details"])
    vids = sum(1 for d in data["details"].values() if d.get("video", {}).get("url"))
    res = sum(len(d.get("resources", [])) for d in data["details"].values())
    print(f"wrote {OUT}  ({len(html)//1024} KB)")
    print(f"  {n} nodes · {vids} videos · {res} resource links")


if __name__ == "__main__":
    main()
