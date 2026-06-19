#!/usr/bin/env python3
"""
Builds a Synthetic Biology skill tree for WorldWideStudios/open-skill-trees.

Emits, in the repo's production schema:
  - src/data/trees/synthetic-biology.json      (the node graph + mainPathNodes)
  - src/data/skill_nodes/<id>.json             (rich detail per node, incl. resources)

Also emits a convenience nested file in the simpler ingest schema:
  - data/synthetic-biology-tree.json
"""
import json, os, pathlib

OUT = pathlib.Path("/home/claude/skilltree_out")
(OUT / "src/data/trees").mkdir(parents=True, exist_ok=True)
(OUT / "src/data/skill_nodes").mkdir(parents=True, exist_ok=True)
(OUT / "data").mkdir(parents=True, exist_ok=True)

NEO = "https://www.neosynbio.com"

# Each node: id, title, lvl(int tier), level(str), time(min), project, desc(tree blurb),
# pos [x,y], deps[], objectives[], prereqs[], intro, tools[], steps[(title,desc)],
# submission, resources[(title,url)]
NODES = [
    dict(
        id="intro", title="Welcome to the Synbio Skill Tree", lvl=1, level="beginner",
        time=10, project="Orientation",
        desc="How to navigate this project-based synthetic biology curriculum and set up for success.",
        pos=[0, -1.5], deps=[], status="inProgress",
        objectives=[
            "understand the wet-lab progression from sterile workspace to protein purification",
            "identify which nodes you can skip based on prior experience",
            "set up a free DNA sequence editor (Benchling or SnapGene)",
            "understand the legal/biosafety framing before doing any genetic modification",
        ],
        prereqs=["an undergraduate background in biology is helpful but not required"],
        intro="This tree turns the open-source NeoSynBio Graduate's Guide into a navigable, project-based curriculum. Each node pairs a hands-on protocol with the best-rated external guides so you can go from zero to expressing and purifying your own protein.",
        tools=["a computer", "internet access", "a notebook (paper or Benchling)"],
        steps=[
            ("Read the guide philosophy", "Skim the NeoSynBio introduction. The guide is comprehensive on purpose: skip anything you already know and dive deep where you have gaps."),
            ("Pick your sequence editor", "Create a free Benchling account or download SnapGene Viewer. You'll use it constantly for plasmid maps, primer design and in-silico cloning."),
            ("Note your local biosafety rules", "Identify your country's gene-technology regulator before any modification work. The well-trodden path (K12-derived E. coli) is the easiest to get approved."),
        ],
        submission="Write a one-paragraph learning plan: which nodes you'll skip, which you'll focus on, and what your target capstone protein is (GFP is a great first choice).",
        resources=[
            ("NeoSynBio: The Graduate's Guide to Synthetic Biology", f"{NEO}/the-graduates-guide-to-synthetic-biology"),
            ("Addgene: Protocols hub & 'Intro to the Lab Bench' series", "https://www.addgene.org/protocols/"),
            ("iGEM Registry of Standard Biological Parts", "https://parts.igem.org/Main_Page"),
            ("Benchling (free academic molecular biology suite)", "https://www.benchling.com/"),
        ],
    ),
    dict(
        id="sterile-workspace", title="The Sterile Workspace", lvl=1, level="beginner",
        time=30, project="Lab Setup",
        desc="Set up PPE, a Bunsen 'cone of protection', and a media-sterilisation strategy.",
        pos=[0, 0], deps=["intro"],
        objectives=[
            "assemble basic PPE (gloves, lab coat, goggles)",
            "create a sterile bench using 70% ethanol and a flame",
            "understand the Bunsen 'cone of protection'",
            "choose a media-sterilisation method (autoclave, pressure cooker, or microwave)",
        ],
        prereqs=["a workspace you can dedicate to lab work"],
        intro="Before any synbio, you need PPE and a sterile workspace. Ethanol kills surface bacteria while the Bunsen flame creates an updraft - your cone of protection. Anything within ~2 feet of a roaring blue flame is reasonably safe from contamination.",
        tools=["nitrile gloves", "lab coat", "goggles", "70% ethanol spray", "Bunsen burner or portable equivalent", "paper towels"],
        steps=[
            ("Suit up", "Put on gloves, lab coat and goggles whenever working with hazardous reagents. Know the hazards of every reagent before you touch it."),
            ("Spray down the bench", "Spray your workspace with 70% ethanol and wipe dry. Spray bare hands and wrists - it won't disable RNAses but prevents most contamination."),
            ("Light the flame correctly", "Spark your lighter/match FIRST, then turn on the gas. Never release flammable gas before you have a flame."),
            ("Pick a sterilisation method", "Autoclave (gold standard), pressure cooker, or microwave (900 W / 10 min). If microwaving, incubate test plates at RT and 37C for a week to confirm sterility."),
        ],
        submission="Photograph your set-up sterile workspace with PPE on and your flame lit. Note which media-sterilisation method you chose and why.",
        resources=[
            ("NeoSynBio: The Sterile Workspace protocol", f"{NEO}/the-sterile-workspace"),
            ("Addgene: Personal Protective Equipment (Intro to the Lab Bench)", "https://www.addgene.org/protocols/"),
            ("Microwave-sterilised media supports microbial growth (ResearchGate)", "https://www.researchgate.net/publication/215796685_Microwave_sterilized_media_supports_better_microbial_growth_than_autoclaved_media"),
            ("JoVE Science Education: Aseptic Technique", "https://www.jove.com/science-education"),
        ],
    ),
    dict(
        id="host-selection", title="Host Selection Criteria", lvl=1, level="beginner",
        time=30, project="Experimental Design",
        desc="Choose a safe, well-characterised, single-celled host - and check it's legal.",
        pos=[-2.1, 0], deps=["intro"],
        objectives=[
            "choose a non-pathogenic, plasmid-compatible host",
            "weigh the trade-offs of well-characterised vs novel organisms",
            "verify the legality of working with your chosen organism",
        ],
        prereqs=["the intro node"],
        intro="Pick a simple single-celled organism that can hold and use a plasmid - bacteria or yeast. Use a well-characterised, non-pathogenic strain from a respected supplier. K12-derived E. coli is the well-trodden, easy-to-approve path.",
        tools=["literature databases", "your local regulator's website"],
        steps=[
            ("Default to E. coli", "Unless you have a reason not to, choose a K12-derived E. coli strain. Decades of literature make culturing and troubleshooting far easier."),
            ("Confirm it's non-pathogenic", "Never work with a strain that could infect you. Source from ATCC, DSMZ, a university, or iGEM."),
            ("Check the law", "Google your government's stance on genetic manipulation and, if unsure, call the regulator. In Australia this is the OGTR."),
        ],
        submission="State your chosen host, its source/strain designation, and a one-line confirmation that it is legal to work with in your jurisdiction.",
        resources=[
            ("NeoSynBio: Host Selection Criteria", f"{NEO}/host-selection-criteria"),
            ("Addgene: Plasmids 101 eBook (host & vector basics)", "https://blog.addgene.org/plasmids-101-ebook-4th-edition"),
            ("ATCC microbial strain catalogue", "https://www.atcc.org/microbe-products"),
            ("iGEM Registry: chassis organisms", "https://parts.igem.org/Main_Page"),
        ],
    ),
    dict(
        id="culturing-conditions", title="Culturing Conditions", lvl=1, level="beginner",
        time=25, project="Experimental Design",
        desc="Know your organism: ideal media, temperature, growth curve and morphology.",
        pos=[-2.1, 1.1], deps=["host-selection"],
        objectives=[
            "identify the optimal growth temperature and media for your host",
            "understand growth curves and morphology",
            "learn to adapt protocols to non-E. coli organisms",
        ],
        prereqs=["a chosen host"],
        intro="The secret to adapting any protocol is to KNOW YOUR ORGANISM. If a protocol says 37C but your critter prefers 30C, you can make the expert decision to optimise. An abundance of literature is your friend.",
        tools=["incubator", "hot water bath", "literature"],
        steps=[
            ("Research your organism", "Google culture conditions, ideal media, growth curves, morphology - anything that improves your success rate."),
            ("Standardise E. coli conditions", "For E. coli: 37C, shaking ~100-200 rpm for liquid culture, LB media."),
            ("Document deviations", "Record any condition where your organism differs from the default protocol so you can adapt every downstream step."),
        ],
        submission="Produce a one-page 'organism profile': optimal temperature, media, doubling time, and any special handling notes.",
        resources=[
            ("NeoSynBio: Common Culturing Conditions", f"{NEO}/culturing-conditions"),
            ("Addgene: Inoculating a liquid bacterial culture", "https://www.addgene.org/protocols/inoculate-bacterial-culture/"),
            ("Addgene: Streaking & picking bacterial colonies", "https://www.addgene.org/protocols/streak-plate/"),
        ],
    ),
    dict(
        id="buffer-mixing", title="DIY Buffer Mixing", lvl=1, level="intermediate",
        time=60, project="Reagent Prep",
        desc="Mix your own buffers safely to cut costs - or buy pre-mixed if working solo.",
        pos=[2.3, 0.6], deps=["sterile-workspace"],
        objectives=[
            "understand what buffers do (resisting pH change)",
            "weigh DIY vs commercial buffers on cost and safety",
            "handle hazardous pure compounds with correct PPE",
            "calibrate and use a pH meter",
        ],
        prereqs=["the sterile workspace and PPE"],
        intro="Buffers resist pH change and you'll use them for nearly everything. Mixing your own can save thousands in a community lab, but involves deadly compounds in pure form (e.g. HCl, guanidine thiocyanate). Solo hobbyists should usually buy pre-mixed.",
        tools=["pH meter", "balance", "fume hood or excellent ventilation", "full PPE"],
        steps=[
            ("Decide DIY vs buy", "Solo and can't source pure acids safely? Buy pre-mixed. In a funded community lab? DIY can cut huge costs."),
            ("Suit up for chemicals", "Pure compounds are far more dangerous than the diluted reagents you've used so far. Read every MSDS."),
            ("Calibrate the pH meter", "Two- or three-point calibrate against standard buffers before measuring; titrate carefully to target pH."),
        ],
        submission="Mix one simple buffer (e.g. 1x TAE) from scratch, record the recipe and final measured pH, and note the hazards you mitigated.",
        resources=[
            ("NeoSynBio: DIY Buffer Mixing protocols", f"{NEO}/diy-buffer-mixing"),
            ("NeoSynBio: pH Meter equipment guide", f"{NEO}/ph-meter"),
            ("Cold Spring Harbor Protocols: buffers & stock solutions", "https://cshprotocols.cshlp.org/"),
        ],
    ),
    dict(
        id="media-plates", title="Mixing Media & Pouring Plates", lvl=1, level="beginner",
        time=90, project="Reagent Prep",
        desc="Mix LB media/agar, pour plates, and make antibiotic selection plates.",
        pos=[0, 1.5], deps=["sterile-workspace", "culturing-conditions"],
        objectives=[
            "mix LB liquid media and LB-agar from scratch",
            "pour even, bubble-free agar plates",
            "prepare antibiotic stock solutions and selection plates",
            "use a micropipette accurately",
        ],
        prereqs=["a sterile workspace", "a media-sterilisation method"],
        intro="Mixing your own media is cheap and self-sufficient: protein, yeast extract, salt, water and agar. Antibiotic media is 'biotech on easy mode' - a few drops purge anything without your plasmid. The only catch is a little maths for antibiotic dilutions.",
        tools=["LB components", "agar", "petri dishes", "glassware", "weighing scale", "RO/MilliQ water", "micropipette", "antibiotic stocks"],
        steps=[
            ("Mix LB liquid media", "Combine tryptone, yeast extract and NaCl in water, then sterilise. This is your standard E. coli media."),
            ("Make LB-agar", "Add agar to LB before sterilising. Cool to ~50C before pouring so it doesn't kill antibiotics."),
            ("Add antibiotics", "Once the agar is hand-warm, add antibiotic from a frozen stock at the working concentration, swirl, and pour."),
            ("Pour plates", "Pour a thin even layer, flame off bubbles, let set, then dry lid-ajar before storing inverted at 4C."),
        ],
        submission="Pour a set of LB-agar plates (plain and antibiotic). Photograph them and report your antibiotic working concentration and stock dilution maths.",
        resources=[
            ("NeoSynBio: Mixing Media & Pouring Plates", f"{NEO}/mixing-media-and-pouring-plates"),
            ("NeoSynBio: Antibiotic Stock Solutions & Dilutions", f"{NEO}/antibiotic-stock-solution-mixing"),
            ("Addgene: Making LB agar plates / Over-agar antibiotic", "https://www.addgene.org/protocols/pouring-lb-agar-plates/"),
            ("Cold Spring Harbor Protocols: LB (Luria-Bertani) medium", "https://cshprotocols.cshlp.org/content/2006/1/pdb.rec8141"),
        ],
    ),
    dict(
        id="sterile-technique", title="Sterile (Aseptic) Technique", lvl=2, level="beginner",
        time=60, project="Core Skills",
        desc="Master the core discipline of microbiology - plus the inoculating loop and spreader.",
        pos=[0, 3], deps=["media-plates"],
        objectives=[
            "perform sterile transfers near a flame",
            "use an inoculating loop/wand and a glass spreader",
            "understand why controls catch non-experimental variables",
            "diagnose contamination from plate morphology",
        ],
        prereqs=["poured plates", "a sterile workspace"],
        intro="Aseptic technique is easy to learn, impossible to master. Technical errors only matter if they introduce non-experimental variables. If you reliably grow contamination-free plates and verify results, the nuances of your set-up don't matter - results are what count.",
        tools=["inoculating loop or wand", "glass spreader", "Bunsen burner", "agar plates", "liquid culture"],
        steps=[
            ("Flame your tools", "Flame the inoculating loop to red-hot, let it cool a moment, then pick a colony or dip into culture - always within the cone of protection."),
            ("Streak for single colonies", "Streak in quadrants, flaming the loop between sectors, to isolate single colonies."),
            ("Spread evenly", "Use a sterile glass spreader to distribute liquid culture across a plate for even lawn or countable colonies."),
            ("Always run controls", "Include positive and negative controls so that contamination or reagent failure is immediately diagnosable."),
        ],
        submission="Streak a plate to obtain isolated single colonies and photograph the result. Include a contamination-free negative control plate.",
        resources=[
            ("NeoSynBio: Sterile Technique protocol", f"{NEO}/sterile-technique"),
            ("NeoSynBio: The Inoculating Loop / Wand", f"{NEO}/inoculation-wand"),
            ("Addgene: Streaking bacteria for single colonies (video protocol)", "https://www.addgene.org/protocols/streak-plate/"),
            ("ASM / JoVE Science Education: Aseptic technique fundamentals", "https://www.jove.com/science-education"),
        ],
    ),
    dict(
        id="dna101", title="DNA101 (Theory)", lvl=2, level="beginner",
        time=45, project="Theory",
        desc="Refresh DNA structure, base pairing and the interactions cloning relies on.",
        pos=[-2.2, 2.1], deps=["intro"],
        objectives=[
            "describe DNA structure and antiparallel base pairing",
            "explain why DNA carries a uniform negative charge",
            "use a sequence viewer (Benchling/SnapGene) to read a .dna map",
        ],
        prereqs=["the intro node"],
        intro="This section fills any gaps in DNA theory before you start manipulating it. If you're confident, skim and move on - but a solid mental model of base pairing, polarity and charge underpins every downstream technique.",
        tools=["Benchling or SnapGene", "a sample plasmid file"],
        steps=[
            ("Review structure", "Refresh the double helix, 5'->3' polarity, A-T/G-C pairing and the phosphate backbone's negative charge."),
            ("Open a real plasmid", "Download a plasmid (e.g. pET-15b) from Addgene and open it in your viewer to see features, ORIs and restriction sites."),
            ("Connect theory to charge", "Note that each base adds one negative charge - the basis for gel electrophoresis later."),
        ],
        submission="Annotate a plasmid map in your viewer, labelling the origin of replication, resistance gene, promoter and multiple cloning site.",
        resources=[
            ("NeoSynBio: DNA101", f"{NEO}/dna101"),
            ("Khan Academy: Biology library (DNA structure & replication)", "https://www.khanacademy.org/science/biology"),
            ("Addgene: Molecular Biology Reference", "https://www.addgene.org/mol-bio-reference/"),
            ("Nature Scitable: nucleic acid structure topic room", "https://www.nature.com/scitable/topic/genetics-5/"),
        ],
    ),
    dict(
        id="genomic-dna", title="Purification of Genomic DNA", lvl=2, level="intermediate",
        time=90, project="DNA Extraction",
        desc="Extract genomic DNA - and learn why you'll usually work with plasmids instead.",
        pos=[-2.2, 3.3], deps=["dna101", "sterile-technique"],
        objectives=[
            "match an extraction method to your genome type",
            "perform a simple boil-prep for E. coli genomic DNA",
            "understand why chromosomes are hard to reintroduce into cells",
        ],
        prereqs=["DNA101", "sterile technique", "a heat block"],
        intro="Genomic DNA is the organism's core code. For E. coli, a simple boil-purification in a heat block extracts the 4.6 Mbp chromosome. But chromosomes are hard to get back into cells - which is why plasmids are the real workhorse of synbio.",
        tools=["heat block", "microcentrifuge", "lysis reagents", "E. coli culture"],
        steps=[
            ("Pick a method for your genome", "Choose an extraction protocol that matches your genome type (ssDNA, dsDNA, etc.)."),
            ("Boil-prep E. coli", "For a quick crude prep, pellet cells, resuspend, and heat in a heat block to release genomic DNA."),
            ("Plan downstream use", "Decide what you'll do with the DNA before extracting - reintroducing whole chromosomes is rarely practical."),
        ],
        submission="Extract genomic DNA from your host and run a small aliquot on a gel (after the gel node) to confirm high-molecular-weight DNA.",
        resources=[
            ("NeoSynBio: Genomic DNA Extraction protocols", f"{NEO}/purification-of-genomic-dna"),
            ("protocols.io: genomic / HMW DNA extraction", "https://www.protocols.io/"),
            ("Addgene: DNA quantification with a spectrophotometer", "https://www.addgene.org/protocols/dna-quantification/"),
        ],
    ),
    dict(
        id="plasmids101", title="Plasmids101 (Theory)", lvl=2, level="beginner",
        time=45, project="Theory",
        desc="Understand plasmids as the programmable 'add-ons' of the cell.",
        pos=[1.9, 2.0], deps=["dna101"],
        objectives=[
            "describe plasmid elements (ORI, resistance, MCS, promoter)",
            "understand copy number and selection",
            "appreciate 'catastrophic success' and metabolic burden",
        ],
        prereqs=["DNA101"],
        intro="Plasmids are like plugins for a cell - files you attach to change its function. But as the saying goes, synbio is 'like writing code inside a burrito': thousands of intersecting messages mean a change can cascade unpredictably, even killing the cell while it makes your protein.",
        tools=["Benchling or SnapGene", "Addgene plasmid files"],
        steps=[
            ("Learn the parts", "Study the ORI, antibiotic-resistance gene, multiple cloning site and promoter, and what each does."),
            ("Understand copy number", "High-copy plasmids give more yield but more burden; pick based on your goal."),
            ("Beware catastrophic success", "Recognise that over-expression can kill cells. Inducible systems mitigate this."),
        ],
        submission="Summarise the function of each major plasmid element in your own words and identify them on a real plasmid map.",
        resources=[
            ("NeoSynBio: Plasmids101", f"{NEO}/plasmids101"),
            ("Addgene: Plasmids 101 eBook (4th edition)", "https://blog.addgene.org/plasmids-101-ebook-4th-edition"),
            ("Addgene: Plasmids 101 blog series", "https://blog.addgene.org/topic/plasmids-101"),
        ],
    ),
    dict(
        id="backbone-selection", title="Backbone Selection (Theory)", lvl=2, level="intermediate",
        time=40, project="Experimental Design",
        desc="Choose the right plasmid backbone for your first experiments.",
        pos=[3.0, 2.3], deps=["plasmids101"],
        objectives=[
            "select a backbone by copy number, resistance and MCS",
            "match a backbone to your expression goal",
            "find and download sequences from Addgene",
        ],
        prereqs=["Plasmids101"],
        intro="Professionals call plasmids 'backbones' and match the backbone to the situation. For a first project, pick a simple plasmid with high copy number and an easy-to-source antibiotic - e.g. pET-15b or an iGEM pSB1C3.",
        tools=["Addgene", "sequence viewer"],
        steps=[
            ("List requirements", "Decide copy number, resistance marker, promoter and whether you need an affinity tag."),
            ("Shortlist backbones", "Compare candidates (pET-15b, pSB1C3, etc.) against your requirements."),
            ("Download the sequence", "Pull the annotated .dna/.gb file from Addgene for in-silico design."),
        ],
        submission="Choose a backbone, justify it against your requirements, and attach the annotated sequence file.",
        resources=[
            ("NeoSynBio: Backbone Selection", f"{NEO}/backbone-selection"),
            ("Addgene: Choosing your perfect plasmid backbone", "https://blog.addgene.org/plasmids-101-choosing-your-perfect-plasmid-backbone"),
            ("iGEM Registry: pSB1C3 and standard backbones", "https://parts.igem.org/Plasmid_backbones/Assembly"),
        ],
    ),
    dict(
        id="miniprep", title="Plasmid Miniprep (Ethanol Lysis)", lvl=2, level="intermediate",
        time=120, project="DNA Extraction",
        desc="Purify plasmid DNA via the premier miniprep workflow: lyse, capture, wash, elute.",
        pos=[0, 4.5], deps=["plasmids101", "sterile-technique", "buffer-mixing"],
        objectives=[
            "perform a silica-column miniprep end to end",
            "handle guanidine-based buffers safely",
            "judge plasmid yield (gel is more reliable than nanodrop)",
        ],
        prereqs=["a fresh pure colony", "miniprep buffers", "a high-speed centrifuge"],
        intro="The miniprep is the premier method for purifying plasmid DNA - doable in under two hours with the right set-up. It uses some nasty chemicals (guanidine), so read the MSDS. A high-speed centrifuge is the single most important piece of equipment here.",
        tools=["high-speed centrifuge", "silica spin columns", "miniprep buffers (resuspension, lysis, neutralisation, wash)", "oven", "nanodrop/Qubit (optional)"],
        steps=[
            ("Pellet & resuspend", "Spin down an overnight culture and resuspend the pellet in resuspension buffer."),
            ("Lyse & neutralise", "Add lysis buffer, wait ~10 min so RNAse degrades RNA, then neutralise and spin to pellet debris."),
            ("Bind to column", "Load the cleared supernatant onto a silica column and spin to capture plasmid DNA."),
            ("Wash & dry", "Wash with chaotropic salt then ethanol; dry in an oven to evaporate residual ethanol."),
            ("Elute", "Add elution buffer and spin into a fresh tube. Store at -20C."),
        ],
        submission="Miniprep a plasmid and report your yield. Verify quality by running an aliquot on an agarose gel.",
        resources=[
            ("NeoSynBio: Miniprep / Ethanol Lysis protocol", f"{NEO}/purification-of-plasmid-dna-miniprep-aka-ethanol-lysis"),
            ("Addgene: Purifying plasmid DNA (protocol & video)", "https://www.addgene.org/protocols/purify-plasmid-dna/"),
            ("QIAGEN: QIAprep Spin Miniprep Kit handbook", "https://www.qiagen.com/us/products/discovery-and-translational-research/dna-rna-purification/dna-purification/plasmid-dna/qiaprep-spin-miniprep-kit"),
        ],
    ),
    dict(
        id="plasmid-insertion", title="Plasmid Insertion (Transformation)", lvl=3, level="intermediate",
        time=120, project="Genetic Modification",
        desc="Get DNA into cells: heat shock, electroporation, or gene guns.",
        pos=[1.7, 5.0], deps=["miniprep"],
        objectives=[
            "perform heat-shock transformation of chemically competent cells",
            "understand electroporation as a higher-efficiency alternative",
            "recover and plate transformants on selection",
        ],
        prereqs=["purified plasmid", "competent cells", "a legal/registered workspace if required"],
        intro="Heat shock, electroporation, gene guns - 'Plasmid Insertion' buries the lead. For first-timers, chemically competent cells + heat shock need the least investment. NOTE: this may count as Genetic Modification in your jurisdiction - check local law first.",
        tools=["chemically competent cells", "heat block or water bath at 42C", "ice", "SOC/LB recovery media", "selection plates"],
        steps=[
            ("Thaw on ice", "Thaw competent cells on ice and gently add your plasmid DNA. Never vortex competent cells."),
            ("Heat shock", "Incubate on ice, pulse at 42C for the strain-specific time, then return to ice."),
            ("Recover", "Add warm recovery media and shake at 37C for ~1 hour (skip for ampicillin selection)."),
            ("Plate & incubate", "Spread onto antibiotic plates and incubate overnight. Include a no-DNA negative control."),
        ],
        submission="Transform a plasmid into your host, plate with controls, and report colony counts the next day.",
        resources=[
            ("NeoSynBio: Plasmid Insertion protocols", f"{NEO}/plasmid-insertion"),
            ("Addgene: Bacterial transformation (protocol & video)", "https://www.addgene.org/protocols/bacterial-transformation/"),
            ("NEB: High-efficiency transformation protocol", "https://www.neb.com/en-us/protocols/2012/05/21/high-efficiency-transformation-protocol-c2987"),
            ("NeoSynBio: Heat shock of chemically competent cells", f"{NEO}/heat-shock-transformation-of-chemically-competent-cells"),
        ],
    ),
    dict(
        id="gel-electrophoresis", title="Agarose Gel Electrophoresis", lvl=3, level="beginner",
        time=90, project="Analysis Core",
        desc="Separate and size DNA fragments - your bread-and-butter readout.",
        pos=[0, 6.0], deps=["miniprep"],
        objectives=[
            "pour an agarose gel at the right percentage",
            "load samples with running dye without bubbles or tails",
            "size fragments against a DNA ladder",
            "choose a safer stain (e.g. Thiazole Orange) over EtBr",
        ],
        prereqs=["DC power supply", "gel tray & bath", "agarose", "TAE buffer", "DNA ladder"],
        intro="DNA's uniform negative charge lets an electric field drag it through agarose; smaller fragments run faster. High-% gels resolve large fragments better and low-% gels resolve small ones. Loading is the skill everyone fears - bubbles are your enemy.",
        tools=["agarose", "TAE buffer", "casting tray & comb", "DC power supply", "DNA ladder", "loading dye", "DNA stain"],
        steps=[
            ("Pour the gel", "Melt agarose in TAE, cool to ~50C, add stain if pre-staining, pour and add the comb. Tape leaky chambers."),
            ("Prep samples", "Spot running dye on parafilm and mix each DNA sample into a dot; keep dots well separated."),
            ("Load carefully", "Steady both elbows, lower the tip into the well, depress slowly. Lift a little buffer to avoid tails. Change tips between samples - especially ladders."),
            ("Run to red", "Place wells near the black (negative) electrode; DNA migrates to red (positive). Stop before the dye runs off."),
        ],
        submission="Run a gel with a ladder and at least one sample. Submit a labelled gel image and estimate the fragment sizes.",
        resources=[
            ("NeoSynBio: Agarose Gel Electrophoresis protocol", f"{NEO}/agarose-electrophoresis"),
            ("Addgene: How to run an agarose gel (protocol & video)", "https://www.addgene.org/protocols/gel-electrophoresis/"),
            ("Addgene: Purifying DNA from an agarose gel", "https://www.addgene.org/protocols/gel-purification/"),
            ("Bio-Rad: Sub-Cell GT agarose gel electrophoresis manual", "https://www.bio-rad.com/sites/default/files/webroot/web/pdf/lsr/literature/M1704400B.PDF"),
        ],
    ),
    dict(
        id="gel-imaging", title="Gel Illumination & Photography", lvl=3, level="beginner",
        time=30, project="Analysis Core",
        desc="Capture publication-quality gel images with cheap kit and a smartphone.",
        pos=[-1.9, 6.5], deps=["gel-electrophoresis"],
        objectives=[
            "choose the right illumination for your stain",
            "build a cheap enclosure + filter for a smartphone camera",
            "avoid the classic gel-dropping tragedy",
        ],
        prereqs=["a stained gel", "a light source"],
        intro="You don't need a fancy transilluminator - a few LEDs, a black enclosure box and a smartphone can beat institutional kit. A badly lit photo of a perfect gel still looks terrible, so this step is as critical as running the gel.",
        tools=["UV or blue-light source", "orange/amber filter", "dark enclosure", "smartphone camera"],
        steps=[
            ("Match light to stain", "Use the excitation wavelength your stain requires (UV for EtBr, blue light for many safer stains)."),
            ("Build an enclosure", "Use a 3D-printed or cardboard black box with an orange filter over the camera to cut glare."),
            ("Carry the gel carefully", "Everyone drops one eventually - support the gel fully on its way to the imager."),
        ],
        submission="Submit a clean, well-exposed gel photo with the lanes and ladder clearly readable.",
        resources=[
            ("NeoSynBio: Gel Illumination & Photography", f"{NEO}/gel-illumination-photography"),
            ("Flowers for Everyone (Sebastian S. Cocioba) - DIY synbio blog", "https://docs.google.com/document/d/10Y4NgXjMRvG_Vd5D4o2lPJp1ehY2R516gpfrh2PZWfw/edit"),
            ("Bio-Rad: gel documentation fundamentals", "https://www.bio-rad.com/en-us/applications-technologies/gel-documentation"),
        ],
    ),
    dict(
        id="gblock-design", title="gBlock & Insert Design (Theory)", lvl=3, level="intermediate",
        time=60, project="Experimental Design",
        desc="Design the perfect synthetic insert - codon optimisation, tags, cut sites.",
        pos=[3.2, 3.5], deps=["backbone-selection"],
        objectives=[
            "design an insert with correct restriction/assembly sites",
            "add affinity and cleavage tags thoughtfully",
            "apply codon optimisation for your host",
        ],
        prereqs=["Backbone Selection", "a sequence viewer"],
        intro="A gBlock is a synthetic DNA strand designed for insertion. Good design front-loads success: pick compatible cut sites, include the transcription/translation machinery, and plan affinity tags now because they're painful to add later.",
        tools=["Benchling or SnapGene", "a codon-optimisation tool", "synthesis vendor"],
        steps=[
            ("Define the construct", "Lay out promoter, RBS, start/stop codons, your gene, and any tags in the correct frame."),
            ("Add compatible sites", "Include restriction sites (or assembly overhangs) that match your chosen backbone and won't cut internally."),
            ("Codon-optimise", "Optimise codons for your host to boost expression, then order the synthesised fragment."),
        ],
        submission="Design a complete insert in your viewer, with annotated sites and tags, ready to order. Export the sequence.",
        resources=[
            ("NeoSynBio: gBlock Design", f"{NEO}/gblock-design"),
            ("Addgene: Plasmid cloning by PCR (primer & insert design)", "https://www.addgene.org/protocols/pcr-cloning/"),
            ("IDT: gBlocks gene fragments design guidelines", "https://www.idtdna.com/pages/products/genes-and-gene-fragments/double-stranded-dna-fragments/gblocks-gene-fragments"),
            ("Benchling: sequence design tutorials", "https://www.benchling.com/the-basics-of-primer-design-for-pcr"),
        ],
    ),
    dict(
        id="restriction-digest", title="Restriction Enzyme Digest", lvl=3, level="intermediate",
        time=120, project="Cut & Paste Cloning",
        desc="Cut plasmid and insert with restriction enzymes; plan with a sequence viewer.",
        pos=[-0.4, 7.5], deps=["backbone-selection", "gel-electrophoresis", "gblock-design"],
        objectives=[
            "select unique-cutter enzymes using a sequence viewer",
            "design and simulate a clean directional ligation",
            "set up a digest and keep enzymes cold at all times",
        ],
        prereqs=["purified plasmid", "an insert", "restriction enzymes", "a sequence viewer"],
        intro="Restriction enzymes are being phased out by Gibson/Golden Gate, but they're an excellent way to learn. In your viewer, filter to unique cutters to avoid shredding your plasmid, find the MCS, and design a non-palindromic two-enzyme digest for directional cloning.",
        tools=["restriction enzymes (kept on ice)", "digest buffer", "sequence viewer", "thermocycler/heat block"],
        steps=[
            ("Filter to unique cutters", "In SnapGene/Benchling, show only enzymes that cut once to find usable sites in the MCS."),
            ("Pick two enzymes", "Choose two enzymes with compatible buffers and non-homologous ends to force correct orientation."),
            ("Simulate the assembly", "Virtually digest and ligate to confirm a clean junction before touching the bench."),
            ("Run the digest", "Combine DNA, enzymes and buffer; incubate at the enzyme's temperature; keep enzymes on ice whenever out of the freezer."),
        ],
        submission="Submit your in-silico cloning map plus a gel showing the digested backbone and insert at expected sizes.",
        resources=[
            ("NeoSynBio: Restriction Enzyme Digest protocol", f"{NEO}/restriction-enzyme-digest-of-plasmid-and-insert-dna"),
            ("NEB: Restriction enzyme digestion overview & double digest finder", "https://www.neb.com/en-us/tools-and-resources/usage-guidelines/double-digest-finder"),
            ("Addgene: Plasmid screening by restriction digest", "https://blog.addgene.org/plasmids-101-plasmid-screening-strategies"),
            ("SnapGene: simulating restriction cloning", "https://www.snapgene.com/guides"),
        ],
    ),
    dict(
        id="ligation", title="Ligation & Troubleshooting", lvl=3, level="intermediate",
        time=90, project="Cut & Paste Cloning",
        desc="Glue DNA with T4 ligase and design the five control plates that save you weeks.",
        pos=[0, 9.0], deps=["restriction-digest", "plasmid-insertion"],
        objectives=[
            "set up a T4 DNA ligase reaction",
            "protect thermosensitive ligase buffer with tiny aliquots",
            "design the full panel of control plates",
        ],
        prereqs=["digested backbone and insert", "T4 DNA ligase", "competent cells"],
        intro="T4 DNA ligase glues DNA back together. Its buffer is the most thermosensitive reagent in the whole guide - 1-2 freeze/thaw cycles and it's done, so aliquot into 10 ul tubes. Controls aren't optional: they're your bumpers for debugging perishable reagents.",
        tools=["T4 DNA ligase", "ligase buffer (aliquoted)", "digested DNA", "competent cells", "control plates"],
        steps=[
            ("Aliquot the buffer", "Split ligase buffer into 10 ul single-use tubes; only thaw one at a time."),
            ("Set up the reaction", "Combine vector, insert, ligase and ATP-containing buffer at the right molar ratio; add kinase if ends are dephosphorylated."),
            ("Run the controls", "Set up negative (no plasmid), positive (uncut), digest-only, ligation, and optional dephosphorylation plates."),
            ("Transform & interpret", "Transform the ligation mix and read each control plate to localise any failure."),
        ],
        submission="Submit your ligation plus a labelled photo of all control plates, with a one-line interpretation of each.",
        resources=[
            ("NeoSynBio: Ligation & Troubleshooting", f"{NEO}/ligation-troubleshooting"),
            ("NEB: DNA ligation with T4 DNA ligase (protocol)", "https://www.neb.com/en-us/protocols/0001/01/01/dna-ligation-with-t4-dna-ligase-m0202"),
            ("Addgene: DNA ligation protocol", "https://www.addgene.org/protocols/dna-ligation/"),
            ("Addgene: Plasmid screening strategies", "https://blog.addgene.org/plasmids-101-plasmid-screening-strategies"),
        ],
    ),
    dict(
        id="pcr", title="Polymerase Chain Reaction (PCR)", lvl=4, level="intermediate",
        time=120, project="Amplification",
        desc="Amplify any DNA region exponentially with a thermocycler and a master mix.",
        pos=[1.9, 7.0], deps=["gel-electrophoresis"],
        objectives=[
            "explain denaturation, annealing and extension",
            "assemble a master mix and distribute reactions",
            "program thermocycler variables for your amplicon",
        ],
        prereqs=["template DNA", "primers", "a thermocycler", "polymerase + dNTPs"],
        intro="PCR uses heating/cooling cycles to make a polymerase replicate the region between two primers, doubling product each cycle until millions of copies exist by ~25 cycles. Set up a master mix, distribute, add your variable, and let the machine work while you have a sandwich.",
        tools=["thermocycler", "DNA polymerase (Taq/Q5/Phusion)", "dNTPs", "primers", "template", "master mix tubes"],
        steps=[
            ("Build a master mix", "Combine water, buffer, dNTPs, polymerase and primers common to all reactions; add polymerase last on ice."),
            ("Distribute & add template", "Split the mix into tubes and add each template/variable."),
            ("Program the cycler", "Set initial denaturation, then 25-35 cycles of denature/anneal/extend, using the NEB Tm Calculator for annealing temperature."),
            ("Check on a gel", "Run the product on an agarose gel to confirm a band of the expected size."),
        ],
        submission="Amplify a target region and submit a gel showing a clean single band at the expected size.",
        resources=[
            ("NeoSynBio: PCR protocol", f"{NEO}/polymerase-chain-reaction"),
            ("NEB: Polymerase Chain Reaction (PCR) overview", "https://www.neb.com/en-us/applications/dna-amplification-pcr-and-qpcr/polymerase-chain-reaction-pcr"),
            ("NEB: Protocol for a routine PCR reaction", "https://www.neb.com/en/protocols/protocol-for-a-routine-pcr-reaction-e0553"),
            ("NEB Tm Calculator (annealing temperature)", "https://tmcalculator.neb.com/"),
        ],
    ),
    dict(
        id="primer-design", title="Primer Design", lvl=4, level="intermediate",
        time=60, project="Amplification",
        desc="Design primer pairs that bind your template, not each other.",
        pos=[3.0, 7.8], deps=["pcr"],
        objectives=[
            "apply length, GC%, Tm and GC-clamp guidelines",
            "avoid self-dimers and primer dimers",
            "use Benchling/Primer3 and the NEB Tm Calculator",
        ],
        prereqs=["PCR fundamentals", "a sequence viewer"],
        intro="Primers are short (~15-30 bp) sequences that kickstart PCR. The biggest challenge is designing them to prefer your template over each other - primer dimers can ruin a month. Aim for Tm 50-60C, GC 40-60%, and keep paired Tms within 5C.",
        tools=["Benchling primer wizard or Primer3", "NEB Tm Calculator", "NCBI BLAST"],
        steps=[
            ("Set parameters", "Target length ~18-25 nt, GC 40-60%, Tm 50-60C, with a 3' GC clamp where possible."),
            ("Check for dimers", "Use a design wizard to flag self-dimers, hairpins and primer-primer complementarity."),
            ("Validate specificity", "BLAST your primers against the genome to rule out off-target binding."),
            ("Confirm Tm", "Calculate annealing temperature with the NEB Tm Calculator for your specific polymerase."),
        ],
        submission="Design a validated primer pair, report Tm/GC/length for each, and show the dimer/specificity checks.",
        resources=[
            ("NeoSynBio: Primer Design", f"{NEO}/primer-design"),
            ("Benchling: The basics of primer design for PCR", "https://www.benchling.com/the-basics-of-primer-design-for-pcr"),
            ("NEB Tm Calculator", "https://tmcalculator.neb.com/"),
            ("Primer3 / Primer3Plus", "https://primer3.org/"),
        ],
    ),
    dict(
        id="gradient-pcr", title="Gradient PCR", lvl=4, level="intermediate",
        time=60, project="Amplification",
        desc="Find the optimal annealing temperature in a single run.",
        pos=[3.2, 9.0], deps=["primer-design"],
        objectives=[
            "use a temperature gradient to optimise annealing",
            "interpret a gradient gel to pick the best Tm",
            "substitute day-by-day runs if you lack a gradient cycler",
        ],
        prereqs=["a primer pair", "ideally a gradient thermocycler"],
        intro="A gradient thermocycler runs the same reaction at a different temperature per column, testing up to 12 annealing temperatures at once. Without one, you can run the same reaction day after day - a gradient cycler is a quality-of-life upgrade worth scouting university surplus for.",
        tools=["gradient thermocycler (ideal)", "primers", "template", "polymerase"],
        steps=[
            ("Set the gradient", "Program a temperature gradient spanning ~5-10C around your predicted Tm."),
            ("Run & gel", "Run all columns, then load each on a gel side by side."),
            ("Pick the winner", "Choose the temperature giving the strongest specific band with the least non-specific product."),
        ],
        submission="Submit a gradient gel image and state the optimal annealing temperature you'll use going forward.",
        resources=[
            ("NeoSynBio: Gradient PCR", f"{NEO}/gradient-pcr"),
            ("NEB Tm Calculator (gradient planning)", "https://tmcalculator.neb.com/"),
            ("Bio-Rad: PCR temperature optimization", "https://www.bio-rad.com/en-us/applications-technologies/pcr-optimization"),
        ],
    ),
    dict(
        id="flanking-addition", title="Flanking Sequence Addition", lvl=4, level="intermediate",
        time=60, project="Amplification",
        desc="Add restriction sites or assembly overhangs via 5' primer overhangs.",
        pos=[1.8, 8.5], deps=["primer-design"],
        objectives=[
            "exploit that 3' homology matters more than 5'",
            "add sites by designing 5' primer overhangs",
            "'lift' a gene out of a plasmid or environmental sample",
        ],
        prereqs=["Primer Design", "PCR"],
        intro="A neat PCR trick: because 3' homology matters far more than 5', you can add whatever you want to the 5' end of a primer. That lets you append restriction sites - or Gibson/Golden Gate overhangs - and even lift genes out of their natural context.",
        tools=["custom primers with 5' overhangs", "PCR reagents"],
        steps=[
            ("Design the overhang", "Keep the 3' end fully complementary to the template; append your new sequence to the 5' end."),
            ("Amplify", "Run PCR - early cycles use only the template-binding region, later cycles incorporate the full primer."),
            ("Confirm", "Gel-check that the product gained the expected length from the added flanks."),
        ],
        submission="Add restriction sites (or assembly overhangs) to a fragment by PCR and confirm the size shift on a gel.",
        resources=[
            ("NeoSynBio: Flanking Sequence Addition", f"{NEO}/flanking-restriction-site-addition"),
            ("Addgene: Adding restriction sites by PCR (PCR cloning)", "https://www.addgene.org/protocols/pcr-cloning/"),
            ("NEB: designing primers with 5' additions", "https://www.neb.com/en-us/tools-and-resources/usage-guidelines"),
        ],
    ),
    dict(
        id="confirmation", title="Confirmation of Edits", lvl=5, level="intermediate",
        time=180, project="Screening",
        desc="Screen clones with patch plates, colony PCR and restriction-digest analysis.",
        pos=[0, 10.7], deps=["ligation", "pcr"],
        objectives=[
            "verify controls before trusting colonies",
            "run a patch plate + colony PCR to screen candidates",
            "confirm identity by diagnostic restriction digest",
        ],
        prereqs=["colonies on a ligation plate", "PCR", "primers"],
        intro="Colonies don't equal success - undigested plasmid and contamination produce false positives that look identical to real clones. First check your control plates, then patch-plate and colony-PCR your candidates, and confirm the best ones with a diagnostic digest (or sequencing).",
        tools=["fresh antibiotic plate", "PCR master mix + screening primers", "restriction enzymes", "gel kit"],
        steps=[
            ("Check controls first", "Confirm each control plate matches expectations before screening anything."),
            ("Patch + colony PCR", "Number colonies, patch them onto a gridded plate, and colony-PCR each with junction/spanning primers."),
            ("Gel the screen", "Run the colony PCR on a gel; candidates with the expected band advance."),
            ("Diagnostic digest", "Miniprep the best candidates and digest to confirm band sizes match the in-silico map."),
        ],
        submission="Submit a colony-PCR gel and a diagnostic-digest gel identifying at least one confirmed correct clone.",
        resources=[
            ("NeoSynBio: Confirmation of Edits", f"{NEO}/confirmation-of-edits"),
            ("NeoSynBio: Patch Plate & Colony PCR", f"{NEO}/patch-plate-colony-pcr"),
            ("Addgene: Plasmid screening strategies (incl. colony PCR)", "https://blog.addgene.org/plasmids-101-plasmid-screening-strategies"),
            ("Addgene: Verify your clones with colony PCR (Gateway blog)", "https://blog.addgene.org/plasmids-101-gateway-cloning"),
        ],
    ),
    dict(
        id="sequencing", title="Sequencing Prep & Interpretation", lvl=5, level="intermediate",
        time=90, project="Screening",
        desc="Prepare samples for external (or in-house Nanopore) sequencing and read results.",
        pos=[-2.0, 11.0], deps=["confirmation"],
        objectives=[
            "prepare purified product + primer for Sanger sequencing",
            "decide when sequencing beats gel screening on cost",
            "interpret chromatograms / alignments",
        ],
        prereqs=["a purified plasmid or PCR product", "a sequencing primer"],
        intro="Sequencing prices keep dropping (synbio's Carlson Curve). At under ~$0.10/bp you can treat sequencing as an alternative to screening everything yourself - though preliminary screening still saves money. Send only your best candidates with a good primer.",
        tools=["purified DNA", "sequencing primer", "sequence-alignment software"],
        steps=[
            ("Purify & quantify", "Clean up your plasmid or PCR product and quantify it to the provider's spec."),
            ("Send with a primer", "Pair the sample with an appropriate sequencing primer per the provider's instructions."),
            ("Align & interpret", "Align the read to your designed sequence to confirm the edit and check for mutations."),
        ],
        submission="Submit an alignment of your sequencing read against your designed construct, highlighting that the edit is correct.",
        resources=[
            ("NeoSynBio: Preparation for External Sequencing", f"{NEO}/external-sequencing-prep"),
            ("Oxford Nanopore: protocols resource centre (in-house sequencing)", "https://nanoporetech.com/resource-centre/protocols"),
            ("Addgene: analyze sequencing results (Sanger)", "https://blog.addgene.org/plasmids-101-plasmid-screening-strategies"),
        ],
    ),
    dict(
        id="gibson", title="Gibson Assembly", lvl=6, level="advanced",
        time=120, project="Advanced Assembly",
        desc="Scarless single-tube assembly of up to ~6 fragments via homologous overlaps.",
        pos=[2.0, 10.7], deps=["flanking-addition", "ligation"],
        objectives=[
            "design primers with homologous overlaps",
            "assemble multiple fragments in one isothermal reaction",
            "decide when to switch from RE digest to single-step cloning",
        ],
        prereqs=["Primer Design", "Flanking Sequence Addition"],
        intro="Gibson Assembly replaces digest+ligation with a single isothermal reaction that joins fragments via homologous overlapping ends - reportedly up to 6 at once. Most of the work is primer design for scarless overlaps, so revise that first.",
        tools=["Gibson assembly master mix", "PCR fragments with overlaps", "thermocycler"],
        steps=[
            ("Design overlaps", "Design ~20-40 bp homologous overlaps between adjacent fragments using your assembly wizard."),
            ("Amplify fragments", "PCR each fragment with the overlap-adding primers; gel-confirm sizes."),
            ("Assemble", "Combine fragments with the master mix and incubate at 50C; transform directly."),
        ],
        submission="Assemble a multi-fragment construct by Gibson and confirm it by colony PCR or sequencing.",
        resources=[
            ("NeoSynBio: Gibson Assembly", f"{NEO}/gibson-assembly"),
            ("NEB: Gibson Assembly overview & protocol", "https://www.neb.com/en-us/applications/cloning-and-synthetic-biology/dna-assembly-and-cloning/gibson-assembly"),
            ("Addgene: choosing a molecular cloning technique", "https://blog.addgene.org/plasmids-101-sequence-and-ligation-independent-cloning"),
            ("Benchling: Gibson assembly wizard", "https://www.benchling.com/"),
        ],
    ),
    dict(
        id="golden-gate", title="Golden Gate Assembly", lvl=6, level="advanced",
        time=120, project="Advanced Assembly",
        desc="Type IIS scarless assembly of 10+ ordered fragments in one tube.",
        pos=[3.4, 10.9], deps=["flanking-addition", "restriction-digest"],
        objectives=[
            "use Type IIS enzymes that cut outside their recognition site",
            "design fragments without internal recognition sites ('domestication')",
            "assemble many ordered fragments in one reaction",
        ],
        prereqs=["Restriction Digest", "Flanking Sequence Addition"],
        intro="Golden Gate uses Type IIS enzymes (which cut outside their recognition site) to create scarless, directional, one-tube assemblies of 10+ fragments. Because cut sites are removed during assembly, ligation can proceed immediately - no purification step.",
        tools=["Type IIS enzyme (BsaI/BsmBI)", "T4 ligase", "fragments with designed overhangs", "thermocycler"],
        steps=[
            ("Design overhangs", "Place Type IIS sites so digestion leaves unique 4 nt overhangs that define fragment order."),
            ("Domesticate fragments", "Remove internal recognition sites via silent mutations so only the designed sites are cut."),
            ("Cycle digest-ligate", "Run alternating digest/ligation cycles in one tube, then transform."),
        ],
        submission="Assemble an ordered multi-part construct by Golden Gate and confirm correct assembly by screening.",
        resources=[
            ("NeoSynBio: Golden Gate Assembly", f"{NEO}/golden-gate-assembly"),
            ("NEB: Golden Gate Assembly overview & protocol", "https://www.neb.com/en-us/applications/cloning-and-synthetic-biology/dna-assembly-and-cloning/golden-gate-assembly"),
            ("Addgene: Plasmids 101 - Golden Gate cloning", "https://blog.addgene.org/plasmids-101-golden-gate-cloning"),
        ],
    ),
    dict(
        id="sdm", title="Site-Directed Mutagenesis", lvl=6, level="advanced",
        time=120, project="Advanced Editing",
        desc="Introduce a precise point mutation via megaprimer or round-the-world PCR.",
        pos=[4.0, 9.2], deps=["primer-design", "gradient-pcr"],
        objectives=[
            "design mutagenic primers carrying the desired change",
            "choose megaprimer vs round-the-world strategies",
            "screen for the intended mutation",
        ],
        prereqs=["Primer Design", "Gradient PCR"],
        intro="SDM makes an almost-perfect copy of your gene with a single intentional point mutation. Use a megaprimer assembled with a backbone, or a round-the-world SDM PCR to remake the backbone too. This is genetic modification - check local rules.",
        tools=["mutagenic primers", "high-fidelity polymerase", "DpnI (to remove template)"],
        steps=[
            ("Design mutagenic primers", "Centre the mismatch within the primer with sufficient flanking complementarity."),
            ("Amplify the mutant", "Run high-fidelity PCR; for round-the-world, amplify the whole plasmid."),
            ("Remove template & screen", "DpnI-digest the methylated template, transform, and sequence to confirm the mutation."),
        ],
        submission="Introduce a defined point mutation and confirm it by sequencing the screened clone.",
        resources=[
            ("NeoSynBio: Site Directed Mutagenesis", f"{NEO}/site-directed-mutagenesis"),
            ("NEB: Q5 Site-Directed Mutagenesis Kit protocol", "https://www.neb.com/en-us/products/e0554-q5-site-directed-mutagenesis-kit"),
            ("Addgene: site-directed mutagenesis overview", "https://blog.addgene.org/plasmids-101-mutagenesis"),
        ],
    ),
    dict(
        id="crispr", title="CRISPR / Cas9", lvl=6, level="advanced",
        time=180, project="Advanced Editing",
        desc="Target precise genomic edits with a Cas enzyme and a designed guide RNA.",
        pos=[2.4, 12.2], deps=["ligation", "primer-design"],
        objectives=[
            "design a specific ~20 nt gRNA with a valid PAM",
            "plan knockout vs knock-in (HDR) experiments",
            "balance on-target activity against off-targets",
        ],
        prereqs=["Ligation/cloning", "Primer Design"],
        intro="CRISPR uses a short guide RNA to direct a Cas enzyme to a ~20 nt target adjacent to a PAM, where it cuts DNA. Repair by NHEJ yields knockouts; an HDR template yields precise edits. The art is choosing a unique target and minimising off-targets.",
        tools=["gRNA design tool (CRISPOR/Benchling/SnapGene)", "Cas9 plasmid", "cloning reagents", "(HDR template if knock-in)"],
        steps=[
            ("Define the edit", "Decide knockout (no template) vs precise edit (HDR template)."),
            ("Design the gRNA", "Pick a unique ~20 nt target next to a PAM; score on-/off-target with a design tool."),
            ("Clone the guide", "Insert the gRNA oligos into a Cas9 plasmid (often via Golden Gate)."),
            ("Deliver & validate", "Deliver the Cas9+gRNA into cells and validate the edit by sequencing."),
        ],
        submission="Design a validated gRNA (with PAM and off-target assessment) and outline your knockout or knock-in strategy.",
        resources=[
            ("NeoSynBio: CRISPR/Cas9 protocol", f"{NEO}/crisprcas9"),
            ("Addgene: CRISPR Guide & 'Plan your experiment'", "https://www.addgene.org/guides/crispr/"),
            ("Addgene: CRISPR references & gRNA design tools", "https://www.addgene.org/crispr/reference/"),
            ("SnapGene: guide to gRNA design for CRISPR", "https://www.snapgene.com/guides/design-grna-for-crispr"),
        ],
    ),
    dict(
        id="proteins101", title="Proteins101 (Theory)", lvl=7, level="intermediate",
        time=45, project="Theory",
        desc="Working knowledge of protein mechanics before producing them in the lab.",
        pos=[0, 12.2], deps=["confirmation"],
        objectives=[
            "describe protein structure levels and folding",
            "connect sequence to expression and purification choices",
            "understand disulphide bonds and misfolding risks",
        ],
        prereqs=["a confirmed expression construct"],
        intro="Whether you've mastered DNA manipulation or just want to make GFP, a working knowledge of protein mechanics serves you well. This theory primer covers enough to produce, purify and observe proteins - read more widely for the deep end.",
        tools=["literature", "structure viewers (e.g. PyMOL, AlphaFold DB)"],
        steps=[
            ("Review structure", "Refresh primary->quaternary structure and how folding determines function."),
            ("Plan for folding", "Note where disulphide bonds or complex folds may require slower expression."),
            ("Map to methods", "Connect your protein's properties to induction, lysis and purification choices."),
        ],
        submission="Summarise your target protein's key properties (size, tags, folding needs) and how they shape your downstream plan.",
        resources=[
            ("NeoSynBio: Proteins101 (Graduate's Guide)", f"{NEO}/the-graduates-guide-to-synthetic-biology"),
            ("Khan Academy: Macromolecules / proteins", "https://www.khanacademy.org/science/biology"),
            ("RCSB PDB-101: protein structure education", "https://pdb101.rcsb.org/"),
            ("EMBL-EBI: protein bioinformatics training", "https://www.ebi.ac.uk/training/"),
        ],
    ),
    dict(
        id="protein-induction", title="Induction of Protein Expression", lvl=7, level="intermediate",
        time=120, project="Protein Production",
        desc="Trigger protein expression at the right growth phase using OD600.",
        pos=[0, 13.7], deps=["proteins101"],
        objectives=[
            "compare inducible vs constitutive expression",
            "measure OD600 to time induction",
            "tune temperature post-induction for correct folding",
        ],
        prereqs=["an expression construct in a host", "a spectrophotometer"],
        intro="Inducible expression lets you switch protein production on during exponential growth, avoiding the burden of constitutive expression. For E. coli, time induction by OD600. After inducing, you can lower the temperature to slow folding for complex proteins.",
        tools=["spectrophotometer + cuvettes", "inducer (e.g. IPTG)", "shaking incubator", "baffled flasks"],
        steps=[
            ("Grow to phase", "Grow cells at 37C with shaking until OD600 reaches the target window for your system."),
            ("Induce", "Add inducer (e.g. IPTG) to switch on expression."),
            ("Tune temperature", "For disulphide-bonded/complex proteins, drop the temperature to slow folding and reduce misfolding."),
        ],
        submission="Produce a growth curve (OD600 vs time), mark your induction point, and note your post-induction conditions.",
        resources=[
            ("NeoSynBio: Induction of Protein Expression", f"{NEO}/induction-of-protein-expression"),
            ("Thermo Fisher: recombinant protein expression learning center", "https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center.html"),
            ("NEB: protein expression with T7 systems", "https://www.neb.com/en-us/applications/protein-expression-and-analysis"),
        ],
    ),
    dict(
        id="cell-lysis", title="Cell Lysis", lvl=7, level="intermediate",
        time=90, project="Protein Production",
        desc="Bust open cells to release your protein into cell slurry.",
        pos=[0, 15.2], deps=["protein-induction"],
        objectives=[
            "choose a lysis method (chemical, sonication, bead-beating)",
            "include protease inhibitors and keep samples cold",
            "clarify lysate to separate soluble protein",
        ],
        prereqs=["induced cell pellet"],
        intro="Once your protein is made, you have to extract it - 'there are many ways to skin E. coli'. Lysis releases everything inside the cell as 'cell slurry'; the right enzymes/inhibitors protect your protein of interest during the process.",
        tools=["lysis buffer / detergent reagent", "sonicator or bead beater", "protease inhibitors", "centrifuge"],
        steps=[
            ("Resuspend cold", "Resuspend the pellet in cold lysis buffer with protease inhibitors; keep on ice throughout."),
            ("Lyse", "Sonicate (pulsed, on ice) or bead-beat until the cloudy suspension turns translucent."),
            ("Clarify", "Centrifuge to separate soluble protein (supernatant) from debris/inclusion bodies (pellet)."),
        ],
        submission="Lyse an induced culture and keep aliquots of lysate, cleared supernatant and pellet for SDS-PAGE analysis.",
        resources=[
            ("NeoSynBio: Cell Lysis protocols", f"{NEO}/cell-lysis"),
            ("Thermo Scientific: Pierce Cell Lysis Technical Handbook", "https://tools.thermofisher.com/content/sfs/brochures/1601757-Cell-Lysis-Handbook.pdf"),
            ("Thermo Fisher: traditional methods of cell lysis", "https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/traditional-methods-cell-lysis.html"),
        ],
    ),
    dict(
        id="affinity-purification", title="Affinity Tag Purification", lvl=7, level="advanced",
        time=150, project="Protein Production",
        desc="Recover tagged protein from cell slurry (His-tag / Ni-NTA, or Car9/silica).",
        pos=[-1.6, 16.2], deps=["cell-lysis", "gblock-design"],
        objectives=[
            "bind, wash and elute a His-tagged protein on Ni-NTA",
            "use imidazole gradients to maximise purity",
            "consider cheaper tags (Car9/silica) at design time",
        ],
        prereqs=["clarified lysate with a tagged protein", "Ni-NTA resin"],
        intro="With an affinity tag (designed in at the gBlock stage), purification is tractable: the tag binds a substrate (His-tag to Ni-NTA), contaminants wash away, then a competitor (imidazole) elutes your protein. FPLC scales this up; gravity columns work on a budget.",
        tools=["Ni-NTA resin / spin columns", "binding/wash/elution buffers", "imidazole", "centrifuge or gravity column"],
        steps=[
            ("Bind", "Apply cleared lysate to equilibrated Ni-NTA resin so the His-tag binds the nickel."),
            ("Wash", "Wash with low-imidazole buffer (~20-30 mM) to remove weakly-bound contaminants."),
            ("Elute", "Elute with high imidazole (~250-500 mM); collect fractions for analysis."),
            ("Analyse", "Save load, flow-through, wash and elution fractions for SDS-PAGE."),
        ],
        submission="Purify a tagged protein and submit the fraction set (load/FT/wash/elution) ready for an SDS-PAGE gel.",
        resources=[
            ("NeoSynBio: Affinity Tag Purification", f"{NEO}/affinity-tag-purification"),
            ("Thermo Fisher: His-tagged protein production & purification", "https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/his-tagged-proteins-production-purification.html"),
            ("Thermo Fisher: HisPur Ni-NTA purification kit handbook", "https://assets.fishersci.com/TFS-Assets/LSG/manuals/MAN0011702_HisPur_NiNTA_Purifi_UG.pdf"),
            ("Hebrew University: small-scale His-tag purification protocol", "https://wolfson.huji.ac.il/purification/TagProteinPurif/HisTag_nature.htm"),
        ],
    ),
    dict(
        id="sds-page", title="SDS-PAGE", lvl=7, level="advanced",
        time=150, project="Proteome Analysis",
        desc="Size and quantify proteins on a denaturing polyacrylamide gel.",
        pos=[0, 16.7], deps=["affinity-purification", "gel-electrophoresis"],
        objectives=[
            "cast/handle a polyacrylamide gel safely",
            "denature samples and coat them in SDS for uniform charge",
            "size proteins against a ladder and assess purity",
        ],
        prereqs=["protein fractions", "an SDS-PAGE rig"],
        intro="SDS-PAGE separates proteins by size. Because proteins lack DNA's uniform charge, they're denatured and wrapped in negative SDS ions so migration depends on size alone. It's the smelliest, most technically demanding gel in the guide - master it and everyone will beg you to run theirs.",
        tools=["polyacrylamide gel rig", "SDS sample buffer + reducing agent (DTT)", "protein ladder", "Coomassie/GelCode stain"],
        steps=[
            ("Prep samples", "Mix fractions with SDS loading buffer and a reducing agent (DTT to avoid the b-mercaptoethanol smell); heat to denature."),
            ("Cast or use a gel", "Use a pre-cast or hand-cast polyacrylamide gel of the right percentage for your protein size."),
            ("Run & stain", "Load samples + ladder, run at constant voltage, then stain (e.g. Coomassie/GelCode) to visualise bands."),
            ("Assess purity", "Compare your elution lane to load/wash lanes to judge purity and confirm the expected molecular weight."),
        ],
        submission="Submit a stained SDS-PAGE gel showing your purified protein at the expected size, alongside load/flow-through/wash lanes.",
        resources=[
            ("NeoSynBio: SDS-PAGE protocol", f"{NEO}/sds-page"),
            ("Bio-Rad: A guide to polyacrylamide gel electrophoresis and detection", "https://www.bio-rad.com/en-us/applications-technologies/protein-electrophoresis-methods"),
            ("Thermo Fisher: overview of SDS-PAGE", "https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/overview-electrophoresis.html"),
            ("NeoSynBio: SDS-PAGE enclosure equipment", f"{NEO}/sdspage-enclosure"),
        ],
    ),
    dict(
        id="final-project", title="Capstone: Express & Purify a Protein", lvl=8, level="advanced",
        time=600, project="Capstone",
        desc="Demonstrate mastery end to end: design, build, confirm, express and purify a protein.",
        pos=[0, 18.2], deps=["sds-page", "gel-imaging", "confirmation"],
        objectives=[
            "integrate every skill from sterile technique to purification",
            "produce a verifiable protein product (e.g. GFP)",
            "document the full workflow reproducibly",
        ],
        prereqs=["the core wet-lab nodes above"],
        intro="Synthesise everything: pick a target (GFP is ideal - you can literally see success), design and build the construct, transform and confirm it, induce expression, lyse, and purify. This is the bowling-with-bumpers victory lap that proves you're an independent synthetic biologist.",
        tools=["everything from the preceding nodes"],
        steps=[
            ("Design & build", "Design an expression construct and assemble it (RE digest, Gibson, or Golden Gate)."),
            ("Confirm", "Screen and sequence-confirm a correct clone."),
            ("Express & purify", "Induce expression, lyse cells, and affinity-purify the protein."),
            ("Verify & document", "Confirm the product (fluorescence and/or SDS-PAGE) and write up a reproducible protocol."),
        ],
        submission="Submit a complete mini lab-report: design rationale, confirmation data, expression/purification gels, and a reproducible protocol.",
        resources=[
            ("NeoSynBio: All Protocols", f"{NEO}/protocols"),
            ("iGEM: project & engineering resources", "https://technology.igem.org/"),
            ("Addgene: fluorescent proteins guide (GFP capstone)", "https://www.addgene.org/fluorescent-proteins/"),
            ("Benchling: notebook for documenting your build", "https://www.benchling.com/"),
        ],
    ),
    dict(
        id="advanced-omics", title="Beyond the Bench: RNA, Omics & Bio-Programming", lvl=8, level="advanced",
        time=240, project="Future Directions",
        desc="Stretch goals: Western/ELISA, RNA workflows (RT-qPCR), gene switches and omics.",
        pos=[0, 19.7], deps=["final-project"],
        objectives=[
            "survey proteome analysis (Western blot, ELISA, mass spec)",
            "survey RNA workflows (RT-PCR, RT-qPCR, Northern blot)",
            "explore gene switches, omics and advanced biological programming",
        ],
        prereqs=["the capstone"],
        intro="The guide's frontier: antibody production, Western/Eastern blots, ELISA, aptamers and mass spec for proteomes; RNA purification, RT-PCR/RT-qPCR and Northern blots for transcriptomes; plus gene switches, omics and advanced biological programming. Pick a thread and go deep.",
        tools=["depends on the chosen sub-topic"],
        steps=[
            ("Pick a track", "Choose proteome analysis, RNA/transcriptomics, or biological programming."),
            ("Find the canonical guide", "Use the linked references to find the best-rated protocol for your chosen technique."),
            ("Run a pilot", "Design and run a small pilot experiment in your chosen area."),
        ],
        submission="Pick one advanced technique, summarise the best protocol you found, and propose a pilot experiment.",
        resources=[
            ("NeoSynBio: Graduate's Guide (advanced sections)", f"{NEO}/the-graduates-guide-to-synthetic-biology"),
            ("Bio-Rad: Western blotting guide", "https://www.bio-rad.com/en-us/applications-technologies/western-blotting"),
            ("Thermo Fisher: ELISA technical guide", "https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/overview-elisa.html"),
            ("NEB: RNA reagents & RT-qPCR resources", "https://www.neb.com/en-us/applications/rna-analysis"),
        ],
    ),
]

# ======================= EXPANSION: new nodes ============================
NODES += [
    # ---- Equipment side-tree ----
    dict(
        id="micropipette", title="THE Micropipette", lvl=1, level="beginner",
        time=30, project="Equipment",
        desc="Master the single most important tool in the lab: accurate, bubble-free pipetting.",
        pos=[-3.5, -0.6], deps=["intro"],
        objectives=["set volume correctly across P10/P100/P1000", "use first vs second stop", "avoid bubbles and ensure accuracy/precision"],
        prereqs=["a set of micropipettes and tips"],
        intro="The micropipette is the most important tool in your arsenal. Accurate, confident pipetting underpins every protocol in this tree - get comfortable here and everything downstream gets easier.",
        tools=["P10/P100/P1000 micropipettes", "appropriate tips", "practice tubes", "coloured water"],
        steps=[
            ("Pick the right pipette", "Choose the pipette whose range brackets your target volume; never set beyond the marked range."),
            ("Set the volume", "Dial to the target volume, reading the digits correctly for each pipette model."),
            ("Aspirate & dispense", "Press to the first stop to draw up; use the second stop to fully expel. Pipette slowly to avoid bubbles."),
            ("Verify accuracy", "Practise with coloured water and, if possible, check by weighing on a balance."),
        ],
        submission="Demonstrate accurate transfers across P10/P100/P1000 (a photo or short clip), and note any accuracy check you performed.",
        resources=[
            ("NeoSynBio: THE Micropipette equipment guide", f"{NEO}/micropipette"),
            ("Addgene: pipetting fundamentals (Intro to the Lab Bench)", "https://www.addgene.org/protocols/"),
            ("Eppendorf: how to pipette correctly", "https://www.eppendorf.com/us-en/lab-academy/lab-practice/"),
        ],
    ),
    dict(
        id="centrifuge", title="The Centrifuge", lvl=1, level="beginner",
        time=20, project="Equipment",
        desc="Pellet cells and clear lysates safely - the workhorse behind minipreps.",
        pos=[-3.7, 1.0], deps=["micropipette"],
        objectives=["balance a rotor correctly", "select g-force vs rpm", "pellet cells and clarify lysate"],
        prereqs=["the micropipette node"],
        intro="The high-speed centrifuge is the single most important piece of equipment for the miniprep. Balance is everything - an unbalanced rotor is dangerous and ruins runs.",
        tools=["microcentrifuge", "balanced tubes"],
        steps=[
            ("Always balance", "Place tubes symmetrically; add a water-filled balance tube if you have an odd number."),
            ("Choose the speed", "Convert between rpm and relative centrifugal force (g) for your rotor; use g in protocols."),
            ("Pellet & decant", "Spin to pellet cells/debris, then carefully decant or pipette off the supernatant."),
        ],
        submission="Describe a balanced loading scheme for an odd number of samples and the g-force you'd use to pellet E. coli.",
        resources=[
            ("NeoSynBio: Centrifuge equipment guide", f"{NEO}/centrifuge"),
            ("Eppendorf: centrifugation basics & rcf/rpm conversion", "https://www.eppendorf.com/us-en/lab-academy/"),
        ],
    ),
    dict(
        id="thermocycler", title="The Thermocycler", lvl=1, level="beginner",
        time=20, project="Equipment",
        desc="Program the heating/cooling cycles that drive PCR.",
        pos=[3.7, 6.3], deps=["micropipette"],
        objectives=["program denature/anneal/extend cycles", "use heated lids and ramp rates", "scout affordable/second-hand options"],
        prereqs=["the micropipette node"],
        intro="The thermocycler is the biggest barrier to entry for many synthetic biologists. Cheap options (e.g. miniPCR) exist, and old units from university surplus often work admirably.",
        tools=["thermocycler", "thin-wall PCR tubes"],
        steps=[
            ("Enter the program", "Set initial denaturation, then the 3-step cycle (denature/anneal/extend) and final extension."),
            ("Use the heated lid", "Enable the heated lid to prevent condensation/evaporation during cycling."),
            ("Save & reuse", "Save common programs; note ramp rates if your enzyme is sensitive."),
        ],
        submission="Write out a complete thermocycler program for a routine PCR of a ~1 kb amplicon.",
        resources=[
            ("NeoSynBio: Thermocycler equipment guide", f"{NEO}/thermocycler"),
            ("miniPCR bio: affordable thermal cyclers", "https://www.minipcr.com/"),
            ("NEB Tm Calculator (program your annealing temp)", "https://tmcalculator.neb.com/"),
        ],
    ),
    dict(
        id="spectrophotometer", title="The Spectrophotometer", lvl=2, level="beginner",
        time=20, project="Equipment",
        desc="Measure OD600 to track cell growth and time induction.",
        pos=[1.6, 13.0], deps=["micropipette"],
        objectives=["measure OD600 against a blank", "relate OD to growth phase", "consider DIY photometer options"],
        prereqs=["the micropipette node"],
        intro="The spectrophotometer measures optical density (OD600) - how much light your culture blocks as it grows. It's how you choose the right moment to induce protein expression. It's relatively easy to DIY.",
        tools=["spectrophotometer", "cuvettes", "media blank"],
        steps=[
            ("Blank the instrument", "Zero the reading with a cuvette of sterile media."),
            ("Measure OD600", "Read your culture at 600 nm; dilute if the reading exceeds the linear range."),
            ("Map to growth", "Track OD600 over time to identify exponential phase for induction."),
        ],
        submission="Record a short OD600 time-course of a growing culture and identify the exponential phase.",
        resources=[
            ("NeoSynBio: Spectrophotometer & cuvettes guide", f"{NEO}/spectrophotometer-cuvettes"),
            ("OD600 and bacterial growth curves (overview)", "https://www.thermofisher.com/us/en/home/life-science/lab-equipment/spectrophotometers-refractometers-electrochemistry/uv-vis-spectrophotometers.html"),
        ],
    ),
    # ---- Proteome analysis branch ----
    dict(
        id="western-blot", title="Western Blot", lvl=8, level="advanced",
        time=240, project="Proteome Analysis",
        desc="Detect a specific protein by size + antibody after transferring an SDS-PAGE gel to a membrane.",
        pos=[-2.0, 17.6], deps=["sds-page"],
        objectives=["transfer proteins to a membrane", "block and probe with primary/secondary antibodies", "detect and interpret bands"],
        prereqs=["SDS-PAGE", "antibodies against your target"],
        intro="The western blot (immunoblot) separates proteins by size, transfers them to a membrane, and detects your target with antibodies. It's the standard for confirming a specific protein's identity and relative abundance.",
        tools=["SDS-PAGE gel", "transfer apparatus", "nitrocellulose/PVDF membrane", "primary & secondary antibodies", "detection reagent"],
        steps=[
            ("Run & transfer", "Run an SDS-PAGE gel, then transfer the proteins to a membrane (wet or semi-dry)."),
            ("Block", "Block the membrane to prevent non-specific antibody binding."),
            ("Probe", "Incubate with a primary antibody, wash, then a labelled secondary antibody."),
            ("Detect", "Develop with chemiluminescent or fluorescent detection and image the blot."),
        ],
        submission="Submit a western blot image showing a specific band for your target, with the ladder for size reference.",
        resources=[
            ("Bio-Rad: Introduction to Western Blotting (learning center)", "https://www.bio-rad.com/en-us/applications-technologies/introduction-western-blotting"),
            ("Thermo Fisher: Overview of Western Blotting", "https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/overview-western-blotting.html"),
            ("Abcam: Western blot protocol & troubleshooting", "https://www.abcam.com/en-us/technical-resources/protocols/western-blot"),
        ],
    ),
    dict(
        id="elisa", title="ELISA", lvl=8, level="advanced",
        time=180, project="Proteome Analysis",
        desc="Quantify a protein/antigen in solution with an antibody-based plate assay.",
        pos=[-3.3, 16.6], deps=["affinity-purification"],
        objectives=["choose direct/indirect/sandwich format", "build a standard curve", "quantify your antigen"],
        prereqs=["a purified antigen or sample", "matched antibodies"],
        intro="ELISA (enzyme-linked immunosorbent assay) quantifies an antigen in solution using antibodies and a colourimetric readout. With a standard curve, it turns a colour change into a concentration.",
        tools=["microplate", "capture/detection antibodies", "substrate", "plate reader"],
        steps=[
            ("Pick a format", "Choose direct, indirect or sandwich ELISA based on your antibodies and sensitivity needs."),
            ("Coat & block", "Immobilise antigen or capture antibody, then block the plate."),
            ("Detect & quantify", "Add detection antibody and substrate, read absorbance, and interpolate against a standard curve."),
        ],
        submission="Run (or design) an ELISA with a standard curve and report the calculated concentration of your sample.",
        resources=[
            ("Thermo Fisher: Overview of ELISA", "https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/overview-elisa.html"),
            ("Bio-Rad: ELISA basics & formats", "https://www.bio-rad-antibodies.com/elisa-types-direct-indirect-sandwich-competition-elisa-formats.html"),
        ],
    ),
    # ---- RNA / transcriptomics branch ----
    dict(
        id="rna-purification", title="RNA Purification", lvl=5, level="intermediate",
        time=120, project="RNA Workflows",
        desc="Extract intact RNA while keeping ubiquitous RNases at bay.",
        pos=[-3.7, 4.6], deps=["genomic-dna"],
        objectives=["maintain an RNase-free workspace", "lyse and separate RNA from DNA/protein", "assess RNA integrity"],
        prereqs=["nucleic-acid handling basics", "an RNase-free setup"],
        intro="RNA work demands extra care: RNases are everywhere and degrade your sample fast. Extraction lyses cells under RNase-inhibiting conditions, then separates RNA from DNA, protein and lipids.",
        tools=["RNase-free tubes/tips", "lysis reagent (e.g. guanidinium/phenol or column kit)", "DNase", "cold block"],
        steps=[
            ("Go RNase-free", "Use RNase-free consumables, gloves and reagents; keep samples cold."),
            ("Lyse under denaturing conditions", "Lyse cells in a chaotropic/denaturing buffer that inactivates RNases."),
            ("Separate & DNase-treat", "Bind/precipitate RNA, wash, and DNase-treat to remove genomic DNA before downstream use."),
        ],
        submission="Extract RNA and assess its integrity (e.g. gel or A260/A280), reporting yield and purity.",
        resources=[
            ("Thermo Fisher: RNA extraction for real-time PCR", "https://www.thermofisher.com/us/en/home/life-science/dna-rna-purification-analysis/rna-extraction/rna-applications/rna-extraction-for-real-time-pcr.html"),
            ("NEB: RNA reagents & handling", "https://www.neb.com/en-us/applications/rna-analysis"),
            ("JoVE: RNA extraction & RT-PCR (video)", "https://www.jove.com/v/10104/rna-extraction-and-rt-pcr-analysis-of-environmental-microbes"),
        ],
    ),
    dict(
        id="rt-qpcr", title="RT-qPCR", lvl=5, level="advanced",
        time=150, project="RNA Workflows",
        desc="Reverse-transcribe RNA to cDNA and quantify transcript levels in real time.",
        pos=[-3.5, 6.1], deps=["rna-purification", "pcr"],
        objectives=["reverse-transcribe RNA to cDNA", "design qPCR assays and controls", "interpret Ct values and quantification"],
        prereqs=["RNA Purification", "PCR"],
        intro="RT-qPCR transforms RNA into cDNA via reverse transcriptase, then quantifies it in real time. It's the gold standard for measuring gene expression - but genomic-DNA contamination causes false positives, so clean RNA matters.",
        tools=["reverse transcriptase", "qPCR master mix (dye or probe)", "real-time thermocycler", "qPCR primers"],
        steps=[
            ("Reverse transcribe", "Convert purified RNA to cDNA with reverse transcriptase."),
            ("Set up qPCR", "Design specific primers (often spanning exon junctions); include no-RT and no-template controls."),
            ("Quantify", "Run real-time PCR and interpret Ct values for relative or absolute quantification."),
        ],
        submission="Design an RT-qPCR assay (primers + controls) for a target transcript and outline how you'd interpret the Ct data.",
        resources=[
            ("Bio-Rad: Real-Time PCR (qPCR) applications guide", "https://www.bio-rad.com/en-us/applications-technologies/real-time-pcr-qpcr"),
            ("Thermo Fisher: RT-qPCR basics", "https://www.thermofisher.com/us/en/home/life-science/pcr/real-time-pcr/real-time-pcr-learning-center.html"),
            ("JoVE: RNA extraction & RT-PCR (video)", "https://www.jove.com/v/10104/rna-extraction-and-rt-pcr-analysis-of-environmental-microbes"),
        ],
    ),
]

# Equipment nodes are OPTIONAL, non-blocking reference cards: each hangs off
# `intro` and nothing on the main spine depends on them, so they can be browsed
# freely in parallel without gating miniprep / pcr / protein-induction.
EQUIP_POS = {
    "micropipette": [-3.6, -0.6], "centrifuge": [-4.8, -0.6],
    "thermocycler": [-3.6, -1.8], "spectrophotometer": [-4.8, -1.8],
}
for _n in NODES:
    if _n["id"] in EQUIP_POS:
        _n["deps"] = ["intro"]
        _n["pos"] = EQUIP_POS[_n["id"]]
    if _n["id"] == "advanced-omics":
        _n["deps"] = ["final-project", "western-blot", "rt-qpcr"]
        _n["desc"] = "The frontier: gene switches, omics, aptamers, mass spec and advanced biological programming."
        _n["pos"] = [0, 21.0]

# ---- Verified technique videos (wired into node detail files) -----------
VIDEOS = {
    "micropipette": "https://www.youtube.com/watch?v=aSeod1Y5MRc",
    "plasmid-insertion": "https://www.youtube.com/watch?v=1PqWnu2uBrY",
    "pcr": "https://www.youtube.com/watch?v=WfiBa2Exdr4",
    "primer-design": "https://www.youtube.com/watch?v=mcOwlFVEino",
    "gel-electrophoresis": "https://www.youtube.com/watch?v=uAttNVEEEwY",
    "miniprep": "https://www.youtube.com/watch?v=MxV6FXPn6VU",
    "gibson": "https://www.youtube.com/watch?v=tlVbf5fXhp4",
    "golden-gate": "https://www.youtube.com/watch?v=NzQdLQ44I7w",
    "crispr": "https://www.youtube.com/watch?v=2pp17E4E-O8",
    "restriction-digest": "https://www.youtube.com/watch?v=qKvtxi_CegQ",
    "sds-page": "https://www.jove.com/v/30378/sodium-dodecyl-sulphate-polyacrylamide-gel-electrophoresis-for",
    "western-blot": "https://www.youtube.com/watch?v=sldmSbygsSI",
    "rna-purification": "https://www.jove.com/v/10104/rna-extraction-and-rt-pcr-analysis-of-environmental-microbes",
    "rt-qpcr": "https://www.jove.com/v/10104/rna-extraction-and-rt-pcr-analysis-of-environmental-microbes",
    # --- second pass: push coverage higher ---
    "sterile-technique": "https://www.jove.com/v/10040/aseptic-technique-in-environmental-science",
    "ligation": "https://www.neb.com/en-us/tools-and-resources/video-library/dna-ligation",
    "elisa": "https://www.youtube.com/watch?v=RRbuz3VQ100",
    "sequencing": "https://www.youtube.com/watch?v=-T60I1MJVko",
    "sdm": "https://www.youtube.com/watch?v=7xFvaI7coyg",
    "confirmation": "https://www.youtube.com/watch?v=Crv38J3_ZnM",
    "dna101": "https://www.youtube.com/watch?v=ni1ajYMQxt8",
    "media-plates": "https://www.addgene.org/protocols/pouring-lb-agar-plates/",
    "culturing-conditions": "https://www.addgene.org/protocols/streak-plate/",
}

# ---- Build the production tree graph -------------------------------------
tree_nodes = []
for n in NODES:
    tree_nodes.append({
        "id": n["id"],
        "title": n["title"].lower(),
        "description": n["desc"],
        "defaultStatus": n.get("status", "locked"),
        "link": "/" + n["id"],
        "initialPosition": n["pos"],
        "dependencies": n["deps"],
    })

main_path = [
    "intro", "sterile-workspace", "media-plates", "sterile-technique",
    "miniprep", "gel-electrophoresis", "pcr", "restriction-digest",
    "ligation", "confirmation", "proteins101", "protein-induction",
    "affinity-purification", "sds-page", "final-project",
]

tree = {
    "name": "synthetic biology",
    "subtitle": "from sterile bench to purified protein",
    "author": "neosynbio (curated)",
    "description": "A project-based wet-lab synthetic biology curriculum adapted from the open-source NeoSynBio Graduate's Guide, with the best-rated external guides (NEB, Addgene, Benchling, SnapGene, Thermo Fisher, Bio-Rad, iGEM) attached to every node.",
    "nodes": tree_nodes,
    "mainPathNodes": main_path,
}

with open(OUT / "src/data/trees/synthetic-biology.json", "w") as f:
    json.dump(tree, f, indent=2)

# ---- Build per-node detail files -----------------------------------------
for n in NODES:
    detail = {
        "treeId": "synthetic-biology",
        "id": n["id"],
        "title": {"name": n["title"].lower(), "level": n["lvl"]},
        "project": n["project"],
        "video": {"url": VIDEOS.get(n["id"], "")},
        "time": n["time"],
        "level": n["level"],
        "overview": {
            "description": n["intro"],
            "objectives": n["objectives"],
            "prerequisites": n["prereqs"],
        },
        "steps": {
            "description": n["intro"],
            "intro": n["intro"],
            "tools": n["tools"],
            "estimatatedTime": {
                "setup": max(2, n["time"] // 6),
                "config": max(3, n["time"] // 3),
                "testing": max(3, n["time"] // 3),
            },
            "instructions": [{"title": t, "description": d} for (t, d) in n["steps"]],
        },
        "submission": {"description": n["submission"]},
        "resources": [{"title": t, "url": u} for (t, u) in n["resources"]],
    }
    with open(OUT / f"src/data/skill_nodes/{n['id']}.json", "w") as f:
        json.dump(detail, f, indent=2)

# ---- Build a simple nested fallback (data/ schema) -----------------------
by_id = {n["id"]: n for n in NODES}
children_of = {n["id"]: [] for n in NODES}
roots = []
for n in NODES:
    deps = n["deps"]
    if not deps:
        roots.append(n["id"])
    else:
        # attach to first dependency as nesting parent (graph -> tree projection)
        children_of[deps[0]].append(n["id"])

def nest(nid):
    n = by_id[nid]
    node = {
        "name": n["title"],
        "id": nid,
        "description": n["desc"],
        "isUnlocked": n.get("status") == "inProgress",
    }
    kids = children_of[nid]
    if kids:
        node["children"] = [nest(k) for k in kids]
    return node

nested = [nest(r) for r in roots]
with open(OUT / "data/synthetic-biology-tree.json", "w") as f:
    json.dump(nested, f, indent=2)

print(f"Nodes: {len(NODES)}")
print(f"Tree file: src/data/trees/synthetic-biology.json")
print(f"Detail files: {len(NODES)} in src/data/skill_nodes/")
print(f"Main path: {len(main_path)} nodes")
# integrity check: every dependency id exists
ids = set(by_id)
for n in NODES:
    for d in n["deps"]:
        assert d in ids, f"missing dep {d} for {n['id']}"
for m in main_path:
    assert m in ids, f"main path id {m} missing"
print("Integrity check passed: all dependencies and main-path ids resolve.")