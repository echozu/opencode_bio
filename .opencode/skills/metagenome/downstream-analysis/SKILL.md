---
name: downstream-analysis
description: Use when primary profiling (taxonomy/function) is complete for any data type — provides shared downstream analyses including diversity, differential abundance, and interaction networks
---

<HARD-GATE>
Do NOT execute downstream analysis without:
1. Primary profiling complete (taxonomy and/or functional tables generated)
2. Domain sanity check passed on primary results
3. Parameters locked in analysis-protocol.yaml
</HARD-GATE>

# Downstream Analysis (Phase 4 Sub-Skill — Shared Across Types)

## Overview

Shared downstream analyses applicable to all metagenome data types: diversity analysis, differential abundance testing, co-occurrence networks, and biomarker identification. All parameters from locked `analysis-protocol.yaml`.

## Analysis Module 1: Alpha Diversity

Calculate within-sample diversity using LOCKED metrics:
```
metrics: [from protocol]  # e.g., Shannon, Simpson, Chao1, observed_features
rarefaction_depth: [from protocol]
```

**Outputs:**
- Per-sample alpha diversity values for each metric
- Rarefaction curves (to verify depth sufficiency)
- Statistical comparison between groups (Kruskal-Wallis or Wilcoxon)
- Box plots with individual data points

<IRON-LAW>
Rarefaction depth must be justified:
- Should be set at or near the minimum sample depth
- If minimum depth is too low, flag those samples rather than over-rarefying
- Report how many samples are excluded by rarefaction
- NEVER change rarefaction depth after G2 without user approval
</IRON-LAW>

## Analysis Module 2: Beta Diversity

Calculate between-sample distances:
```
metrics: [from protocol]  # e.g., Bray-Curtis, UniFrac, Jaccard
permanova_permutations: [from protocol]
```

**Outputs:**
- Distance matrices for each metric
- PCoA ordination plots (with 95% confidence ellipses per group)
- PERMANOVA results (R², p-value, per-group comparisons)
- ANOSIM results (as supplementary)
- Betadisper test (test for homogeneity of dispersions)

<IRON-LAW>
PERMANOVA requires checking assumptions:
1. Run betadisper BEFORE interpreting PERMANOVA
2. If betadisper is significant (groups have different dispersions), PERMANOVA results may be confounded
3. Report BOTH betadisper and PERMANOVA results — do NOT hide negative betadisper results

A significant PERMANOVA with significant betadisper is AMBIGUOUS — state this clearly.
</IRON-LAW>

## Analysis Module 3: Differential Abundance

Identify differentially abundant taxa/functions:
```
tool: [from protocol]  # DESeq2, ANCOM-BC, LEfSe, MaAsLin2
significance_threshold: [from protocol]
lfc_threshold: [from protocol]
multiple_testing: [from protocol]
confounders: [from protocol]
```

**Outputs:**
- Differentially abundant features table (feature, log2FC, p-value, adjusted p-value)
- Volcano plot
- Heatmap of top differentially abundant features
- Effect size plots (for LEfSe)

**Tool-specific considerations:**
- **DESeq2**: Handles unrarefied count data; good for small sample sizes
- **ANCOM-BC**: Handles compositional bias; recommended for microbiome data
- **LEfSe**: Effect size-based; good for biomarker discovery
- **MaAsLin2**: Handles confounders explicitly; recommended for complex designs

<IRON-LAW>
Run at LEAST two differential abundance methods and compare results:
- Concordant results strengthen claims
- Discordant results require investigation and transparent reporting
- Do NOT cherry-pick the method that gives the most significant results
</IRON-LAW>

## Analysis Module 4: Network Analysis (if included)

Co-occurrence network construction:
```
tool: [from protocol]  # SparCC, SpiecEasi, WGCNA
correlation_method: [from protocol]
significance_threshold: [from protocol]
min_prevalence: [from protocol]
```

**Outputs:**
- Correlation matrix (filtered by significance and effect size)
- Network visualization (nodes = taxa, edges = correlations)
- Network metrics (modularity, hub taxa, betweenness centrality)
- Module-trait associations (if metadata available)

**Quality controls:**
- Minimum 20 samples recommended for network analysis
- Prevalence filter to remove rare taxa (typically present in ≥10% samples)
- Multiple testing correction on correlations

## Analysis Module 5: Biomarker Identification (if included)

Random forest or machine learning-based classification:
- Feature importance ranking
- Cross-validation performance (AUC, accuracy)
- Selected biomarker panel
- Validation on held-out samples (if available)

## Visualization Standards

All figures must follow locked visualization parameters:
- Consistent color palette across all figures
- Group colors match throughout (control = green, disease = red, etc.)
- Publication-ready format (vector format preferred)
- Font size ≥8pt for all text
- Error bars or confidence intervals shown

## Domain Sanity Check After Downstream

- [ ] Alpha diversity patterns match biological expectation (e.g., reduced in disease)
- [ ] PCoA shows grouping consistent with experimental design
- [ ] Differentially abundant taxa are biologically plausible
- [ ] Network modules contain functionally related organisms
- [ ] Results are consistent across different methods (diversity, differential)

## Red Flags — STOP

- All groups showing identical diversity (no biological signal?)
- PERMANOVA p-value exactly 0.001 with R² <0.05 (statistically significant but biologically meaningless)
- >1000 differentially abundant features (likely analysis error or no multiple testing correction)
- Zero differentially abundant features (insufficient power or wrong method?)
- Network with >90% positive correlations (compositional artifact)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "One differential method is sufficient" | Methods disagree. Run ≥2 and compare. |
| "Rarefaction is outdated, skip it" | Rarefaction is still valid for diversity. Use appropriate normalization per analysis. |
| "The p-value is significant so the result is real" | Effect size matters more than p-value. Report R², log2FC, not just p. |
| "Network analysis is exploratory" | Exploratory ≠ unrestricted. Still needs prevalence filter and correction. |
| "I'll adjust the significance threshold later" | Threshold is LOCKED in protocol. Change requires user approval. |
| "Betadisper isn't important" | Betadisper determines PERMANOVA interpretation. Always report it. |
