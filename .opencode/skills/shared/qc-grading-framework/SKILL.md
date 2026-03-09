---
name: qc-grading-framework
description: "Use during Phase 1 (Data Assessment & QC) for ANY omics type — provides a universal A/B/C/D/F grading framework with domain-specific threshold configurations. Grades data quality and determines if analysis should proceed, proceed with caution, or halt."
---

# QC Grading Framework — Universal Data Quality Assessment

## Overview

Data quality determines everything downstream. This skill provides a **standardized A/B/C/D/F grading system** that works across all omics types, with domain-specific threshold configurations. Every Phase 1 must produce a quality grade using this framework.

## 1. Universal Grade Definitions

| Grade | Meaning | Action |
|:-----:|---------|--------|
| **A** | Excellent — high-quality data, ready for analysis | Proceed directly |
| **B** | Good — minor issues, needs small adjustments | Proceed after standard preprocessing |
| **C** | Acceptable — significant preprocessing needed but analyzable | Proceed with caution; document compromises |
| **D** | Poor — analysis results may be unreliable | **CONDITIONAL** — must inform user of risks; require explicit confirmation |
| **F** | Unusable — fundamental quality failure | **HALT** — do not proceed; recommend re-sequencing/re-collection |

## 2. Gate 1 Logic

<IRON-LAW>
QC grade determines Gate 1 verdict:

| Grade | Gate 1 Verdict | Next Step |
|:-----:|---------------|-----------|
| A or B | **PASS** | Proceed to Phase 2 |
| C | **PASS** (with notes) | Proceed; document quality limitations in checkpoint |
| D | **CONDITIONAL PASS** | Present risks to user; wait for explicit approval |
| F | **FAIL** | Stop analysis; provide diagnostic report |

You MUST NOT proceed past Gate 1 with grade F data. No exceptions.
</IRON-LAW>

## 3. Domain-Specific Threshold Configurations

### 3.1 scRNA-seq

| Metric | A (Excellent) | B (Good) | C (Acceptable) | D (Poor) | F (Fail) |
|--------|:---:|:---:|:---:|:---:|:---:|
| Median genes/cell | > 3000 | > 2000 | > 1000 | > 500 | ≤ 500 |
| Median UMI/cell | > 8000 | > 5000 | > 2000 | > 1000 | ≤ 1000 |
| Mitochondrial % | < 5% | < 10% | < 15% | < 20% | ≥ 20% |
| Doublet rate | < 3% | < 5% | < 8% | < 12% | ≥ 12% |
| Cell recovery rate | > 80% | > 60% | > 40% | > 20% | ≤ 20% |

### 3.2 Bulk RNA-seq

| Metric | A | B | C | D | F |
|--------|:---:|:---:|:---:|:---:|:---:|
| Total reads | > 30M | > 20M | > 10M | > 5M | ≤ 5M |
| Mapping rate | > 90% | > 85% | > 75% | > 60% | ≤ 60% |
| Duplication rate | < 30% | < 40% | < 50% | < 65% | ≥ 65% |
| rRNA % | < 5% | < 10% | < 15% | < 25% | ≥ 25% |
| Exonic rate | > 70% | > 60% | > 50% | > 35% | ≤ 35% |

### 3.3 Metagenome (16S / Shotgun)

| Metric | A | B | C | D | F |
|--------|:---:|:---:|:---:|:---:|:---:|
| Total reads (shotgun) | > 10M | > 5M | > 2M | > 1M | ≤ 1M |
| Q30 % | > 90% | > 85% | > 80% | > 70% | ≤ 70% |
| Host contamination % | < 5% | < 10% | < 20% | < 40% | ≥ 40% |
| Adapter % | < 1% | < 3% | < 5% | < 10% | ≥ 10% |
| 16S reads (amplicon) | > 50k | > 30k | > 10k | > 5k | ≤ 5k |

### 3.4 Proteomics (LC-MS/MS)

| Metric | A | B | C | D | F |
|--------|:---:|:---:|:---:|:---:|:---:|
| Identified proteins | > 5000 | > 3000 | > 1500 | > 500 | ≤ 500 |
| Peptide FDR | < 1% | < 1% | < 5% | < 5% | ≥ 5% |
| Missing values % | < 10% | < 20% | < 35% | < 50% | ≥ 50% |
| CV (technical) | < 10% | < 15% | < 20% | < 30% | ≥ 30% |

### 3.5 Epigenomics (ChIP-seq / ATAC-seq)

| Metric | A | B | C | D | F |
|--------|:---:|:---:|:---:|:---:|:---:|
| Total reads | > 30M | > 20M | > 10M | > 5M | ≤ 5M |
| Mapping rate | > 90% | > 80% | > 70% | > 50% | ≤ 50% |
| FRiP (ATAC) | > 30% | > 20% | > 10% | > 5% | ≤ 5% |
| TSS enrichment (ATAC) | > 10 | > 7 | > 4 | > 2 | ≤ 2 |
| Duplication rate | < 20% | < 30% | < 50% | < 70% | ≥ 70% |

## 4. Grade Calculation Rules

1. **Per-metric grading**: Each metric receives its own grade independently
2. **Overall grade**: Use the **WORST** individual metric grade as the overall grade (conservative approach)
3. **Exception**: If only ONE metric is one grade lower while all others are higher, overall grade = second-worst grade (one-metric tolerance)
4. **Flag outlier samples**: Any sample with grade ≥ 2 levels below median sample grade → flag as potential outlier

## 5. QC Report Template

After QC assessment, produce a structured report:

```yaml
# QC Report — Phase 1
qc_report:
  domain: "{omics_type}"
  date: "{YYYY-MM-DD}"
  overall_grade: "{A/B/C/D/F}"
  
  per_sample_grades:
    - sample: "sample_1"
      grade: "A"
      metrics:
        total_reads: 35000000
        mapping_rate: 0.92
        # ... domain-specific metrics
    - sample: "sample_2"
      grade: "C"
      flagged: true
      flag_reason: "High mitochondrial percentage (18%)"
  
  summary:
    total_samples: N
    grade_distribution: { A: n, B: n, C: n, D: n, F: n }
    flagged_samples: ["sample_2"]
    
  recommendation: |
    Overall grade {X}. {Action recommendation based on Gate 1 logic}.
    
  preprocessing_needed:
    - "Remove adapter contamination (samples X, Y)"
    - "Filter cells with mito% > 15%"
```

## 6. Integration with Workflow

1. **Phase 1**: Run QC → apply grading → produce QC report → write to checkpoint
2. **Gate 1**: Use `overall_grade` to determine verdict (see §2)
3. **Phase 2**: Reference QC report when designing analysis parameters
4. **Checkpoint**: QC grade and report MUST be recorded in `phase-1-qc.yaml`

## 7. Red Flags — STOP

- Proceeding past Gate 1 with grade F data
- Upgrading a grade without justification
- Ignoring flagged outlier samples without user acknowledgment
- Running analysis without completing QC first
- Reporting a grade without showing the underlying metrics
