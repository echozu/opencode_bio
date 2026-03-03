---
name: results-verification
description: Use when making any claim about analysis results — enforces domain sanity checking, biological plausibility verification, and evidence-based status reporting
---

# Results Verification (Discipline Layer)

## Overview

AI agents can produce technically correct but biologically nonsensical results without noticing. This skill enforces systematic domain sanity checking before any result is reported or claim is made.

**Core principle:** Fresh evidence required before any status claim. Results must make biological sense.

## The Iron Law

<IRON-LAW>
BEFORE REPORTING ANY RESULT AS A FINDING:
1. Check biological plausibility — does it make sense given gut microbiome biology?
2. Compare against known ranges — are the values within expected bounds?
3. Verify internal consistency — do different analyses tell the same story?
4. Check for artifacts — could this be a technical artifact rather than biology?

"The analysis ran successfully" ≠ "The results are correct."
A pipeline that runs without errors can still produce wrong results.
</IRON-LAW>

## Domain Sanity Checks for Gut Microbiome

### Taxonomic Composition Checks

| Check | Expected Range | Red Flag |
|-------|---------------|----------|
| Top phyla (human gut) | Firmicutes (30-70%), Bacteroidetes (20-50%), Proteobacteria (<10%), Actinobacteria (<10%) | Proteobacteria >30% OR Cyanobacteria >1% OR Archaea >10% |
| Shannon diversity | 2.0-5.0 for healthy gut | <1.0 or >7.0 |
| Dominant species | No single species >30% in healthy adult gut | Single species >80% (except infants) |
| Total detected species | 50-500 (amplicon), 100-1000 (shotgun) | <10 or >5000 |
| Phylum:genus ratio | Multiple genera per phylum | Single genus per phylum |

### Diversity Checks

| Check | Expected | Red Flag |
|-------|----------|----------|
| Alpha diversity in disease vs control | Often reduced in disease | HIGHER in disease than control (verify — unusual but possible) |
| Beta diversity R² | 0.05-0.30 typical for gut studies | R² >0.50 (too clean for microbiome) OR R² <0.01 (no signal) |
| Betadisper | Should be NS for valid PERMANOVA | Significant betadisper → PERMANOVA ambiguous |
| Rarefaction curves | Should plateau | Not plateauing → insufficient depth |

### Differential Abundance Checks

| Check | Expected | Red Flag |
|-------|----------|----------|
| Number of significant features | 5-100 typical | 0 (underpowered?) or >1000 (no correction?) |
| Effect sizes | log2FC 0.5-3 typical | log2FC >10 (artifact?) |
| Direction consistency | Biological coherence | Random directions with no pattern |
| Known associations | Confirm known markers | Known markers missing or reversed |

### Functional Profiling Checks

| Check | Expected | Red Flag |
|-------|----------|----------|
| Core metabolic pathways | Always present | Missing basic metabolism |
| SCFA genes | Present in gut samples | Absent in healthy gut samples |
| Antibiotic resistance | Low baseline in healthy | Very high in healthy controls |
| PICRUSt2 NSTI | <2.0 for gut bacteria | >2.0 (unreliable predictions) |

## Artifact Detection

Common artifacts in metagenome analysis:

| Artifact | How to Detect | Cause |
|----------|--------------|-------|
| Batch effect | PCoA clusters by batch, not biology | Different extraction dates/kits |
| Depth artifact | Results correlate with sequencing depth | Insufficient rarefaction/normalization |
| Compositional artifact | All correlations positive in network | Not using compositional-aware methods |
| Database artifact | Many "unclassified" in specific clades | Database version mismatch |
| Chimeric ASVs | ASVs matching multiple genera | Insufficient chimera filtering |

## Verification Protocol

When any result is produced:

```
1. BIOLOGICAL PLAUSIBILITY
   "Would a gut microbiome expert look at this and say 'that makes sense'?"
   If NO → investigate before reporting

2. KNOWN RANGE CHECK
   "Are the key values within expected ranges from the literature?"
   If NO → investigate. Could be novel OR could be artifact.

3. INTERNAL CONSISTENCY
   "Do different analyses support the same biological story?"
   If NO → investigate discrepancies before reporting

4. ARTIFACT SCREEN
   "Could this result be explained by a technical artifact?"
   If YES → rule out the artifact with additional checks
```

## Red Flags — STOP

- Reporting results without biological plausibility check
- Values dramatically outside known ranges without investigation
- Different analyses contradicting each other without explanation
- "The pipeline ran successfully" as evidence of correct results
- Presenting all findings as equally reliable without quality assessment
- Not checking for batch effects

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The statistics are significant, so it's real" | Significant artifacts are still artifacts. Check biology. |
| "The pipeline is well-tested" | Well-tested tools can still produce wrong results with wrong parameters. |
| "These are just preliminary results" | Preliminary results that are wrong become wrong final results. Check now. |
| "I don't recognize this taxon, it might be novel" | Novel taxon OR database error OR contamination. Investigate. |
| "The effect size is very large, must be important" | Very large effects in metagenomics are often artifacts. Verify. |
| "Results differ between methods because methods differ" | Methods should agree on strong signals. Disagreement = investigate. |

## The Bottom Line

```
"The analysis completed successfully" ≠ "The results are correct"
Verify biology. Check ranges. Screen artifacts. Then report.
```
