# Redesigning the Agentic Workflow

This document proposes improvements and a more robust redesign of the current Markdown-driven workflow system to enhance reliability, scalability, and complexity handling.

---

## 🚀 Proposed Improvements

### 1. Multi-Agent Pipelines & DAG Chains
Currently, the system mostly selects a single agent. We should allow the [workflow_router.md](file:///Users/faizanpersonal/Desktop/Personal/Experimenting/agent/backend/workflow_templates/workflow/workflow_router.md) to define a sequence or a Directed Acyclic Graph (DAG) of agents.
- **Why**: Complex tasks like "Research a topic and write a summary and then translate it" require three different agents.
- **Fix**: Update [agent_execution.md](file:///Users/faizanpersonal/Desktop/Personal/Experimenting/agent/backend/workflow_templates/workflow/agent_execution.md) to allow sequential execution and state passing via a shared `context.json`.

### 2. Strict Schema Validation (YAML/JSON in MD)
Instead of just free-form text in `input_details.md`, use YAML or JSON blocks within the Markdown files.
- **Why**: Allows the system (and the agent) to programmatically validate inputs before execution.
- **Example**: 
    ```markdown
    ## Input Schema
    ```yaml
    parameters:
      text: string
      limit: integer
    ```

### 3. Human-in-the-loop (HITL) Integration
Add a `pause_for_input.md` workflow step.
- **Why**: High-stakes decisions or low-confidence routing should trigger a request for user confirmation.
- **Mechanism**: The agent writes a `pending_user_confirmation.json` artifact; the UI detects this and shows a prompt.

### 4. Modular Tools for Agents
Allow agents to specify which "Core Tools" they need access to in their `agent.md`.
- **Ex**: `Tools Required: [web_search, local_file_access, python_repl]`
- **Implementation**: The `CodexCLI` can dynamically enable/disable capabilities based on these requirements.

---

## 📐 Redesigned Workflow Template (Example)

### New `workflow_router.md`
```markdown
# Enhanced Router

## Strategy
1. **Detect Complexity**: Is the request multi-part?
2. **Decompose**: Breakdown into sub-tasks.
3. **Route**:
   - If single sub-task -> Single Agent Execution.
   - If multi sub-task -> Multi-Agent Pipeline.

## Capabilities
- Use `ls` to check `agent_created/` for matches.
- Use `cat` to read [description.md](file:///Users/faizanpersonal/Desktop/Personal/Experimenting/agent/backend/workflow_templates/agent_created/word_counter/description.md) of candidate agents.

## Execution Order
Write a `plan.json` in the execution directory before starting sub-agents.
```

### New `agent_execution.md` (Multi-Agent Support)
```markdown
# Multi-Agent Orchestrator

## Step 1: Initialize Stage
Create `stage_context.json` to store intermediate results.

## Step 2: Sequential Loop
For each task in `plan.json`:
1. Select Agent.
2. Read [agent.md](file:///Users/faizanpersonal/Desktop/Personal/Experimenting/agent/backend/workflow_templates/agent_created/word_counter/agent.md).
3. Map `stage_context.json` to Agent Inputs.
4. Execute Agent via `codex exec`.
5. Capture Agent Output and update `stage_context.json`.

## Step 3: Synthesis
The Orchestrator synthesizes the final result from `stage_context.json`.
```

---

## 🌟 Future Vision: "Agents as Microservices"
- **Agent Registry**: A central `registry.json` that agents register themselves to, including their metadata and performance metrics.
- **Auto-Improvement**: A "Meta-Agent" that reviews `logs.json` of past executions and suggests edits to [agent.md](file:///Users/faizanpersonal/Desktop/Personal/Experimenting/agent/backend/workflow_templates/agent_created/word_counter/agent.md) to improve accuracy.
- **Visual Workflow Builder**: A drag-and-drop UI where users can connect [.md](file:///Users/faizanpersonal/.gemini/antigravity/brain/38db6b35-d513-4e24-8641-11f3e6fe9aca/architecture_overview.md) files to create visual pipelines.
