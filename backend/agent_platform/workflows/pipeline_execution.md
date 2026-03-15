---
workflow:
  name: pipeline_execution

steps:

  - id: load_pipeline
    action: parse_pipeline

  - id: validate_pipeline
    action: validate_schema

  - id: build_dag
    action: construct_dag

  - id: execute_steps
    action: execute_dag

  - id: collect_outputs
    action: assemble_outputs

  - id: save_execution
    action: persist_execution
---