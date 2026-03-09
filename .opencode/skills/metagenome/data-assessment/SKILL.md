---
name: data-assessment
description: Use when Phase 0 (project-anchoring) is complete — performs QC profiling, validates data quality, selects appropriate tools, and produces the G1 gate checklist before analysis design begins
---

<HARD-GATE>
Do NOT proceed to analysis design until data quality has been assessed, tool chain has been selected, and G1 gate checklist is fully satisfied with user approval.
</HARD-GATE>

# Data Assessment (Phase 1)

## Overview

Raw sequencing data quality determines the ceiling of all downstream analyses. This skill profiles the data, identifies quality issues, selects appropriate tools, and ensures the data meets minimum thresholds before any analysis design begins.

## Step 1: Data Inventory

Verify and document all input data:

1. **List all FASTQ files** — count, naming convention, paired-end verification
2. **Check file integrity** — md5sum verification if provided
3. **Match to metadata** — every sample in metadata has corresponding FASTQ files (and vice versa)
4. **Record sequencing depth** — total reads per sample

```
Data Inventory Report:
═══════════════════════
Total files: [N] (expected: [M])
Paired-end verified: [yes/no]
Samples matched to metadata: [N/M]
Missing files: [list or "none"]
Depth range: [min]-[max] reads/sample
Median depth: [value] reads/sample
```

<IRON-LAW>
If ANY sample has fewer than 1,000 reads (amplicon) or 100,000 reads (shotgun), FLAG IT immediately. Low-depth samples can skew ALL downstream analyses.

Do NOT silently exclude low-depth samples. Present the issue to the user and let them decide: exclude, re-sequence, or proceed with warning.
</IRON-LAW>

## Step 2: Quality Profiling

Run or plan quality assessment based on data type:

### For All Types
- **FastQC** per-sample quality profiles
- **MultiQC** aggregated report
- Key metrics to check:
  - Per-base quality scores (should be ≥Q20 for most positions)
  - Adapter content (should be <5% or removed)
  - Sequence duplication levels
  - GC content distribution (unexpected peaks suggest contamination)
  - Sequence length distribution

### Additional for Amplicon (Type A)
- **Primer presence check** — are primer sequences still attached?
- **Amplicon length distribution** — matches expected target region?
- **Chimera rate estimation** (done during DADA2 denoising)

### Additional for Shotgun (Type M/R)
- **Host DNA proportion** — estimate % human reads (critical for gut samples)
- **PhiX contamination** — common Illumina spike-in
- **Sequencing depth adequacy** — sufficient for assembly (>5Gb) or profiling (>1Gb)?

## Step 3: Contamination Screening

<IRON-LAW>
Contamination screening is NEVER optional for gut microbiome data.

Three contamination types MUST be assessed:
1. **Host DNA contamination** — human DNA proportion (should be <10% after removal)
2. **Kit contamination** — reagent-associated taxa (especially in low-biomass samples)
3. **Cross-sample contamination** — barcode hopping, index switching

Invoke the `host-decontamination` skill for detailed protocols.
</IRON-LAW>

## Step 4: Tool Chain Selection

Based on data type, quality profile, and analysis goals, recommend the appropriate tool chain:

### Type A (Amplicon) — Standard Pipeline
```
Raw FASTQ → [fastp/cutadapt] → QC reads → [DADA2] → ASV table
  → [SILVA/Greengenes2] → Taxonomy → [PICRUSt2] → Functional prediction
  → Downstream: diversity, differential, network
```

### Type M (Assembly-Based Metagenome) — Assembly Pipeline
```
Raw FASTQ → [KneadData/fastp] → QC + host removal
  → [MEGAHIT/metaSPAdes] → Contigs → [Prodigal] → Gene catalog
  → [MetaBAT2] → MAGs → [eggNOG/KEGG] → Functional annotation
  → Downstream: diversity, differential, network
```

### Type R (Read-Based Metagenome) — BioBakery Pipeline
```
Raw FASTQ → [KneadData] → QC + host removal
  → [MetaPhlAn3/4] → Taxonomic profiles
  → [HUMAnN3] → Functional profiles (gene families, pathways)
  → Downstream: diversity, differential, enrichment
```

### Type C (Combined)
```
Amplicon pipeline (Type A) + Shotgun pipeline (Type M or R)
  → Cross-validation: taxonomy concordance check
  → Integrated analysis
```

Present tool recommendations with version numbers and rationale.

## Step 5: Multi-Agent Data Assessment Review

<IRON-LAW>
Data assessment MUST include a 3-agent review before proceeding. The agents evaluate whether data quality is sufficient and tool chain is appropriate.
</IRON-LAW>

Dispatch three agents (max 5 rounds) following `multi-round-deliberation` protocol:

| Agent | Role | Focus |
|-------|------|-------|
| **Gut Microbiome Scientist** | Domain expert | Is the data adequate for the stated analysis goals? |
| **Bioinformatics Tool Expert** | Pipeline expert | Is the tool chain optimal for this data type and quality? |
| **Data Quality Auditor** | QC specialist | Are there quality issues that could invalidate results? |

Present deliberation results and any concerns to the user.

## G1 Gate Checklist — Data & Path Confirmed

ALL items must be satisfied before proceeding:

- [ ] Data inventory complete — all files accounted for, paired-end verified
- [ ] Quality profiling done — FastQC/MultiQC summary available
- [ ] Minimum quality thresholds met (or low-quality samples flagged and user-approved handling)
- [ ] Contamination screening planned or completed
- [ ] Sequencing depth adequate for planned analyses
- [ ] Tool chain selected with version numbers
- [ ] Data type confirmed (A/M/R/C)
- [ ] Analysis path confirmed (which downstream analyses to run)
- [ ] Multi-agent review completed with no unresolved FAIL verdicts
- [ ] Resource requirements estimated (disk, RAM, CPU time)

Present to user for sign-off.

<IRON-LAW>
## ⛔ MANDATORY STOP

After presenting the G1 gate checklist, **END YOUR RESPONSE IMMEDIATELY.**

Do NOT invoke `analysis-design-validation` or any other skill in this same response.
Do NOT begin designing the analysis plan.

**STOP. WAIT. The user must confirm the G1 gate before you proceed.**

Your final output should be the G1 checklist followed by:
"G1 gate checklist presented. Please review and confirm. Once approved, I'll begin Phase 2 (Analysis Design Validation)."
"G1门禁检查清单已呈现。请审核确认。确认后，我将开始第2阶段（分析设计验证）。"

Then STOP.
</IRON-LAW>

## Red Flags — STOP

- Skipping quality profiling "because the data looks fine"
- Ignoring low-depth samples without flagging
- Not checking for host DNA contamination in gut samples
- Selecting tools without checking version compatibility
- Proceeding to analysis design with unresolved data quality issues
- Using default parameters without considering data characteristics

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "QC looks fine at a glance" | Glance ≠ verified. Run FastQC/MultiQC. Check adapter content. |
| "Host contamination won't matter" | 50% host reads means 50% wasted sequencing. It ALWAYS matters for gut. |
| "Standard depth is sufficient" | Standard for WHAT analysis? Check depth requirements per analysis type. |
| "I'll check contamination later" | Contamination invalidates everything downstream. Check NOW. |
| "These tools are the standard" | Standard tools still need version pinning and parameter justification. |
| "MultiQC is overkill for small studies" | Small studies need QC MORE, not less — each sample matters more. |
