# HPC Skills — Directory Rules

You are using HPC infrastructure skills. These rules are CRITICAL and NON-NEGOTIABLE.

<IRON-LAW>
## HPC Discipline

1. **NEVER** run heavy computation on login nodes
   - Login nodes are shared — hogging resources blocks other users
   - Heavy jobs get killed by cluster admins without warning
   - "Heavy" = any bioinformatics pipeline tool, any task >30s, any task >2GB RAM

2. **ALWAYS** submit via `sbatch` for these tasks:
   - QC pipelines (fastp, FastQC, MultiQC, Trimmomatic)
   - Alignment (STAR, bowtie2, BWA, HISAT2, minimap2)
   - Assembly (MEGAHIT, metaSPAdes, SPAdes, Trinity)
   - Taxonomy/Annotation (DADA2, Kraken2, MetaPhlAn, DIAMOND, eggNOG-mapper)
   - Clustering/Dimensionality reduction on large datasets (Scanpy, Seurat with >10K cells)
   - Differential expression on large datasets (DESeq2, edgeR with >50 samples)
   - Any R/Python script processing >1GB data

3. **ALWAYS** read `hpc-env.yaml` for cluster-specific settings
   - Partition names, resource limits, storage paths
   - NEVER hardcode partition names or paths — always reference hpc-env.yaml

4. **ALWAYS** check `squeue -u $(whoami)` before submitting new jobs
   - Avoid queue flooding
   - Check if previous steps completed successfully

5. **ALWAYS** verify job completion — "finished" ≠ "succeeded"
   - Check exit code via `sacct -j $JOB_ID --format=State,ExitCode`
   - Check output files exist with non-zero size
   - Check log files for errors
</IRON-LAW>

## Quick Reference

| Task | Where | Method |
|------|-------|--------|
| File I/O, git, pip/conda install | Login node | Direct bash |
| Small scripts (<30s, <2GB RAM) | Login node | Direct bash |
| squeue, sinfo, sacct monitoring | Login node | Direct bash |
| Bioinformatics tools | **Compute node** | `sbatch` |
| Data processing >1GB | **Compute node** | `sbatch` |
| GPU tasks | **GPU node** | `sbatch -p gpu` |
| Large memory tasks >64GB | **Fat node** | `sbatch -p fat` |
