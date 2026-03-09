---
name: statistical-testing-framework
description: "Use when performing ANY statistical comparison in omics analysis — guides selection of appropriate statistical tests based on data type, distribution, sample size, and study design. Covers parametric vs non-parametric, multiple testing correction, and effect size reporting."
---

# Statistical Testing Framework — Omics Analysis

## Overview

Correct statistical testing is non-negotiable. Wrong test → wrong conclusion → retraction. This skill guides test selection, enforces multiple testing correction, and mandates effect size reporting for all omics analyses.

## 1. Statistical Test Selection Decision Tree

### 1.1 Two-Group Comparison

| Condition | Test | R Function | Python Function |
|-----------|------|-----------|----------------|
| Continuous, normal, equal variance | Student's t-test | `t.test()` | `scipy.stats.ttest_ind()` |
| Continuous, normal, unequal variance | Welch's t-test | `t.test(var.equal=FALSE)` | `scipy.stats.ttest_ind(equal_var=False)` |
| Continuous, non-normal or n < 6/group | Wilcoxon rank-sum | `wilcox.test()` | `scipy.stats.mannwhitneyu()` |
| RNA-seq counts (raw) | DESeq2 Wald test | `DESeq2::results()` | `pydeseq2` |
| scRNA-seq (sparse counts) | Wilcoxon rank-sum | `Seurat::FindMarkers(test.use="wilcox")` | `scanpy.tl.rank_genes_groups(method='wilcoxon')` |
| Proportions / frequencies | Fisher's exact test | `fisher.test()` | `scipy.stats.fisher_exact()` |

### 1.2 Multi-Group Comparison (≥ 3 groups)

| Condition | Test | Post-hoc |
|-----------|------|----------|
| Continuous, normal | One-way ANOVA | Tukey HSD |
| Continuous, non-normal | Kruskal-Wallis | Dunn's test with BH correction |
| RNA-seq counts | DESeq2 LRT | Pairwise Wald with BH correction |
| Ecological (community composition) | PERMANOVA | Pairwise PERMANOVA |

### 1.3 Paired / Repeated Design

| Condition | Test |
|-----------|------|
| Paired, normal | Paired t-test |
| Paired, non-normal | Wilcoxon signed-rank |
| Repeated measures, normal | Repeated-measures ANOVA |
| Repeated measures, non-normal | Friedman test |

### 1.4 Correlation / Association

| Condition | Test | When |
|-----------|------|------|
| Both continuous, linear + normal | Pearson | Expression correlation |
| Monotonic relationship | Spearman | Abundance correlation, rank-based |
| Ordinal data | Kendall tau | Ordered categories |
| Community similarity | Mantel test | Distance matrices (beta diversity) |

### 1.5 Categorical / Compositional

| Condition | Test |
|-----------|------|
| 2×2 table, small n | Fisher's exact |
| r×c table, large n | Chi-squared |
| Community composition vs factor | PERMANOVA (`adonis2`) |
| Differential abundance (16S/shotgun) | ANCOM-BC / ALDEx2 / MaAsLin2 |

## 2. Multiple Testing Correction

<IRON-LAW>
When performing multiple comparisons, correction is MANDATORY. No exceptions.

| Method | When to Use | R | Python |
|--------|------------|---|--------|
| **Benjamini-Hochberg (FDR)** | Default for all omics | `p.adjust(method="BH")` | `statsmodels.stats.multitest.multipletests(method='fdr_bh')` |
| **Bonferroni** | Conservative; few comparisons (< 20) | `p.adjust(method="bonferroni")` | `multipletests(method='bonferroni')` |
| **Storey q-value** | Large-scale testing (> 1000 tests) | `qvalue::qvalue()` | — |

### Correction Rules:
- **DESeq2 / edgeR / limma**: Automatic BH correction built-in (`padj`)
- **Manual comparisons**: YOU must apply correction yourself
- **Reporting threshold**: FDR-adjusted p < 0.05 (default); state explicitly
- **No correction = red line violation**: Report adjusted AND raw p-values

Uncorrected multiple comparisons → Gate FAIL.
</IRON-LAW>

## 3. Effect Size Reporting

<IRON-LAW>
p-value alone is INSUFFICIENT. Every statistical comparison must also report effect size.

| Test | Effect Size Metric | Interpretation |
|------|-------------------|----------------|
| t-test / Wilcoxon | Cohen's d or rank-biserial r | small: 0.2, medium: 0.5, large: 0.8 |
| ANOVA / Kruskal-Wallis | eta² (η²) or epsilon² | small: 0.01, medium: 0.06, large: 0.14 |
| DESeq2 / differential expression | log₂FoldChange | biologically meaningful: |log₂FC| ≥ 1 |
| Correlation | r or ρ value | weak: 0.1–0.3, moderate: 0.3–0.5, strong: > 0.5 |
| PERMANOVA | R² | proportion of variance explained |
| Fisher / Chi-squared | Odds ratio / Cramér's V | — |

### Report Format:
```
Test: Wilcoxon rank-sum
p-value: 0.003 (BH-adjusted: 0.012)
Effect size: Cohen's d = 1.23 (large)
Sample size: n1=15, n2=12
```
</IRON-LAW>

## 4. Sample Size Constraints

| Sample Size (per group) | Allowed Tests | Notes |
|:---:|---|---|
| n < 3 | **No statistical testing** | Descriptive only; state "n too small for inference" |
| n = 3–5 | Non-parametric only | Wilcoxon, Fisher exact; cannot assess normality |
| n ≥ 6 | Parametric or non-parametric | Check normality first (Shapiro-Wilk) |
| n ≥ 30 | Full suite | CLT applies; most tests valid |

<IRON-LAW>
NEVER perform statistical testing with n < 3 per group. Report descriptive statistics only.
NEVER use parametric tests with n < 6 per group without validated normality.
</IRON-LAW>

## 5. Common Pitfalls in Bioinformatics

| Pitfall | Problem | Fix |
|---------|---------|-----|
| **Pseudoreplication** | Technical replicates treated as biological replicates | Aggregate technical replicates; use biological n for stats |
| **No multiple testing correction** | False discovery rate explodes with thousands of tests | Always apply BH/FDR (see §2) |
| **Ignoring batch effects** | Confounded results | Include batch in model or use `ComBat` / `limma::removeBatchEffect` |
| **Parametric on n=3** | Cannot validate normality assumption | Use non-parametric tests |
| **p-hacking** | Testing many subsets until "significant" | Pre-register analysis plan; report ALL tests performed |
| **Compositional data** | Relative abundance is not independent | Use compositional methods (ANCOM-BC, ALDEx2) for microbiome |
| **Ignoring zero-inflation** | scRNA-seq has many zeros | Use appropriate models (ZINB, hurdle) or Wilcoxon |

## 6. Normality Assessment

Before choosing parametric vs non-parametric:

1. **Visual**: Q-Q plot, histogram
2. **Formal test**: Shapiro-Wilk (n < 50) or Anderson-Darling (n ≥ 50)
3. **Rule of thumb**: If p(Shapiro) < 0.05 → non-normal → use non-parametric
4. **For omics**: Most omics data is NOT normally distributed. When in doubt, use non-parametric.

## 7. Integration with Workflow

- **Phase 2 (Analysis Design)**: Select statistical tests based on study design
- **Phase 4 (Execution)**: Apply tests with proper correction
- **Phase 5 (Integration)**: Cross-validate statistical findings
- **Checkpoint**: Record all tests used, correction methods, and justification in phase checkpoint files
