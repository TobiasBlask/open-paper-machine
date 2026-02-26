---
name: method-engine
description: >
  Activate when the user needs to select, justify, describe, or execute a research 
  methodology. Provides method selection guidance, complete method section templates,
  quality criteria, and tool recommendations. Covers SLR, qualitative (case study, 
  Gioia, Mayring, Grounded Theory), quantitative (SEM, regression, survey), DSR, 
  and mixed methods.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Method Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (method-engine)
> **Input:** [brief description of the methodology request]
> **Output:** [brief description of what was produced — e.g., "DSR method section drafted with 3 evaluation criteria"]
> ```

# Method Engine

## Method Selection Guide

### Decision Tree

```
What is your primary research goal?
│
├─ "I want to map what the literature says" 
│   → Systematic Literature Review (Section A)
│
├─ "I want to understand a phenomenon in depth"
│   → Qualitative Study (Section B)
│   ├─ Single context, deep → Single Case Study
│   ├─ Multiple contexts, comparison → Multiple Case Study  
│   ├─ Build new theory from data → Grounded Theory / Gioia
│   └─ Analyze text/documents systematically → Content Analysis (Mayring)
│
├─ "I want to test hypotheses / measure relationships"
│   → Quantitative Study (Section C)
│   ├─ Complex model with latent variables → SEM (PLS or CB)
│   ├─ Simpler relationships → Regression
│   └─ Experimental comparison → Experiment / Quasi-experiment
│
├─ "I want to build something (tool, framework, model)"
│   → Design Science Research (Section D)
│
└─ "I want to combine approaches"
    → Mixed Methods (Section E)
```

---

## Section A: Systematic Literature Review

### Method Section Template (ready to adapt):

```
3. Research Methodology

We conducted a systematic literature review following the guidelines of 
[vom Brocke et al. (2009, 2015) / Webster & Watson (2002) / Kitchenham & 
Charters (2007) / PRISMA 2020 (Page et al., 2021)]. This approach is 
appropriate because [justification: need to synthesize a growing but 
fragmented body of knowledge / field is maturing and needs stock-taking / 
practical guidance requires evidence synthesis].

3.1 Search Strategy

We searched [N] electronic databases: Semantic Scholar, OpenAlex, CrossRef, 
[and arXiv for preprints / and AIS eLibrary for IS-specific venues]. 
The search was conducted in [month/year] using the following query terms:

  [("generative AI" OR "generative artificial intelligence" OR "large language 
  model*" OR "LLM" OR "GPT" OR "foundation model*") AND ("enterprise" OR 
  "organization*" OR "business" OR "implementation" OR "adoption")]

  [("AI agent*" OR "autonomous agent*" OR "agentic AI") AND ("organization*" 
  OR "enterprise" OR "business process" OR "implementation")]

The search was limited to publications from [year] to [year], in 
[English / English and German].

3.2 Selection Criteria

Table [N] summarizes our inclusion and exclusion criteria.

| ID | Criterion | Rationale |
|----|-----------|-----------|
| IC1 | Peer-reviewed journal article or conference paper | Quality assurance |
| IC2 | Focuses on [topic] in organizational context | Scope alignment |
| IC3 | Published between [year] and [year] | Recency |
| IC4 | Available in English [or German] | Accessibility |
| EC1 | Purely technical (no organizational dimension) | Out of scope |
| EC2 | Editorial, book review, or abstract-only | Insufficient depth |
| EC3 | Duplicate publication | Avoid double-counting |

3.3 Search and Screening Process

Figure [N] presents the PRISMA flow diagram of our search and selection process. 
The initial search yielded [N] records across all databases. After removing 
[N] duplicates, [N] records were screened based on title and abstract, of 
which [N] were excluded. The remaining [N] articles were assessed in full text, 
resulting in [N] studies included in the final synthesis.

[Forward and backward citation tracking (snowballing) on the [N] most-cited 
included studies identified an additional [N] relevant papers, bringing the 
total to [N] studies.]

3.4 Data Extraction and Analysis

From each included study, we extracted: [list categories: research question, 
theoretical lens, methodology, sample/context, key findings, limitations, 
and contribution type].

We synthesized findings using a concept-centric approach (Webster & Watson, 2002), 
organizing results in a concept matrix that maps studies against key themes 
identified through iterative reading and coding.
```

### PRISMA Flow Diagram (text version):

```
Identification:
  Records from Semantic Scholar:     [n]
  Records from OpenAlex:             [n]  
  Records from CrossRef:             [n]
  Records from arXiv:                [n]
  Records from manual/snowballing:   [n]
  ─────────────────────────────────
  Total identified:                  [N]
  Duplicates removed:               -[n]
  Records after deduplication:       [N]

Screening:
  Title/abstract screened:           [N]
  Excluded:                         -[n]
  Full-text assessed:                [N]

Eligibility:
  Full-text excluded (with reasons): -[n]
    - Not organizational context:    [n]
    - Not empirical/conceptual:      [n]  
    - Not accessible:                [n]

Included:
  Studies in final synthesis:        [N]
```

---

## Section B: Qualitative Methods

### Case Study (Yin, 2018 / Eisenhardt, 1989)

Method section template:
```
3. Research Methodology

We employed a [single/multiple] case study approach (Yin, 2018) to investigate 
[phenomenon] in [context]. Case study research is appropriate when investigating 
a contemporary phenomenon within its real-world context, particularly when the 
boundaries between phenomenon and context are not clearly evident (Yin, 2018).

3.1 Case Selection

[For single case:] We selected [case] as a [revelatory/critical/typical/extreme] 
case (Yin, 2018) because [justification].

[For multiple cases:] Following [theoretical/literal] replication logic 
(Yin, 2018), we selected [N] cases based on [selection criteria]. Table [N] 
provides an overview of the cases.

| Case | Industry | Size | AI Maturity | Selection Rationale |
|------|----------|------|-------------|---------------------|
| A    | [X]      | [X]  | [X]         | [X]                 |
| B    | [X]      | [X]  | [X]         | [X]                 |

3.2 Data Collection

We collected data from multiple sources to enable triangulation (Yin, 2018):
- [N] semi-structured interviews with [roles] (average duration: [X] minutes)
- Internal documents: [list types]
- [Observation / workshop protocols / system logs]
- [Archival data: annual reports, press releases]

All interviews were recorded and transcribed [verbatim / in summary form].

3.3 Data Analysis

We analyzed the data using [thematic analysis (Braun & Clarke, 2006) / 
the Gioia methodology (Gioia et al., 2013) / qualitative content analysis 
(Mayring, 2014)]. [Method-specific description — see subsections below.]

3.4 Research Quality

We ensured research quality through:
- **Construct validity**: Multiple data sources, chain of evidence
- **Internal validity**: Pattern matching, explanation building
- **External validity**: [Replication logic across cases / analytical generalization]
- **Reliability**: Case study protocol, case study database
```

### Gioia Methodology (Gioia et al., 2013)

```
Data analysis followed the Gioia methodology (Gioia et al., 2013). First, we 
engaged in open coding of interview transcripts and documents, identifying 
first-order concepts that remained close to informant language. This yielded 
[N] initial codes. Through constant comparison and iterative abstraction, we 
grouped these into [N] second-order themes reflecting more abstract, 
researcher-driven categories. Finally, we aggregated themes into [N] 
overarching dimensions that form the basis of our emerging framework.

Figure [N] presents the resulting data structure.
```

### Mayring Content Analysis (Mayring, 2014)

```
We analyzed the data using qualitative content analysis following Mayring (2014). 
We employed [deductive / inductive / mixed] category formation. 

[Deductive:] Categories were derived from [Theory/prior framework] and applied 
to the material. Coding rules and anchor examples were defined a priori.

[Inductive:] Categories emerged from the data through systematic paraphrasing, 
generalization, and reduction of text passages. After coding [X]% of the 
material, the category system was revised and finalized.

[Both:] Inter-coder reliability was assessed using [Cohen's κ / Krippendorff's α], 
yielding a value of [X], indicating [substantial/excellent] agreement.
```

---

## Section C: Quantitative Methods

### Survey + PLS-SEM

```
3. Research Methodology

3.1 Research Model and Hypotheses
[Refer to Section 2 where hypotheses were developed]

3.2 Measurement
All constructs were measured using validated scales from prior literature. 
[Construct 1] was measured with [N] items adapted from [Author] (Year). 
[Construct 2] used [N] items from [Author] (Year). All items were assessed 
on a [7-point Likert / 5-point Likert] scale. Table [N] lists all 
measurement items with their sources.

3.3 Data Collection
Data were collected via an online survey distributed to [target population] 
through [distribution channels] between [month] and [month year]. 
After removing incomplete and inattentive responses (attention check items, 
completion time < [X] minutes), our final sample comprised N = [N] responses.

3.4 Analysis Method
We employed partial least squares structural equation modeling (PLS-SEM) 
using SmartPLS [version] (Ringle et al., Year). PLS-SEM is appropriate 
for our study because [exploratory nature / complex model / formative 
constructs / prediction-oriented / small sample] (Hair et al., 2019).

3.5 Measurement Model Assessment
[Convergent validity:] All indicator loadings exceed 0.708, composite 
reliability (CR) values are above 0.70, and average variance extracted 
(AVE) exceeds 0.50 for all constructs (Table [N]).

[Discriminant validity:] The Fornell-Larcker criterion is satisfied, and 
HTMT values are below 0.85 (Table [N+1]).

[Common method bias:] We assessed common method bias using [Harman's 
single-factor test / marker variable technique / ULMC]. Results suggest 
that CMB does not pose a significant concern.

3.6 Structural Model Assessment
[Report: path coefficients, significance (bootstrapping, N=5000), R², f², Q²]
```

---

## Section D: Design Science Research

### Method Section Template (Peffers et al., 2007):

```
3. Research Approach

We follow the Design Science Research Methodology (DSRM) by Peffers et al. 
(2007), complemented by the guidelines of Hevner et al. (2004). DSR is 
appropriate because our objective is to develop [artifact type: a framework / 
a model / a method / a prototype] that addresses [practical problem].

Our research process comprises six activities:

(1) Problem identification: [Derived from literature review + practice, Section 2]
(2) Solution objectives: [Design requirements, Section 3.1]
(3) Design and development: [Artifact construction, Section 4]
(4) Demonstration: [Application to real-world scenario, Section 4.x]
(5) Evaluation: [Evaluation method and results, Section 5]
(6) Communication: [This paper]

3.1 Design Requirements

Based on our problem analysis (Section 2) and [N] expert interviews / 
[analysis of practice], we derived the following design requirements:

| ID  | Design Requirement | Source | Type |
|-----|-------------------|--------|------|
| DR1 | The [artifact] must [capability] | Literature: Author (Year) | Functional |
| DR2 | The [artifact] should [quality] | Expert interview #[N] | Non-functional |
| DR3 | [Users] need to [capability] | Practice analysis | User |

3.2 Kernel Theories

Our design is grounded in [Theory 1] (Author, Year) and [Theory 2] (Author, Year). 
[Theory 1] informs the design by [specific mechanism → design decision]. 
[Theory 2] guides [specific aspect] because [reasoning].

3.3 Evaluation Strategy

Following Venable et al. (2016), we employ [evaluation strategy: 
human risk & effectiveness / technical risk & efficacy / quick & simple]. 
Specifically, we evaluate the artifact through [method: expert interviews / 
user study / field experiment / case study application / scenario-based].
```

---

## Section E: Mixed Methods

```
3. Research Methodology

We employed an [explanatory sequential / exploratory sequential / convergent] 
mixed methods design (Creswell & Creswell, 2018; Venkatesh et al., 2013).

[Explanatory sequential:] First, we conducted a quantitative [survey/experiment] 
(Phase 1) to [test hypotheses / identify patterns]. Subsequently, we conducted 
qualitative [interviews/case studies] (Phase 2) to explain and deepen the 
quantitative findings.

[Exploratory sequential:] First, we conducted qualitative [interviews/observations] 
(Phase 1) to explore [phenomenon] and develop [a conceptual model / hypotheses]. 
Subsequently, we tested these through a quantitative [survey] (Phase 2).
```

---

## Quality Criteria Quick Reference

| Method | Key Quality Criteria | How to Address |
|--------|---------------------|----------------|
| SLR | Reproducibility, Comprehensiveness | Protocol, multiple databases, PRISMA |
| Case Study | Construct/Internal/External validity, Reliability | Triangulation, chain of evidence, protocol |
| Gioia/GT | Trustworthiness | Thick description, data structure display, informant validation |
| Content Analysis | Inter-coder reliability | Cohen's κ > 0.7, Krippendorff's α > 0.8 |
| Survey/SEM | Reliability, Validity, CMB | CR > 0.7, AVE > 0.5, HTMT < 0.85, Harman |
| DSR | Utility, Quality, Efficacy | Evaluation framework (Venable et al.), kernel theories |
| Mixed Methods | Integration quality | Meta-inferences, explicit integration strategy |
