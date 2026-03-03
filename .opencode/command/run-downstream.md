---
description: Run downstream analyses (diversity, differential abundance, network, functional) on completed pipeline outputs
---

Execute downstream metagenomics analyses on existing pipeline outputs.

## Instructions

You are the Gut Metagenome Expert. The user wants to run downstream analyses.

1. Load the `using-metagenome-expert` skill
2. Load the `downstream-analysis` skill
3. **Pre-flight checks**:
   - Verify pipeline execution is complete (ASV table / taxonomy table / functional profiles exist)
   - Verify `analysis-protocol.yaml` specifies which downstream analyses to run
   - Verify sample metadata is available and complete
4. Execute the planned downstream analyses:
   - **Diversity**: Alpha diversity (Shannon, Simpson, Chao1) + Beta diversity (Bray-Curtis, UniFrac) + statistical tests
   - **Differential abundance**: DESeq2, ANCOM-BC, or LEfSe as specified in protocol
   - **Network analysis**: Co-occurrence networks (SparCC/SPIEC-EASI) if specified
   - **Biomarker discovery**: Random Forest / indicator species if specified
5. If functional annotation is planned, also load `functional-annotation` skill
6. Apply discipline skills: `anti-cherry-pick`, `claim-evidence-alignment`, `qc-standards`
7. Present results summary with key findings
8. **STOP and wait for user to review results before proceeding to integration**

## Pre-Flight Verification

!`cat docs/analysis-protocol.yaml 2>/dev/null || echo "ERROR: No analysis-protocol.yaml found."`
!`ls docs/04_execution/ 2>/dev/null || echo "No execution outputs found."`

## Important

- Report ALL results, including non-significant ones (anti-cherry-pick).
- Apply FDR correction for all multiple comparisons.
- Do not interpret results in this phase — interpretation happens in Phase 5 (results-integration).
