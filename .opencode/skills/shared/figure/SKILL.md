---
name: figure
description: "Generate publication-quality academic figures with enforced bioinformatics visualization standards. Two capabilities: (1) AutoFigure-Edit: method text to editable SVG via SAM3 + LLM. (2) Data Visualization: comprehensive reference for ggplot2, seaborn, ComplexHeatmap, clusterProfiler GO visualization, BioCircos circular plots, and 50+ chart types. Includes mandatory quality standards for UMAP, heatmap, volcano plot, species composition barplot, diversity plot, enrichment bubble plot, survival curve. Covers color schemes, resolution, labeling, and accessibility."
tool_type: mixed
primary_tool: ggplot2
---

## Version Compatibility

Reference examples tested with: Python 3.10+, torch 2.1+, Pillow 10.0+, matplotlib 3.8+

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures

If code throws ImportError, AttributeError, or TypeError, introspect the installed
package and adapt the example to match the actual API rather than retrying.

# Academic Figure Generation

This skill provides two capabilities for generating publication-quality academic figures:

| Goal | Capability | Output |
|------|------------|--------|
| Method text -> editable SVG figure | **AutoFigure-Edit** | `final.svg` (vector, editable) |
| Statistical plots, heatmaps, enrichment plots, circos... | **Data Visualization References** | R/Python code |

## Routing Logic

**Use AutoFigure-Edit when:**
- User wants an editable SVG output
- User says "method diagram", "pipeline figure", "可编辑图", "SVG"
- The input is a method/approach section of a paper
- User needs to manually tweak the figure after generation

**Use Data Visualization References when:**
- User needs statistical plots (scatter, bar, box, violin, heatmap, etc.)
- User says "画图", "ggplot", "seaborn", "heatmap", "enrichment plot"
- Task involves GO/KEGG enrichment visualization, circos plots, volcano plots
- User needs code examples for ggplot2, seaborn, ComplexHeatmap, clusterProfiler, BioCircos

---

## Engine 1: AutoFigure-Edit

Converts paper method text into fully editable SVG figures through a multi-stage pipeline.

> **Note:** AutoFigure-Edit source code is located **outside** the skills directory to avoid
> slow scanning on startup. Location: `<project_root>/../autofigure-edit/`
> (e.g. `/jinxianstor/home/<user>/openBio/autofigure-edit/`).
> This section contains all the information the Agent needs to use it.

### Pipeline

```
Method Text -> [LLM Image Gen] -> figure.png
    -> [SAM3 Segmentation] -> samed.png + boxlib.json
    -> [Icon Extraction + RMBG2] -> icons/
    -> [LLM SVG Generation] -> template.svg
    -> [LLM SVG Optimization] -> optimized_template.svg
    -> [Icon Replacement] -> final.svg
```

### Prerequisites

```bash
# AutoFigure-Edit is located at: <openBio_root>/autofigure-edit/
# Install dependencies
pip install -r /path/to/openBio/autofigure-edit/requirements.txt

# SAM3 (for local segmentation backend)
git clone https://github.com/facebookresearch/sam3.git
cd sam3 && pip install -e .
```

### Usage

```bash
# Set the path to autofigure-edit (adjust to your environment)
AUTOFIGURE_DIR="/path/to/openBio/autofigure-edit"

# Basic usage with Bianxie provider (recommended)
python "$AUTOFIGURE_DIR/autofigure2.py" \
    --method_file paper_method.txt \
    --output_dir ./output \
    --api_key "your-api-key"

# Use Gemini provider
python "$AUTOFIGURE_DIR/autofigure2.py" \
    --method_file paper_method.txt \
    --output_dir ./output \
    --api_key "your-key" \
    --provider gemini

# Use OpenRouter provider
python "$AUTOFIGURE_DIR/autofigure2.py" \
    --method_file paper_method.txt \
    --output_dir ./output \
    --api_key "sk-or-v1-xxx" \
    --provider openrouter

# Use label placeholder mode (recommended) with multi-prompt SAM3
python "$AUTOFIGURE_DIR/autofigure2.py" \
    --method_file paper_method.txt \
    --output_dir ./output \
    --api_key "your-key" \
    --placeholder_mode label \
    --sam_prompt "icon,diagram,arrow,chart"

# Control SVG optimization iterations (0 = skip, default = 1)
python "$AUTOFIGURE_DIR/autofigure2.py" \
    --method_file paper_method.txt \
    --output_dir ./output \
    --optimize_iterations 3

# Custom box merge threshold (default 0.9, set 0 to disable)
python "$AUTOFIGURE_DIR/autofigure2.py" \
    --method_file paper_method.txt \
    --output_dir ./output \
    --merge_threshold 0.8
```

### Key Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `--provider` | `bianxie`, `openrouter`, `gemini` | `bianxie` | LLM API provider |
| `--placeholder_mode` | `none`, `box`, `label` | `label` | How placeholders appear in SVG |
| `--sam_prompt` | comma-separated strings | `"icon"` | SAM3 text prompts for segmentation |
| `--merge_threshold` | 0.0-1.0 | `0.9` | Overlap threshold for box merging |
| `--optimize_iterations` | integer >= 0 | `1` | SVG optimization rounds |
| `--sam_backend` | `local`, `fal`, `roboflow` | `local` | SAM3 backend |

### Output Artifacts

```
output_dir/
├── figure.png              # Generated raster image
├── samed.png               # Segmentation mask visualization
├── boxlib.json             # Detected regions with coordinates
├── icons/                  # Individual icon assets (background removed)
├── template.svg            # Initial SVG template
├── optimized_template.svg  # Optimized SVG template
└── final.svg               # Final editable SVG with icons
```

### Web UI (Optional)

AutoFigure-Edit includes a FastAPI-based web interface with SVG editor:

```bash
python "$AUTOFIGURE_DIR/server.py" --port 8080
# Open http://localhost:8080 in browser
```

---

## Engine 2: Data Visualization Libraries

Comprehensive reference for programmatic data visualization. Detailed API docs in `references/` subdirectory.

### Routing by Tool/Language

| Need | R Package | Python Package | Reference File |
|------|-----------|----------------|----------------|
| General plots (scatter, bar, line, box, violin...) | **ggplot2** | **seaborn** / matplotlib | `ggplot2.md`, `seaborn.md` |
| Grammar of graphics tutorial | **ggplot2** (R4DS) | — | `r4ds-visualization.md` |
| Complex heatmaps with annotations | **ComplexHeatmap** | seaborn.clustermap | `complexheatmap.md` |
| GO/KEGG enrichment visualization | **clusterProfiler** + enrichplot | — | `clusterprofiler-go-viz.md` |
| Circular genomic plots | **BioCircos** / circlize | — | `biocircos.md` |
| 50+ chart type gallery | **R Graph Gallery** | Python Graph Gallery | `r-graph-gallery.md` |

### Quick Reference: Chart Type Selection

| Data Pattern | Recommended Chart | R | Python |
|-------------|-------------------|---|--------|
| Distribution of one variable | Histogram, Density, Violin | `geom_histogram()`, `geom_violin()` | `sns.histplot()`, `sns.violinplot()` |
| Compare groups | Box, Violin, Bar | `geom_boxplot()` | `sns.boxplot()`, `sns.barplot()` |
| Two continuous variables | Scatter, Hex | `geom_point()`, `geom_hex()` | `sns.scatterplot()` |
| Trend over time | Line, Area | `geom_line()`, `geom_area()` | `sns.lineplot()` |
| Correlation matrix | Heatmap | `ComplexHeatmap::Heatmap()` | `sns.clustermap()` |
| Gene expression matrix | Clustered heatmap | `ComplexHeatmap` | `sns.clustermap()` |
| Differential expression | Volcano plot | `EnhancedVolcano` | `matplotlib.scatter()` |
| GO/KEGG enrichment | Dot, Bar, Cnet, Emap | `dotplot()`, `cnetplot()`, `emapplot()` | — |
| Genomic landscape | Circos plot | `circlize`, `BioCircos` | — |
| Set intersections | UpSet plot | `ComplexHeatmap::UpSet()` | `upsetplot` |
| Cancer mutations | OncoPrint | `ComplexHeatmap::oncoPrint()` | — |
| Multi-panel composition | Patchwork | `patchwork` | `fig, axes = plt.subplots()` |
| UMAP/tSNE embedding | Scatter | `geom_point()` | `sns.scatterplot()` / `sc.pl.umap()` |

### Data Visualization References (in `references/`)

Each file is a self-contained API reference with copy-paste examples:

- **`ggplot2.md`** — All geom/stat/scale/coord/facet/theme functions, composition with patchwork
- **`seaborn.md`** — Objects API + classic API, relational/distributional/categorical/matrix plots
- **`complexheatmap.md`** — Heatmap(), annotations (anno_*), OncoPrint, UpSet, combining heatmaps
- **`clusterprofiler-go-viz.md`** — enrichGO/gseGO workflow + all viz: dotplot, barplot, cnetplot, emapplot, treeplot, ridgeplot, gseaplot2
- **`biocircos.md`** — SNP/Arc/Link/Heatmap/Histogram tracks, circlize for static Circos
- **`r-graph-gallery.md`** — 50+ chart types organized by category (distribution, correlation, ranking, evolution, map, flow)
- **`r4ds-visualization.md`** — Grammar of graphics tutorial, aesthetic mappings, faceting, position adjustments

### Source URLs

- https://ggplot2.tidyverse.org/
- https://seaborn.pydata.org/
- https://jokergoo.github.io/ComplexHeatmap-reference/book/
- https://yulab-smu.top/biomedical-knowledge-mining-book/021-go.html
- https://r4ds.had.co.nz/data-visualisation.html
- http://bioinfo.ibp.ac.cn/biocircos/document/biocircos.html
- https://github.com/holtzy/R-graph-gallery

---

---

## Publication-Quality Standards (Bioinformatics)

Every figure produced in an omics analysis MUST meet the standards below. This section is automatically enforced during Phase 4–6.

### Universal Figure Standards

#### Resolution and Format

| Property | Requirement |
|----------|------------|
| Format | Vector (PDF or SVG) for all plots; PNG at ≥ 300 DPI only for raster (photos, complex heatmaps) |
| Minimum DPI | 300 for raster; vector preferred |
| File format for reports | PDF first choice; SVG acceptable |

#### Typography

| Property | Requirement |
|----------|------------|
| Font family | **Helvetica / Arial** (sans-serif) — standard for life sciences |
| Axis label size | ≥ 8pt at final print size |
| Tick label size | ≥ 7pt |
| Legend text size | ≥ 7pt |
| Figure title | **OMIT on image** — title belongs in caption / report text |
| Panel labels | Bold lowercase: **a**, **b**, **c** — top-left of each panel |

#### Layout and Readability

| Property | Requirement |
|----------|------------|
| Axis labels | Present on every axis; include units (e.g., "log₂FC", "−log₁₀(p)") |
| Legend | Always present when multiple groups/series; never overlap data |
| White space | `bbox_inches='tight'`; no excessive margins |
| Spines | Left + bottom only; no top/right |
| Grid | None or very subtle for life sciences |
| Aspect ratio | Standard (4:3, 1:1). Never distorted. |

### Color Standards for Bioinformatics

#### Discrete Variables (groups, clusters, cell types)

| Palette | Use Case | Package |
|---------|----------|---------|
| **ggsci::npg** | Nature-style ≤ 10 groups | `ggsci` (R) |
| **RColorBrewer Set2** | Soft colors ≤ 8 groups | `RColorBrewer` |
| **RColorBrewer Paired** | 12 groups with paired design | `RColorBrewer` |
| **Scanpy default (Zeileis)** | scRNA cell types ≤ 28 | `scanpy` |
| **Tableau 10** | General purpose | `matplotlib` / `seaborn` |

#### Continuous Variables

| Palette | Use Case |
|---------|----------|
| **viridis** | Sequential data (expression, abundance). Default choice. |
| **RdBu** (diverging) | Log₂FC, z-scores — centered at 0 |
| **YlOrRd** | Heatmaps with zero baseline (abundance, counts) |
| **coolwarm** | Correlation matrices |

#### Color Rules

<IRON-LAW>
- **Colorblind-safe**: ALL figures must be distinguishable without color (use shape, line style, hatching as backup)
- **Consistent**: Same group = same color across ALL figures in the project
- **Maximum**: ≤ 10 distinct colors per panel; beyond that → use facets / subplots
- **No rainbow**: NEVER use `jet` or `rainbow` colormaps
</IRON-LAW>

```python
# Recommended bioinformatics palette (Nature-style)
BIO_COLORS = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488',
              '#F39B7F', '#8491B4', '#91D1C2', '#DC0000',
              '#7E6148', '#B09C85']

BIO_STYLE = {
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 8,
    'axes.titlesize': 9,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'axes.linewidth': 0.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
}
```

### Bioinformatics-Specific Plot Standards

#### UMAP / t-SNE Clustering Plot

| Property | Standard |
|----------|---------|
| Point size | 0.5–2 (scale inversely with cell count; ≤ 5k → 2, ≥ 50k → 0.5) |
| Alpha | 0.6–0.8 (show density via overlap) |
| Axes | Remove axis ticks and labels — UMAP/t-SNE axes have no numerical meaning |
| Legend | Cluster names/cell types outside plot; use `legend_fontoutline` in Scanpy |
| Palette | Scanpy default or `ggsci::npg` for ≤ 10 types; `Paired` for > 10 |
| Perplexity (t-SNE) | Report in figure caption |
| Label overlay | Optional: annotate cluster centers with cell type name |

#### Heatmap

| Property | Standard |
|----------|---------|
| Clustering | Row: hierarchical (ward.D2/complete); Column: group-ordered OR clustered |
| Color scale | Diverging (RdBu/coolwarm) for z-score; sequential (viridis/YlOrRd) for raw counts |
| Annotations | Column annotation bar for groups/conditions; Row annotation for gene categories |
| Dendrogram | Show for rows if clustered; optional for columns |
| Cell size | Readable gene names on rows (≥ 6pt) |
| Scale | Row z-score normalization for expression; specify in caption |
| Tools | `ComplexHeatmap` (R) preferred; `seaborn.clustermap` (Python) acceptable |

#### Volcano Plot

| Property | Standard |
|----------|---------|
| X-axis | log₂(Fold Change) |
| Y-axis | −log₁₀(adjusted p-value) |
| Threshold lines | Vertical: |log₂FC| ≥ 1 (dashed); Horizontal: padj ≤ 0.05 (dashed) |
| Color coding | Red = up-regulated, Blue = down-regulated, Gray = non-significant |
| Label | Top 10–20 significant genes by padj (use `ggrepel` / `adjustText` to avoid overlap) |
| Counts | Annotate total up/down/NS in corner |

#### Species/Taxon Composition Bar Plot (Metagenome)

| Property | Standard |
|----------|---------|
| Orientation | Vertical (samples on x-axis) or Horizontal |
| Ordering | Samples grouped by condition; taxa sorted by mean abundance |
| Top N | Show top 10–15 taxa; group remaining as "Others" (gray) |
| Y-axis | Relative abundance (0–100%) |
| Color | Distinct per taxon; consistent across all composition plots |

#### Alpha Diversity Plot

| Property | Standard |
|----------|---------|
| Plot type | Box plot + strip/jitter overlay (show individual samples) |
| Metrics | Report ≥ 2 metrics: Shannon + Chao1/Observed (or Simpson) |
| Statistics | Wilcoxon/Kruskal-Wallis p-value; brackets with significance markers |
| Y-axis | Named metric with units if applicable |

#### Beta Diversity / Ordination Plot

| Property | Standard |
|----------|---------|
| Plot type | PCoA / NMDS scatter |
| Axes | Include variance explained % in axis labels for PCoA |
| Ellipses | 95% confidence ellipse per group |
| Statistics | Report PERMANOVA R² and p-value in caption |
| Legend | Group names; consistent colors with other figures |

#### Enrichment Bubble Plot

| Property | Standard |
|----------|---------|
| X-axis | GeneRatio or RichFactor |
| Y-axis | Term name (sorted by p.adjust or grouped by category) |
| Size | Gene count |
| Color | p.adjust (continuous; viridis or RdYlBu) |
| Top N | Show top 15–20 significant terms |
| Redundancy | Apply `simplify()` or REVIGO before plotting |

#### Survival Curve (Kaplan-Meier)

| Property | Standard |
|----------|---------|
| Y-axis | Survival probability (0–1) |
| X-axis | Time (specify unit: days/months/years) |
| Risk table | MUST include below plot |
| Statistics | Log-rank test p-value; hazard ratio with 95% CI |
| Censoring | Tick marks on curves |
| Colors | One per group; consistent with project palette |
| Tool | `survminer::ggsurvplot` (R) or `lifelines` (Python) |

### Per-Figure Quality Checklist

<IRON-LAW>
Before including ANY figure in the report, verify EVERY item:

#### Image file:
- [ ] Resolution ≥ 300 DPI (or vector format)
- [ ] Axis labels present with units
- [ ] No title on figure (title goes in report text)
- [ ] Legend present and non-overlapping
- [ ] Panel labels (**a**, **b**, **c**) if multi-panel
- [ ] Colors consistent with project palette
- [ ] Colorblind-safe (markers/hatching as backup)
- [ ] Statistical annotations correct (p-value, effect size)
- [ ] Font ≥ 7pt at final size
- [ ] No chartjunk (no 3D, no rainbow, no excessive decoration)

#### Report text:
- [ ] Figure referenced in text
- [ ] Caption describes what figure shows and key takeaway
- [ ] Statistical details noted (test used, p-value threshold)
- [ ] Multi-panel: each panel described

Violation of any checked item → Gate CONDITIONAL at minimum.
</IRON-LAW>

### Anti-Patterns — NEVER

| Anti-Pattern | Fix |
|-------------|-----|
| Default matplotlib/ggplot2 theme | Apply `BIO_STYLE` or `theme_classic()` |
| `jet` / `rainbow` colormap | Use `viridis`, `RdBu`, or qualitative palette |
| 3D bar / pie charts | 2D grouped bars or stacked bars |
| Axis ticks on UMAP/t-SNE | Remove — coordinates are meaningless |
| Heatmap without scale bar | Always include color scale legend |
| Volcano plot without threshold lines | Add dashed lines at |log₂FC|=1 and padj=0.05 |
| Figures without error bars / variance | Always show variance (boxplot, CI, std) |

---

## Integration with Other Skills

This skill is designed to be invoked from multiple contexts:

- **`paper-writing`** (amplify): Invoke this skill during Phase 4/5/6 for figure generation
- **`analysis-storyboard-design`** (amplify): Reference when planning figures for story lines
- **Documentation skills** (doc): Invoke for any visualization in reports, slides, or markdown docs
- **`bio-data-visualization-volcano-customization`** (bio): Specialized volcano plots (complementary)
- **`bio-pathway-enrichment-visualization`** (bio): Specialized pathway visualization (complementary)

## Related Skills

- `report-generation-framework` - Report generation with figure referencing standards
- `paper-writing` - Full paper writing pipeline (invokes this skill for figures)
- `analysis-storyboard-design` - Story arc and figure planning for research projects
- `bio-data-visualization-volcano-customization` - Volcano plots
- `bio-pathway-enrichment-visualization` - Pathway visualization
- `bio-spatial-transcriptomics-spatial-visualization` - Spatial visualization
