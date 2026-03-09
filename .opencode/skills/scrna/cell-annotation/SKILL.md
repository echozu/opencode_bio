---
name: cell-annotation
description: >
  MANDATORY for Phase 2-3 of scRNA-seq analysis. Guides automated and manual cell type annotation.
  Covers SingleR, scType, Azimuth, CellTypist for auto-annotation, and canonical marker gene
  validation. Use when annotating cell clusters or validating cell type assignments.
---

# Cell Annotation — Automated + Manual Marker Validation

## Overview

Cell type annotation requires BOTH automated reference-based methods AND manual marker gene validation. Neither alone is sufficient.

## Step 1: Automated Annotation

### Option A: SingleR (R, reference-based)
```r
library(SingleR)
library(celldex)

# Choose reference appropriate for tissue type
ref <- celldex::HumanPrimaryCellAtlasData()  # or MonacoImmuneData(), etc.
predictions <- SingleR(test = GetAssayData(obj), ref = ref, labels = ref$label.main)
obj$SingleR_labels <- predictions$labels
```

### Option B: scType (R, marker-based)
```r
# Uses curated marker gene database
# See: https://github.com/IanevskiAlexandr/sc-type
source("https://raw.githubusercontent.com/IanevskiAlexandr/sc-type/master/R/sctype_score_.R")
source("https://raw.githubusercontent.com/IanevskiAlexandr/sc-type/master/R/gene_sets_prepare.R")
# Provide tissue type for marker database selection
```

### Option C: Azimuth (R, Seurat v5 reference mapping)
```r
# Best for well-characterized tissues (PBMC, lung, motor cortex, etc.)
obj <- RunAzimuth(obj, reference = "pbmcref")
```

### Option D: CellTypist (Python, logistic regression)
```python
import celltypist
model = celltypist.models.download_models(model='Immune_All_Low.pkl')
predictions = celltypist.annotate(adata, model='Immune_All_Low.pkl', majority_voting=True)
adata.obs['celltypist'] = predictions.predicted_labels
```

### Reference Selection Guide
| Tissue | Recommended Reference | Tool |
|--------|----------------------|------|
| PBMC / Blood | MonacoImmuneData, pbmcref | SingleR, Azimuth |
| Tumor microenvironment | BlueprintEncodeData + custom markers | SingleR + manual |
| Brain | Allen Brain Atlas | Azimuth |
| Lung | LungRef | Azimuth |
| General human | HumanPrimaryCellAtlasData | SingleR |
| General mouse | ImmGenData, MouseRNAseqData | SingleR |

## Step 2: Marker Gene Validation (MANDATORY)

<IRON-LAW>
Automated annotation alone is NEVER sufficient. Every annotated cell type MUST be validated
with canonical marker genes. If markers do not support the annotation, the label is WRONG.

Validation steps:
1. Find cluster markers: FindAllMarkers(obj) or sc.tl.rank_genes_groups(adata)
2. Compare top markers against known cell type markers
3. Visualize: DotPlot, VlnPlot, FeaturePlot for key markers
4. If auto-label and markers disagree → markers win
</IRON-LAW>

### Common Marker Genes (Human)
| Cell Type | Key Markers |
|-----------|-------------|
| T cells | CD3D, CD3E, CD3G |
| CD4+ T | CD4, IL7R, CCR7 (naive) |
| CD8+ T | CD8A, CD8B, GZMB (cytotoxic) |
| B cells | CD79A, MS4A1 (CD20), CD19 |
| NK cells | NKG7, GNLY, KLRD1 |
| Monocytes | CD14, LYZ, S100A8/A9 |
| Dendritic cells | FCER1A, CD1C (cDC), CLEC4C (pDC) |
| Macrophages | CD68, CD163, MRC1 |
| Fibroblasts | COL1A1, DCN, LUM |
| Endothelial | PECAM1, VWF, CDH5 |
| Epithelial | EPCAM, KRT18, KRT19 |

### Validation Visualizations
```r
# Dot plot of key markers across clusters
DotPlot(obj, features = marker_list, group.by = "seurat_clusters") + RotatedAxis()

# Feature plots for top markers
FeaturePlot(obj, features = c("CD3D", "CD79A", "LYZ", "NKG7"))

# Violin plots for ambiguous clusters
VlnPlot(obj, features = c("CD3D", "CD14"), group.by = "seurat_clusters")
```

## Step 3: Handle Ambiguous Clusters

- Clusters with mixed markers → likely doublets or transitional states
- Clusters with no clear markers → label as "Unknown" (do NOT force annotation)
- Small clusters (< 50 cells) → may be real rare types or artifacts; document uncertainty
- Document all annotation decisions and reasoning

## Step 4: Annotation Finalization

```r
# Assign final annotations
new_labels <- c("0" = "CD4+ T cells", "1" = "CD14+ Monocytes", ...)
obj$cell_type <- plyr::mapvalues(obj$seurat_clusters, from = names(new_labels), to = new_labels)
```

## Quality Checks

- [ ] At least 2 auto-annotation methods used (or 1 + manual)
- [ ] Marker gene validation performed for ALL clusters
- [ ] Ambiguous clusters documented (not forced into labels)
- [ ] Annotation stored in metadata column
- [ ] DotPlot/FeaturePlot of key markers saved
- [ ] Reference dataset and version documented

## Red-Line Signals

| Signal | Action |
|--------|--------|
| Auto-annotation assigns "Unknown" to >30% cells | Reference may not match tissue; try different reference |
| Same cell type label for clusters with very different markers | Over-generalized annotation; split or re-annotate |
| Rare cell type called in large cluster | Verify — may be ambient RNA contamination |
| Conflicting auto-annotation results between tools | Manual marker validation is the tiebreaker |
