---
agent:
  name: summarizer
  version: 1.0

capabilities:
  - summarize_text

inputs:
  text:
    type: string

outputs:
  summary:
    type: string
---

# Text Summarizer Agent

Summarizes text into a short paragraph.