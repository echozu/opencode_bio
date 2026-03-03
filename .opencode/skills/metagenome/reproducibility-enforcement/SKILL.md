---
name: reproducibility-enforcement
description: Use when executing any pipeline step — enforces that all tool versions, database versions, commands, parameters, and random seeds are logged for complete reproducibility
---

# Reproducibility Enforcement (Discipline Layer)

## Overview

A metagenome analysis that cannot be reproduced is not science — it's anecdote. This skill enforces systematic documentation of every element needed for exact reproduction.

**Core principle:** If someone can't reproduce it from your documentation, you didn't document it.

## The Iron Law

<IRON-LAW>
EVERY PIPELINE STEP MUST BE LOGGED WITH:
1. Exact tool name and version
2. Exact database name and version
3. Complete command with all parameters
4. Input file paths
5. Output file paths
6. Random seeds (if applicable)
7. Execution environment (OS, conda env, hardware)

"Standard protocols were used" is NEVER acceptable documentation.
</IRON-LAW>

## What Must Be Logged

### Tool Versions
```yaml
# Example — REQUIRED for every tool used
- tool: fastp
  version: 0.23.4
  installed_via: conda
  environment: qiime2-2023.9

- tool: DADA2
  version: 1.28.0
  installed_via: BiocManager
  R_version: 4.3.2
```

### Database Versions
```yaml
# Example — REQUIRED for every database used
- database: SILVA
  version: "138.1"
  download_date: "2024-01-15"
  download_url: "https://www.arb-silva.de/..."
  md5: "abc123..."
  file: silva-138-99-nb-classifier.qza
```

### Command Logging
```bash
# Example — REQUIRED for every pipeline step
# Step: Quality Control
# Date: 2024-01-20
# Input: data/raw/sample001_R1.fastq.gz, data/raw/sample001_R2.fastq.gz
# Output: data/qc/sample001_R1.fastq.gz, data/qc/sample001_R2.fastq.gz
fastp \
  --in1 data/raw/sample001_R1.fastq.gz \
  --in2 data/raw/sample001_R2.fastq.gz \
  --out1 data/qc/sample001_R1.fastq.gz \
  --out2 data/qc/sample001_R2.fastq.gz \
  --qualified_quality_phred 20 \
  --length_required 150 \
  --detect_adapter_for_pe \
  --thread 8 \
  --json data/qc/sample001.fastp.json
```

### Environment Documentation
```yaml
# Required — save as envs/analysis-env.yml or similar
environment:
  os: "Ubuntu 22.04 LTS"
  kernel: "5.15.0-91-generic"
  conda: "23.11.0"
  python: "3.10.12"
  R: "4.3.2"
  hardware:
    cpu: "AMD EPYC 7763 64-Core"
    ram: "256GB"
    storage: "2TB NVMe SSD"
```

### Random Seeds
```yaml
# Required for any stochastic process
random_seeds:
  rarefaction: 42
  permanova: 999  # permutations, not seed
  network_bootstrap: 123
  machine_learning: [42, 123, 456]
```

## Reproducibility Checklist

Before declaring any phase complete, verify:

- [ ] All tool versions recorded in `docs/04_execution/pipeline-log.md`
- [ ] All database versions recorded with download sources
- [ ] All commands logged with full parameters
- [ ] Environment files (conda yml) created and tested
- [ ] Random seeds documented
- [ ] Raw data preserved (never modified)
- [ ] Processing scripts saved in `scripts/` directory
- [ ] Master pipeline script (`repro/run_all.sh`) updated

## Red Flags — STOP

- "I used QIIME2" without version number
- "Default parameters" without listing them
- Commands not logged at execution time
- No environment file
- Raw data modified (NEVER acceptable)
- Scripts using absolute paths specific to one machine

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Everyone knows what QIIME2 defaults are" | Defaults change between versions. Log them explicitly. |
| "I'll document it after the analysis" | After = never. Document at execution time. |
| "The conda environment is too complex to export" | `conda env export > env.yml` takes 5 seconds. Do it. |
| "Logging every command is tedious" | Running the entire analysis again because you can't reproduce it is MORE tedious. |
| "Version pinning makes environments fragile" | Unpinned versions make results irreproducible. Pin everything. |
| "Raw data takes too much space" | Raw data is irreplaceable. Everything else can be regenerated. |

## The Bottom Line

```
Can another researcher reproduce your EXACT results from your documentation?
If no → your documentation is insufficient.
If you're not sure → it's insufficient.
```
