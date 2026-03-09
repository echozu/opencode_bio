# BioCircos Reference

> Source: http://bioinfo.ibp.ac.cn/biocircos/document/biocircos.html
> Package: BioCircos (R), also see circlize for static plots

Interactive circular visualization for genomic data. Creates Circos-style plots in R (HTML widgets).

## Installation

```r
# CRAN
install.packages("BioCircos")
# Or devtools
devtools::install_github("bindbindz/BioCircos.R")
```

## Basic Usage

```r
library(BioCircos)

# Empty circular plot with default genome
BioCircos()

# With custom genome
BioCircos(genome = list("chr1" = 249250621, "chr2" = 243199373, "chr3" = 198022430))
```

## Track Types

### 1. SNP Track (Manhattan-style)
```r
snp_track <- BioCircosSNPTrack("snpTrack",
    chromosomes = c("chr1", "chr2", "chr3"),
    positions = c(100000, 200000, 300000),
    values = -log10(pvalues),
    colors = c("red", "blue", "green"),
    minRadius = 0.5, maxRadius = 0.9)
BioCircos(snp_track)
```

### 2. Arc Track (Region highlighting)
```r
arc_track <- BioCircosArcTrack("arcTrack",
    chromosomes = c("chr1", "chr1"),
    starts = c(1000000, 5000000),
    ends = c(3000000, 8000000),
    colors = c("#E64B35", "#4DBBD5"),
    minRadius = 0.4, maxRadius = 0.5)
```

### 3. Link Track (Inter-chromosomal connections)
```r
link_track <- BioCircosLinkTrack("linkTrack",
    gene1Chromosomes = c("chr1", "chr2"),
    gene1Starts = c(100000, 200000),
    gene1Ends = c(150000, 250000),
    gene2Chromosomes = c("chr3", "chr5"),
    gene2Starts = c(300000, 400000),
    gene2Ends = c(350000, 450000),
    colors = c("#FF6B6B", "#4ECDC4"))
```

### 4. Heatmap Track
```r
heatmap_track <- BioCircosHeatmapTrack("heatTrack",
    chromosomes = chromosomes,
    starts = starts,
    ends = ends,
    values = values,
    minRadius = 0.3, maxRadius = 0.4,
    color = c("#4DBBD5", "white", "#E64B35"))
```

### 5. Histogram Track (Bar plot around circle)
```r
hist_track <- BioCircosBarTrack("histTrack",
    chromosomes = chromosomes,
    starts = starts,
    ends = ends,
    values = values,
    color = "#3C5488",
    minRadius = 0.2, maxRadius = 0.3)
```

### 6. Line Track
```r
line_track <- BioCircosLineTrack("lineTrack",
    chromosomes = chromosomes,
    positions = positions,
    values = values,
    color = "#E64B35",
    minRadius = 0.6, maxRadius = 0.8)
```

### 7. Background Track
```r
bg_track <- BioCircosBackgroundTrack("bgTrack",
    minRadius = 0.3, maxRadius = 0.5,
    fillColors = "#F0F0F0",
    borderColors = "#CCCCCC")
```

## Combining Multiple Tracks

```r
tracklist <- BioCircosTracklist()
tracklist <- tracklist + snp_track + arc_track + link_track + heatmap_track

BioCircos(tracklist,
    genomeFillColor = "Spectral",
    chrPad = 0.02,
    displayGenomeBorder = TRUE,
    genomeTicksDisplay = TRUE,
    genomeTicksScale = 1e7)
```

## Static Alternative: circlize

For publication-quality static circular plots, use `circlize`:

```r
library(circlize)

# Initialize
circos.par(gap.degree = 2)
circos.initialize(factors = chr, xlim = chr_ranges)

# Add tracks
circos.track(ylim = c(0, 1), panel.fun = function(x, y) {
    circos.text(CELL_META$xcenter, 0.5, CELL_META$sector.index)
})

# Genomic tracks
circos.genomicTrack(bed_data, panel.fun = function(region, value, ...) {
    circos.genomicPoints(region, value, pch = 16, cex = 0.5)
})

# Heatmap
circos.genomicHeatmap(bed_data, col = colorRamp2(c(-1, 0, 1), c("blue", "white", "red")))

# Links
circos.link("chr1", c(1e6, 2e6), "chr5", c(3e6, 4e6), col = "red")

# Chord diagram (for interaction/flow data)
chordDiagram(adjacency_matrix, transparency = 0.5)

circos.clear()
```

## Bio Use Cases

- **CNV visualization**: Heatmap track showing copy number across genome
- **Structural variants**: Link tracks connecting translocation breakpoints
- **Multi-omics**: Stacked tracks (expression, methylation, mutations)
- **Chromosome ideogram**: Background with cytobands
- **Gene fusion**: Links between fusion gene pairs
