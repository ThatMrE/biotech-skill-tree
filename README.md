# Synthetic Biology Skill Tree

A project-based wet-lab curriculum for **WorldWideStudios/open-skill-trees**, adapted from the
open-source [NeoSynBio *Graduate's Guide to Synthetic Biology*](https://www.neosynbio.com/the-graduates-guide-to-synthetic-biology)
and enriched with the best-rated external guides for every topic (NEB, Addgene, Benchling,
SnapGene, Thermo Fisher, Bio-Rad, IDT, iGEM, Cold Spring Harbor Protocols).

**43 nodes · 147 curated resource links · 23 nodes with verified technique videos · one coherent dependency graph**
that takes a learner from a sterile bench all the way to expressing, purifying, and analysing their own protein.

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
