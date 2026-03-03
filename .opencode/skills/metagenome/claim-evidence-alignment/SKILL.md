---
name: claim-evidence-alignment
description: Use when integrating results (Phase 5) or writing report (Phase 6) — enforces that every claim maps to specific evidence and every piece of evidence is correctly interpreted
---

# Claim-Evidence Alignment (Discipline Layer)

## Overview

Every claim in the report must be traceable to a specific figure, table, or statistical test. Claims without evidence are speculation. Evidence without claims is wasted analysis.

**Core principle:** No claim without evidence. No evidence without a claim.

## The Iron Law

<IRON-LAW>
BUILD THE FULL CLAIM-EVIDENCE MAPPING TABLE BEFORE WRITING ANY REPORT SECTION.

For EACH intended claim:
1. What SPECIFIC evidence supports it? (figure number, table number, p-value, effect size)
2. Is the evidence SUFFICIENT for the strength of the claim?
3. Are there ALTERNATIVE explanations the evidence doesn't rule out?

Claims that cannot be mapped to evidence are DELETED. No exceptions.
</IRON-LAW>

## Claim-Evidence Map Format

Save to `docs/05_integration/claim-evidence-map.md`:

| # | Claim | Evidence Type | Source File | Statistical Support | Strength | Alternatives Ruled Out |
|---|-------|-------------|------------|-------------------|----------|----------------------|
| 1 | "[specific biological claim]" | Figure 1 + Table 1 | results/diversity/alpha.tsv | p=0.003, FDR<0.05, Kruskal-Wallis | Strong | Batch effect (betadisper NS) |
| 2 | "[specific claim]" | Table 2 | results/differential/deseq2.tsv | padj<0.05, log2FC>1, 15 taxa | Moderate | Confounders not fully controlled |

## Claim Strength Categories

| Strength | Criteria | Language to Use |
|----------|---------|----------------|
| **Strong** | Multiple lines of evidence, significant statistics, confounders controlled | "demonstrated", "showed", "revealed" |
| **Moderate** | Single line of evidence, significant but without validation | "indicated", "suggested", "was associated with" |
| **Weak** | Borderline significance, small effect size, or observational only | "may", "appeared to", "trends toward" |
| **Unsupported** | No matching evidence | DELETE THE CLAIM |

## Common Alignment Failures in Metagenome Studies

| Claim Pattern | Evidence Required | Common Gap |
|--------------|------------------|------------|
| "Diversity was reduced in disease" | Alpha diversity stats + rarefaction curves | Missing p-value or effect size |
| "Community composition differed" | PERMANOVA + betadisper + PCoA | Missing betadisper (dispersion check) |
| "Taxa X was enriched" | Differential abundance with correction | Missing multiple testing correction |
| "Functional pathway Y was altered" | HUMAnN/PICRUSt2 results + statistics | Pathway presence ≠ pathway enrichment |
| "Microbiome-host interaction" | Correlation + mechanism evidence | Correlation ≠ causation caveat missing |

## Red Flags — STOP

- Claims in the report that don't appear in the mapping table
- Evidence cited that doesn't match the claim
- "Significant" without p-value or effect size
- Causal language for observational data
- Claims based on visual inspection of figures without statistics

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The trend is clear from the figure" | Trends require statistical support. Visual ≠ verified. |
| "It's well-known that diversity is reduced in IBD" | Known or not, YOUR data must support YOUR claim. |
| "The p-value is 0.06, close enough" | 0.06 is not significant. Report as "trending" with appropriate language. |
| "Multiple testing correction is too conservative" | Correction prevents false discoveries. Use it. |
| "This claim doesn't need evidence, it's background" | Background claims need citations. Analytical claims need evidence. |
| "The evidence is in the supplementary" | If the claim is in the main text, the evidence reference must be there too. |

## The Bottom Line

```
Claim without evidence = speculation → delete
Evidence without claim = wasted work → add claim or remove
Claim stronger than evidence = over-reach → weaken claim
```
