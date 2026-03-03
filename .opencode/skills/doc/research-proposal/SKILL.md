---
name: research-proposal
description: "Generate structured research proposals and grant applications for bioinformatics and life sciences. Covers specific aims, significance, innovation, approach, and budget justification. Use when drafting NIH R01/R21, NSFC, ERC, or similar grant proposals. Adapts to funding agency requirements."
allowed-tools: [Read, Write, Edit, Bash, WebSearch]
---

# Research Proposal Generator

## Overview

Generate comprehensive, well-structured research proposals for bioinformatics and life sciences funding applications. This skill guides through the complete proposal writing process from specific aims to budget justification, following agency-specific formats.

## When to Use This Skill

- Drafting NIH grants (R01, R21, R03, K-series, F-series)
- Writing NSFC (国家自然科学基金) proposals
- Preparing ERC Starting/Consolidator/Advanced grants
- Creating institutional research proposals
- Writing project proposals for bioinformatics collaborations
- Preparing preliminary/white papers for funding agencies
- Developing research plans for fellowship applications

## Supported Formats

| Agency | Format | Page Limits |
|--------|--------|-------------|
| NIH R01 | PHS 398 | 12 pages (Research Strategy) |
| NIH R21 | PHS 398 | 6 pages (Research Strategy) |
| NSFC 面上项目 | NSFC Template | 按基金委要求 |
| NSFC 青年基金 | NSFC Template | 按基金委要求 |
| ERC Starting | ERC Template | Part B1: 5 pages, B2: 15 pages |
| Generic | Custom | Flexible |

## Proposal Structure

### NIH-Style Research Strategy

#### 1. Specific Aims (1 page)
- **Opening paragraph**: Establish importance and knowledge gap
- **Central hypothesis**: Clear, testable statement
- **Aims** (2-3): Each with rationale and expected outcomes
- **Impact statement**: How this advances the field

**Template:**
```
[Field] is critical for [broader impact]. However, [knowledge gap] remains
unresolved because [barrier]. Our preliminary data show [key finding],
suggesting [hypothesis].

We propose to test the central hypothesis that [specific hypothesis] using
[approach overview]. This hypothesis is based on [supporting evidence].

Aim 1: [Action verb] [objective]. We will [approach]. We expect [outcome].
Aim 2: [Action verb] [objective]. We will [approach]. We expect [outcome].
Aim 3: [Action verb] [objective]. We will [approach]. We expect [outcome].

This project is significant because [impact]. The proposed research is
innovative because [novelty]. Successful completion will [outcomes].
```

#### 2. Significance (1-2 pages)
- Current state of the field with citations
- Knowledge gaps and unmet needs
- How proposed research addresses these gaps
- Potential for clinical/translational impact
- Relevance to public health or scientific advancement

#### 3. Innovation (0.5-1 page)
- Novel concepts, approaches, or methodologies
- New application of existing tools
- Unique combinations of techniques
- Advantages over existing approaches

#### 4. Approach (6-8 pages for R01)
For each aim:
- **Rationale**: Why this aim is needed
- **Preliminary data**: Supporting evidence
- **Experimental design**: Detailed methodology
- **Expected results**: Anticipated outcomes
- **Potential pitfalls**: Known challenges
- **Alternative strategies**: Backup plans
- **Timeline**: Milestones and deliverables

### Bioinformatics-Specific Sections

When writing bioinformatics proposals, include:

**Data Sources and Management:**
- Public databases (GEO, TCGA, GTEx, etc.)
- Data types (RNA-seq, scRNA-seq, WGS, proteomics)
- Data volume estimates and storage plans
- Data sharing and reproducibility plans

**Computational Methods:**
- Software tools and pipelines
- Statistical approaches and power analysis
- Machine learning methods with validation strategy
- Benchmark datasets and performance metrics

**Infrastructure:**
- Computing resources (HPC, cloud)
- Software dependencies and versions
- Reproducibility framework (containers, workflows)

## Writing Principles

### DO:
- Start with a compelling problem statement
- Use active voice and strong verbs
- Include quantitative preliminary data
- Cite recent high-impact literature
- Address potential pitfalls proactively
- Make figures self-explanatory
- Follow the funding agency's formatting exactly

### DON'T:
- Use jargon without definition
- Propose unfocused, overly ambitious aims
- Ignore the review criteria
- Submit without addressing previous reviewer comments
- Leave significance implicit—state it explicitly
- Use vague language ("we will explore", "we may find")

## Workflow

### Stage 1: Planning
1. Identify funding opportunity and review criteria
2. Gather preliminary data and citations
3. Define central hypothesis and 2-3 specific aims
4. Create a 1-page aims document for feedback

### Stage 2: Drafting
1. Write Specific Aims page first (this drives everything)
2. Draft Significance and Innovation
3. Write Approach for each aim
4. Create figures and tables
5. Draft budget justification

### Stage 3: Review and Polish
1. Check page limits and formatting
2. Verify all claims have citations or data support
3. Ensure logical flow between sections
4. Get feedback from collaborators
5. Proofread for clarity and grammar

## Budget Justification

Include justifications for:
- **Personnel**: Role, % effort, expertise needed
- **Equipment**: Computing hardware, software licenses
- **Supplies**: Sequencing costs, reagents, cloud computing
- **Travel**: Conferences for dissemination
- **Other**: Publication costs, subject payments

## Review Criteria (NIH)

| Criterion | Weight | Focus |
|-----------|--------|-------|
| Significance | High | Does it address an important problem? |
| Investigator(s) | High | Are they qualified? |
| Innovation | Medium | Does it employ novel approaches? |
| Approach | High | Is the strategy well-designed? |
| Environment | Medium | Is the scientific environment suitable? |

## Integration with Other Skills

- **scientific-writing**: For polishing prose and ensuring proper citations
- **paper-audit**: For quality checking the proposal
- **bio/ skills**: For validating bioinformatics methodology descriptions
