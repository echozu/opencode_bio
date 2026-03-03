---
name: tool-recommendation
description: Use when selecting bioinformatics tools for any analysis step — provides context-aware tool selection based on data type, quality, goals, and resource constraints
---

# Tool Recommendation (Utility Skill)

## Overview

Context-aware tool selection for gut metagenome analysis. Considers data type, sequencing platform, sample characteristics, analysis goals, and available resources to recommend the most appropriate tools.

## When to Use

- During Phase 1 (data-assessment): selecting QC and profiling tools
- During Phase 3 (pipeline-design): finalizing tool chain
- During Phase 4 (pipeline-execution): selecting additional tools for specific analyses
- Any time a tool selection decision is needed

## Tool Selection Criteria

For each tool recommendation, evaluate:

1. **Accuracy** — Does it produce correct results for this data type?
2. **Scalability** — Can it handle the sample count and sequencing depth?
3. **Memory** — Does it fit within available RAM?
4. **Speed** — Can it complete within a reasonable timeframe?
5. **Community support** — Is it actively maintained? Last update?
6. **Documentation** — Is it well-documented for reproducibility?
7. **Citation count** — Is it widely used and peer-reviewed?

## Tool Recommendation Tables

### QC Tools

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **fastp** | All data types | Fast, comprehensive, auto-adapter detection | Less common in QIIME2 pipelines |
| **Trimmomatic** | Illumina data | Widely cited, well-documented | Slower than fastp |
| **cutadapt** | Primer removal | Precise primer trimming | QC only, not comprehensive |
| **KneadData** | Shotgun + host removal | Integrates QC + host removal + contamination | Slower, BioBakery ecosystem |

### Amplicon Analysis Tools

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **DADA2** | ASV inference | High resolution, built-in chimera removal | Memory-intensive for large datasets |
| **Deblur** | ASV inference | Fast, conservative | Requires uniform read lengths |
| **QIIME2** | Full pipeline | Comprehensive, well-documented | Learning curve, ecosystem lock-in |

### Taxonomy Classification

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **SILVA** | 16S/18S | Comprehensive, well-curated | Large database size |
| **Greengenes2** | 16S | Updated, UniFrac-compatible | Newer, less tested |
| **GTDB** | Genome-level | Most up-to-date taxonomy | Not for amplicon directly |

### Shotgun Metagenome — Taxonomy

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **MetaPhlAn4** | Species-level profiling | Accurate, marker-based, fast | Misses novel species |
| **Kraken2** | Fast classification | Very fast, sensitive | Can over-classify |
| **Bracken** | Abundance estimation | Corrects Kraken2 abundance | Requires Kraken2 |
| **mOTUs** | Species profiling | Sensitive to novel species | Slower than MetaPhlAn |

### Shotgun Metagenome — Function

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **HUMAnN3** | Pathway profiling | Species-stratified, MetaCyc pathways | Slow, large databases |
| **eggNOG-mapper** | Gene annotation | Comprehensive, fast | Assembly-based only |
| **KEGG/KOfamScan** | KO assignment | Standard functional categories | License for full KEGG |

### Assembly Tools

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **MEGAHIT** | Large datasets | Memory efficient, fast | Lower N50 than metaSPAdes |
| **metaSPAdes** | Quality assemblies | Higher N50, better for low-complexity | Memory hungry |

### Differential Abundance

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **DESeq2** | Small sample sizes | Handles zero inflation, well-tested | Assumes negative binomial |
| **ANCOM-BC** | Compositional data | Addresses compositionality bias | Newer, less tested |
| **LEfSe** | Biomarker discovery | Effect size-based, intuitive | No confounder control |
| **MaAsLin2** | Complex designs | Handles confounders, multiple models | Requires careful setup |
| **ALDEx2** | Compositional data | CLR-based, conservative | Can be too conservative |

### Network Analysis

| Tool | Best For | Strengths | Limitations |
|------|---------|-----------|-------------|
| **SparCC** | Compositional data | Handles compositionality | Slow for large datasets |
| **SpiecEasi** | Sparse networks | Graphical model-based | Complex setup |
| **WGCNA** | Module detection | Well-established | Originally for gene expression |

## Decision Framework

```
IF data_type == A (Amplicon):
  QC: fastp or cutadapt → DADA2 (includes denoising)
  Taxonomy: SILVA 138.1 + sklearn classifier
  Function: PICRUSt2 (if needed)

IF data_type == M (Assembly):
  QC: fastp + KneadData (host removal)
  Assembly: MEGAHIT (large dataset) or metaSPAdes (small dataset)
  Genes: Prodigal (meta mode)
  Binning: MetaBAT2 + DAS Tool
  Annotation: eggNOG-mapper + CAZy

IF data_type == R (Read-Based):
  QC: KneadData (QC + host removal)
  Taxonomy: MetaPhlAn4
  Function: HUMAnN3

IF data_type == C (Combined):
  Run both A and (M or R) pipelines
  Cross-validate taxonomy assignments
```

## Red Flags — STOP

- Recommending tools without checking version compatibility
- Using deprecated tools when better alternatives exist
- Selecting tools based on familiarity rather than data appropriateness
- Not considering resource constraints (RAM, disk, time)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I always use QIIME2" | QIIME2 is excellent but not always optimal. Consider alternatives. |
| "Latest version is best" | Latest may have bugs. Use proven stable versions. |
| "This tool is cited most" | Citations don't mean it's best for YOUR data. Evaluate fit. |
| "We don't need host removal" | For human gut samples, you ALWAYS need host removal. |
| "One differential method is enough" | Methods disagree. Run ≥2 for robustness. |
