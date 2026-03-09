---
name: multimodal-integration
description: >
  CONDITION-TRIGGERED for Phase 5 of scRNA-seq analysis when multimodal data is present.
  Guides integration of CITE-seq (RNA + ADT), Multiome (RNA + ATAC), and scTCR/BCR data.
  Covers Seurat WNN, MOFA+, ArchR, Signac, and scRepertoire workflows.
  Use when integrating multi-modal single-cell data.
---

# Multimodal Integration — CITE-seq, Multiome, Immune Repertoire

## Overview

Modern single-cell technologies generate multiple data modalities from the same cell. Integration requires modality-specific preprocessing followed by joint analysis.

## Type C: CITE-seq / DOGMA-seq (RNA + ADT ± ATAC)

### Step 1: ADT Preprocessing
```r
# Seurat v5 — process ADT assay
obj[["ADT"]] <- CreateAssayObject(counts = adt_counts)
obj <- NormalizeData(obj, assay = "ADT", normalization.method = "CLR", margin = 2)
# CLR normalization is standard for ADT data
```

### Step 2: Weighted Nearest Neighbors (WNN)
```r
# WNN finds cell neighbors using both RNA and ADT
obj <- FindMultiModalNeighbors(
  obj,
  reduction.list = list("pca", "apca"),  # apca = ADT PCA
  dims.list = list(1:30, 1:15),
  modality.weight.name = "RNA.weight"
)

# WNN-based clustering and UMAP
obj <- RunUMAP(obj, nn.name = "weighted.nn", reduction.name = "wnn.umap")
obj <- FindClusters(obj, graph.name = "wsnn", resolution = 0.8)
```

### Step 3: Protein-RNA Correlation
```r
# Verify ADT and RNA concordance for known markers
FeaturePlot(obj, features = c("adt_CD3", "rna_CD3D"), blend = TRUE)
```

## Type A: Multiome (RNA + ATAC)

### Using Signac (Seurat ecosystem)
```r
library(Signac)

# Process ATAC data
obj[["ATAC"]] <- CreateChromatinAssay(
  counts = atac_counts, fragments = fragments_path,
  annotation = gene_annotation
)

# ATAC preprocessing
obj <- RunTFIDF(obj, assay = "ATAC")
obj <- FindTopFeatures(obj, assay = "ATAC", min.cutoff = "q0")
obj <- RunSVD(obj, assay = "ATAC")

# WNN integration (same as CITE-seq)
obj <- FindMultiModalNeighbors(obj,
  reduction.list = list("pca", "lsi"),
  dims.list = list(1:30, 2:30))  # exclude LSI component 1 (depth-correlated)
```

### Using ArchR
```r
library(ArchR)

# ArchR provides comprehensive scATAC-seq analysis
proj <- ArchRProject(ArrowFiles = arrow_files, outputDirectory = "ArchR_output")
proj <- addIterativeLSI(proj, useMatrix = "TileMatrix")
proj <- addClusters(proj, reducedDims = "IterativeLSI")
proj <- addUMAP(proj, reducedDims = "IterativeLSI")

# Integration with scRNA-seq
proj <- addGeneIntegrationMatrix(proj, seRNA = seurat_rna,
  groupATAC = "Clusters", groupRNA = "cell_type")

# Peak calling and motif analysis
proj <- addGroupCoverages(proj, groupBy = "cell_type")
proj <- addReproduciblePeakSet(proj, groupBy = "cell_type")
proj <- addMotifAnnotations(proj, motifSet = "cisbp")
```

## Type I: Immune Repertoire (scTCR/BCR)

### Using scRepertoire (R)
```r
library(scRepertoire)

# Load contigs from CellRanger VDJ output
contig_list <- loadContigs(input = "filtered_contig_annotations.csv", format = "10X")

# Combine contigs
combined <- combineTCR(contig_list, samples = sample_names)
# OR: combineBCR() for B cell receptors

# Add to Seurat object
obj <- combineExpression(combined, obj, cloneCall = "aa", chain = "both")

# Clonotype analysis
clonalQuant(combined, cloneCall = "aa", scale = TRUE)
clonalAbundance(combined, cloneCall = "aa")
clonalDiversity(combined, cloneCall = "aa")
clonalOverlap(combined, cloneCall = "aa", method = "morisita")

# Visualize on UMAP
DimPlot(obj, group.by = "cloneType")
```

## MOFA+ (Multi-Omics Factor Analysis)

```r
library(MOFA2)

# Create MOFA object from multiple modalities
mofa <- create_mofa(list(RNA = rna_matrix, ADT = adt_matrix))
mofa <- prepare_mofa(mofa)
mofa <- run_mofa(mofa)

# Analyze factors
plot_factor_cor(mofa)
plot_variance_explained(mofa)
plot_weights(mofa, view = "RNA", factor = 1, nfeatures = 20)
```

<IRON-LAW>
Multimodal integration rules:
1. Each modality must be preprocessed INDEPENDENTLY before integration
2. WNN modality weights should be inspected — extreme weights indicate one modality dominates
3. LSI component 1 from ATAC data is typically depth-correlated — EXCLUDE it
4. ADT normalization MUST use CLR (not LogNormalize)
5. scATAC peak calling must use reproducible peaks (ArchR/MACS2)
</IRON-LAW>

## Quality Checks

- [ ] Each modality preprocessed independently
- [ ] Integration method documented (WNN / MOFA+ / other)
- [ ] Modality weights inspected and reasonable
- [ ] Known marker concordance verified across modalities
- [ ] Cell barcodes matched correctly between modalities

## Red-Line Signals

| Signal | Action |
|--------|--------|
| Very few cells with both modalities | Check barcode matching; data may be incompatible |
| One modality dominates WNN weights | Check preprocessing; may need rebalancing |
| ATAC LSI component 1 included | REMOVE — it correlates with sequencing depth |
| ADT not CLR-normalized | Redo normalization with CLR |
