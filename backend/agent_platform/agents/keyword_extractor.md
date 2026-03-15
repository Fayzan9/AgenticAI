---
agent:
  name: keyword_extractor
  version: 1.0

capabilities:
  - keyword_extraction
  - text_statistics

inputs:
  text:
    type: string
    required: true

outputs:
  keywords:
    type: array
    items: string

execution:
  strategy: llm
  timeout_seconds: 10
---

# Keyword Extractor Agent

Extracts keywords from a given text.

Rules:

1. Extract the most relevant keywords from the text
2. Return the keywords in a JSON array
3. The keywords should be in lowercase
4. The keywords should be in alphabetical order
5. The keywords should be in the same language as the text
6. The keywords should be in the same language as the text