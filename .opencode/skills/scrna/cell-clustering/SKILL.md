---
name: cell-clustering
description: >
  MANDATORY for Phase 2-3 of scRNA-seq analysis. Guides normalization, feature selection,
  dimensionality reduction, batch correction, and clustering. Covers Seurat and Scanpy workflows,
  SCTransform/LogNormalize, Harmony/scVI/CCA integration, Leiden/Louvain clustering, and
  resolution optimization. Use when performing cell clustering or integration.
---

# Cell Clustering — Normalization, Integration, and Clustering

## Overview

This skill covers the computational core of scRNA-seq analysis: from raw count matrix to cell clusters. Every step must be documented and reproducible.

## Step 1: Normalization & Feature Selection

### Seurat Workflow
```r
# Option A: SCTransform (recommended for most cases)
obj <- SCTransform(obj, vars.to.regress = "percent.mt", verbose = FALSE)
# Automatically selects variable features (default: 3000)

# Option B: LogNormalize (lighter, suitable for smaller datasets)
obj <- NormalizeData(obj, normalization.method = "LogNormalize", scale.factor = 10000)
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 2000)
obj <- ScaleData(obj, vars.to.regress = "percent.mt")
```

### Scanpy Workflow
```python
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor='seurat_v3')
adata = adata[:, adata.var.highly_variable]
sc.pp.scale(adata, max_value=10)
```

<IRON-LAW>
Normalization method must be chosen BEFORE processing and LOCKED in project-anchor.yaml.
Do NOT switch normalization methods mid-analysis without restarting from this step.
</IRON-LAW>

## Step 2: Dimensionality Reduction

```r
# Seurat
obj <- RunPCA(obj, npcs = 50, verbose = FALSE)
ElbowPlot(obj, ndims = 50)  # Determine number of PCs
# Typically 20-40 PCs for scRNA-seq
```

```python
# Scanpy
sc.tl.pca(adata, n_comps=50, svd_solver='arpack')
sc.pl.pca_variance_ratio(adata, n_pcs=50)
```

**PC Selection**: Use ElbowPlot / variance ratio to determine PCs. Record the chosen number.

## Step 3: Batch Correction / Integration (if multi-sample)

| Method | When to Use | Tool |
|--------|-------------|------|
| **Harmony** | Default choice; fast, effective for most cases | `harmony::RunHarmony()` / `scanpy.external.pp.harmony_integrate()` |
| **Seurat CCA/RPCA** | When samples have shared cell types with different proportions | `IntegrateLayers(method = CCAIntegration)` |
| **scVI** | Large datasets, complex batch structure | `scvi-tools` (Python) |
| **scanorama** | Fast, memory efficient | `scanorama.integrate_scanpy()` |
| **LIGER/iNMF** | When batch effects are strong | `rliger` |

### Integration Assessment
```r
# Check integration quality — MANDATORY after batch correction
# Visual: UMAP colored by batch vs cell type
DimPlot(obj, group.by = "batch") + DimPlot(obj, group.by = "celltype")

# Quantitative (optional but recommended):
# LISI (Local Inverse Simpson's Index) — higher = better mixing
# Silhouette score — cell types should remain separable
```

<IRON-LAW>
Integration must PRESERVE biological differences while removing technical batch effects.
After integration, VERIFY:
1. Batches are mixed (no batch-specific clusters)
2. Known cell types remain separable (not over-corrected)
3. Document which integration method was used and why
</IRON-LAW>

## Step 4: Clustering

```r
# Seurat
obj <- FindNeighbors(obj, dims = 1:30, reduction = "harmony")
obj <- FindClusters(obj, resolution = c(0.3, 0.5, 0.8, 1.0, 1.2))
# Test multiple resolutions — compare cluster numbers and marker stability

# Visualization
obj <- RunUMAP(obj, dims = 1:30, reduction = "harmony")
DimPlot(obj, group.by = paste0("RNA_snn_res.", c(0.3, 0.5, 0.8, 1.0, 1.2)))
```

```python
# Scanpy
sc.pp.neighbors(adata, n_pcs=30, use_rep='X_harmony')
for res in [0.3, 0.5, 0.8, 1.0, 1.2]:
    sc.tl.leiden(adata, resolution=res, key_added=f'leiden_res{res}')
sc.tl.umap(adata)
```

### Resolution Selection Criteria
- Too low: biologically distinct populations merged (check marker genes)
- Too high: homogeneous populations over-split (check DE between adjacent clusters)
- Use `clustree` (R) to visualize cluster stability across resolutions
- Final resolution must be documented and locked

## Step 5: Quality Checks

- [ ] Normalization method documented and locked
- [ ] Number of HVGs and PCs documented
- [ ] Integration method documented with assessment
- [ ] Multiple resolutions tested and final resolution justified
- [ ] UMAP/t-SNE parameters documented (seed, n_neighbors, min_dist)
- [ ] Random seeds set for reproducibility
- [ ] Cluster assignments saved to metadata

## Red-Line Signals

| Signal | Action |
|--------|--------|
| All cells in one cluster regardless of resolution | Check normalization; likely failed |
| Clusters split perfectly by batch | Integration failed; redo |
| Hundreds of clusters at resolution 0.5 | Data quality issue or doublets remaining |
| UMAP shows continuous gradient, no clusters | May be trajectory-driven data; consider trajectory analysis |
