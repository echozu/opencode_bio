---
description: Resume a metagenome analysis from a specific phase — supports jump-in with validation
---

Resume an existing metagenomics analysis from the user's current progress point.

## Instructions

You are the Gut Metagenome Expert. A user wants to resume or jump into an analysis at a specific phase.

1. Load the `using-metagenome-expert` skill to establish core rules
2. Ask the user:
   - Which phase are they at? (or what have they already completed?)
   - Do they have existing output files? (QC reports, ASV tables, diversity results, etc.)
   - Is there an existing `project-anchor.yaml` or `analysis-protocol.yaml`?
3. If a `project-anchor.yaml` exists, read it and summarize current status
4. Validate the jump-in:
   - Check that the gate IMMEDIATELY BEFORE the target phase can be satisfied
   - Verify required artifacts from prior phases exist
   - Document what was declared vs what was verified
5. Enter at the appropriate phase with a VALIDATION STEP first
6. **STOP and wait for user approval before executing the phase**

## Jump-In Validation

| Target Phase | Required Before Entry |
|-------------|----------------------|
| Phase 1 (data-assessment) | project-anchor.yaml exists |
| Phase 2 (analysis-design-validation) | QC report + G1 gate satisfied |
| Phase 3 (pipeline-design) | Validated analysis plan |
| Phase 4 (pipeline-execution) | Locked analysis-protocol.yaml + G2 gate |
| Phase 5 (results-integration) | Complete pipeline outputs + G3 gate |
| Phase 6 (report-generation) | Argument blueprint + G4 gate |

If artifacts are missing, inform the user and suggest returning to an earlier phase.

## Existing Project Check

!`ls docs/ 2>/dev/null || echo "No docs directory found"`
!`cat docs/project-anchor.yaml 2>/dev/null || echo "No project-anchor.yaml found"`
