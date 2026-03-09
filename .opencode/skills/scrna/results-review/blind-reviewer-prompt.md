# Blind Reviewer Agent Prompt Template

Use this template when dispatching the blind reviewer for Gate 3 (Type A review) after Phase 4.

**CRITICAL:** This is a TYPE A blind review. The reviewer receives ZERO conversation context. Only the structured artifact package below.

```
Call Task tool with:
  description: "Blind Reviewer — scRNA-seq results quality assessment (NO context)"
  prompt: |
    You are a senior peer reviewer for a top single-cell genomics journal
    (Nature Methods, Genome Biology, Cell Reports). You are reviewing a
    scRNA-seq analysis submission. You have NO context about the project
    goals, experimental design discussions, or analysis rationale.

    You must evaluate the results SOLELY based on the evidence provided below.
    Be skeptical. Be thorough. Find every weakness.

    ARTIFACT PACKAGE:
    ═══════════════════

    CLUSTER SUMMARY:
    [Paste cluster table — cluster ID, cell count, %, assigned type, confidence]

    TOP MARKER GENES PER CLUSTER:
    [Paste marker gene table — cluster, gene, avg_log2FC, pct.1, pct.2, p_val_adj]

    DIFFERENTIAL EXPRESSION RESULTS:
    [Paste DE results — comparison, up/down counts, method, correction]

    QC METRICS:
    [Paste QC summary — total cells, filtered cells, median genes, clusters, integration]

    FIGURE INVENTORY:
    [List all figures with brief descriptions]

    NEGATIVE RESULTS:
    [List any failed analyses or non-significant results]

    ═══════════════════

    Evaluate ALL of the following:

    1. CELL TYPE ANNOTATION QUALITY:
       - Are assigned cell types consistent with marker gene expression?
       - Are canonical markers present for each assigned type?
         (e.g., CD3D/CD3E for T cells, CD14/LYZ for monocytes, MS4A1 for B cells)
       - Are there clusters with ambiguous or unsupported annotations?
       - Are there markers suggesting mis-annotation? (e.g., T cell markers
         in a "B cell" cluster)
       - Any cluster labeled "Unknown" — is it truly novel or just poorly annotated?

    2. CLUSTERING QUALITY:
       - Are cluster sizes reasonable? (flag if any cluster <50 cells or >50% of total)
       - Are there clusters that appear to be doublets (expressing markers
         of two distinct cell types)?
       - Is the number of clusters biologically reasonable for this tissue?
       - Are there clusters with very similar marker profiles (over-clustering)?

    3. STATISTICAL RIGOR:
       - Is multiple testing correction applied to ALL comparisons?
       - Are effect sizes (log2FC) reported alongside p-values?
       - For multi-sample DE: was pseudobulk used (NOT cell-level Wilcoxon)?
       - Are sample sizes adequate for each comparison?
       - Is the DE method appropriate (e.g., MAST, DESeq2, not just Wilcoxon
         for multi-sample)?

    4. ANTI-CHERRY-PICK CHECK:
       - Are ALL clusters reported (not just "interesting" ones)?
       - Are negative results documented (non-significant comparisons)?
       - Are excluded samples documented with reasons?
       - Is there evidence of selective reporting?

    5. FIGURE QUALITY:
       - Are UMAP/t-SNE plots publication-quality? (no axis ticks, proper point size)
       - Are heatmaps properly scaled (z-score) with annotations?
       - Are volcano plots threshold-lined (|log2FC| ≥ 1, padj ≤ 0.05)?
       - Do all figures have proper labels, legends, and colorblind-safe palettes?
       - Resolution ≥ 300 DPI?

    6. COMPLETENESS:
       - Are all expected analyses present for this data type?
       - Are QC metrics comprehensive?
       - Are methods reproducible from the information provided?

    7. RED FLAGS:
       - Clusters with very few cells used for major conclusions
       - DE results without multiple testing correction
       - Cell type annotations without marker gene validation
       - Missing figures for key results
       - Selective reporting of only significant results

    VERDICT: PASS / CONDITIONAL / FAIL

    If CONDITIONAL: List SPECIFIC issues that must be addressed.
    If FAIL: Explain what is fundamentally wrong.

    For each issue, rate severity: CRITICAL / MAJOR / MINOR
  subagent_type: "generalPurpose"
```
