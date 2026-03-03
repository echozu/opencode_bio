# Standard Gut Metagenome Analysis Project Directory Structure

Use this structure for all metagenome analysis projects managed by the Gut Metagenome Expert.

```
project_root/
├── docs/
│   ├── 01_intake/
│   │   └── project-anchor.yaml          # Global anchor (from template)
│   ├── 02_assessment/
│   │   ├── qc-report.md                 # FastQC/MultiQC summary
│   │   ├── data-inventory.md            # Sample inventory with metadata
│   │   ├── contamination-report.md      # Host/kit contamination screening results
│   │   └── sequencing-depth-report.md   # Per-sample depth statistics
│   ├── 03_plan/
│   │   ├── analysis-protocol.yaml       # Locked analysis parameters
│   │   ├── analysis-design.md           # Analysis plan (validated in Phase 2)
│   │   └── tool-chain.md               # Selected tools with versions
│   ├── 04_execution/
│   │   ├── pipeline-log.md              # Step-by-step execution journal
│   │   ├── qc-validation.md             # Post-QC quality verification
│   │   ├── taxonomy-results.md          # Taxonomic profiling summary
│   │   ├── diversity-results.md         # Alpha/beta diversity results
│   │   ├── differential-results.md      # Differential abundance results
│   │   ├── functional-results.md        # Functional annotation results
│   │   ├── negative-results.md          # Failed analyses and unexpected outcomes
│   │   └── domain-sanity-check.md       # Biological plausibility verification
│   ├── 05_integration/
│   │   ├── argument-blueprint.md        # Story design from multi-agent discussion
│   │   ├── claim-evidence-map.md        # Every claim → evidence mapping
│   │   └── acknowledged-gaps.md         # Known limitations and missing analyses
│   └── 06_report/
│       ├── analysis-report.md           # Final comprehensive report
│       ├── methods-section.md           # Reproducible methods description
│       └── supplementary/
│           ├── full-taxonomy-table.md   # Complete taxonomy abundance table
│           ├── full-diversity-stats.md  # Complete diversity statistics
│           └── pipeline-commands.md     # All commands used (reproducibility)
├── data/
│   ├── raw/                             # Immutable raw FASTQ files
│   ├── qc/                              # Quality-controlled reads
│   ├── host_removed/                    # Host-DNA-removed reads (if applicable)
│   └── processed/                       # Analysis-ready processed data
├── results/
│   ├── taxonomy/                        # Taxonomy tables, barplots
│   ├── diversity/                       # Alpha/beta diversity results, PCoA
│   ├── differential/                    # DESeq2/ANCOM-BC/LEfSe results
│   ├── functional/                      # HUMAnN/PICRUSt2 outputs
│   ├── network/                         # Co-occurrence network results
│   └── figures/                         # Publication-ready figures
├── scripts/
│   ├── 01_qc.sh                         # Quality control pipeline
│   ├── 02_denoise.sh                    # Denoising (amplicon) or assembly (shotgun)
│   ├── 03_taxonomy.sh                   # Taxonomic classification
│   ├── 04_diversity.R                   # Diversity analysis
│   ├── 05_differential.R                # Differential abundance
│   ├── 06_functional.sh                 # Functional profiling
│   └── 07_visualization.R               # Figure generation
├── envs/
│   ├── qiime2.yml                       # QIIME2 conda environment
│   ├── biobakery.yml                    # BioBakery tools environment
│   └── r-analysis.yml                   # R analysis environment
└── repro/
    ├── README.md                        # Reproduction instructions
    ├── run_all.sh                       # Master pipeline script
    ├── environment-versions.txt         # All tool versions
    └── database-versions.txt            # All database versions
```

**Notes:**
- `data/raw/` is IMMUTABLE — never modify raw FASTQ files.
- All scripts must include version numbers and database paths.
- Environment files must pin exact versions for reproducibility.
- Results directories mirror the analysis pipeline stages.
