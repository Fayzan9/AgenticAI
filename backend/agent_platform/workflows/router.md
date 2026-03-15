---
workflow:
  name: router
  version: 1.0

steps:

  - id: load_history
    action: load_thread_history

  - id: classify_request
    action: intent_classifier
    output:
      intent: string
      execution_type: string

  - id: route
    type: conditional
    conditions:
      - if: execution_type == "pipeline"
        next: pipeline_execution
      - if: execution_type == "agent"
        next: agent_execution
      - if: execution_type == "dynamic_pipeline"
        next: planner
      - else:
        next: direct_response
---

# Router Workflow

Determines how user requests are processed.