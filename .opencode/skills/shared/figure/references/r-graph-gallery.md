# R Graph Gallery Reference

> Source: https://github.com/holtzy/R-graph-gallery / https://r-graph-gallery.com/

400+ examples organized into ~50 chart types. All built with R (ggplot2, base R, interactive).

## Chart Types by Category

### Distribution
- **Violin** - `geom_violin()` — distribution shape comparison across groups
- **Density** - `geom_density()` — smoothed distribution curves
- **Histogram** - `geom_histogram()` — binned frequency distribution
- **Boxplot** - `geom_boxplot()` — median, quartiles, outliers
- **Ridgeline** - `ggridges::geom_density_ridges()` — stacked density plots
- **Beeswarm** - `ggbeeswarm::geom_beeswarm()` — non-overlapping strip plots

### Correlation
- **Scatter** - `geom_point()` — two continuous variables
- **Heatmap** - `geom_tile()` / `ComplexHeatmap::Heatmap()` — matrix visualization
- **Correlogram** - `GGally::ggpairs()` / `corrplot::corrplot()` — correlation matrix
- **Bubble** - `geom_point(aes(size=z))` — scatter with size encoding
- **Connected scatter** - `geom_point() + geom_segment()` — ordered scatter
- **Density 2d** - `geom_density_2d()` — 2D density contours

### Ranking
- **Barplot** - `geom_bar()` / `geom_col()` — categorical comparisons
- **Spider / Radar** - `fmsb::radarchart()` / `ggradar` — multivariate comparison
- **Wordcloud** - `wordcloud2::wordcloud2()` — text frequency
- **Parallel coordinates** - `GGally::ggparcoord()` — multivariate patterns
- **Lollipop** - `geom_segment() + geom_point()` — alternative to bar chart
- **Circular Barplot** - `coord_polar()` — bars in polar coordinates

### Part of a Whole
- **Grouped/Stacked barplot** - `geom_bar(position="stack"/"dodge")`
- **Treemap** - `treemapify::geom_treemap()` — hierarchical proportions
- **Doughnut** - `coord_polar() + geom_rect()` — ring chart
- **Pie chart** - `coord_polar() + geom_bar()` — proportions (use sparingly)
- **Dendrogram** - `ggdendro::ggdendrogram()` — hierarchical clustering
- **Circular packing** - `packcircles` — nested circles
- **Waffle** - `waffle::waffle()` — grid-based proportions

### Evolution / Time Series
- **Line plot** - `geom_line()` — trends over time
- **Area** - `geom_area()` — filled line plot
- **Stacked area** - `geom_area(position="stack")` — composition over time
- **Streamchart** - `ggstream::geom_stream()` — smoothed stacked area
- **Time Series** - `dygraphs` / `plotly` — interactive time series

### Map
- **Choropleth** - `geom_sf() + scale_fill_*` — geographic heatmap
- **Hexbin map** - `geom_hex()` — hexagonal binning on maps
- **Cartogram** - `cartogram` package — area-distorted maps
- **Connection map** - `geom_curve()` — origin-destination flows
- **Bubble map** - `geom_sf() + geom_point(aes(size=))` — sized points on map

### Flow / Network
- **Sankey** - `networkD3::sankeyNetwork()` — flow diagram
- **Network** - `igraph` + `ggraph` — node-edge graphs
- **Chord diagram** - `circlize::chordDiagram()` — circular flow
- **Arc diagram** - connections as arcs
- **Edge bundling** - `ggraph` — bundled network edges

### Other
- **Circular plots** - `circlize` — genomic circular layouts
- **Upset plot** - `UpSetR::upset()` — set intersections
- **Venn** - `VennDiagram` / `ggvenn` — set overlaps
- **3D** - `plotly`, `rgl` — 3D visualizations
- **Animation** - `gganimate` — animated transitions

## Key R Packages

| Package | Purpose |
|---------|---------|
| `ggplot2` | Grammar of graphics (bindstone) |
| `plotly` | Interactive charts |
| `ggridges` | Ridgeline plots |
| `ggbeeswarm` | Beeswarm plots |
| `GGally` | Pairs, parallel coords |
| `corrplot` | Correlation matrices |
| `ComplexHeatmap` | Advanced heatmaps |
| `circlize` | Circular plots |
| `gganimate` | Animations |
| `ggraph` / `igraph` | Network graphs |
| `sf` | Spatial/map data |
| `patchwork` | Multi-panel composition |
| `ggrepel` | Non-overlapping labels |
| `scales` | Axis formatting |
