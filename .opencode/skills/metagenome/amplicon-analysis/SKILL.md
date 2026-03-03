---
name: amplicon-analysis
description: Use when data type is A (Amplicon) and pipeline execution is in progress — provides step-by-step DADA2/QIIME2 workflow from denoising through taxonomy assignment and functional prediction
---

<HARD-GATE>
Do NOT execute amplicon analysis without:
1. G2 gate passed (analysis-protocol.yaml locked)
2. Data type confirmed as A (Amplicon) in project-anchor.yaml
3. QC-validated reads available
</HARD-GATE>

# Amplicon Analysis (Type A — Phase 4 Sub-Skill)

## Overview

Standard amplicon (16S/18S/ITS rRNA) analysis pipeline: quality-controlled reads → denoising → ASV table → taxonomy assignment → functional prediction. All parameters from locked `analysis-protocol.yaml`.

## Pipeline Steps

### Step 1: Import and Verify Data
- Import QC-validated FASTQ files
- Verify sample manifest matches metadata
- Generate per-sample read count summary

### Step 2: Denoising (DADA2)
Execute with LOCKED parameters from `analysis-protocol.yaml`:
```
# Parameters from analysis-protocol.yaml — DO NOT modify
truncation_length_fwd: [from protocol]
truncation_length_rev: [from protocol]
max_ee_fwd: [from protocol]
max_ee_rev: [from protocol]
chimera_method: [from protocol]
```

**Outputs:**
- ASV feature table (samples × ASVs)
- ASV representative sequences
- Denoising statistics (input reads, filtered, denoised, merged, non-chimeric)

<IRON-LAW>
Check denoising statistics BEFORE proceeding:
- If >50% reads lost at any step → STOP and investigate
- If chimera rate >25% → STOP and check library prep quality
- If merged reads <50% of filtered → STOP and check truncation lengths

Do NOT proceed with poor denoising results. Report to user.
</IRON-LAW>

### Step 3: Taxonomy Assignment
Execute with LOCKED parameters:
```
classifier: [from protocol]
classifier_version: [from protocol]
confidence_threshold: [from protocol]
```

**Outputs:**
- Taxonomy table (ASV → kingdom through species)
- Classification confidence scores
- Unassigned ASV count

**Quality check:**
- If >30% ASVs unassigned at phylum level → flag database mismatch
- If unexpected phyla dominate (e.g., Cyanobacteria in gut) → flag contamination

### Step 4: Filtering and Normalization
- Remove mitochondrial and chloroplast sequences
- Remove ASVs present in <N samples (prevalence filter from protocol)
- Generate rarefied table at LOCKED depth
- Generate relative abundance table
- Generate CLR-transformed table (for compositional-aware methods)

### Step 5: Functional Prediction (PICRUSt2)
If included in analysis goals:
```
tool: PICRUSt2
version: [from protocol]
```

**Outputs:**
- Predicted metagenome (KO, EC, MetaCyc pathways)
- NSTI scores per sample (Nearest Sequenced Taxon Index)

<IRON-LAW>
If mean NSTI >2.0, WARN the user:
"PICRUSt2 predictions may be unreliable — many ASVs are distant from reference genomes (NSTI >2.0). Consider shotgun metagenomics for more accurate functional profiling."
</IRON-LAW>

### Step 6: Generate Analysis-Ready Outputs
Save all outputs to structured directories:
- `results/taxonomy/` — taxonomy tables, barplots
- `results/diversity/` — input for downstream analysis
- `results/functional/` — PICRUSt2 outputs

## Domain Sanity Check

Before proceeding to downstream analysis, verify:
- [ ] Top phyla are expected for gut (Firmicutes, Bacteroidetes, Proteobacteria, Actinobacteria)
- [ ] No single ASV dominates >80% of reads (unless expected)
- [ ] Negative controls (if present) show low/no amplification
- [ ] Positive controls (if present) match expected composition
- [ ] Total ASV count is reasonable (typically 100-10,000 for gut 16S)

## Red Flags — STOP

- >50% read loss at any denoising step
- Chimera rate >25%
- Unexpected taxa dominating (non-gut organisms in gut samples)
- All samples clustering together regardless of group (batch effect?)
- Negative controls showing high diversity

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "50% read loss is normal for DADA2" | Normal loss is 20-40%. >50% means truncation lengths are wrong. |
| "Unassigned ASVs don't matter" | >30% unassigned means database mismatch. Investigate. |
| "Let me adjust truncation lengths" | Parameters are LOCKED. Report to user, request change approval. |
| "Chloroplast sequences are fine to keep" | Chloroplast/mitochondria are NOT microbes. Remove them. |
| "PICRUSt2 predictions are good enough" | Check NSTI first. High NSTI = unreliable predictions. |
