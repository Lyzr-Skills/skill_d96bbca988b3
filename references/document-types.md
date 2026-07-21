# Document Type Summarization Guide

Use this reference when summarizing specific types of PDF documents.
Each section explains what to focus on and any special structural requirements.

---

## 📜 Legal Contracts & Agreements

**Focus on:**
- Parties involved (who is signing / bound by the agreement)
- Effective date and duration / termination clauses
- Core obligations of each party
- Payment terms, amounts, and schedules
- Key restrictions, prohibitions, or exclusivity clauses
- Liability limitations and indemnification
- Dispute resolution mechanism (arbitration, jurisdiction)
- Termination conditions and notice requirements
- Any unusual or non-standard clauses

**Output structure:**
```
## Parties
## Effective Date & Term
## Key Obligations
## Financial Terms
## Restrictions & Exclusivity
## Termination
## Governing Law
## Notable Clauses
```

**Caution**: Always note that this is a summary and not legal advice. Flag
anything that seems unusual or potentially risky without interpreting it as
legal counsel.

---

## 🔬 Research Papers & Academic Articles

**Focus on:**
- Research question / hypothesis
- Methodology (how the study was conducted)
- Sample size, dataset, or scope
- Key findings and results (with specific numbers if available)
- Conclusions and implications
- Limitations acknowledged by the authors
- Future research directions

**Output structure:**
```
## Research Question
## Methodology
## Key Findings
## Conclusions
## Limitations
## Significance / Implications
```

**Tip**: Preserve technical terminology but briefly define it if the user
seems non-specialist. Always cite specific numbers/statistics from the results.

---

## 💰 Financial Reports & Earnings Documents

**Focus on:**
- Reporting period
- Revenue, net income, EPS (earnings per share) vs prior period
- Gross margin and operating margin
- Key business segments performance
- Balance sheet highlights (cash, debt)
- Guidance / forward-looking statements
- Key risks mentioned
- Dividends or share buybacks

**Output structure:**
```
## Period
## Financial Highlights
## Segment Performance
## Balance Sheet Snapshot
## Guidance / Outlook
## Key Risks
```

**Tip**: Always express changes as percentages alongside absolute numbers.
Flag any restatements or accounting changes.

---

## 🔧 Technical Manuals & Documentation

**Focus on:**
- What the product/system is and what it does
- Intended audience and prerequisites
- Installation / setup steps (summarized, not verbatim)
- Key features and capabilities
- Common use cases or workflows
- Troubleshooting topics covered
- Where to find further help

**Output structure:**
```
## What It Is
## Who It's For
## Setup Overview
## Key Features
## Common Workflows
## Troubleshooting Topics
```

**Tip**: Don't reproduce step-by-step instructions verbatim — summarize the
process and tell the user which sections to refer to for details.

---

## 📰 News Articles & Blog Posts

**Focus on:**
- The main news/event/claim (the "lede")
- Who is involved
- When and where
- Why it matters / what the impact is
- Any counterpoints or alternative views mentioned

**Output structure:**
Use a short narrative summary followed by 3–5 key points.

---

## 🏛️ Government & Policy Documents

**Focus on:**
- What policy/regulation/law this pertains to
- Who it applies to
- Key requirements or changes
- Effective date / implementation timeline
- Consequences of non-compliance (if applicable)
- Who to contact for questions

**Output structure:**
```
## Overview
## Who Is Affected
## Key Requirements
## Timeline
## Compliance & Enforcement
```

---

## 📊 Business Reports & Strategy Documents

**Focus on:**
- The core recommendation or strategic direction
- Key findings that support it
- Data or evidence cited
- Proposed actions / next steps
- Stakeholders involved
- Timeline for implementation

**Output structure:**
```
## Executive Summary
## Key Findings
## Recommendations
## Action Plan
## Metrics / Success Criteria
```
