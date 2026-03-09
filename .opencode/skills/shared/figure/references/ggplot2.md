# ggplot2 Complete Reference

> Source: https://ggplot2.tidyverse.org/ + https://r4ds.had.co.nz/data-visualisation.html

Grammar of graphics implementation for R. Version 4.0+.

## Core Pattern

```r
ggplot(data, aes(x, y, color, fill, size, shape, linetype, alpha, group)) +
  geom_*() +         # geometric objects (what to draw)
  stat_*() +         # statistical transformations
  scale_*() +        # axis/aesthetic scales
  coord_*() +        # coordinate system
  facet_*() +        # subplots
  theme_*() +        # visual styling
  labs()             # titles and labels
```

## All Geom Functions

### Points & Scatter
| Function | Description |
|----------|-------------|
| `geom_point()` | Scatter plot points |
| `geom_jitter()` | Jittered points (categorical x) |
| `geom_count()` / `stat_sum()` | Sized points by overlap count |
| `geom_rug()` | Marginal rug marks |

### Lines & Paths
| Function | Description |
|----------|-------------|
| `geom_line()` | Connected points (ordered by x) |
| `geom_path()` | Connected points (in data order) |
| `geom_step()` | Step function |
| `geom_segment()` | Line segments (x,y → xend,yend) |
| `geom_curve()` | Curved segments |
| `geom_spoke()` | Line from point at angle |
| `geom_abline()` | Diagonal reference line (slope, intercept) |
| `geom_hline()` | Horizontal reference line |
| `geom_vline()` | Vertical reference line |

### Bars & Columns
| Function | Description |
|----------|-------------|
| `geom_bar()` | Bar chart (counts by default) |
| `geom_col()` | Bar chart (pre-computed values) |
| `geom_histogram()` | Histogram (continuous x binned) |
| `geom_freqpoly()` | Frequency polygon (histogram as line) |

### Distribution
| Function | Description |
|----------|-------------|
| `geom_density()` | Smoothed density curve |
| `geom_density_2d()` | 2D density contours |
| `geom_density_2d_filled()` | Filled 2D density |
| `geom_boxplot()` | Box-and-whisker |
| `geom_violin()` | Violin plot |
| `geom_dotplot()` | Dot plot (stacked dots) |
| `geom_qq()` / `geom_qq_line()` | Q-Q plot |

### Area & Ribbon
| Function | Description |
|----------|-------------|
| `geom_area()` | Area under curve |
| `geom_ribbon()` | Band between ymin and ymax |

### Error Bars
| Function | Description |
|----------|-------------|
| `geom_errorbar()` | Vertical error bars |
| `geom_errorbarh()` | Horizontal error bars |
| `geom_crossbar()` | Crossbar (box with middle line) |
| `geom_linerange()` | Vertical line range |
| `geom_pointrange()` | Point with vertical range |

### Rectangles & Tiles
| Function | Description |
|----------|-------------|
| `geom_tile()` | Rectangles (centered on x,y) — heatmaps |
| `geom_rect()` | Rectangles (xmin,xmax,ymin,ymax) |
| `geom_raster()` | Fast tiles (equal-sized) |
| `geom_bin_2d()` | 2D rectangular binning |
| `geom_hex()` | 2D hexagonal binning |

### Text & Labels
| Function | Description |
|----------|-------------|
| `geom_text()` | Plain text labels |
| `geom_label()` | Text with background box |
| `ggrepel::geom_text_repel()` | Non-overlapping text |
| `ggrepel::geom_label_repel()` | Non-overlapping labels |

### Maps & Spatial
| Function | Description |
|----------|-------------|
| `geom_sf()` | Simple features geometry |
| `geom_sf_text()` / `geom_sf_label()` | Labels on sf |
| `geom_map()` | Polygons from reference map |
| `coord_sf()` | Map coordinate system |

### Smooth & Regression
| Function | Description |
|----------|-------------|
| `geom_smooth()` | Smoothed conditional means (loess/lm/gam) |
| `geom_quantile()` | Quantile regression lines |
| `geom_function()` | Arbitrary function curve |

### Other
| Function | Description |
|----------|-------------|
| `geom_contour()` / `geom_contour_filled()` | Contour lines/fills |
| `geom_polygon()` | Closed polygons |
| `geom_blank()` | Draw nothing (expand limits) |

## Scales

```r
# Continuous
scale_x_continuous(limits, breaks, labels, trans = "log10")
scale_y_log10()
scale_x_reverse()

# Discrete
scale_x_discrete(limits, labels)

# Color
scale_color_manual(values = c("A"="red", "B"="blue"))
scale_color_brewer(palette = "Set2")
scale_color_viridis_c()  # continuous viridis
scale_color_viridis_d()  # discrete viridis
scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0)

# Size, shape, alpha, linetype
scale_size_continuous(range = c(1, 10))
scale_shape_manual(values = c(16, 17, 15))
```

## Faceting

```r
facet_wrap(~ variable, ncol = 3, scales = "free_y")
facet_grid(rows ~ cols, scales = "free", space = "free")
facet_grid(. ~ variable)  # columns only
```

## Coordinates

```r
coord_cartesian(xlim, ylim)   # zoom without clipping
coord_flip()                   # swap x/y
coord_polar(theta = "y")       # polar (pie/donut)
coord_fixed(ratio = 1)         # 1:1 aspect ratio
```

## Themes

```r
theme_minimal()     # clean minimal
theme_classic()     # white background, axis lines
theme_bw()          # black & white
theme_void()        # nothing (for maps, diagrams)
theme_light()       # light grey

# Custom
theme(
    plot.title = element_text(size = 14, face = "bold"),
    axis.text = element_text(size = 10),
    legend.position = "bottom",      # "none", "left", "right", "top", "bottom"
    panel.grid.minor = element_blank(),
    strip.background = element_rect(fill = "white")
)
```

## Composition (patchwork)

```r
library(patchwork)
p1 + p2                 # side by side
p1 / p2                 # stacked
(p1 | p2) / p3          # layout
p1 + p2 + plot_layout(ncol = 1, heights = c(2, 1))
p1 + p2 + plot_annotation(tag_levels = "a")  # panel labels
```

## Save

```r
ggsave("figure.pdf", width = 8, height = 6)
ggsave("figure.png", dpi = 300, width = 8, height = 6)
ggsave("figure.svg", width = 8, height = 6)
```
