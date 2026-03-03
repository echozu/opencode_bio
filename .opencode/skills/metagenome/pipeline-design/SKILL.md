---
name: pipeline-design
description: Use when Phase 2 (analysis-design-validation) is complete — locks all pipeline parameters, database versions, and thresholds into analysis-protocol.yaml, produces the G2 gate checklist before execution begins
---

<HARD-GATE>
Do NOT begin pipeline execution until ALL parameters are locked in analysis-protocol.yaml and G2 gate checklist is fully satisfied with user approval.
</HARD-GATE>

# Pipeline Design (Phase 3)

## Overview

Validated analysis design (Phase 2) defines WHAT to analyze. This skill defines exactly HOW — locking every parameter, database version, threshold, and tool configuration into an immutable protocol. After G2, changes require explicit user authorization.

**Core principle:** Locked means locked. No silent modifications.

## Step 1: Parameter Specification

For each step in the analysis pipeline, specify EVERY parameter. No "default" values without explicit documentation.

### QC Parameters
- Exact tool and version (e.g., fastp 0.23.4)
- Quality threshold (e.g., Q20)
- Minimum read length (e.g., 150bp)
- Adapter sequences or auto-detect mode
- Host removal reference genome and tool (if applicable)

### Analysis-Type-Specific Parameters

**Type A (Amplicon):**
- DADA2 truncation lengths (forward and reverse) — MUST be based on quality profiles, not defaults
- Maximum expected errors
- Chimera detection method
- Taxonomy classifier and database version
- Classification confidence threshold

**Type M (Assembly):**
- Assembler and version
- Minimum contig length
- Gene prediction tool and parameters
- Binning tool and refinement strategy
- Annotation databases and versions

**Type R (Read-Based):**
- MetaPhlAn version and database
- HUMAnN version, nucleotide database, protein database
- Minimum alignment quality

### Downstream Parameters
- Alpha diversity metrics list
- Beta diversity metrics and distance method
- Rarefaction depth (with justification)
- Differential abundance tool, significance threshold, multiple testing correction
- Network analysis parameters (correlation method, prevalence filter)

## Step 2: Multi-Agent Pipeline Review

<IRON-LAW>
Pipeline parameters MUST be reviewed by 3 agents before locking. Poorly chosen parameters waste the entire project.
</IRON-LAW>

Dispatch three agents (max 5 rounds) following `multi-round-deliberation` protocol:

| Agent | Role | Focus |
|-------|------|-------|
| **Analysis Design Advisor** | Design perspective | Are the parameter choices appropriate for the biological question? |
| **Technical Implementation Expert** | Technical perspective | Are the parameters technically optimal for this data? |
| **Reproducibility Advocate** | Standards perspective | Can these parameters be exactly reproduced? Are versions pinned? |

Each agent reviews the complete `analysis-protocol.yaml` draft.

## Step 3: Generate analysis-protocol.yaml

Write `docs/03_plan/analysis-protocol.yaml` using the template at `templates/analysis-protocol.yaml`. Fill ALL fields relevant to the data type. Leave irrelevant sections empty (e.g., amplicon_parameters for Type R).

<IRON-LAW>
Every parameter must have a JUSTIFICATION — not just a value. Document WHY each parameter was chosen:

```yaml
# Example — DO NOT just write values without rationale
qc_parameters:
  min_quality: 20  # Based on per-base quality drop at position 230 in FastQC
  min_length: 150  # Matches V3-V4 expected amplicon length minus primers
```

Parameters without justification are NOT locked — they are guesses.
</IRON-LAW>

## Step 4: Database Version Pinning

<IRON-LAW>
ALL reference databases MUST be pinned to exact versions. Database updates between analysis runs can change results silently.

Document in analysis-protocol.yaml:
- Database name and version (e.g., SILVA 138.1, GTDB r220)
- Download date
- Download URL or source
- MD5 checksum if available
</IRON-LAW>

## G2 Gate Checklist — Pipeline Freeze

ALL items must be satisfied before proceeding:

- [ ] All QC parameters specified with justification
- [ ] Analysis-type-specific parameters specified with justification
- [ ] All downstream analysis parameters specified
- [ ] All tool versions pinned (no "latest" or version ranges)
- [ ] All database versions pinned with download source
- [ ] analysis-protocol.yaml generated and complete
- [ ] Multi-agent pipeline review completed — all agents PASS
- [ ] Visualization standards defined (color palette, figure format)
- [ ] Resource requirements confirmed (compute time, memory, storage)
- [ ] Rarefaction depth justified (not just "standard" value)
- [ ] Multiple testing correction method specified
- [ ] Confounder variables listed for differential analysis

Present to user for sign-off.

<IRON-LAW>
## ⛔ MANDATORY STOP

After presenting the G2 gate checklist and frozen analysis-protocol.yaml, **END YOUR RESPONSE IMMEDIATELY.**

Do NOT invoke any execution skill or begin running pipelines in this same response.

**STOP. WAIT. The user must confirm the G2 gate before you proceed.**

Your final output should be the frozen protocol summary + G2 checklist followed by:
"G2 gate: Pipeline parameters frozen. Please review and confirm. Once approved, I'll begin Phase 4 (Pipeline Execution)."
"G2门禁：流程参数已冻结。请审核确认。确认后，我将开始第4阶段（流程执行）。"

Then STOP.
</IRON-LAW>

## Post-Lock Change Process

After G2 is passed, the protocol is IMMUTABLE. If a change is needed:

```
IF you believe a locked parameter must change:

1. EXPLAIN: What exactly needs to change?
2. JUSTIFY: Why is the current value flawed?
3. PROVE: Show evidence the locked value is defective (not just suboptimal)
4. WAIT: User decides — not you
5. LOG: Record old value, new value, reason in change_log

Skip any step = unauthorized modification = results invalidation
```

## Red Flags — STOP

- Using "default" parameters without data-specific justification
- Not pinning database versions
- Skipping the multi-agent review
- Setting rarefaction depth without checking minimum sample depth
- Using different QC parameters for different samples without justification
- Changing parameters after G2 without user authorization

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Default parameters are fine" | Default for WHOSE data? Justify for THIS dataset. |
| "The database version doesn't matter" | Database updates change taxonomy assignments. Pin the version. |
| "Rarefaction to 10,000 is standard" | Standard is irrelevant if your lowest sample has 5,000 reads. Check. |
| "We can adjust parameters during execution" | After G2, parameters are LOCKED. Adjustments need user approval. |
| "These parameters worked for another study" | Different study, different data, different parameters. Justify fresh. |
| "Version pinning is overkill" | Version drift causes irreproducible results. Pin everything. |
