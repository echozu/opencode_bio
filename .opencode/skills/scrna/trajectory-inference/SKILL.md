---
name: trajectory-inference
description: >
  CONDITION-TRIGGERED for Phase 5 of scRNA-seq analysis. Guides trajectory inference, pseudotime
  analysis, and RNA velocity. Covers Monocle3, Slingshot, scVelo, and CytoTRACE.
  Use when performing trajectory analysis, pseudotime ordering, or RNA velocity estimation.
---

# Trajectory Inference — Pseudotime & RNA Velocity

## Overview

Trajectory inference computationally orders cells along developmental or differentiation paths. Results are hypotheses requiring biological validation. Multiple methods should be compared.

## Method Selection

| Method | Best For | Language | Notes |
|--------|----------|----------|-------|
| **Monocle3** | Complex trajectories, branching | R | UMAP-based, graph learning |
| **Slingshot** | Simple linear/branching trajectories | R | Stable, well-validated |
| **scVelo** | RNA velocity (splicing dynamics) | Python | Requires spliced/unspliced counts |
| **CytoTRACE** | Stemness / differentiation potential | R/Python | Does not require trajectory assumption |
| **PAGA** | Trajectory topology exploration | Python (Scanpy) | Good for initial exploration |

## Step 1: Monocle3 Workflow

```r
library(monocle3)

# Convert Seurat to CDS
cds <- as.cell_data_set(obj)
cds <- preprocess_cds(cds, num_dim = 30)
cds <- reduce_dimension(cds, reduction_method = "UMAP")
cds <- cluster_cells(cds)

# Learn trajectory graph
cds <- learn_graph(cds)

# Order cells (requires root cell/cluster specification)
cds <- order_cells(cds, root_cells = root_cell_ids)
# OR: order_cells(cds) → interactive root selection

# Plot
plot_cells(cds, color_cells_by = "pseudotime", cell_size = 0.5)
```

<IRON-LAW>
Root cell/cluster selection MUST be biologically justified:
- Use known progenitor/stem markers to identify root
- Document the reasoning for root selection
- If root is uncertain, test multiple roots and compare
- NEVER pick root arbitrarily
</IRON-LAW>

## Step 2: RNA Velocity (scVelo)

```python
import scvelo as scv

# Requires spliced/unspliced count matrices (from velocyto or alevin)
scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

# Dynamical model (recommended over stochastic)
scv.tl.recover_dynamics(adata, n_jobs=8)
scv.tl.velocity(adata, mode='dynamical')
scv.tl.velocity_graph(adata)

# Visualization
scv.pl.velocity_embedding_stream(adata, basis='umap', color='cell_type')
scv.pl.velocity_embedding_grid(adata, basis='umap', color='cell_type')
```

### RNA Velocity Prerequisites
- **velocyto** or **STARsolo** must have been run to get spliced/unspliced counts
- CellRanger output can be processed with `velocyto run10x`
- Check splicing ratio before proceeding (typically 10-30% unspliced)

## Step 3: Slingshot Workflow

```r
library(slingshot)

# Run on reduced dimensions (PCA or UMAP)
sce <- slingshot(sce, clusterLabels = 'cell_type', reducedDim = 'PCA',
                 start.clus = 'Progenitor')  # specify start cluster

# Extract pseudotime
pseudotime <- slingPseudotime(sce)
```

## Step 4: Trajectory Validation

- Compare results from ≥ 2 methods (e.g., Monocle3 + Slingshot)
- Validate with known biology: are progenitors at the root? Do terminal states make sense?
- Check genes changing along pseudotime (should include known differentiation markers)
- If trajectory does not match known biology, report honestly

## Quality Checks

- [ ] Root cell/cluster selection biologically justified and documented
- [ ] At least 2 trajectory methods compared (or justified why only 1)
- [ ] Key differentiation genes plotted along pseudotime
- [ ] Trajectory result consistent with known biology (or deviation documented)
- [ ] For RNA velocity: spliced/unspliced ratio checked
- [ ] Random seeds set and documented

## Red-Line Signals

| Signal | Action |
|--------|--------|
| Trajectory reverses known differentiation | Root selection likely wrong; re-evaluate |
| All cells have similar pseudotime | Data may not have trajectory structure |
| RNA velocity arrows are random/noisy | Velocity model may not fit; try stochastic mode or report limitation |
| Disconnected trajectory graph | Check if cell types are correctly annotated |
