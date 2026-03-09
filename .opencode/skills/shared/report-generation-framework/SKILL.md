---
name: report-generation-framework
description: "Use in Phase 6 to generate the final analysis report — provides report structure template, section requirements, figure/table referencing standards, and methods description format suitable for direct use in publications."
---

# Report Generation Framework — Omics Analysis Report

## Overview

Phase 6 produces the final analysis report. This skill defines the standard report structure, section requirements, Methods description format, and quality checklist. Reports must be publication-ready — usable directly in papers or as supplementary materials.

## 1. Report Structure Template

```
1. Executive Summary (关键发现摘要)
   - 1-2 paragraph summary of key findings
   - Final data quality grade
   - Sample sizes and groups analyzed

2. Introduction & Background
   - Study context and biological question
   - Brief description of experimental design

3. Materials & Methods
   - 3.1 Data Sources and Preprocessing
   - 3.2 Quality Control
   - 3.3 Analysis Pipeline (with versions)
   - 3.4 Statistical Methods
   - 3.5 Software and Databases

4. Results
   - 4.1 Data Quality Assessment (with QC grade)
   - 4.2 Primary Analysis Results
   - 4.3 Secondary / Downstream Analysis
   - 4.4 Cross-Validation (if multi-omics)

5. Discussion
   - Key findings and biological significance
   - Limitations
   - Comparison with known literature (if applicable)

6. Supplementary Materials
   - Complete parameter tables
   - Additional figures
   - Full gene/pathway lists
```

## 2. Methods Description Standards

<IRON-LAW>
Methods sections must contain sufficient detail for independent reproduction.

### Required Elements:
| Element | Requirement | Example |
|---------|------------|---------|
| Tool name | Full name + version | "fastp v0.23.4" |
| Key parameters | Non-default parameters | "--qualified_quality_phred 20 --length_required 50" |
| Database | Name + version/date | "SILVA database (release 138.1)" |
| Reference genome | Assembly + annotation | "GRCh38, GENCODE v44" |
| Statistical test | Test name + correction | "Wilcoxon rank-sum test, BH-corrected (FDR < 0.05)" |
| Cutoffs | Exact thresholds | "|log₂FC| ≥ 1 and adjusted p-value < 0.05" |

### Methods Template:
```
Raw sequencing reads were quality-trimmed using fastp v0.23.4
(--qualified_quality_phred 20, --length_required 50). Reads were
aligned to the GRCh38 reference genome (GENCODE v44) using STAR
v2.7.11a with default parameters. Gene-level counts were generated
using featureCounts v2.0.6. Differential expression analysis was
performed using DESeq2 v1.40.2 with the model ~condition + batch.
Genes with |log₂FC| ≥ 1 and BH-adjusted p-value < 0.05 were
considered significantly differentially expressed.
```
</IRON-LAW>

## 3. Figure and Table Referencing

### Rules:
1. Every figure/table MUST be referenced in the text at least once
2. References use consistent numbering: "Figure 1", "Table 1", "Figure S1" (supplementary)
3. Every claim in the text MUST point to supporting figure/table/data
4. Multi-panel figures: reference specific panels — "Figure 2a shows..."

### Figure Caption Requirements:
- Describe what the figure shows (one sentence)
- Key observation / takeaway
- Panel descriptions for multi-panel figures
- Statistical details (test used, p-value, n)
- Self-contained — reader should understand without main text

## 4. Results Section Writing Rules

### Structure per Finding:
```
Context → Method → Result → Interpretation

Example:
"To assess data quality, we performed QC analysis using FastQC and
fastp. All samples passed quality filters with an overall grade of B
(median Q30 = 92.3%, mapping rate = 89.1%; Figure 1a, Table S1).
Three samples showed elevated duplication rates (> 40%) but remained
within acceptable thresholds (grade C). These samples were retained
for downstream analysis with noted limitations."
```

### Rules:
- Lead with the most important findings
- Report exact numbers, not vague qualifiers ("many", "several")
- Include effect sizes alongside p-values
- Non-significant results get full reporting (see reproducibility-discipline)
- Use past tense for results

## 5. Discussion Section Guidelines

| Do | Don't |
|----|-------|
| Interpret results in biological context | Over-speculate beyond evidence |
| Acknowledge limitations honestly | Minimize known issues |
| Compare with published literature | Ignore conflicting evidence |
| Suggest follow-up experiments | Make unsupported causal claims |
| State confidence level | Use absolute language ("proves") |

### Required Discussion Elements:
1. **Key findings summary** — in context of the biological question
2. **Biological significance** — what do the results mean?
3. **Limitations** — data quality issues, sample size, analytical choices
4. **Concordance** — agreement/disagreement with known literature
5. **Future directions** — what analyses or experiments would strengthen conclusions

## 6. Quality Checklist — Final Report

Before submitting the report, verify:

### Completeness:
- [ ] All analysis phases represented in Results
- [ ] Methods contain all tools + versions + parameters
- [ ] Every figure/table referenced in text
- [ ] Every claim supported by evidence
- [ ] Non-significant results reported
- [ ] Limitations discussed

### Accuracy:
- [ ] Numbers match checkpoint files
- [ ] Figure descriptions match actual figure content
- [ ] Statistical test names and p-values correct
- [ ] Sample sizes accurate

### Format:
- [ ] Consistent figure/table numbering
- [ ] Consistent terminology throughout
- [ ] All abbreviations defined at first use
- [ ] Language matches user preference (Chinese/English)

### Reproducibility:
- [ ] Complete software environment documented
- [ ] Database versions recorded
- [ ] Full parameter tables in supplementary
- [ ] All commands available in checkpoint files

## 7. Integration with Workflow

1. **Phase 5 → Phase 6**: Gather all checkpoint files, figures, and tables from Phases 1–5
2. **Draft generation**: Follow structure template (§1)
3. **Self-review**: Apply quality checklist (§6)
4. **Gate 4**: Report undergoes review before delivery

## 8. Output Files

```
docs/{domain}/report/
  ├── analysis_report.md          # Main report
  ├── methods_section.md          # Standalone Methods (publication-ready)
  ├── supplementary_materials.md  # Supplementary tables and figures
  └── figures/                    # All report figures (PDF/SVG)
```
