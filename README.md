# Synthetic Biology Skill Tree

A project-based wet-lab curriculum for **WorldWideStudios/open-skill-trees**, adapted from the
open-source [NeoSynBio *Graduate's Guide to Synthetic Biology*](https://www.neosynbio.com/the-graduates-guide-to-synthetic-biology)
and enriched with the best-rated external guides for every topic (NEB, Addgene, Benchling,
SnapGene, Thermo Fisher, Bio-Rad, IDT, iGEM, Cold Spring Harbor Protocols).

**▶ Live: https://biotech-skill-tree.netlify.app**

**59 nodes · 189 curated resource links · 37 nodes with verified technique videos · one coherent dependency graph**
that takes a learner from a sterile bench all the way to expressing, purifying, and analysing their own protein —
and out into computational protein design, genetic circuits, cell-free systems, genome-scale assembly, and biofabrication.

### Emerging / job-market skills layer

A bottom tier of 11 nodes covers the skills modern biotech roles actually screen for, beyond core wet-lab:

- **Lab automation & data** — laboratory automation (Opentrons/robotics), ELN/LIMS & data hygiene (Benchling, FAIR), bioinformatics foundations, NGS data analysis
- **Bio AI / ML** — computational protein design (AlphaFold/RFdiffusion/ProteinMPNN) and ML/AI for biology (ESM foundation models, leakage-proof evaluation, generative design)
- **Other emerging & industry** — mammalian cell culture, flow cytometry & FACS, directed evolution, bioprocess & biomanufacturing, design of experiments & rigor, and biosafety & biosecurity (BSL/DURC)

## HTGAA course companion

Nodes carry a **⬢ HTGAA course companion** card (mapping in `src/data/htgaa_companion.json`) that ties each
technique to the week it is taught in MIT Media Lab's *How To Grow (Almost) Anything* — with the module title,
date, and instructors from the published **Spring 2026** schedule (e.g. CRISPR → Week 2 *DNA Read, Write & Edit*;
Gibson/Golden Gate → Week 6 *Genetic Circuits I: Assembly*). Five HTGAA-derived nodes extend the tree into the
course's advanced scope: **computational protein design, genetic circuits, cell-free systems (TX-TL), building
genomes, and bio design & biofabrication**. 20 nodes are week-mapped.

## Deploying

**Automatic:** every push to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml),
which validates the data, rebuilds the viewer from JSON, and deploys to Netlify. Editing a node file
or the interview bank and pushing is enough to ship — you don't need to rebuild locally.

The workflow requires one repository secret:

| Secret | Where to get it |
| --- | --- |
| `NETLIFY_AUTH_TOKEN` | [Netlify → User settings → Applications → Personal access tokens](https://app.netlify.com/user/applications#personal-access-tokens) |

Add it under **Settings → Secrets and variables → Actions**. (The site ID is not secret and is set
as a plain env var in the workflow.)

**Manual / local:**

```bash
python validate.py          # integrity checks (CI runs this too)
python build_viewer.py
netlify deploy --prod --dir=viewer --site=<site-id>
```

`netlify.toml` sets `publish = "viewer"` with an SPA catch-all redirect. **Always deploy with an
explicit `--dir=viewer`** — this repo lives inside a larger private working folder, and `--dir`
guarantees only the viewer is ever published. The workflow enforces the same rule: it aborts unless
the publish directory contains exactly one file, `viewer/index.html`.

## Hands-on training kits

Every node carries a `kits` array — a purchasable kit (or free online toolset) that lets a learner
actually *do* the skill, not just read about it. **[KITS.md](KITS.md)** is the full catalogue (111
kits across all 59 skills); the same data renders as a **🧰 hands-on kits** section in each node's popup.

- Vendors span DIY/education (The ODIN, Amino Labs, Bio-Rad Explorer, miniPCR, Edvotek, Carolina) and
  research (NEB, IDT, Zymo, Addgene, Opentrons, Oxford Nanopore, Pioreactor, Chai Bio).
- Every kit URL points to a vendor domain **verified to resolve**. Prices are ballpark USD and flagged
  as approximate in the UI. Items tagged **online** are free software/datasets/courses, not products.
- Skills that realistically need a shared facility (mammalian cell culture → BSL-2; flow cytometry →
  a core) say so and point to community-lab / core-facility access instead of implying a home kit.
- Genetic-modification framing is preserved throughout: **work only in a legal, registered space.**

## Validation

`python validate.py` fails the build on: graph/detail mismatch, unresolved dependencies, dependency
cycles, **any locked node**, malformed YouTube IDs, duplicate/invalid interview questions, or a node
missing an interview question. CI runs it before every deploy.

## Nothing is locked — explore in any order

This is a **reference curriculum and trajectory map, not a gated game**. Every node is open,
openable, and completable from the first visit, regardless of what you have finished:

- No node is ever `locked`. The data carries no gating either (`defaultStatus: "inProgress"`
  throughout, and `isUnlocked: true` in the nested fallback file).
- Dependencies are preserved as **guidance**, not gates — they still draw the graph and populate
  each node's *builds on* / *leads to* lists so you can preview where a skill sits in the
  progression and what it opens up.
- Node states are only ever **done**, **next up** (a suggested next step whose prerequisites you
  happen to have finished), or **open**. "Open" is a soft de-emphasis, never a barrier — you can
  jump straight to CRISPR, biomanufacturing, or the capstone on day one.

## Interactive viewer (start here)

`viewer/index.html` is a **self-contained, dependency-free** interactive front end — all 43 nodes,
23 videos, and 147 resources are embedded inline, so it needs no build step, no database, and no
internet (fonts/videos load online when available; the app itself works offline).

**Serve it over HTTP** (do *not* just double-click the file — a `file://` sandbox strips the inline
script and blocks the YouTube/font requests, which is what made earlier builds look "dead"):

```bash
cd synbio-skilltree
python build_viewer.py          # regenerate viewer/index.html from the data (only if data changed)
python -m http.server 8000      # then open http://localhost:8000/viewer/
```

What it does:

- **Map view** — the real dependency graph laid out from each node's `initialPosition`, green main-path
  spine, dashed-orange optional equipment links, pan/drag, scroll- and pinch-zoom, +/−/⤢/⟲ controls.
- **Click any node → popup** with overview, trajectory (**builds on** / **leads to**), objectives,
  numbered protocol, embedded technique video (with YouTube fallback link), resource links, and
  **🧰 hands-on kits** — purchasable kits (or free online toolsets) to actually practise the skill.
  Prerequisite and downstream names are **clickable**, so you can walk the trajectory node to node.
- **List view** — searchable, tappable index grouped by tier; auto-defaults on phones (≤720px).
- **Search** filters both views; **progress** (mark-complete → unlock cascade) persists via `localStorage`.
- **Light & dark mode** — see below.

`build_viewer.py` re-emits the viewer from the JSON data, so the data files remain the single source
of truth — edit a node file, rerun the script, reload.

## Theming & typography

**Typeface:** [Inter](https://rsms.me/inter/) — an open, Helvetica-style neo-grotesque — with a
`Helvetica Neue → Helvetica → Arial → Liberation Sans` fallback stack. The CSS variables are still
named `--mono` / `--disp` (both now resolve to Inter) so existing rules keep working.

**Light & dark mode** via the ☀/☾ button in the header:

- Every colour is a themed custom property. `:root` holds the dark palette,
  `:root[data-theme="light"]` the light one — so there are no hardcoded colours to miss.
  (The single literal left is `#000`, the video letterbox, which is correct in both.)
- The theme **follows your OS** and keeps following it until you click the toggle; an explicit
  choice then persists in `localStorage` under `synbio-theme`.
- An inline `<head>` script applies the theme **before first paint**, so there is no flash of the
  wrong scheme on load.
- The light palette is contrast-checked to WCAG AA: body 17.2:1, muted text 5.4:1, accent 4.86:1,
  primary button 4.99:1. (The acid green darkens to `#4d7c0f` in light mode — the dark-mode
  `#c6f24e` is unreadable on white.)

Note that the SVG dependency edges set `stroke="var(--edge)"` as a presentation attribute, which
re-resolves on theme change — don't replace those with literal colours.

## Interview mode (technical-screen tool)

The **◇ interview** tab turns the skill tree into a hiring/prep tool backed by a practical question
bank (`src/data/interview_questions.json` — **116 questions covering all 59 nodes (100%)**, tagged
`foundational` / `core` / `advanced` and anchored to the tree node they test). Questions are written
to probe *how to actually use the equipment* — pick the right pipette for 2.5 µL, why you balance a
centrifuge, star activity in a digest, imidazole elution off Ni-NTA, inclusion-body rescue, PAM
requirements, etc. — not trivia.

Two roles:

- **Practice quiz (interviewee)** — pick difficulty and length (5/10/20/all), then answer one question
  at a time with shuffled options, instant right/wrong feedback, a model explanation, and the
  interviewer's follow-up probe. A results screen scores you, breaks performance down by topic, and
  lists every miss with the correct answer — each links straight to its node in the tree to go study.
  A "retry only the missed" button drills weak spots. Everything is client-side (no external calls).
- **Interviewer kit** — every question (optionally filtered by difficulty) grouped by topic, answer-keyed
  with the model explanation and a depth-probe to ask live. **Print / save-to-PDF** styled for a clean
  interviewer handout.

To extend the bank, add objects to `interview_questions.json` (`nodeId` must match a skill-node id;
`answer` is the 0-based index of the correct option) and rerun `python build_viewer.py`.

## Files (drop straight into the repo)

```
src/data/trees/synthetic-biology.json     # the node graph + mainPathNodes (TreeDescriptor schema)
src/data/skill_nodes/<id>.json             # 43 rich detail files (Skill schema): overview,
                                           #   objectives, prerequisites, step-by-step
                                           #   instructions, submission, video, and resources
data/synthetic-biology-tree.json           # simple nested fallback (matches data/multi-root-node-tree.json)
```

The detail files use the exact `Skill` interface from `src/types/skill.d.ts`
(`treeId, id, title{name,level}, project, video, time, level, overview{...}, steps{...},
submission, resources[]`), and the graph uses the `TreeDescriptor` / `SkillNode` shape from
`voice-agents.json` (`id, title, description, defaultStatus, link, initialPosition, dependencies`).

## Loading it

The repo already ships the importer. With Mongo running (see `docker-compose.yml`):

```bash
# treeToDb.ts reads src/data/trees/<name>.json and the linked src/data/skill_nodes/<link>.json
npx tsx scripts/treeToDb.ts synthetic-biology
```

`syncTree()` inserts the tree + each skill (attaching the detail file as `node.details`), and
`updateDependencies()` rewrites the human-readable dependency ids to the inserted Mongo `_id`s.

## The learning path

The highlighted **main path** (the spine the canvas emphasises) is:

`intro → sterile-workspace → media-plates → sterile-technique → miniprep →
gel-electrophoresis → pcr → restriction-digest → ligation → confirmation →
proteins101 → protein-induction → affinity-purification → sds-page → final-project`

Branches hang off the spine: a **theory** strand (DNA101, Plasmids101, Backbone Selection,
gBlock Design, Proteins101), a **PCR** strand (Primer Design → Gradient PCR → Flanking Addition →
SDM), an **advanced assembly/editing** strand (Gibson, Golden Gate, CRISPR), **reagent-prep**
side quests (Host Selection, Culturing, DIY Buffer Mixing, Genomic DNA, Gel Imaging, Sequencing),
and the branches below. Nodes start `locked` except `intro` (`inProgress`); completing a node's
dependencies unlocks it.

## What's new in this version

**+8 nodes** expand the tree:
- An **optional equipment side-tree** — `micropipette`, `centrifuge`, `thermocycler`,
  `spectrophotometer`. These are **non-blocking reference cards**: each hangs off `intro` and
  nothing on the main spine depends on them, so they can be browsed freely in parallel without
  gating miniprep / pcr / protein-induction.
- A **proteome-analysis branch** — `western-blot` (after SDS-PAGE) and `elisa` (after affinity
  purification).
- An **RNA / transcriptomics branch** — `rna-purification` (after genomic DNA) and `rt-qpcr`
  (after RNA purification + PCR). `advanced-omics` now sits at the very end, gated behind the
  western-blot and RT-qPCR branches.

**Videos are wired in.** The `video.url` field is populated for **23** techniques with verified,
authoritative videos: Addgene (transformation, primer design, pouring plates, streaking), NEB
(Gibson, ligation, Q5 site-directed mutagenesis), MIT McGovern (CRISPR), Bio-Rad (restriction
digest), Harvard LabXchange / CSHL (miniprep, DNA structure), Thermo Fisher (colony PCR), JoVE
(SDS-PAGE, aseptic technique, RNA/RT-PCR) and high-quality explainer animations (PCR, gel
electrophoresis, Golden Gate, western blot, ELISA, Sanger sequencing, micropipetting). A handful
of nodes with no clean dedicated video (e.g. cell lysis, affinity purification, plasmids101) keep
the schema's empty-string default rather than linking something unvetted — their text resources
remain strong.

## How resources were chosen

Every node carries 3–4 links: the original NeoSynBio protocol page **plus** the canonical,
highest-authority guide(s) for that technique — e.g. NEB for PCR/assembly/ligation and the Tm
Calculator, Addgene's *Plasmids 101*, *CRISPR Guide* and *Intro to the Lab Bench* protocol series,
Benchling/SnapGene/Primer3 for primer & gRNA design, and Thermo Fisher/Bio-Rad for lysis,
His-tag purification, SDS-PAGE, western blot, ELISA and RT-qPCR.

> Note on biosafety: several nodes (Plasmid Insertion onward) constitute genetic modification in
> many jurisdictions. The content preserves NeoSynBio's repeated reminders to work only in a
> legal, registered space and to consult the local regulator first.

## Regenerating

All output files are produced by the included generator (pure Python 3, no dependencies):

```bash
python3 build_tree.py        # rewrites src/data/ and data/ from the NODES list + VIDEOS map
```

Edit the `NODES` list (node specs), the `VIDEOS` map (technique videos), or `MAIN_PATH`
(the highlighted spine) in `build_tree.py`, then re-run.

## Repo layout

This package mirrors the target repo's paths, so you can either push it as its own repository
or copy the two data folders into an existing `open-skill-trees` clone:

```
src/data/trees/synthetic-biology.json   ->  src/data/trees/
src/data/skill_nodes/*.json             ->  src/data/skill_nodes/
data/synthetic-biology-tree.json        ->  data/
```
