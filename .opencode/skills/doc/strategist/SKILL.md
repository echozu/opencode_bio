---
name: strategist
description: "Strategic planning for academic papers in bioinformatics and life sciences. Analyze research landscape, identify publication targets, structure arguments, and create paper roadmaps. Use when planning a new paper, choosing a journal, defining the narrative arc, or positioning results within the field."
allowed-tools: [Read, Write, Edit, Bash, WebSearch]
---

# Academic Paper Strategist

## Overview

Strategic planning companion for academic paper writing. This skill focuses on the pre-writing phase: analyzing the research landscape, identifying the best publication strategy, structuring the paper's argument, and creating a detailed roadmap before any prose is written.

## When to Use This Skill

- **Before writing**: Planning a new paper from research results
- **Journal selection**: Choosing the right target journal
- **Narrative design**: Structuring the argument and story arc
- **Gap analysis**: Positioning your work within the literature
- **Revision strategy**: Responding to reviewer feedback
- **Multi-paper planning**: Splitting a large project into publications

## Core Capabilities

### 1. Research Landscape Analysis

Before writing, map the competitive landscape:

**Step 1: Literature Mapping**
- Search recent publications (last 2-3 years) in the target area
- Identify key competing groups and their approaches
- Map the methodological landscape
- Find the gap your work fills

**Step 2: Identify Your Unique Angle**

| Question | Purpose |
|----------|---------|
| What is genuinely new? | Core contribution |
| What existing problem does this solve? | Significance |
| Who would cite this paper? | Target audience |
| What are the closest competitors? | Differentiation |
| What is the strongest result? | Lead finding |

**Step 3: Position Statement**
Write a 2-sentence position statement:
```
"Despite advances in [area], [gap] remains unsolved because [reason].
We present [approach] that achieves [result], enabling [impact]."
```

### 2. Journal Selection Strategy

Match your work to the right venue:

**Impact vs. Fit Matrix:**

| Factor | Weight | Assessment |
|--------|--------|------------|
| Scope alignment | High | Does the journal publish this topic? |
| Audience match | High | Will readers care about your results? |
| Impact factor | Medium | Appropriate for your contribution level? |
| Review speed | Medium | Time constraints? |
| Open access | Variable | Funder requirements? |
| Page limits | Low | Can you tell the story in allowed space? |

**Bioinformatics Journal Tiers:**

| Tier | Journals | Best For |
|------|----------|----------|
| Top General | Nature, Science, Cell | Transformative discoveries |
| High Impact | Nature Methods, Nature Biotechnology, Genome Research | Major methodological advances |
| Strong | Genome Biology, Nucleic Acids Research, Bioinformatics | Solid computational advances |
| Specialized | BMC Bioinformatics, BMC Genomics, PLoS Computational Biology | Focused contributions |
| Methods | bioRxiv (preprint) + above | Establishing priority |

### 3. Paper Architecture Design

Design the paper structure before writing:

**The Narrative Arc:**
```
Hook → Context → Gap → Approach → Evidence → Impact
```

**Section Planning Template:**

```markdown
# Paper Plan: [Working Title]

## One-Sentence Contribution
[What is the single takeaway?]

## Target Journal: [Name] (IF: X.X)
- Scope fit: [Why this journal]
- Page limit: [N pages]
- Formatting: [Requirements]

## Narrative Arc
1. HOOK: [Opening that grabs attention]
2. CONTEXT: [What the field knows]
3. GAP: [What's missing]
4. APPROACH: [Your solution]
5. EVIDENCE: [Key results that prove it]
6. IMPACT: [Why it matters]

## Figure Plan (backbone of the paper)
- Fig 1: [Overview/method schematic]
- Fig 2: [Key result 1]
- Fig 3: [Key result 2]
- Fig 4: [Validation/comparison]
- Fig S1-SN: [Supplementary]

## Section Outline
### Abstract (150-250 words)
- Problem: [1 sentence]
- Approach: [1-2 sentences]
- Key results: [1-2 sentences with numbers]
- Impact: [1 sentence]

### Introduction (1-1.5 pages)
- Para 1: [Broad context]
- Para 2: [Specific problem]
- Para 3: [Why existing solutions fail]
- Para 4: [Our approach + contribution bullets]

### Methods
- [Section 1]: [Key method description]
- [Section 2]: [Data and preprocessing]
- [Section 3]: [Analysis pipeline]

### Results
- [Result 1]: Supports claim [X] → Fig 2
- [Result 2]: Supports claim [Y] → Fig 3
- [Result 3]: Validation → Fig 4

### Discussion
- Para 1: [Summary of findings]
- Para 2: [Comparison to prior work]
- Para 3: [Implications]
- Para 4: [Limitations]
- Para 5: [Future directions]

## Required Datasets
- [Dataset 1]: Source, size, purpose
- [Dataset 2]: Source, size, purpose

## Key Baselines/Comparisons
- [Method 1]: Why compare
- [Method 2]: Why compare

## Timeline
- Week 1-2: [Figures and tables]
- Week 3-4: [Methods and results]
- Week 5: [Introduction and discussion]
- Week 6: [Polish, get feedback]
- Week 7: [Submit]
```

### 4. Multi-Paper Strategy

For large projects, plan publication sequence:

**Splitting Criteria:**
- Each paper should have ONE clear contribution
- Papers should be independent (not requiring readers to read the others)
- Methods paper first → Application papers later
- Database/resource paper → Analysis papers

**Example for a scRNA-seq project:**
```
Paper 1: New analysis method (→ Bioinformatics)
Paper 2: Biological findings using the method (→ domain journal)
Paper 3: Database/web tool for the community (→ NAR)
```

### 5. Reviewer Response Strategy

When papers are rejected or receive revisions:

**Triage Reviews:**
1. Classify each comment: Easy fix / Requires work / Disagree
2. Prioritize: Address critical concerns first
3. Look for patterns: Multiple reviewers flagging same issue = must fix
4. Plan new analyses needed

**Response Letter Structure:**
```
Dear Editor and Reviewers,

We thank the reviewers for their constructive feedback. We have
addressed all comments as detailed below. Major changes include:
1. [Change 1]
2. [Change 2]

## Reviewer 1

> Comment 1: [Quote the comment]

**Response**: [Explain what you did and why]
[Reference specific pages/figures in revised manuscript]

> Comment 2: [Quote]

**Response**: [...]
```

### 6. Bioinformatics-Specific Strategy

**Computational Paper Checklist:**
- [ ] Code availability (GitHub + Zenodo DOI)
- [ ] Data availability (GEO, SRA, Zenodo)
- [ ] Docker/Singularity container
- [ ] Benchmarking against state-of-the-art
- [ ] Runtime and memory benchmarks
- [ ] Documentation and tutorials
- [ ] Example datasets for reproduction

**Figure Strategy for Bioinformatics:**
- Fig 1: Always a method overview/schematic
- Include UMAP/t-SNE only if genuinely informative
- Benchmark plots: box plots > bar charts
- Use colorblind-friendly palettes
- Genome browser screenshots at proper resolution

## Workflow

1. **Analyze**: Map research landscape (1-2 hours)
2. **Position**: Define unique angle and contribution
3. **Target**: Select journal using fit matrix
4. **Architect**: Design paper structure and figure plan
5. **Outline**: Create detailed section outlines
6. **Handoff**: Pass to scientific-writing skill for prose

## Integration with Other Skills

- **scientific-writing**: Converts strategy into polished prose
- **paper-audit**: Quality-checks the final manuscript
- **bio/ skills**: Validates methodology descriptions
- **paper-slide-deck**: Creates presentation from the paper
