# ComplexHeatmap Reference

> Source: https://jokergoo.github.io/ComplexHeatmap-reference/book/
> Citation: Gu, Z. (2022) Complex Heatmap Visualization, iMeta. DOI: 10.1002/imt2.43

R/Bioconductor package for creating complex, publication-quality heatmaps with rich annotations.

## Installation

```r
# Bioconductor
BiocManager::install("ComplexHeatmap")
# Or GitHub (latest)
devtools::install_github("jokergoo/ComplexHeatmap")
```

## Book Chapters & Features

| Ch | Topic | Key Functions |
|----|-------|---------------|
| 1 | Introduction | Overview, philosophy |
| 2 | A Single Heatmap | `Heatmap()`, clustering, splitting |
| 3 | Heatmap Annotations | `HeatmapAnnotation()`, `anno_*()` |
| 4 | A List of Heatmaps | `HeatmapList`, `+` / `%v%` operators |
| 5 | Legends | `Legend()`, continuous/discrete |
| 6 | Heatmap Decoration | `decorate_*()`, post-hoc modification |
| 7 | OncoPrint | `oncoPrint()` — cancer genomics |
| 8 | UpSet plot | `UpSet()` / `make_comb_mat()` — set intersections |
| 9 | Interactive | `InteractiveComplexHeatmap` — Shiny |
| 10 | Integration | pheatmap, ggplot2 compatibility |
| 11 | Other High-level Plots | density, enriched heatmap |
| 12 | 3D Heatmap | 3D rendering |
| 13 | Genome-level Heatmap | `EnrichedHeatmap` — ChIP-seq |
| 14 | More Examples | Real-world use cases |

## Core API

### Basic Heatmap

```r
library(ComplexHeatmap)

Heatmap(matrix,
    name = "expression",              # legend title
    col = colorRamp2(c(-2, 0, 2), c("blue", "white", "red")),  # color mapping

    # Clustering
    cluster_rows = TRUE,
    cluster_columns = TRUE,
    clustering_method_rows = "ward.D2",
    clustering_distance_rows = "euclidean",

    # Splitting
    row_split = 3,                    # k-means split
    column_split = factor(c(...)),    # factor-based split

    # Labels
    row_names_gp = gpar(fontsize = 8),
    column_names_gp = gpar(fontsize = 8),
    column_names_rot = 45,

    # Visual
    rect_gp = gpar(col = "white", lwd = 0.5),
    border = TRUE,
    show_row_names = TRUE,
    show_column_names = TRUE,

    # Annotations (see below)
    top_annotation = ha_top,
    left_annotation = ha_left,
    right_annotation = ha_right,
)
```

### Annotations (`HeatmapAnnotation`)

```r
# Column annotation
ha_top = HeatmapAnnotation(
    # Categorical
    group = c("A","A","B","B","C"),
    col = list(group = c("A"="red", "B"="blue", "C"="green")),

    # Continuous bar
    value = anno_barplot(values_vector, gp = gpar(fill = "steelblue")),

    # Continuous points
    score = anno_points(scores, gp = gpar(col = "darkred")),

    # Boxplot per column
    expr = anno_boxplot(expr_matrix, gp = gpar(fill = "lightblue")),

    # Text
    label = anno_text(labels, gp = gpar(fontsize = 8)),

    # Custom function
    custom = anno_simple(values, col = color_fun),

    annotation_name_side = "left"
)

# Row annotation
ha_left = rowAnnotation(
    cell_type = cell_types,
    col = list(cell_type = cell_type_colors),

    gene_set = anno_mark(at = idx, labels = gene_names),  # mark specific rows
)
```

### Annotation Functions (`anno_*`)

| Function | Description |
|----------|-------------|
| `anno_simple()` | Simple color block |
| `anno_barplot()` | Bar plot per row/column |
| `anno_boxplot()` | Box plot per row/column |
| `anno_histogram()` | Histogram per row/column |
| `anno_density()` | Density curve per row/column |
| `anno_points()` | Point plot per row/column |
| `anno_lines()` | Line plot per row/column |
| `anno_text()` | Text labels |
| `anno_mark()` | Highlight specific rows/columns with labels |
| `anno_block()` | Block annotation for split heatmaps |
| `anno_image()` | Image annotations |
| `anno_zoom()` | Zoomed sub-heatmap |
| `anno_link()` | Link annotations (for genome) |
| `anno_empty()` | Empty placeholder |

### Combining Heatmaps

```r
# Horizontal concatenation
ht_list = Heatmap(mat1, name="expr") + Heatmap(mat2, name="cnv") + Heatmap(mat3, name="methyl")

# Vertical concatenation
ht_list = Heatmap(mat1) %v% Heatmap(mat2)

# Draw
draw(ht_list,
     row_title = "Genes",
     column_title = "Samples",
     heatmap_legend_side = "right",
     annotation_legend_side = "right")
```

### OncoPrint (Cancer Genomics)

```r
oncoPrint(mat,
    alter_fun = list(
        background = alter_graphic("rect", fill = "#CCCCCC"),
        snv = alter_graphic("rect", fill = "red", height = 0.9),
        del = alter_graphic("rect", fill = "blue", height = 0.3),
        amp = alter_graphic("rect", fill = "orange", height = 0.3)
    ),
    col = c(snv = "red", del = "blue", amp = "orange"),
    top_annotation = HeatmapAnnotation(
        cbar = anno_oncoprint_barplot()
    ),
    right_annotation = rowAnnotation(
        rbar = anno_oncoprint_barplot()
    )
)
```

### UpSet Plot (Set Intersections)

```r
# From a list of sets
lt = list(A = 1:10, B = 5:15, C = 8:20)
m = make_comb_mat(lt)
UpSet(m,
    comb_order = order(comb_size(m), decreasing = TRUE),
    top_annotation = upset_top_annotation(m, add_numbers = TRUE)
)
```

## Bio Use Cases

```r
# Gene expression heatmap with cell type + condition annotations
Heatmap(scaled_expr,
    name = "z-score",
    col = colorRamp2(c(-2, 0, 2), c("#4DBBD5", "white", "#E64B35")),
    top_annotation = HeatmapAnnotation(
        condition = sample_meta$condition,
        batch = sample_meta$batch,
        col = list(condition = c("ctrl"="#3C5488", "treat"="#E64B35"))
    ),
    left_annotation = rowAnnotation(
        pathway = gene_meta$pathway,
        log2FC = anno_barplot(gene_meta$log2FC)
    ),
    row_split = gene_meta$cluster,
    column_split = sample_meta$condition
)
```
