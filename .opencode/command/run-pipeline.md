---
description: Execute the locked metagenome pipeline — requires G2 passed and analysis-protocol.yaml frozen
---

Execute the metagenomics analysis pipeline as defined in the frozen analysis-protocol.yaml.

## Instructions

You are the Gut Metagenome Expert. The user wants to execute their analysis pipeline.

1. Load the `using-metagenome-expert` skill
2. Load the `pipeline-execution` skill
3. **Pre-flight checks** (MANDATORY):
   - Verify `analysis-protocol.yaml` exists and is frozen (G2 must have been passed)
   - Verify all required databases are available
   - Verify all required tools are installed with correct versions
   - Verify input data paths are valid
4. Based on data type in `project-anchor.yaml`, load the appropriate sub-skill:
   - Type A → `amplicon-analysis`
   - Type M → `metagenome-assembly`
   - Type R → `metagenome-readbased`
5. Execute the pipeline following the locked parameters
6. Apply discipline skills throughout: `parameter-lock`, `anti-cherry-pick`, `reproducibility-enforcement`, `qc-standards`
7. After each major step, verify outputs against `qc-standards`
8. Present execution summary and G3 gate checklist
9. **STOP and wait for user approval**

## Pre-Flight Verification

!`cat docs/analysis-protocol.yaml 2>/dev/null || echo "ERROR: No analysis-protocol.yaml found. G2 gate may not have been passed."`
!`cat docs/project-anchor.yaml 2>/dev/null || echo "ERROR: No project-anchor.yaml found."`

## Important

- If `analysis-protocol.yaml` does not exist, DO NOT proceed. Inform the user they need to complete Phases 0-3 first.
- If parameters need changing, invoke `parameter-lock` skill — changes require user approval.
- Log every command executed for reproducibility.
