---
name: shotgun-readbased
description: Use when data type is R (Metagenome-ReadBased) and pipeline execution is in progress — provides step-by-step read-based metagenome workflow using MetaPhlAn and HUMAnN for taxonomic and functional profiling
---

<HARD-GATE>
Do NOT execute read-based metagenome analysis without:
1. G2 gate passed (analysis-protocol.yaml locked)
2. Data type confirmed as R in project-anchor.yaml
3. Host-removed, QC-validated reads available
</HARD-GATE>

# Read-Based Metagenome Analysis (Type R — Phase 4 Sub-Skill)

## Overview

Read-based metagenome analysis (BioBakery workflow): host-removed reads → MetaPhlAn3/4 taxonomic profiling → HUMAnN3 functional profiling → pathway/gene family abundance. All parameters from locked `analysis-protocol.yaml`.

## Pipeline Steps

### Step 1: Verify Input Data
- Confirm host DNA removal completed
- Verify sufficient depth for profiling (recommended: >1Gb per sample for MetaPhlAn, >5Gb for HUMAnN)
- Check paired-end integrity

### Step 2: Taxonomic Profiling (MetaPhlAn3/4)
Execute with LOCKED parameters:
```
tool: [from protocol]  # MetaPhlAn3 or MetaPhlAn4
version: [from protocol]
database: [from protocol]  # e.g., mpa_vJun23_CHOCOPhlAnSGB_202307
```

**Outputs:**
- Species-level relative abundance table (samples × species)
- Genus/family/phylum-level aggregated tables
- Per-sample profiling statistics (mapped reads, unmapped fraction)

<IRON-LAW>
Check profiling statistics BEFORE proceeding:
- If >80% reads unmapped → sample may have high host contamination or unusual community
- If <50 species detected across all samples → may indicate database limitation or very low diversity
- If one species >50% relative abundance in most samples → verify this is biologically expected

Do NOT proceed with poor profiling results without investigation.
</IRON-LAW>

### Step 3: Functional Profiling (HUMAnN3)
Execute with LOCKED parameters:
```
tool: HUMAnN3
version: [from protocol]
nucleotide_db: [from protocol]  # ChocoPhlAn
protein_db: [from protocol]  # UniRef90
pathway_db: [from protocol]  # MetaCyc
```

**Outputs:**
- Gene family abundance table (RPK — reads per kilobase)
- Pathway abundance table (RPK)
- Pathway coverage table (proportion of pathway detected)
- Species-stratified contributions (which species contribute to which pathways)

<IRON-LAW>
HUMAnN3 quality checks:
- If total gene family mapping <40% → flag insufficient database coverage
- If pathway coverage <0.5 for most pathways → flag incomplete pathway detection
- Species-stratified results are critical for biological interpretation — do not skip

These checks prevent reporting functions that aren't actually present.
</IRON-LAW>

### Step 4: Normalization and Aggregation
- Normalize gene families to CPM (copies per million)
- Normalize pathways to RPK then CPM
- Aggregate by taxonomic level if needed
- Unstratify tables for community-level analysis
- Keep stratified tables for species-contribution analysis

### Step 5: Quality Metrics Summary
Generate a comprehensive profiling quality report:

```
Read-Based Profiling Summary:
═════════════════════════════
Samples profiled: [N]
Median species detected: [N] (range: [min]-[max])
Median reads mapped (MetaPhlAn): [N]% (range: [min]-[max]%)
Median gene families detected: [N]
Median pathways detected: [N]
HUMAnN mapping rate: [N]% (nucleotide + translated)
```

### Step 6: Generate Analysis-Ready Outputs
Save all outputs:
- `results/taxonomy/` — MetaPhlAn abundance tables
- `results/functional/` — HUMAnN gene family and pathway tables
- `results/functional/stratified/` — species-stratified functional tables

## Domain Sanity Check

- [ ] Top species are expected gut commensals (Bacteroides, Faecalibacterium, Prevotella, etc.)
- [ ] Functional profiles show expected gut pathways (carbohydrate metabolism, amino acid biosynthesis)
- [ ] No unexpected dominance of oral or environmental microbes
- [ ] Species diversity is consistent across biological replicates within groups
- [ ] Known gut-associated pathways (e.g., SCFA production) are detected

## Red Flags — STOP

- >80% unmapped reads in MetaPhlAn
- <40% gene family mapping in HUMAnN
- Unexpected organisms dominating (soil/water microbes in gut samples)
- Zero species overlap between technical replicates
- All pathways showing same abundance (normalization error?)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "High unmapped rate is normal" | >80% unmapped means most community is unknown or data is contaminated. Investigate. |
| "MetaPhlAn3 is fine, no need for v4" | Use the version in the LOCKED protocol. Do NOT switch without approval. |
| "Unstratified results are sufficient" | Species contributions are critical for biological interpretation. Keep stratified tables. |
| "HUMAnN is slow, let me skip it" | Functional profiling is a core analysis goal. Do NOT skip. |
| "Low pathway coverage means the pathways aren't there" | Low coverage can mean insufficient depth. Check per-sample. |
