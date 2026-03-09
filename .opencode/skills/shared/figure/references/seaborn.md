# Seaborn API Reference

> Source: https://seaborn.pydata.org/

Statistical data visualization built on matplotlib. Version 0.13+.

## Objects Interface (New API)

```python
import seaborn.objects as so

(
    so.Plot(data, x="x", y="y")
    .add(so.Dot(), color="group")
    .facet("category")
    .scale(color="Set2")
    .layout(size=(8, 5))
    .save("plot.pdf")
)
```

### Marks
| Mark | Description |
|------|-------------|
| `so.Dot` / `so.Dots` | Single / multiple scatter points |
| `so.Line` / `so.Lines` | Single / grouped lines |
| `so.Path` / `so.Paths` | Connected paths (unordered) |
| `so.Bar` / `so.Bars` | Single / grouped bars |
| `so.Dash` | Short line marks (tick-like) |
| `so.Range` | Interval/range marks |
| `so.Area` | Filled area |
| `so.Band` | Filled band between y values |
| `so.Text` | Text annotations |

### Stats
| Stat | Description |
|------|-------------|
| `so.Agg` | Aggregate (mean, median, etc.) |
| `so.Est` | Estimate with error bars |
| `so.Count` | Count occurrences |
| `so.Hist` | Histogram binning |
| `so.KDE` | Kernel density estimation |
| `so.Perc` | Percentile computation |
| `so.PolyFit` | Polynomial fit |

### Moves
`so.Dodge`, `so.Jitter`, `so.Norm`, `so.Stack`, `so.Shift`

### Scales
`so.Boolean`, `so.Continuous`, `so.Nominal`, `so.Temporal`

## Classic Interface (Function API)

### Relational Plots
```python
sns.relplot(data, x, y, hue, size, style, col, row, kind="scatter"|"line")
sns.scatterplot(data, x, y, hue, size, style, alpha)
sns.lineplot(data, x, y, hue, style, estimator, ci)
```

### Distribution Plots
```python
sns.displot(data, x, hue, kind="hist"|"kde"|"ecdf", col, row)
sns.histplot(data, x, hue, bins, stat="count"|"density"|"probability", kde=True)
sns.kdeplot(data, x, y, hue, fill, bw_adjust, common_norm)
sns.ecdfplot(data, x, hue, stat="proportion"|"count")
sns.rugplot(data, x, hue, height)
```

### Categorical Plots
```python
sns.catplot(data, x, y, hue, col, row, kind="strip"|"swarm"|"box"|"violin"|"boxen"|"point"|"bar"|"count")
sns.stripplot(data, x, y, hue, jitter, dodge)
sns.swarmplot(data, x, y, hue, dodge)
sns.boxplot(data, x, y, hue, whis, fliersize)
sns.violinplot(data, x, y, hue, split, inner="box"|"quart"|"point"|"stick")
sns.boxenplot(data, x, y, hue, k_depth)
sns.pointplot(data, x, y, hue, estimator, ci, join)
sns.barplot(data, x, y, hue, estimator, ci)
sns.countplot(data, x, hue)
```

### Regression Plots
```python
sns.lmplot(data, x, y, hue, col, row, order, logistic, lowess)
sns.regplot(data, x, y, order, ci, scatter_kws, line_kws)
sns.residplot(data, x, y, order, lowess)
```

### Matrix Plots
```python
sns.heatmap(data, annot=True, fmt=".2f", cmap, vmin, vmax, linewidths, square,
            xticklabels, yticklabels, mask, cbar_kws)
sns.clustermap(data, method, metric, row_cluster, col_cluster, row_colors,
               col_colors, figsize, dendrogram_ratio, cmap)
```

### Multi-Plot Grids
```python
g = sns.FacetGrid(data, col, row, hue, col_wrap, height, aspect)
g.map(plt.scatter, "x", "y")
g.map_dataframe(sns.scatterplot, x="x", y="y")

g = sns.PairGrid(data, vars, hue, diag_sharey=False)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot)

sns.pairplot(data, vars, hue, kind="scatter"|"kde"|"hist"|"reg", diag_kind)
sns.jointplot(data, x, y, hue, kind="scatter"|"kde"|"hist"|"hex"|"reg"|"resid")
```

### Style & Context
```python
sns.set_theme(style="whitegrid", context="paper", palette="Set2", font_scale=1.2)
sns.set_style("whitegrid"|"darkgrid"|"white"|"dark"|"ticks")
sns.set_context("paper"|"notebook"|"talk"|"poster", font_scale)
sns.set_palette("Set2"|"husl"|"muted"|list_of_colors)
sns.color_palette("Set2", n_colors=8)  # get palette
```

## Common Patterns for Bio

```python
# Volcano plot
sns.scatterplot(data=df, x='log2FC', y='-log10p', hue='sig', palette={'Up':'red','Down':'blue','NS':'grey'})

# Expression heatmap with clustering
sns.clustermap(expr_matrix, method='ward', cmap='RdBu_r', z_score=0, figsize=(12,8),
               row_colors=cell_type_colors, col_colors=condition_colors)

# Violin + strip for gene expression
sns.violinplot(data=df, x='cell_type', y='expression', inner=None, palette='Set2')
sns.stripplot(data=df, x='cell_type', y='expression', color='black', size=2, alpha=0.3)

# UMAP embedding
sns.scatterplot(data=df, x='UMAP1', y='UMAP2', hue='cluster', palette='tab20', s=5, linewidth=0)
```
