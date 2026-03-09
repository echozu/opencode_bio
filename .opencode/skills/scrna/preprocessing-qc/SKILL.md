---
name: preprocessing-qc
description: >
  MANDATORY for Phase 0-1 of scRNA-seq analysis. Guides experimental design validation,
  sample metadata verification, and preprocessing QC. Covers Cell Ranger / STARsolo output
  validation, ambient RNA removal (SoupX/CellBender), doublet detection (DoubletFinder/Scrublet),
  and QC metric assessment. Use when setting up a new scRNA-seq project or performing initial QC.
---

# Preprocessing & QC — Phase 0–1

## Overview

This skill covers the critical first steps: validating experimental design, preprocessing raw data, and performing quality control filtering. Errors here propagate through the entire analysis.

## Step 1: Experimental Design Validation

### Mandatory Metadata Fields
| Field | Example | Why Required |
|-------|---------|-------------|
| Sample ID | S001, S002 | Unique per library |
| Condition/Group | Treatment, Control | For DE analysis |
| Batch | Batch1, Batch2 | For batch correction |
| Tissue | PBMC, Tumor | For reference selection |
| Species | Human, Mouse | For genome/annotation |
| Chemistry | 3' v3, 5' v2 | Affects preprocessing |
| Sequencing depth | ~50k reads/cell | For saturation check |

<IRON-LAW>
Before ANY analysis:
1. Verify sample metadata is complete (all fields above)
2. Confirm biological replicates exist (≥ 2 per group, ≥ 3 recommended)
3. Check for confounding (batch ≠ condition)
4. If metadata is incomplete → STOP and request from user
5. Lock experimental design in project-anchor.yaml
</IRON-LAW>

## Step 2: Preprocessing (Cell Ranger / STARsolo)

### Cell Ranger (10x Genomics)
```bash
# Standard pipeline — MUST run via sbatch on HPC
cellranger count \
  --id=sample_id \
  --transcriptome=/path/to/refdata-gex-GRCh38 \
  --fastqs=/path/to/fastqs \
  --sample=sample_name \
  --localcores=16 \
  --localmem=64
```

### STARsolo (Open-source alternative)
```bash
STAR --soloType CB_UMI_Simple \
  --soloCBwhitelist /path/to/barcode_whitelist.txt \
  --genomeDir /path/to/star_genome \
  --readFilesIn read2.fq.gz read1.fq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --soloFeatures Gene GeneFull Velocyto
```

### Output Validation
```r
# Load Cell Ranger output
obj <- Read10X(data.dir = "sample/outs/filtered_feature_bc_matrix/")
# OR: Read10X_h5("sample/outs/filtered_feature_bc_matrix.h5")

# Basic checks
dim(obj)  # genes × cells
# Expected: 20,000-35,000 genes × 500-20,000 cells per sample
```

## Step 3: Ambient RNA Removal

### SoupX
```r
library(SoupX)
sc <- load10X("sample/outs/")
sc <- autoEstCont(sc)
adj_counts <- adjustCounts(sc, roundToInt = TRUE)
```

### CellBender (GPU recommended → sbatch)
```bash
cellbender remove-background \
  --input raw_feature_bc_matrix.h5 \
  --output cellbender_output.h5 \
  --expected-cells 5000 \
  --total-droplets-included 25000 \
  --epochs 150
```

## Step 4: Doublet Detection

### DoubletFinder (R)
```r
library(DoubletFinder)
# Requires preprocessed Seurat object (normalized, PCA done)
sweep.res <- paramSweep(obj, PCs = 1:20, sct = TRUE)
sweep.stats <- summarizeSweep(sweep.res, GT = FALSE)
bcmvn <- find.pK(sweep.stats)
optimal_pk <- bcmvn$pK[which.max(bcmvn$BCmetric)]

# Estimate expected doublet rate (~0.8% per 1000 cells captured)
nExp <- round(0.008 * nrow(obj@meta.data)^2 / 10000)
obj <- doubletFinder(obj, PCs = 1:20, pN = 0.25, pK = as.numeric(as.character(optimal_pk)),
                      nExp = nExp, sct = TRUE)
```

### Scrublet (Python)
```python
import scrublet as scr
scrub = scr.Scrublet(adata.X, expected_doublet_rate=0.06)
doublet_scores, predicted_doublets = scrub.scrub_doublets()
adata.obs['doublet_score'] = doublet_scores
adata.obs['predicted_doublet'] = predicted_doublets
```

## Step 5: QC Metric Assessment

```r
# Calculate QC metrics
obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")  # human
# obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^mt-")  # mouse
obj[["percent.ribo"]] <- PercentageFeatureSet(obj, pattern = "^RP[SL]")

# Visualization (MANDATORY before filtering)
VlnPlot(obj, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
FeatureScatter(obj, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")
FeatureScatter(obj, feature1 = "nCount_RNA", feature2 = "percent.mt")
```

### QC Filtering Guidelines
- QC thresholds should be data-adaptive (see `qc-grading-framework` skill)
- Use MAD-based thresholds rather than fixed cutoffs
- Document ALL filtering decisions and cell counts before/after
- Save QC plots BEFORE filtering

## Step 6: Gate 1 — Data Quality Review

<IRON-LAW>
After QC assessment, dispatch a blind QC reviewer via Task tool to independently verify data quality. Use the `qc-reviewer-prompt.md` template in this skill's directory.

The QC reviewer checks:
- Per-sample quality metrics across ALL samples
- Cross-sample consistency and batch effects
- Depth adequacy for planned analyses
- Contamination indicators
- Filtering decision appropriateness

Reviewer verdict feeds into Gate 1 decision:
- QC grade ≥ C AND reviewer PASS → Gate 1 PASS
- QC grade D OR reviewer CONDITIONAL → Gate 1 CONDITIONAL (user decision)
- QC grade F OR reviewer FAIL → Gate 1 FAIL
</IRON-LAW>

## Quality Checks

- [ ] Sample metadata complete and locked in project-anchor.yaml
- [ ] Cell Ranger / STARsolo ran successfully (web_summary.html reviewed)
- [ ] Ambient RNA removal performed (SoupX or CellBender)
- [ ] Doublet detection performed (DoubletFinder or Scrublet)
- [ ] QC metrics visualized BEFORE any filtering
- [ ] Cell count before and after each filter step documented
- [ ] Batch-condition confounding assessed
- [ ] QC blind reviewer dispatched and verdict received

## Red-Line Signals

| Signal | Action |
|--------|--------|
| < 500 cells after filtering | Sample may have failed; report to user |
| Mitochondrial % > 20% for majority of cells | Tissue dissociation damage; adjust threshold carefully |
| No biological replicates | Analysis severely limited; warn user explicitly |
| Batch perfectly confounded with condition | Cannot distinguish batch from biology; STOP and report |
| Very low gene detection (< 200 genes/cell) | Empty droplets or failed library; check Cell Ranger metrics |
