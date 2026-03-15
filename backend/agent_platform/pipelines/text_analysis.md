---
pipeline:
  name: text_analysis
  version: 1.0

inputs:
  text: string

steps:

  - id: summarize
    agent: summarizer
    input:
      text: ${input.text}

  - id: keywords
    agent: keyword_extractor
    depends_on: summarize
    input:
      text: ${steps.summarize.summary}

  - id: word_count
    agent: word_counter
    input:
      text: ${input.text}

outputs:
  summary: ${steps.summarize.summary}
  keywords: ${steps.keywords.keywords}
  word_count: ${steps.word_count.word_count}
---

# Text Analysis Pipeline