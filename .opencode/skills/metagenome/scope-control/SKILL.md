---
name: scope-control
description: "Use when analysis scope expansion is detected at any phase — enforces focus by quantifying risk and requiring explicit user approval before scope changes"
---

# Scope Control (Meta-Control Layer — Metagenome)

## Overview

A focused metagenomics study with 2–3 well-defined research questions beats a scattered study with 8 vague ones. This skill can trigger at **ANY phase** when scope expansion is detected.

**Core principle:** Focus is a feature. Scope creep is a bug.

> **[IRON-LAW]** Violating the letter of this rule is violating the spirit of this rule.

## Trigger Conditions

Any **ONE** of these activates this skill:

- Research questions exceed 3 distinct topics
- Analysis pipeline branches exceed what was locked in `analysis-protocol.yaml`
- User requests additional data types not in the original `project-anchor.yaml`
- Tool chain grows beyond what was validated in Phase 2 (analysis-design-validation)
- Downstream analysis adds unplanned comparisons (e.g., adding new group contrasts post-hoc)
- Sample subset selections proliferate (too many inclusion/exclusion criteria variants)
- "One more comparison" or "also run X" requests accumulate (≥ 3 unplanned additions)
- Timeline or compute budget is being exceeded

## The Mandatory Response

> **[HARD-GATE]** When triggered, the agent **MUST** execute all four steps in order.

```
1. WARN:     "Current scope may be too large for a coherent metagenomics study."
             List each unplanned addition that triggered this check.

2. QUANTIFY: "Current analysis plan has N research questions, M tool pipelines,
              P downstream comparisons. A focused study typically has 2-3 questions
              and one primary pipeline."
             OR: "Estimated compute time for all analyses: X hours. Budget: Y hours."

3. PROPOSE:  Reduction options, prioritized:
             a) Core research questions to KEEP (max 2-3)
             b) Analyses to DEFER to a follow-up study
             c) Analyses to CUT entirely
             d) Whether to split into two separate studies

4. PRESENT:  User decides. Agent CANNOT decide scope reduction on its own.
             Print: "⏸️ SCOPE DECISION REQUIRED — Please choose from the options above."

Skip any step = scope creep enabled = analysis quality at risk
```

## Metagenomics-Specific Scope Traps

| Trap | Example | Why It's Dangerous |
|------|---------|-------------------|
| Pipeline multiplication | "Run both DADA2 and Deblur, also add QIIME2 OTU" | Triples QC burden, makes results incomparable |
| Database sprawl | "Also annotate against CARD, VFDB, CAZy, and eggNOG" | Each database adds interpretation complexity; unfocused annotation dilutes the story |
| Contrast explosion | "Compare every group pair, also by timepoint, also by medication" | Multiple testing burden explodes; p-value corrections kill power |
| Data type creep | "Also incorporate the metabolomics data" | Multi-omics integration requires separate validation and is a study in itself |
| Taxonomy level shopping | "Show results at phylum, class, order, family, genus, AND species" | Most levels will show noise; pick the biologically relevant level |

## Rules

1. The agent proposes reductions but **never executes them** without user approval
2. Deferred analyses go into an explicit **"future-work.md"** log — they are not forgotten, just prioritized out
3. After user decides, update `analysis-protocol.yaml` and re-verify scope is within bounds
4. If a new scope item is approved, its QC requirements must also be defined (invoke `qc-standards`)

## Red Flags — STOP

- Adding a 4th major research question
- Pipeline tool count exceeding 8 distinct tools for a single data type
- More than 10 pairwise group comparisons
- "Just one more database" appearing more than twice
- Compute estimate exceeding budget by > 30%
- Story line requiring two separate introductions

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "We can fit all analyses in one report" | Unfocused reports confuse reviewers and bury key findings. |
| "Each extra analysis is quick to run" | Running is quick; interpreting, validating, and defending each result is not. |
| "We already have the data for it" | Having data ≠ having the statistical power, expertise, or time to analyze it properly. |
| "The reviewer might ask for it" | Anticipate likely requests, but don't preemptively run every possible analysis. |
| "It's just one more comparison" | Comparisons compound: 1 extra comparison × 5 taxonomy levels × 3 metrics = 15 more tests. |
| "Multi-omics integration would make it stronger" | Multi-omics integration done poorly is worse than single-omics done well. |

## The Bottom Line

```
More analyses ≠ better study
Focused questions + rigorous pipeline + complete validation = publishable results
```

Detect expansion. Quantify risk. Propose cuts. Let the user decide.
