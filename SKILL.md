---
name: pdf-summarizer
description: >
  Summarizes PDF documents into clear, structured, and actionable summaries.
  Use this skill whenever a user uploads, mentions, or references a PDF file and
  asks for a summary, overview, key points, highlights, takeaways, or "what's in
  this document". Also trigger when users say things like "read this PDF for me",
  "give me the gist of this report", "what does this paper say?", "TL;DR this
  document", or share a file path ending in .pdf and ask any question about its
  content. Even if the user doesn't say the word "summary", trigger this skill
  whenever they clearly want to understand the contents of a PDF without reading
  it themselves. Always use this skill for multi-page documents, research papers,
  legal contracts, financial reports, manuals, academic articles, or business
  documents in PDF format.
---

# PDF Summarizer Skill

This skill extracts text from a PDF document and produces a comprehensive,
well-structured summary tailored to what the user actually needs.

---

## Step 1 — Extract Text from the PDF

Use the bundled extraction script to pull text from the PDF:

```bash
python pdf-summarizer/scripts/extract_pdf.py "<path_to_pdf>"
```

The script outputs:
- Extracted text (page by page)
- Page count
- Detected document type (if possible)

If the PDF is image-based or scanned (no selectable text), the script will
notify you. In that case, inform the user that OCR is required and suggest they
use a tool like Adobe Acrobat or Google Drive to convert it first, or try the
OCR fallback below.

**OCR fallback** (if `pytesseract` is available):
```bash
python pdf-summarizer/scripts/extract_pdf.py "<path_to_pdf>" --ocr
```

---

## Step 2 — Understand the User's Intent

Before writing the summary, consider what the user actually needs:

| User says… | What they probably want |
|---|---|
| "Summarize this" | Full structured summary |
| "Key points / takeaways" | Bullet-point highlights only |
| "What's the main argument?" | Core thesis/conclusion only |
| "TL;DR" | 3–5 sentence executive summary |
| "Summarize for a non-expert" | Plain-language explanation |
| "Legal/financial summary" | Structured by clauses/sections with key obligations, dates, figures |
| "Give me the data/numbers" | Focus on statistics, figures, tables |

Adapt the output format to match the request. If no specific format is
requested, use the FULL STRUCTURED SUMMARY format below.

---

## Step 3 — Write the Summary

### Full Structured Summary (default)

Use this template:

```
# Summary: [Document Title or Filename]

## 📄 Document Overview
- **Type**: [Report / Research Paper / Legal Contract / Manual / Article / Other]
- **Length**: [X pages]
- **Author(s)/Source**: [if available]
- **Date**: [if available]

## 🔑 Key Takeaways
- [Most important point]
- [Second most important point]
- [Third most important point]
(3–7 bullets, each one concrete and specific — not vague)

## 📝 Detailed Summary
[Section-by-section or topic-by-topic summary. Match the structure of the
original document where possible. Each section should be 2–5 sentences.
Aim for completeness without padding.]

## 📊 Important Data / Figures
[Any notable statistics, numbers, dates, financial figures, percentages —
only if present in the document]

## ✅ Conclusions / Recommendations
[What the document concludes, recommends, or calls the reader to do]

## ❓ Potential Questions This Raises
[1–3 questions a reader might want answered after reading this]
```

Omit any section that isn't applicable to the document (e.g., no "Important
Data" section for a short opinion piece).

---

### Short Formats

**TL;DR / Executive Summary** (when user asks for brief/quick version):
```
**TL;DR — [Document Title]**

[3–5 sentences covering: what it is, what it says, and why it matters.]

Key points:
- ...
- ...
- ...
```

**Bullet Points Only** (when user asks for key points/takeaways):
```
**Key Points — [Document Title]**
- ...
- ...
- ...
```

---

## Step 4 — Handle Special Document Types

Read `references/document-types.md` for guidance on summarizing specific
document types including:
- Legal contracts and agreements
- Research papers and academic articles
- Financial reports and earnings documents
- Technical manuals and documentation
- News articles and blog posts
- Government and policy documents

---

## Step 5 — Quality Check

Before presenting the summary, verify:

- [ ] The summary reflects the **actual content** of the document (don't
      hallucinate or fill gaps with assumptions)
- [ ] All specific figures, names, dates, and claims come from the PDF text
- [ ] The length and format match what the user asked for
- [ ] Jargon is either preserved (for expert audiences) or explained (for
      general audiences)
- [ ] No critical information has been dropped that a reader would feel was
      "missing"

---

## Step 6 — Offer Follow-Up

After presenting the summary, always offer:

> "Would you like me to dive deeper into any specific section, extract all
> figures/data, answer questions about the document, or reformat this summary
> in a different way?"

This gives the user a clear path to get more out of the document.

---

## Tips for Better Summaries

- **Length calibration**: A 5-page document needs a shorter summary than a
  50-page one. Aim for roughly 10–15% of the original length in words.
- **Stay grounded**: Never infer things not in the text. If something is
  ambiguous, say so.
- **Use the document's own language** for key terms, names, and branded concepts.
- **Chunk large PDFs**: If a document exceeds ~100 pages, summarize it in
  logical chunks (by chapter, part, or section) and then produce an overall
  executive summary at the top.
- **Signal uncertainty**: If extraction was incomplete or pages were missing,
  note that in the overview section.
