---
name: analysis-design-validation
description: Use when Phase 1 (data-assessment) is complete and G1 gate has passed — subjects the analysis design to adversarial 3-agent review, validates biological rationale, and produces a final feasibility ruling before pipeline design begins
---

<IRON-LAW>
THIS PHASE IS NEVER OPTIONAL. It is required for ALL data types:
- Type A (Amplicon): adversarial questioning catches flawed diversity metrics, inappropriate normalization, or missing confounders
- Type M (Assembly): stress-testing prevents wasted computation on poor assembly strategies
- Type R (Read-Based): questioning reveals database bias and profiling limitations
- Type C (Combined): both pipelines need validation

"It's just standard 16S analysis, no need for validation" is the #1 reason metagenome projects produce shallow findings. DO NOT SKIP THIS PHASE.
</IRON-LAW>

# Analysis Design Validation (Phase 2)

## Overview

A data assessment that passed G1 confirms data QUALITY, not analysis STRATEGY. This skill stress-tests the proposed analysis design through adversarial multi-agent review before resources are invested in pipeline configuration.

<HARD-GATE>
Do NOT proceed to pipeline design, parameter locking, or any Phase 3 activity until the multi-agent deliberation converges and the user has explicitly approved. No exceptions.
</HARD-GATE>

## Step 0 — Scientific Novelty Litmus Test

<IRON-LAW>
Before detailed review, apply this quick filter:

"If this analysis succeeds perfectly, what NEW biological knowledge exists that didn't exist before?"

**FAIL examples (NOT publishable):**
- "We confirm that IBD patients have reduced diversity" → This is known. Running standard pipeline on known data confirms nothing new.
- "We show that MetaPhlAn3 can profile gut samples" → This is a tutorial, not research.
- "We provide a reproducible 16S analysis pipeline" → Reproducibility is good practice, not a contribution.

**PASS examples (potentially publishable):**
- "We discover that specific Bacteroides species correlate with treatment response in [disease X]"
- "We reveal distinct functional pathway enrichment in early vs late-stage [condition]"
- "Cross-cohort analysis reveals a conserved microbial signature across 5 independent IBD studies"

If the proposed analysis fails this test, tell the user honestly and suggest alternatives.
Do NOT proceed with a plan that will only confirm known findings.
</IRON-LAW>

## Step 1 — Multi-Agent Analysis Design Deliberation (AUTOMATED — MANDATORY)

<IRON-LAW>
The analysis design determines the entire project's outcome. A single agent cannot adequately evaluate whether the design will produce meaningful results. This step dispatches THREE specialist agents through the `multi-round-deliberation` protocol (max 5 rounds). This is NOT optional.
</IRON-LAW>

### Agent Composition

Three agents with distinct perspectives:

| Agent | Role | Focus |
|-------|------|-------|
| **Senior Microbiome Professor** | Domain authority | Is this analysis scientifically meaningful? Will it produce publishable findings? |
| **Pipeline Architecture Expert** | Technical expert | Is the tool chain optimal? Are there better alternatives? Will it scale? |
| **Clinical/Translational Advisor** | External perspective | Are the results translatable? Does the design account for clinical confounders? |

### Dispatch — Round 1 (parallel)

Use the prompt templates in this skill's directory:
- `microbiologist-prompt.md` for Agent A
- `pipeline-expert-prompt.md` for Agent B
- `clinical-advisor-prompt.md` for Agent C

Each agent receives:
- The proposed analysis plan from Phase 1
- Data quality summary from G1
- Project anchor (data type, sample info, analysis goals)
- Available resources

### Process Results — Multi-Round Deliberation (up to 5 rounds)

**REQUIRED SUB-SKILL:** Follow `multi-round-deliberation` protocol.

After each round:
1. **Synthesize** feedback from all three agents
2. **Modify** the analysis plan based on feedback
3. **Re-dispatch ALL three agents** with the modified plan
4. Check convergence (all PASS → done; any FAIL/CONDITIONAL → next round)

**Convergence criteria:**
- All three agents give PASS on the analysis design
- The design addresses: biological rationale, technical feasibility, clinical relevance

**Non-convergence or persistent failure — Escalation to User:**

If after 3+ rounds the design cannot achieve consensus:

```
⚠️ ANALYSIS DESIGN ESCALATION
═══════════════════════════════

After [N] rounds, the analysis design has not achieved consensus.

Current design: [summary]
Agent verdicts: Microbiologist [X], Pipeline Expert [X], Clinical Advisor [X]

Core problem: [summarize]

YOUR OPTIONS:
1. 🔄 RETURN TO PHASE 1 — Re-assess data and consider different analysis path
2. 🔧 CONTINUE REFINING — Try alternative approaches:
   [list 2-3 specific alternatives]
3. ✅ PROCEED AS-IS — Accept design with known limitations
4. ⏸️ PAUSE — Take time to consult with domain experts

Which option do you prefer?
```

## Step 2 — Analysis Rationale Documentation

After deliberation converges, document:

1. **Biological rationale** — WHY this analysis approach (not just WHAT)
2. **Expected findings** — What would a positive/negative result look like?
3. **Confounders identified** — What variables could confound results?
4. **Limitations acknowledged** — What can this analysis NOT tell us?
5. **Comparison to literature** — How does this design compare to published studies?

Save to `docs/03_plan/analysis-design.md`.

## Step 3 — Present Validated Design to User

```
Phase 2 — Analysis Design Validation Results:
══════════════════════════════════════════════

Rounds completed: [N] / max 5

VALIDATED ANALYSIS DESIGN:
[summary of the validated analysis plan]

Agent verdicts:
  Senior Microbiome Professor: [PASS/COND/FAIL] — [summary]
  Pipeline Architecture Expert: [PASS/COND/FAIL] — [summary]
  Clinical/Translational Advisor: [PASS/COND/FAIL] — [summary]

Key improvements from deliberation:
  [what changed and why]

Remaining concerns (if any):
  ⚠️ [concern] — [recommendation]
```

<IRON-LAW>
## ⛔ MANDATORY STOP

After presenting the validated analysis design, **END YOUR RESPONSE IMMEDIATELY.**

Do NOT invoke `pipeline-design` or any other skill in this same response.
Do NOT begin parameter selection.

**STOP. WAIT. The user must approve before you proceed.**

Your final output should be the validation summary followed by:
"Phase 2 validation complete. Do you approve proceeding to Phase 3 (Pipeline Design)?"
"第2阶段验证完成。是否批准进入第3阶段（流程设计）？"

Then STOP.
</IRON-LAW>

## Red Flags — STOP

- Skipping the novelty litmus test
- Running only 1 agent instead of 3
- Proceeding without agent convergence
- Not documenting analysis rationale
- Ignoring clinical confounders in clinical gut studies
- "Standard analysis doesn't need validation"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The analysis plan is straightforward" | Straightforward ≠ correct. Adversarial review catches blind spots. |
| "We already discussed this in Phase 1" | Phase 1 assessed DATA quality. Phase 2 validates ANALYSIS design. Different purpose. |
| "Three agents are overkill for 16S analysis" | 16S analysis has MORE pitfalls than people realize. Three perspectives catch more. |
| "The clinical advisor isn't needed for basic ecology" | Even basic ecology benefits from translational perspective on confounders. |
| "Validation slows us down" | Discovering a flawed design in Phase 4 wastes WEEKS. Validate now. |
| "The agents will just agree with each other" | If they do, great — validation is quick. If they don't, you caught a problem. |
