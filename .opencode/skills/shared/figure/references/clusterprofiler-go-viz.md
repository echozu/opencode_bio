# clusterProfiler GO Enrichment Visualization Reference

> Source: https://yulab-smu.top/biomedical-knowledge-mining-book/021-go.html
> Package: clusterProfiler (Bioconductor), enrichplot

## GO Enrichment Workflow

```r
library(clusterProfiler)
library(org.Hs.eg.db)  # or org.Mm.eg.db for mouse
library(enrichplot)

# 1. GO Classification (groupGO)
ggo <- groupGO(gene = gene_list, OrgDb = org.Hs.eg.db,
               ont = "BP", level = 3, readable = TRUE)

# 2. GO Over-Representation Analysis (enrichGO)
ego <- enrichGO(gene = gene_list,
                OrgDb = org.Hs.eg.db,
                ont = "BP",           # "BP", "MF", "CC", or "ALL"
                keyType = "ENTREZID", # or "SYMBOL", "ENSEMBL"
                pAdjustMethod = "BH",
                pvalueCutoff = 0.05,
                qvalueCutoff = 0.2,
                readable = TRUE)

# 3. GO Gene Set Enrichment Analysis (gseGO)
gse <- gseGO(geneList = ranked_gene_list,  # named numeric vector, sorted decreasing
             OrgDb = org.Hs.eg.db,
             ont = "BP",
             minGSSize = 10,
             maxGSSize = 500,
             pvalueCutoff = 0.05)
```

## Visualization Functions

All visualization functions work with both `enrichGO` and `gseGO` results.

### 1. Bar Plot

```r
barplot(ego, showCategory = 20, font.size = 10)

# Customized
barplot(ego, showCategory = 15, x = "Count",
        color = "p.adjust", font.size = 10) +
    scale_fill_gradient(low = "red", high = "blue")
```

### 2. Dot Plot

```r
dotplot(ego, showCategory = 20)

# With gene ratio on x-axis, color = p.adjust, size = count
dotplot(ego, x = "GeneRatio", color = "p.adjust",
        showCategory = 20, font.size = 10)
```

### 3. Gene-Concept Network (cnetplot)

Shows which genes are involved in which enriched terms.

```r
cnetplot(ego, showCategory = 5,
         categorySize = "pvalue",
         foldChange = geneList,      # color by fold change
         colorEdge = TRUE,
         node_label = "all")         # "category", "gene", "all", "none"

# Circular layout
cnetplot(ego, circular = TRUE, colorEdge = TRUE)
```

### 4. Heatmap-like Plot (heatplot)

Gene-term association matrix.

```r
heatplot(ego, showCategory = 20,
         foldChange = geneList)      # color genes by fold change
```

### 5. Enrichment Map (emapplot)

Network of enriched terms, edges = gene overlap.

```r
# Requires pairwise term similarity
ego2 <- pairwise_termsim(ego)

emapplot(ego2, showCategory = 30,
         color = "p.adjust",
         cex.params = list(category_label = 0.8),
         layout = "kk")             # "kk", "nicely", "fr", etc.

# Clustered
emapplot(ego2, showCategory = 30, cluster.params = list(cluster = TRUE, n = 4))
```

### 6. Tree Plot (treeplot)

Hierarchical clustering of enriched terms.

```r
ego2 <- pairwise_termsim(ego)
treeplot(ego2, showCategory = 30,
         cluster.params = list(method = "ward.D"),
         hclust_method = "ward.D")
```

### 7. UpSet Plot

```r
upsetplot(ego, n = 10)
```

### 8. Ridge Plot (for GSEA results)

```r
ridgeplot(gse, showCategory = 15,
          fill = "p.adjust",
          core_enrichment = TRUE)
```

### 9. GSEA Plot

```r
gseaplot2(gse, geneSetID = 1:3,    # plot multiple gene sets
          pvalue_table = TRUE,
          ES_geom = "line")         # "line" or "dot"

# Single gene set
gseaplot2(gse, geneSetID = 1, title = gse$Description[1])
```

### 10. Comparing Multiple Conditions

```r
# Compare clusters or conditions
compareCluster(geneCluster ~ cluster, data = gene_df,
               fun = "enrichGO", OrgDb = org.Hs.eg.db, ont = "BP")

dotplot(cc, showCategory = 5)   # side-by-side dot plots
```

## Simplifying GO Terms

```r
# Remove redundant terms
ego_simplified <- simplify(ego, cutoff = 0.7, by = "p.adjust", select_fun = min)

# Remove specific GO levels
dropGO(ego, level = 1:3)

# Filter terms
ego_filtered <- ego[ego$p.adjust < 0.01 & ego$Count > 5, ]
```

## KEGG / Reactome (Same Visualization)

```r
# KEGG
kk <- enrichKEGG(gene = gene_list, organism = "hsa")
dotplot(kk)
cnetplot(kk)

# Reactome
library(ReactomePA)
rpa <- enrichPathway(gene = gene_list, organism = "human")
dotplot(rpa)
emapplot(pairwise_termsim(rpa))
```
