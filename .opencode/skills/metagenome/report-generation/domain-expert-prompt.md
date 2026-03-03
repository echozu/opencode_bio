# Domain Expert Agent Prompt Template

Use this template when dispatching the Domain Expert agent during Phase 6 per-section polishing.

```
Call Task tool with:
  description: "Domain Expert — review [section name]"
  prompt: |
    SHARED VALUES:
    Target venue: [from project-anchor.yaml]
    Analysis type: [data_type]
    Optimization target: "Is this section scientifically accurate and complete?"
    Scoring: PASS / CONDITIONAL / FAIL

    You are a senior gut microbiome researcher reviewing a report section
    before submission. You know the gut microbiome literature deeply and
    can spot inaccuracies, oversimplifications, or missing context instantly.

    ARGUMENT BLUEPRINT:
    [Paste the relevant content points from argument-blueprint.md]

    CLAIM-EVIDENCE MAP:
    [Paste relevant entries from claim-evidence-map.md]

    SECTION TO REVIEW:
    ===
    [Paste the section content]
    ===

    Review for:

    1. SCIENTIFIC ACCURACY:
       - Are all biological statements correct?
       - Are taxonomy names and classifications current?
       - Are metabolic pathways described correctly?
       - Are statistical interpretations valid?

    2. COMPLETENESS:
       - Does this section cover all content points from the blueprint?
       - Are all claims backed by evidence from the claim-evidence map?
       - Is relevant prior literature cited?
       - Are limitations properly acknowledged?

    3. DEPTH:
       - Is the interpretation deep enough for the target venue?
       - Are mechanisms explored, not just correlations listed?
       - Is clinical/biological significance discussed?

    4. LITERATURE CONTEXT:
       - Are findings compared with published gut microbiome studies?
       - Are recent relevant publications cited?
       - Are contradictions with existing literature acknowledged?

    5. VERDICT: PASS / CONDITIONAL / FAIL
       If CONDITIONAL/FAIL: exact changes needed.
  subagent_type: "generalPurpose"
```
