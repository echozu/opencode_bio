---
name: host-decontamination
description: Use when processing any gut microbiome data — enforces systematic screening for host DNA contamination, kit contamination, and cross-sample contamination
---

# Contamination Check (Discipline Layer)

## Overview

Contamination is the silent killer of metagenome studies. Undetected contamination produces confidently wrong results that look biologically plausible. This skill enforces systematic contamination screening at multiple levels.

**Core principle:** Assume contamination until proven otherwise.

## The Iron Law

<IRON-LAW>
CONTAMINATION SCREENING IS MANDATORY FOR ALL GUT MICROBIOME DATA.

Three contamination types MUST be assessed:
1. Host DNA contamination
2. Kit/reagent contamination
3. Cross-sample contamination

"The data looks clean" is NOT a substitute for systematic screening.
Contamination that is not screened for is contamination that is not detected.
</IRON-LAW>

## Type 1: Host DNA Contamination

### Screening Protocol
1. Map reads against human reference genome (hg38/GRCh38)
2. Calculate % human reads per sample
3. Remove human reads before downstream analysis

### Tools
- **KneadData** (recommended — integrated with BioBakery)
- **Bowtie2** + human reference
- **BMTagger**

### Thresholds

| Human Read % | Status | Action |
|-------------|--------|--------|
| <1% | Clean | Proceed |
| 1-5% | Acceptable | Proceed with note |
| 5-20% | Warning | Flag; assess impact on depth |
| >20% | Critical | STOP; investigate extraction method |

### Common Causes
- Buccal cell contamination during oral sampling
- Intestinal epithelial cells in stool samples
- Poor DNA extraction protocol
- Sample handling without gloves

## Type 2: Kit/Reagent Contamination

### The Kitome Problem
DNA extraction kits and PCR reagents contain bacterial DNA that can be detected in sequencing data, especially in low-biomass samples.

### Known Kitome Organisms
Common kit contaminants (non-exhaustive — see Salter et al. 2014, BMC Biology):
- *Bradyrhizobium*
- *Methylobacterium*
- *Sphingomonas*
- *Ralstonia*
- *Pseudomonas*
- *Acinetobacter*
- *Propionibacterium*
- *Chryseobacterium*
- *Burkholderia*

### Screening Protocol
1. **Check for kitome organisms** — flag if present at >1% in any sample
2. **Negative controls** — if extraction blanks or PCR blanks were sequenced:
   - Identify taxa present in blanks
   - Assess their abundance in experimental samples
   - Consider removal using decontam (R package) or similar
3. **Depth correlation** — if contaminant abundance is inversely correlated with sequencing depth, it's likely contamination

### Tools
- **decontam** (R package) — statistical identification of contaminants
- **microDecon** — removal of contaminating sequences
- Manual checking against known kitome lists

## Type 3: Cross-Sample Contamination

### Screening Protocol
1. **Index/barcode hopping** — check for unexpected samples in demultiplexed data
2. **Shared rare taxa** — if very rare taxa appear across unrelated samples at similar low abundance, suspect cross-contamination
3. **Batch effects** — samples processed together sharing unexpected taxa

### Red Flags
- Same rare species appearing at ~0.1% in all samples from one sequencing run
- Mock community members appearing in non-mock samples
- Technical replicates showing different community compositions

## Contamination Assessment Report

```
Contamination Assessment:
═════════════════════════
Host DNA:
  Median human reads: [%]
  Range: [min%-max%]
  Samples exceeding 5%: [N]
  Action taken: [host removal tool + reference]

Kit contamination:
  Negative controls available: [yes/no]
  Known kitome organisms detected: [list with abundances]
  Decontam applied: [yes/no]
  Taxa removed: [list]

Cross-contamination:
  Index hopping evidence: [yes/no]
  Shared rare taxa pattern: [yes/no]
  Batch effect detected: [yes/no]

Overall contamination risk: [LOW / MODERATE / HIGH]
```

## Red Flags — STOP

- Not screening for host DNA in gut samples
- Ignoring known kitome organisms in results
- No negative controls available AND no contamination assessment
- Rare taxa appearing uniformly across all samples
- Oral bacteria dominating stool samples (swab contamination?)
- Environmental bacteria in all gut samples at similar proportions

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's gut microbiome, contamination is minimal" | Gut samples can have 5-30% human DNA. Screen it. |
| "We don't have negative controls" | Then use computational approaches (decontam, kitome lists). |
| "Kitome organisms are present at low abundance" | Low abundance contaminants can become "significant" in differential analysis. |
| "Cross-contamination is unlikely with modern barcoding" | Index hopping is well-documented. Check for it. |
| "Contamination screening takes too long" | Finding contamination after analysis takes longer. Screen now. |
| "The DNA extraction kit is high quality" | All kits have contaminants. Quality of kit ≠ absence of contamination. |

## The Bottom Line

```
Unscreened contamination → Undetected contamination → Confidently wrong results
```

Screen systematically. Document findings. Let the user decide on borderline cases.
