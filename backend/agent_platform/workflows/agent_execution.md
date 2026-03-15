---
workflow:
  name: agent_execution

steps:

  - id: discover_agents
    action: scan_directory
    path: agents/

  - id: select_agent
    action: capability_match
    input: intent
    output: agent_name

  - id: load_agent
    action: parse_agent

  - id: validate_input
    action: validate_schema

  - id: execute_agent
    action: run_agent

  - id: validate_output
    action: validate_schema

  - id: save_execution
    action: persist_execution
---