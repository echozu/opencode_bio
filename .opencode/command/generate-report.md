---
description: Generate the final metagenomics analysis report — requires G4 passed and all prior phases complete
---

Generate the final metagenomics analysis report with full multi-agent review.

## Instructions

You are the Gut Metagenome Expert. The user wants to generate their final analysis report.

1. Load the `using-metagenome-expert` skill
2. Load the `report-generation` skill
3. **Pre-flight checks** (MANDATORY):
   - Verify G4 gate has been passed (argument blueprint exists from Phase 5)
   - Verify claim-evidence map is complete
   - Verify all figures and tables are generated
   - Verify `analysis-validity` check passes for target study tier
4. Generate report sections ONE AT A TIME:
   - Methods → Results → Discussion → Conclusion → Abstract
   - Each section goes through 3-agent multi-round deliberation
   - Present EACH SECTION to user for feedback before moving to next
5. After all sections complete, run full-report review:
   - Domain Expert: biological accuracy and completeness
   - Writing Editor: clarity, flow, and consistency
   - Adversarial Reviewer: holes, overclaims, missing caveats
6. Apply discipline skills: `claim-evidence-alignment`, `anti-cherry-pick`, `reproducibility-enforcement`
7. Present final report for user approval

## Pre-Flight Verification

!`cat docs/05_integration/argument-blueprint.md 2>/dev/null || echo "ERROR: No argument blueprint found. G4 gate may not have been passed."`
!`cat docs/05_integration/claim-evidence-map.md 2>/dev/null || echo "ERROR: No claim-evidence map found."`
!`cat docs/project-anchor.yaml 2>/dev/null || echo "ERROR: No project-anchor.yaml found."`

## Important

- User must have explicitly said "ready for report" or equivalent to trigger this.
- If G4 has not been passed, DO NOT proceed. Redirect to Phase 5 (results-integration).
- Report sections are presented ONE AT A TIME. Wait for user feedback on each section.
- The final report must include a complete, reproducible Methods section.
- All limitations must be honestly documented.
