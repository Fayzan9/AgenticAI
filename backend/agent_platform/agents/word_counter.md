---
agent:
  name: word_counter
  version: 1.0

capabilities:
  - word_count
  - text_statistics

inputs:
  text:
    type: string
    required: true

outputs:
  word_count:
    type: integer

execution:
  strategy: llm
  timeout_seconds: 10
---

# Word Counter Agent

Counts words in a given text.

Rules:

1. Words separated by whitespace
2. Ignore leading/trailing spaces
3. Punctuation ignored