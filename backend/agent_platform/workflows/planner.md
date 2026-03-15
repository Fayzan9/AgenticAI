---
planner:
  name: dynamic_pipeline_planner

inputs:
  user_request: string
  agents: list

output:
  pipeline: object
---

# Dynamic Pipeline Planner

Generate an execution pipeline based on the user request.

Use available agents to create a DAG pipeline.
Return JSON structure with:

pipeline
steps
dependencies
inputs
outputs