---
name: functional-annotation
description: Use when functional gene mining is needed — provides specialized analysis for specific functional categories including short-chain fatty acids (SCFAs), bile acid metabolism, antibiotic resistance, and other gut-relevant functions
---

<HARD-GATE>
Do NOT execute functional annotation without:
1. Primary taxonomic and/or functional profiling complete
2. Parameters locked in analysis-protocol.yaml
3. Relevant databases available and version-pinned
</HARD-GATE>

# Functional Annotation (Phase 4 Sub-Skill)

## Overview

Specialized functional gene mining beyond standard pathway profiling. Targets gut-specific functional categories that are biologically and clinically relevant. This skill complements the general functional profiling from `metagenome-readbased` or `metagenome-assembly`.

## Functional Category 1: Short-Chain Fatty Acid (SCFA) Production

Key genes and pathways for butyrate, propionate, and acetate production:

| SCFA | Key Genes | Pathway |
|------|-----------|---------|
| Butyrate | but, buk, bcd, crt | Acetyl-CoA → Butyryl-CoA → Butyrate |
| Propionate | mmdA, lcdA, pct | Succinate → Propionate (succinate pathway) |
| Acetate | pta, ackA | Acetyl-CoA → Acetate |

**Analysis:**
1. Search gene catalog or HUMAnN output for SCFA-related genes
2. Quantify abundance per sample
3. Correlate with taxa known to produce SCFAs (Faecalibacterium, Roseburia, etc.)
4. Compare between groups

## Functional Category 2: Bile Acid Metabolism

Key genes for bile acid biotransformation:

| Function | Key Genes | Organisms |
|----------|-----------|-----------|
| Deconjugation | bsh (bile salt hydrolase) | Lactobacillus, Bifidobacterium, Clostridium |
| 7α-dehydroxylation | baiCD, baiE, baiH | Clostridium scindens, C. hylemonae |
| Oxidation/epimerization | hsdh genes | Various Firmicutes |

## Functional Category 3: Antibiotic Resistance Genes (ARGs)

Databases and tools:
- **CARD (Comprehensive Antibiotic Resistance Database)** — curated reference
- **ResFinder** — acquired resistance genes
- **AMRFinderPlus** — NCBI resistance gene finder

**Analysis:**
1. Screen gene catalog or reads against resistance gene databases
2. Classify by resistance mechanism and drug class
3. Quantify ARG abundance (RPKM or TPM)
4. Identify host organisms carrying ARGs (if MAGs available)

## Functional Category 4: Carbohydrate-Active Enzymes (CAZymes)

Use **dbCAN** or **CAZy database** for annotation:
- Glycoside hydrolases (GH)
- Glycosyltransferases (GT)
- Polysaccharide lyases (PL)
- Carbohydrate esterases (CE)
- Carbohydrate-binding modules (CBM)

Relevant for diet-microbiome interaction studies.

## Functional Category 5: Virulence Factors

Databases:
- **VFDB (Virulence Factor Database)**
- **Pathogen-Host Interaction database (PHI-base)**

Screen for known virulence factors, especially in pathobiont species.

## Functional Category 6: Neurotransmitter Metabolism (Gut-Brain Axis)

Key metabolites and genes:
- **GABA**: gadB (glutamate decarboxylase)
- **Serotonin**: tnaA (tryptophanase), biosynthesis genes
- **Dopamine**: tyramine biosynthesis
- **Histamine**: hdcA (histidine decarboxylase)

## Integration with Primary Results

After functional mining:
1. Correlate functional gene abundance with taxonomic composition
2. Link functional findings to clinical metadata
3. Generate species-function association heatmaps
4. Identify keystone species (high functional contribution)

## Domain Sanity Check

- [ ] Known SCFA producers (Faecalibacterium, Roseburia) carry expected SCFA genes
- [ ] ARG abundance is within expected range for gut samples (higher in antibiotic-exposed)
- [ ] CAZyme profiles reflect expected dietary substrates
- [ ] Functional annotations are consistent across biological replicates

## Red Flags — STOP

- ARG abundance dramatically higher in controls than disease (check for batch effect)
- SCFA genes absent in samples dominated by known SCFA producers (database issue?)
- Virulence factors detected in commensal organisms only (false positives?)
- Functional gene abundance not correlated with any taxonomic feature

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Standard pathway analysis is sufficient" | Specific functional categories provide deeper biological insight. |
| "ARG screening isn't relevant for this study" | If it's a clinical gut study, ARGs are ALWAYS relevant. |
| "CAZyme annotation is too specialized" | CAZymes are central to gut microbiome function. Include if diet is a variable. |
| "We don't need gene-level analysis" | Pathway-level averages hide important variation. Gene-level adds resolution. |
| "Species-function correlation is obvious" | Nothing is obvious until quantified. Correlate and report. |
