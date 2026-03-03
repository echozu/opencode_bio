---
name: metagenome-assembly
description: Use when data type is M (Metagenome-Assembly) and pipeline execution is in progress — provides step-by-step assembly-based metagenome workflow from assembly through gene prediction, binning, and functional annotation
---

<HARD-GATE>
Do NOT execute assembly-based metagenome analysis without:
1. G2 gate passed (analysis-protocol.yaml locked)
2. Data type confirmed as M in project-anchor.yaml
3. Host-removed, QC-validated reads available
</HARD-GATE>

# Metagenome Assembly Analysis (Type M — Phase 4 Sub-Skill)

## Overview

Assembly-based metagenome analysis: host-removed reads → assembly → gene prediction → binning → MAG quality → functional annotation. All parameters from locked `analysis-protocol.yaml`.

## Pipeline Steps

### Step 1: Verify Input Data
- Confirm host DNA removal completed (should be <1% human reads)
- Verify sufficient depth for assembly (recommended: >5Gb per sample)
- Check read quality post-QC

### Step 2: Metagenomic Assembly
Execute with LOCKED parameters:
```
assembler: [from protocol]  # MEGAHIT or metaSPAdes
assembler_version: [from protocol]
min_contig_length: [from protocol]  # typically 500bp
```

**For co-assembly (multiple samples):**
- Use when samples are from same environment/condition
- Increases contig length and completeness
- Document which samples were co-assembled

**Outputs:**
- Assembled contigs (FASTA)
- Assembly statistics (N50, total length, number of contigs, largest contig)

<IRON-LAW>
Check assembly quality BEFORE proceeding:
- N50 < 500bp → assembly quality insufficient, consider deeper sequencing
- Total assembly <10Mb for gut metagenome → insufficient depth
- If >90% reads unmapped to assembly → most diversity is unassembled

Report assembly stats to user before continuing.
</IRON-LAW>

### Step 3: Gene Prediction
```
tool: [from protocol]  # Prodigal (meta mode) or MetaGeneMark
version: [from protocol]
```

**Outputs:**
- Predicted genes (nucleotide and protein sequences)
- Gene statistics (total genes, mean length, coding density)

### Step 4: Gene Catalog Construction
- Cluster predicted genes at 95% identity (CD-HIT)
- Generate non-redundant gene catalog
- Map reads back to gene catalog for abundance quantification

### Step 5: Metagenomic Binning
```
binning_tool: [from protocol]  # MetaBAT2, MaxBin2, or CONCOCT
refinement: [from protocol]  # DAS Tool for refinement
```

**Outputs:**
- Metagenome-assembled genomes (MAGs)
- Bin quality metrics (completeness, contamination via CheckM/CheckM2)

<IRON-LAW>
MAG quality standards (MIMAG):
- High-quality: >90% completeness, <5% contamination, 23S+16S+5S rRNA, ≥18 tRNAs
- Medium-quality: ≥50% completeness, <10% contamination
- Low-quality: <50% completeness or >10% contamination → FLAG, do not use in primary analysis

Do NOT report MAGs without quality assessment. CheckM/CheckM2 is MANDATORY.
</IRON-LAW>

### Step 6: Taxonomic Classification of MAGs
- Classify MAGs using GTDB-Tk
- Assign taxonomy at highest confident level
- Identify novel species candidates (no close reference in GTDB)

### Step 7: Functional Annotation
```
annotation_tool: [from protocol]  # eggNOG-mapper, KEGG, COG
databases: [from protocol]
```

**Outputs:**
- Gene-level functional annotations (KO, COG, KEGG pathway)
- MAG-level metabolic reconstruction
- CAZyme annotations (if included)

### Step 8: Generate Analysis-Ready Outputs
Save all outputs:
- `results/assembly/` — contigs, assembly stats
- `results/taxonomy/` — MAG taxonomy, gene catalog taxonomy
- `results/functional/` — annotation tables, pathway abundance
- `results/mags/` — MAG sequences, quality reports

## Domain Sanity Check

- [ ] Assembly N50 is reasonable for gut metagenome (typically 1-50kb)
- [ ] Top taxa in MAGs are expected gut organisms
- [ ] Gene catalog size is reasonable (typically 1-10M genes for gut)
- [ ] Functional annotations show expected gut-associated pathways
- [ ] No single MAG contains >50% of all reads (contamination?)

## Red Flags — STOP

- Assembly N50 <500bp
- CheckM completeness <50% for majority of bins
- Contamination >10% in bins used for analysis
- Unexpected organisms dominating (non-gut taxa)
- Gene catalog dominated by hypothetical proteins (>90%)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Low N50 is fine for metagenomes" | Low N50 means most genes are fragmented. Assess impact. |
| "CheckM can wait until later" | Quality assessment BEFORE analysis. Bad MAGs = bad results. |
| "Co-assembly is always better" | Co-assembly can hide strain-level differences. Justify the choice. |
| "We can skip binning" | Without MAGs, you lose genome-level ecological context. |
| "Assembly parameters are standard" | Standard for WHAT depth and complexity? Justify. |
