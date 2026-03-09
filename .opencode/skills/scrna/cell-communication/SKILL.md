---
name: cell-communication
description: >
  CONDITION-TRIGGERED for Phase 5 of scRNA-seq analysis. Guides cell-cell communication inference
  using CellChat, NicheNet, LIANA+, and CellPhoneDB. Use when analyzing ligand-receptor interactions
  or cell-cell signaling networks from scRNA-seq data.
---

# Cell-Cell Communication — Ligand-Receptor Interaction Analysis

## Overview

Cell communication analysis infers potential signaling interactions between cell types based on ligand-receptor expression. Results are **predictions** requiring experimental validation.

## Method Selection

| Method | Approach | Language | Strengths |
|--------|----------|----------|-----------|
| **CellChat** | Quantitative, mass-action modeling | R | Pathway-level, visualization rich |
| **NicheNet** | Ligand activity prediction from target genes | R | Links ligands to downstream effects |
| **LIANA+** | Consensus across multiple methods | Python | Aggregates multiple databases |
| **CellPhoneDB** | Statistical enrichment of LR pairs | Python | Permutation-based p-values |

## Step 1: CellChat Workflow

```r
library(CellChat)

# Create CellChat object
cellchat <- createCellChat(obj, group.by = "cell_type")

# Set ligand-receptor database
CellChatDB <- CellChatDB.human  # or CellChatDB.mouse
cellchat@DB <- CellChatDB

# Preprocessing
cellchat <- subsetData(cellchat)
cellchat <- identifyOverExpressedGenes(cellchat)
cellchat <- identifyOverExpressedInteractions(cellchat)

# Inference
cellchat <- computeCommunProb(cellchat, type = "triMean")
cellchat <- filterCommunication(cellchat, min.cells = 10)
cellchat <- computeCommunProbPathway(cellchat)
cellchat <- aggregateNet(cellchat)

# Visualization
netVisual_circle(cellchat@net$count, vertex.size = groupSize)
netVisual_bubble(cellchat, sources.use = c(1,2), targets.use = c(3,4))
netVisual_heatmap(cellchat, signaling = "WNT")
```

## Step 2: NicheNet Workflow

```r
library(nichenetr)

# Define sender and receiver cell types
sender_celltypes <- c("Macrophage", "Fibroblast")
receiver <- "T_cell"

# Get DE genes in receiver (these are the target genes)
DE_genes <- FindMarkers(obj, ident.1 = "condition", group.by = "condition",
                         subset.ident = receiver)

# Run NicheNet
ligand_activities <- predict_ligand_activities(
  geneset = DE_genes$gene,
  ligand_target_matrix = ligand_target_matrix,
  potential_ligands = potential_ligands
)
```

## Step 3: LIANA+ Workflow (Python)

```python
import liana as li

# Run LIANA with multiple methods
li.mt.rank_aggregate(
    adata,
    groupby='cell_type',
    resource_name='consensus',
    methods=['cellphonedb', 'connectome', 'natmi', 'singlecellsignalr']
)

# Visualize
li.pl.dotplot(adata, source_labels=['Macrophage'], target_labels=['T_cell'])
```

## Step 4: Comparison Between Conditions

```r
# CellChat comparison between conditions
cellchat_ctrl <- createCellChat(obj_ctrl, group.by = "cell_type")
cellchat_treat <- createCellChat(obj_treat, group.by = "cell_type")
# ... process each separately ...

# Merge and compare
object.list <- list(Control = cellchat_ctrl, Treatment = cellchat_treat)
cellchat_merged <- mergeCellChat(object.list)
compareInteractions(cellchat_merged)
netVisual_diffInteraction(cellchat_merged)
```

<IRON-LAW>
Cell communication results are PREDICTIONS, not validated interactions.
1. Always use language like "predicted interactions" or "inferred signaling"
2. Never claim "Cell X communicates with Cell Y" — say "predicted L-R pairs suggest..."
3. Results should be validated with spatial transcriptomics or perturbation experiments
4. Report the number of significant interactions AND the total tested
</IRON-LAW>

## Quality Checks

- [ ] Ligand-receptor database version documented
- [ ] Minimum cell count per cell type ≥ 10
- [ ] Statistical thresholds documented (p-value cutoff, specificity score)
- [ ] Results compared between ≥ 2 methods (or justified why only 1)
- [ ] Condition comparison performed (if multi-condition study)
- [ ] Key signaling pathways highlighted with biological context

## Red-Line Signals

| Signal | Action |
|--------|--------|
| Dominant interactions are housekeeping genes | Filter database for signaling-relevant genes only |
| Same interactions significant in all cell type pairs | Thresholds too loose; tighten filters |
| Zero significant interactions | Check cell type annotation; too few cells per type? |
| Results contradict known biology | Report discrepancy; do not suppress |
