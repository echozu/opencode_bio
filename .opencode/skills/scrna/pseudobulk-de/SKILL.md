---
name: pseudobulk-de
description: >
  MANDATORY for multi-sample scRNA-seq differential expression in Phase 3-4. Guides pseudobulk
  aggregation and differential expression using DESeq2/edgeR. Cell-level DE (FindMarkers with
  Wilcoxon) inflates significance due to pseudoreplication. Use pseudobulk for any multi-sample
  comparison.
---

# Pseudobulk Differential Expression

## Overview

Cell-level DE tests (Wilcoxon, t-test) treat each cell as an independent observation, which inflates significance in multi-sample designs due to pseudoreplication. **Pseudobulk DE aggregates cells per sample first**, then uses bulk RNA-seq DE methods (DESeq2/edgeR) on the aggregated counts.

<IRON-LAW>
For multi-sample comparisons (treatment vs control, disease vs healthy):
- Cell-level DE (FindMarkers with Wilcoxon/t-test) is INAPPROPRIATE
- Pseudobulk DE (DESeq2/edgeR on aggregated counts) is the STANDARD
- Cell-level DE is ONLY appropriate for:
  - Cluster marker identification (one cluster vs rest, same sample)
  - Exploratory analysis within a single sample
</IRON-LAW>

## Step 1: Pseudobulk Aggregation

### Seurat Workflow
```r
library(Seurat)
library(DESeq2)

# Aggregate counts per sample per cell type
pseudo_bulk <- AggregateExpression(
  obj,
  group.by = c("cell_type", "sample_id"),
  assays = "RNA",
  return.seurat = FALSE
)

# Extract count matrix
counts <- pseudo_bulk$RNA
```

### Scanpy Workflow
```python
import decoupler as dc

# Pseudobulk aggregation
pdata = dc.get_pseudobulk(
    adata,
    sample_col='sample_id',
    groups_col='cell_type',
    min_cells=10,
    min_counts=1000
)
```

## Step 2: DESeq2 Analysis (per cell type)

```r
# For each cell type, run DESeq2
for (ct in unique(obj$cell_type)) {
  # Subset counts for this cell type
  ct_counts <- counts[, grepl(ct, colnames(counts))]
  
  # Create colData
  coldata <- data.frame(
    condition = metadata$condition,  # treatment vs control
    row.names = colnames(ct_counts)
  )
  
  # DESeq2
  dds <- DESeqDataSetFromMatrix(
    countData = round(ct_counts),
    colData = coldata,
    design = ~ condition
  )
  dds <- DESeq(dds)
  res <- results(dds, contrast = c("condition", "treatment", "control"))
  
  # Filter significant genes
  sig_genes <- res[which(res$padj < 0.05 & abs(res$log2FoldChange) > 0.5), ]
}
```

## Step 3: Alternative — edgeR

```r
library(edgeR)

# For each cell type
y <- DGEList(counts = ct_counts, group = coldata$condition)
y <- calcNormFactors(y)
design <- model.matrix(~ condition, data = coldata)
y <- estimateDisp(y, design)
fit <- glmQLFit(y, design)
qlf <- glmQLFTest(fit, coef = 2)
topTags(qlf, n = 20)
```

## Step 4: Quality Checks Before DE

```r
# Minimum cells per sample per cell type
table(obj$cell_type, obj$sample_id)
# If < 10 cells for a cell type in a sample → exclude that sample for that cell type

# Check sample count per group
# DESeq2 needs ≥ 2 samples per group (ideally ≥ 3)
```

<IRON-LAW>
Quality requirements for pseudobulk DE:
1. Minimum 10 cells per sample per cell type (for aggregation)
2. Minimum 3 biological replicates per group (for statistical power)
3. If requirements not met → report as underpowered, do not force analysis
4. Multiple testing correction (BH/FDR) is MANDATORY
5. Report ALL results, not just significant ones
</IRON-LAW>

## Step 5: Visualization

```r
# Volcano plot
EnhancedVolcano::EnhancedVolcano(res, lab = rownames(res),
  x = 'log2FoldChange', y = 'padj',
  pCutoff = 0.05, FCcutoff = 0.5)

# Heatmap of top DE genes
DoHeatmap(obj, features = top_genes, group.by = "condition")
```

## When to Use Cell-Level DE

| Scenario | Method | Appropriate? |
|----------|--------|:----------:|
| Cluster markers (one vs rest) | FindAllMarkers (Wilcoxon) | ✅ |
| Treatment vs control (multi-sample) | Pseudobulk DESeq2/edgeR | ✅ |
| Treatment vs control (single sample) | FindMarkers (MAST/Wilcoxon) | ⚠️ Limited |
| Condition comparison across cell types | Pseudobulk + interaction model | ✅ |

## Red-Line Signals

| Signal | Action |
|--------|--------|
| Using Wilcoxon for multi-sample comparison | STOP — switch to pseudobulk |
| < 3 replicates per group | Report as underpowered; do not over-interpret |
| Thousands of DE genes at very low p-values | Likely pseudoreplication; verify method |
| No DE genes found | May be real; report honestly. Check power. |
