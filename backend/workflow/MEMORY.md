# Agent Memory

This file stores distilled knowledge to improve future performance.

## 💡 Best Practices
- **Success Patterns**: Document strategies that worked well for complex tasks.
- **Mistakes to Avoid**: Record failures and their root causes to prevent repetition.
- **Environment Context**: Notes on codebase idiosyncrasies or specific configurations.

## 📝 Format for New Entries
- **Date/Task**: Brief description of the context.
- **Outcome**: Success or Failure.
- **Trigger**: When this lesson should be applied.
- **Rule**: The concrete action the agent should follow.
- **Lesson**: Additional explanation or context.

---

## 🕒 Recent Lessons
- **Date/Task**: 2026-03-16 - Added PDF text extraction utility.
- **Outcome**: Success.
- **Lesson**: When introducing new workflow utilities, register them in `UTILITIES.md` with a direct usage example to keep discovery friction low.
- **Date/Task**: 2026-03-16 - External PDF analysis with restricted network.
- **Outcome**: Success.
- **Lesson**: If direct `curl` download fails due DNS/network limits, use web search/open retrieval to extract report text, then proceed with interpretation.
- **Date/Task**: 2026-03-17 - CBC PDF template analysis validation.
- **Outcome**: Success.
- **Lesson**: Re-extract values from the exact source each run; template report URLs may resolve to different sample values over time, so avoid reusing prior numeric interpretations.
- **Date/Task**: 2026-03-17 - CBC template PDF text quality handling.
- **Outcome**: Success.
- **Lesson**: Template lab PDFs may contain tightly concatenated OCR text; store both raw extracted text and normalized structured outputs (`analysis.json` + `analysis.md`) for auditability.
- **Date/Task**: 2026-03-17 - Hospital bill reconciliation.
- **Outcome**: Success.
- **Lesson**: Always recompute totals from line items and compare against stated summary; flag exact missing amount and likely omitted charge heads to speed manual verification.
- **Date/Task**: 2026-03-17 - Grocery receipt structured extraction.
- **Outcome**: Success.
- **Lesson**: For receipts with quantity and per-item prices, always compute `line_total = quantity x unit_price` and reconcile against printed subtotal/tax/total; preserve both printed and recomputed totals in output to make discrepancies auditable.
