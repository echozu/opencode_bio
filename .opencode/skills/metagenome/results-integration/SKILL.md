---
name: results-integration
description: Use when core pipeline execution (Phase 4) is complete — transforms raw results into a coherent story through multi-agent deliberation, claim-evidence alignment, and produces the G4 gate checklist before report generation
---

# Results Integration (Phase 5)

## Overview

Raw results are not a report. This skill transforms completed analyses into a structured, evidence-backed argument blueprint that the user reviews before any writing begins. It bridges execution (Phase 4) and report generation (Phase 6).

**Core principle:** Organize, interpret, verify — then and only then, outline.

<IRON-LAW>
### BIOLOGICAL SIGNIFICANCE CHECK — Before ANY integration

Before organizing results, answer this question honestly:

**"Do these results contain at least one finding that a gut microbiome researcher would NOT have predicted before seeing the data?"**

If the answer is NO — if every finding confirms what was already known (e.g., "IBD patients have reduced diversity") — then the results are NOT ready for a research paper. Options:

1. **Deepen the analysis** — return to Phase 4 for additional analyses
2. **Change the angle** — re-examine for unexpected patterns
3. **Honestly downgrade** — tell the user these results are better suited for a technical report or lower-tier venue

Do NOT proceed to write about confirmatory results dressed up as discoveries.
</IRON-LAW>

## Pre-Integration Verification

<IRON-LAW>
RESULTS MUST BE REAL BEFORE THEY CAN BE INTEGRATED. Verify ALL:
</IRON-LAW>

- [ ] All planned analyses from analysis-protocol.yaml completed
- [ ] All samples processed (no silent exclusions)
- [ ] Negative results documented in `docs/04_execution/negative-results.md`
- [ ] Domain sanity check passed (results are biologically plausible)
- [ ] Pipeline completeness review passed
- [ ] QC review passed (no unresolved quality issues)

If ANY check fails: **STOP. Return to Phase 4.**

## Step 1: Compile Results

Gather and structure all results:

1. **Taxonomic summary** — top taxa, abundance distributions, group comparisons
2. **Diversity results** — alpha (with statistics), beta (PCoA + PERMANOVA)
3. **Differential abundance** — significant features with effect sizes
4. **Functional results** — enriched pathways, gene families
5. **Network results** — key network metrics, hub taxa
6. **Key visualizations** — all figures generated

Every number must trace back to a logged pipeline output.

## Step 2: Multi-Agent Story Design (AUTOMATED — MANDATORY)

<IRON-LAW>
### THIS IS WHERE THE REPORT'S STORY IS DESIGNED — NOT IN PHASE 6

Phase 5 is where the DEEP thinking about story, argument structure, claims, and interpretations happens. Phase 6 (report generation) should ONLY execute the story designed here.

This multi-agent discussion is:
- NOT optional and NOT deferred
- NOT just "summarize findings" — it must design the full ARGUMENT structure
- NOT just about listing results — it must specify claims, evidence, interpretations

The user should NOT need to ask for this — it happens automatically as part of Phase 5.
</IRON-LAW>

Dispatch three agents (max 5 rounds) using prompt templates:

| Agent | Template | Focus |
|-------|----------|-------|
| Interpretation Expert | `interpretation-expert-prompt.md` | What do these results MEAN biologically? |
| Methods Rigor Reviewer | `methods-rigor-prompt.md` | Are the claims properly supported? Any vulnerabilities? |
| Audience Specialist | `audience-specialist-prompt.md` | Is this compelling for the target audience/venue? |

**REQUIRED SUB-SKILL:** Follow `multi-round-deliberation` protocol for loop, convergence, non-convergence handling.

### Hot Heart Platform Integration

When interpreting results, leverage these resources:

- **R·base (热心肠数据库)**: Compare your taxonomic findings with reference gut compositions. Are your taxa frequencies consistent with population-level data?
- **Daily Report (每日科研速递)**: Check for recent publications on the same taxa/pathways. Are your findings consistent or contradictory with latest research?
- **iMeta**: Reference methodological best practices for result interpretation.

Use web search to access these resources when available.

## Step 3: Build Argument Blueprint

After deliberation converges, produce:

```
ARGUMENT BLUEPRINT (saved to docs/05_integration/argument-blueprint.md):
═════════════════════════════════════════════════════════════════════

ELEVATOR PITCH: [one sentence — what do we now know about the gut microbiome
that we didn't know before?]

CORE ARGUMENT: [3-5 sentences]

CONTENT POINTS (each fully specified):

Point 1: [TITLE]
  CLAIM: [specific statement about the microbiome]
  EVIDENCE: [figure/table/statistic with exact reference]
  INTERPRETATION: [why this evidence supports the claim]
  PRIOR WORK: [connection to existing gut microbiome literature]
  SIGNIFICANCE: [clinical/biological significance]
  KNOWN WEAKNESS: [from methods rigor reviewer, if any]

Point 2: ...
[Aim for 4-6 content points]

NARRATIVE ARC:
  Opening question: [what the reader wonders about the gut microbiome]
  Build-up: [how evidence accumulates]
  Key insight: [the "aha moment"]
  Resolution: [what the reader now believes]

LIMITATIONS (honest):
  - [limitation 1 — how acknowledged]
  - [limitation 2]
```

## Step 4: Claim-Evidence Alignment

<IRON-LAW>
**EVERY claim must map to specific evidence.** Build the full mapping table:

| Claim | Evidence Type | Source | Statistical Support |
|-------|-------------|--------|-------------------|
| "[specific claim]" | Figure 1 / Table 2 / statistic | pipeline output file | p=0.001, FDR<0.05 |

Unmapped claims are DELETED. No exceptions.
</IRON-LAW>

Save to `docs/05_integration/claim-evidence-map.md`.

## G4 Gate Checklist — Report-Ready

ALL items must be satisfied:

**Results quality:**
- [ ] All planned analyses complete
- [ ] Domain sanity check passed
- [ ] Results are biologically plausible and interesting

**Story quality:**
- [ ] Multi-agent discussion completed (Step 2)
- [ ] Methods Rigor Reviewer found ZERO "fatal" vulnerabilities
- [ ] At least one finding a gut microbiome expert would NOT have predicted
- [ ] Argument blueprint designed with 4-6 content points

**Verification:**
- [ ] Claim-evidence alignment passed — full mapping table reviewed
- [ ] All samples reported (no cherry-picking)
- [ ] Negative results documented
- [ ] At least 3 figures and 2 tables produced

**User confirmation:**
- [ ] User confirmed: "ready for report" (explicit statement)
- [ ] Target venue final confirmation

<IRON-LAW>
## ⛔ MANDATORY STOP — Last checkpoint before report generation

After presenting the G4 checklist, **END YOUR RESPONSE IMMEDIATELY.**

Do NOT invoke `report-generation` in this same response.
Do NOT begin writing any report sections.

**STOP. WAIT.** The user must explicitly say "ready for report" or equivalent.

"G4 gate presented. Shall I proceed to Phase 6 (Report Generation)?"
"G4门禁已呈现。是否进入第6阶段（报告生成）？"
</IRON-LAW>

## Red Flags — STOP

- Declaring results "complete" without biological significance check
- Missing claim-evidence alignment
- Story with fewer than 4 content points
- Proceeding to report writing without user confirmation
- All findings are confirmatory (no novel insights)
- Ignoring methods rigor reviewer's fatal findings

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The results speak for themselves" | Results need interpretation, not just presentation. Explain the mechanism. |
| "Reduced diversity in disease is our main finding" | This is known. What is NEW about your finding? |
| "The multi-agent discussion is overkill" | Three perspectives catch blind spots. One perspective misses them. |
| "We have enough figures already" | Enough for what venue? Check against content outline requirements. |
| "Let's just start writing and fill gaps later" | Gaps found during writing cost 3× more to fill. Verify completeness now. |
| "Hot Heart Platform data isn't available" | Try web search. Reference databases strengthen interpretation. |
