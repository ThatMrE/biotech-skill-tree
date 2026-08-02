#!/usr/bin/env python3
"""Integrity checks for the synthetic-biology skill tree.

Run before building/deploying so a malformed commit never reaches production:

    python validate.py

Exits non-zero (and prints every failure) if anything is wrong.
"""
import json
import pathlib
import re
import sys
from collections import Counter
from itertools import combinations

ROOT = pathlib.Path(__file__).resolve().parent
TREE = ROOT / "src" / "data" / "trees" / "synthetic-biology.json"
NODES_DIR = ROOT / "src" / "data" / "skill_nodes"
QUESTIONS = ROOT / "src" / "data" / "interview_questions.json"
HTGAA = ROOT / "src" / "data" / "htgaa_companion.json"
NESTED = ROOT / "data" / "synthetic-biology-tree.json"

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def main():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    graph = {n["id"]: n for n in tree["nodes"]}
    details = {}
    for f in sorted(NODES_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        details[d["id"]] = d

    # --- graph <-> detail parity -------------------------------------------
    for missing in sorted(set(graph) - set(details)):
        err(f"graph node '{missing}' has no detail file")
    for orphan in sorted(set(details) - set(graph)):
        err(f"detail file '{orphan}.json' is not in the graph")

    # --- dependencies resolve, and the graph is acyclic ---------------------
    for nid, n in graph.items():
        for dep in n.get("dependencies", []):
            if dep not in graph:
                err(f"node '{nid}' depends on unknown node '{dep}'")

    seen, stack = set(), set()

    def visit(nid, path):
        if nid in stack:
            err(f"dependency cycle: {' -> '.join(path + [nid])}")
            return
        if nid in seen or nid not in graph:
            return
        stack.add(nid)
        for dep in graph[nid].get("dependencies", []):
            visit(dep, path + [nid])
        stack.discard(nid)
        seen.add(nid)

    for nid in graph:
        visit(nid, [])

    # --- nothing may be locked (this tree is intentionally ungated) ---------
    for nid, n in graph.items():
        if n.get("defaultStatus") == "locked":
            err(f"node '{nid}' is locked - the tree must stay fully navigable")
    if NESTED.exists():
        nested = json.loads(NESTED.read_text(encoding="utf-8"))

        def check_unlocked(o):
            if isinstance(o, dict):
                if o.get("isUnlocked") is False:
                    err(f"nested fallback node '{o.get('id')}' has isUnlocked=false")
                for v in o.values():
                    check_unlocked(v)
            elif isinstance(o, list):
                for v in o:
                    check_unlocked(v)

        check_unlocked(nested)

    # --- layout: no overlapping node positions -----------------------------
    pos = {nid: n["initialPosition"] for nid, n in graph.items()}
    for a, b in combinations(pos, 2):
        if abs(pos[a][0] - pos[b][0]) < 0.75 and abs(pos[a][1] - pos[b][1]) < 0.6:
            warn(f"nodes '{a}' and '{b}' may visually overlap at {pos[a]} / {pos[b]}")

    # --- videos are well-formed --------------------------------------------
    # YouTube links embed as an iframe, so their 11-char id must be valid.
    # Non-YouTube sources (Addgene, NEB, JoVE) can't be framed and are rendered
    # by the viewer as a "Watch" link instead - they only need to be https URLs.
    yt = re.compile(r"^https://www\.youtube\.com/watch\?v=[\w-]{11}$")
    n_vid = n_yt = n_link = 0
    for nid, d in details.items():
        url = (d.get("video") or {}).get("url", "")
        if not url:
            continue
        n_vid += 1
        if "youtube.com" in url or "youtu.be" in url:
            n_yt += 1
            if not yt.match(url):
                err(f"node '{nid}' has a malformed YouTube URL: {url!r}")
        elif url.startswith("https://"):
            n_link += 1
        else:
            err(f"node '{nid}' has a non-https video URL: {url!r}")

    # --- interview bank -----------------------------------------------------
    qb = json.loads(QUESTIONS.read_text(encoding="utf-8"))["questions"]
    ids = [q["id"] for q in qb]
    for dup, c in Counter(ids).items():
        if c > 1:
            err(f"duplicate question id '{dup}' ({c}x)")
    for q in qb:
        if q["nodeId"] not in graph:
            err(f"question '{q['id']}' references unknown node '{q['nodeId']}'")
        if len(q["options"]) != 4:
            err(f"question '{q['id']}' has {len(q['options'])} options (expected 4)")
        if not 0 <= q["answer"] < len(q["options"]):
            err(f"question '{q['id']}' answer index {q['answer']} out of range")
        for field in ("prompt", "explanation", "topic", "difficulty"):
            if not q.get(field):
                err(f"question '{q['id']}' is missing '{field}'")
        if q["difficulty"] not in ("foundational", "core", "advanced"):
            err(f"question '{q['id']}' has unknown difficulty {q['difficulty']!r}")

    covered = {q["nodeId"] for q in qb}
    uncovered = sorted(set(graph) - covered)
    if uncovered:
        err(f"{len(uncovered)} node(s) have no interview question: {', '.join(uncovered)}")

    # --- hands-on kits ------------------------------------------------------
    n_kits = 0
    for nid, d in details.items():
        kits = d.get("kits", [])
        if not kits:
            err(f"node '{nid}' has no hands-on kits")
            continue
        for i, kit in enumerate(kits):
            n_kits += 1
            for field in ("name", "vendor", "url", "price", "note"):
                if not kit.get(field):
                    err(f"node '{nid}' kit #{i} missing '{field}'")
            if not str(kit.get("url", "")).startswith("https://"):
                err(f"node '{nid}' kit #{i} url is not https: {kit.get('url')!r}")

    # --- HTGAA companion ----------------------------------------------------
    if HTGAA.exists():
        h = json.loads(HTGAA.read_text(encoding="utf-8"))
        for nid in h.get("map", {}):
            if nid not in graph:
                err(f"HTGAA companion references unknown node '{nid}'")

    # --- report -------------------------------------------------------------
    print(f"nodes:      {len(graph)}")
    print(f"details:    {len(details)}")
    print(f"videos:     {n_vid}  ({n_yt} embedded YouTube, {n_link} external link-out)")
    print(f"questions:  {len(qb)}  (coverage {len(covered)}/{len(graph)})")
    print(f"htgaa map:  {len(h.get('map', {})) if HTGAA.exists() else 0}")
    print(f"resources:  {sum(len(d.get('resources', [])) for d in details.values())}")
    print(f"kits:       {n_kits}")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s)")
        return 1
    print("\nOK: all integrity checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
