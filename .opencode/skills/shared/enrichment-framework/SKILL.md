---
name: enrichment-framework
description: "Use when performing functional enrichment analysis (GO, KEGG, Reactome, GSEA) on gene lists from ANY omics type — provides standard workflow, tool selection, visualization standards, and result interpretation guidelines."
---

# Enrichment Framework — Functional Enrichment Analysis

## Overview

Enrichment analysis connects gene lists to biological function. This skill standardizes method selection, database usage, background gene set specification, and result visualization across all omics types.

## 1. Method Selection

| Method | When to Use | Input | Tool |
|--------|------------|-------|------|
| **ORA** (Over-Representation Analysis) | Discrete gene list with clear cutoff | DEGs (padj < 0.05, |log₂FC| ≥ 1) | `clusterProfiler::enrichGO/enrichKEGG` |
| **GSEA** (Gene Set Enrichment Analysis) | Ranked complete gene list; no arbitrary cutoff | All genes ranked by log₂FC or −log₁₀(p)×sign(FC) | `clusterProfiler::gseGO`, `fgsea` |
| **ssGSEA / GSVA** | Sample-level pathway scoring | Expression matrix | `GSVA::gsva()`, `singscore` |

### Decision Logic:
```
Have a clear gene list with cutoff? → ORA
Have a full ranked list? → GSEA (preferred — avoids arbitrary cutoffs)
Need per-sample pathway scores? → ssGSEA / GSVA
```

## 2. Database Selection

| Database | Coverage | R Package | Use Case |
|----------|----------|-----------|----------|
| **GO** (BP/MF/CC) | Gene Ontology | `org.Hs.eg.db`, `org.Mm.eg.db` | Default functional annotation |
| **KEGG** | Metabolic/signaling pathways | `clusterProfiler::enrichKEGG` | Pathway-level interpretation |
| **Reactome** | Curated pathways (human) | `ReactomePA::enrichPathway` | Detailed mechanistic pathways |
| **MSigDB** | Meta-collection | `msigdbr` | Hallmark (H), curated (C2), GO (C5), immune (C7) |
| **WikiPathways** | Community-curated | `clusterProfiler::enrichWP` | Alternative to KEGG |
| **DO** (Disease Ontology) | Disease associations | `DOSE::enrichDO` | Disease-relevant studies |

### Database Selection Rules:
- **Default**: Always run GO (BP) + KEGG
- **Add Reactome**: For mechanistic / signaling studies
- **Add MSigDB Hallmark**: For cancer / pathway-centric studies
- **Species**: Verify organism annotation package matches your species

## 3. Background Gene Set

<IRON-LAW>
You MUST specify the correct background gene set. Wrong background = wrong results.

| Omics Type | Correct Background |
|------------|-------------------|
| RNA-seq | All genes with detectable expression (e.g., counts > 0 in ≥ N samples) |
| Proteomics | All identified proteins in the experiment |
| Microarray | All probes on the array (after filtering) |
| scRNA-seq | All genes detected in the cluster/cell type being tested |
| Metabolomics | All detected metabolites |

**NEVER use**:
- The entire genome as background for RNA-seq (inflates significance)
- Default "all genes" when your experiment detected a subset
- Different backgrounds for different comparisons in the same study

Not specifying background = results are UNINTERPRETABLE. Gate review will flag this.
</IRON-LAW>

## 4. Standard Workflow

### Step 1: Prepare Gene List
```r
# ORA: extract significant genes
sig_genes <- dplyr::filter(res, padj < 0.05, abs(log2FoldChange) >= 1) %>%
  dplyr::pull(gene_id)

# GSEA: rank all genes
gene_ranks <- res %>%
  dplyr::mutate(rank = -log10(pvalue) * sign(log2FoldChange)) %>%
  dplyr::arrange(desc(rank)) %>%
  tibble::deframe()
```

### Step 2: ID Conversion
```r
# Convert gene symbols to Entrez IDs (required by KEGG)
library(clusterProfiler)
gene_entrez <- bitr(sig_genes, fromType="SYMBOL", toType="ENTREZID",
                    OrgDb=org.Hs.eg.db)
```

### Step 3: Run Enrichment
```r
# ORA — GO Biological Process
ego <- enrichGO(gene = gene_entrez$ENTREZID,
                universe = background_entrez$ENTREZID,  # MUST specify
                OrgDb = org.Hs.eg.db,
                ont = "BP",
                pAdjustMethod = "BH",
                pvalueCutoff = 0.05,
                qvalueCutoff = 0.2)

# ORA — KEGG
ekegg <- enrichKEGG(gene = gene_entrez$ENTREZID,
                    universe = background_entrez$ENTREZID,
                    organism = "hsa",
                    pvalueCutoff = 0.05)

# GSEA — GO
gsea_go <- gseGO(geneList = gene_ranks,
                 OrgDb = org.Hs.eg.db,
                 ont = "BP",
                 minGSSize = 10,
                 maxGSSize = 500,
                 pvalueCutoff = 0.05)
```

### Step 4: Remove Redundancy
```r
# Simplify GO results (remove redundant terms)
ego_simplified <- simplify(ego, cutoff = 0.7, by = "p.adjust")
# Alternative: use REVIGO (http://revigo.irb.hr/) for manual curation
```

### Step 5: Visualize
See §5 below.

## 5. Visualization Standards

### 5.1 Bubble / Dot Plot (Default)
```r
dotplot(ego_simplified, showCategory = 20) +
  scale_color_viridis_c(name = "p.adjust") +
  theme_classic(base_size = 10)
```
- X-axis: GeneRatio (proportion of genes in the term)
- Y-axis: Term name (sorted by p.adjust)
- Size: Gene count
- Color: p.adjust

### 5.2 Bar Plot
```r
barplot(ego_simplified, showCategory = 15, x = "Count") +
  scale_fill_viridis_c(name = "-log10(p.adjust)")
```
- Sorted by −log₁₀(p.adjust)

### 5.3 Enrichment Map (Network)
```r
emapplot(ego_simplified) + theme_void()
```
- Groups similar terms by gene overlap
- Useful for identifying biological themes

### 5.4 GSEA Running Score Plot
```r
gseaplot2(gsea_go, geneSetID = 1:3, pvalue_table = TRUE)
```
- Running enrichment score curve
- Gene hit positions
- p-value and NES in table

### 5.5 Pathway Map (KEGG)
```r
pathview(gene.data = gene_fc, pathway.id = "hsa04110",
         species = "hsa", gene.idtype = "entrez")
```

## 6. Result Filtering and Reporting

| Criterion | Standard |
|-----------|---------|
| Significance cutoff | p.adjust < 0.05 |
| Report top N | 15–20 terms per category (BP, MF, CC, KEGG) |
| Redundancy removal | `simplify(cutoff=0.7)` or REVIGO |
| Gene overlap | Report which genes contribute to top terms |
| Direction (GSEA) | Report NES sign — positive (up) or negative (down) |

### Required Report Elements:
1. Method used (ORA or GSEA) with justification
2. Background gene set and size
3. Database version and organism
4. Number of significant terms found
5. Top terms with p.adjust, gene count, gene ratio
6. Dot plot and/or enrichment map
7. GSEA: NES, p.adjust, leading edge genes

## 7. Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| No background specified | Inflated significance | Always set `universe` parameter |
| Using ORA on arbitrary cutoffs | Threshold-dependent results | Prefer GSEA when possible |
| Reporting hundreds of terms | Uninterpretable | Filter to top 20; simplify redundant terms |
| Mixing species | Wrong gene-term mapping | Verify `OrgDb` matches species |
| Ignoring gene ID conversion failures | Missing genes | Check conversion success rate; report failures |
| Not removing redundancy | Redundant GO terms dominate | Use `simplify()` or REVIGO |
