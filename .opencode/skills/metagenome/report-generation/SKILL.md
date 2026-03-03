---
name: report-generation
description: Use when G4 (report-ready) gate has passed and user explicitly says "ready for report" — generates a comprehensive analysis report with per-section multi-agent polishing
---

<HARD-GATE>
Do NOT begin report generation without:
1. G4 gate passed with explicit user approval
2. Argument blueprint finalized in docs/05_integration/argument-blueprint.md
3. Claim-evidence map complete in docs/05_integration/claim-evidence-map.md
4. User explicitly said "ready for report" or equivalent
</HARD-GATE>

# Report Generation (Phase 6)

## Overview

This skill generates a comprehensive analysis report section by section, with multi-agent polishing for each section and a full-report review. The argument blueprint from Phase 5 is the DEFINITIVE guide — Phase 6 EXECUTES the story, it does not reinvent it.

<IRON-LAW>
Phase 6 is EXECUTION of the Phase 5 story design. If you find yourself redesigning the story during writing, STOP — you should be back in Phase 5.
</IRON-LAW>

## Step 1: Report Structure

Standard gut metagenome analysis report structure:

```
1. Executive Summary / Abstract
   - Study overview, key findings, significance

2. Introduction
   - Background on gut microbiome in [context]
   - Current knowledge and gaps
   - Study objectives

3. Materials and Methods
   - Study design and sample collection
   - Sequencing and quality control
   - Bioinformatics pipeline (tools, versions, parameters)
   - Statistical analysis methods

4. Results
   - 4.1 Data Quality and Sample Characteristics
   - 4.2 Taxonomic Composition
   - 4.3 Diversity Analysis
   - 4.4 Differential Abundance
   - 4.5 Functional Profiling
   - 4.6 Network/Interaction Analysis (if applicable)
   - 4.7 Specialized Functional Analysis (if applicable)

5. Discussion
   - Key findings in context of existing literature
   - Biological/clinical implications
   - Comparison with previous studies
   - Limitations
   - Future directions

6. Conclusions

7. Supplementary Materials
   - Complete taxonomy tables
   - All statistical results
   - Pipeline commands for reproducibility
```

## Step 2: Per-Section Writing

For each section, follow this process:

### 2a. Draft the section
- Follow the argument blueprint content points
- Every claim must reference the claim-evidence map
- Use precise language — quantify everything
- Include figure/table references inline

### 2b. Per-Section Multi-Agent Polishing (3 agents × max 5 rounds)

Dispatch three agents for each major section:

| Agent | Template | Focus |
|-------|----------|-------|
| Domain Expert | `domain-expert-prompt.md` | Biological accuracy, completeness, literature context |
| Writing Editor | `writing-editor-prompt.md` | Clarity, structure, scientific writing standards |
| Adversarial Reviewer | `adversarial-reviewer-prompt.md` | Claim over-reach, missing caveats, reviewer objections |

**Follow `multi-round-deliberation` protocol:** Each round, all 3 agents review the COMPLETE section. Modify based on feedback. Re-dispatch ALL agents. Continue until convergence or max 5 rounds.

### 2c. Present section to user

After each section's polishing converges:

```
Section [X]: [Title]
═══════════════════
[The polished section content]

Agent review: Domain Expert [PASS], Editor [PASS], Reviewer [PASS]
Rounds required: [N]

Please review. Feedback or proceed to next section?
```

<IRON-LAW>
Present EACH SECTION individually and wait for user feedback. Do NOT write all sections in one response.

This ensures the user has control over the narrative and can redirect early.
</IRON-LAW>

## Step 3: Full-Report Review

After ALL sections are individually approved, dispatch a full-report review:

| Agent | Focus |
|-------|-------|
| Domain Expert | Cross-section consistency, complete story arc |
| Writing Editor | Flow, transitions, formatting, reference consistency |
| Adversarial Reviewer | "If I were Reviewer #2, what would I reject?" |

Max 5 rounds on the full report.

## Step 4: Methods Section — Reproducibility Standard

The Methods section MUST include:
- Exact tool names and versions
- Exact database names and versions
- All key parameters with justification
- Statistical methods with test names and thresholds
- Data availability statement
- Code/pipeline availability statement

<IRON-LAW>
The Methods section must be detailed enough for an independent researcher to EXACTLY reproduce the analysis. "Standard protocols were used" is NEVER acceptable.
</IRON-LAW>

## Step 5: Final Deliverables

```
Report Generation Complete:
═══════════════════════════
Sections written: [N]
Total figures: [N]
Total tables: [N]
Per-section reviews: all PASS
Full-report review: [PASS/issues]

Output files:
  - docs/06_report/analysis-report.md
  - docs/06_report/methods-section.md
  - docs/06_report/supplementary/
  - results/figures/ (publication-ready)

The report is ready for final review.
```

## Red Flags — STOP

- Writing without following the argument blueprint
- Claims not in the claim-evidence map appearing in the report
- Methods section with "default parameters" or missing versions
- Skipping per-section review
- All sections written in one response
- Discussion that doesn't acknowledge limitations

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I can write all sections at once" | One section per turn. Quality requires focused review. |
| "The methods are obvious" | Write them explicitly. Reviewers check methods first. |
| "Limitations weaken the paper" | Honest limitations STRENGTHEN the paper. Reviewers respect transparency. |
| "The argument blueprint is just a guide" | The blueprint is the DEFINITIVE plan. Execute it. |
| "Per-section review takes too long" | Per-section review catches issues cheaply. Full rewrites are expensive. |
| "Standard phrases are fine" | Precise, specific language beats generic scientific writing. |
