I reviewed the files you uploaded. I now have a fairly clear picture of your **actual runtime architecture**, not just the conceptual one. Below is a reconstruction of how your system currently operates, followed by a few clarifying questions where implementation details are still missing.

---

# 1. Actual Runtime Architecture

Your system is essentially a **Codex-driven filesystem agent** where Markdown files act as **runtime instructions**.

Execution flow:

```
User
 ↓
FastAPI endpoint
 ↓
Prompt = AGENT_PROMPT + user_request
 ↓
CodexCLI.exec()
 ↓
Codex agent starts
 ↓
Reads workflow_router.md
 ↓
Decides:
   direct response
   OR
   agent execution
 ↓
If agent:
   reads agent_execution.md
   discovers agents
   executes selected agent
 ↓
stdout JSON events
 ↓
streaming.py
 ↓
SSE events
 ↓
Frontend
```

---

# 2. Codex Execution Environment

The wrapper launches the Codex CLI like this:

```
codex exec --json --skip-git-repo-check
```

plus configuration flags. 

Important execution settings:

* **Working directory**

```
cwd = workflow_templates
```

so the agent sees:

```
workflow/
agent_created/
agent_executions/
```

from its root. 

* **Threads directory mounted**

```
--add-dir THREADS_DIR
```

This exposes conversation history to the agent. 

* **JSON event mode**

```
--json
```

This produces structured execution events that your streaming layer parses.

---

# 3. Streaming System

The streaming layer converts Codex events to SSE.

Flow:

```
Codex stdout
 ↓
_parse_codex_event()
 ↓
_extract_thinking()
 ↓
_extract_assistant_message()
 ↓
SSE → frontend
```

Thinking logs are captured from:

```
item.started command_execution
item.completed command_execution
```

and stored for UI display. 

Example of captured events:

```
command_start
command_complete
assistant_message
returncode
```

These logs are also persisted into the **thread system**.

---

# 4. Router Logic

Your router is fully LLM-driven.

The agent is told to load:

```
workflow_templates/workflow/workflow_router.md
```

as the **entry point**. 

Router behavior:

1. Load conversation history
2. Analyze request
3. Decide:

```
direct response
or
agent execution
```

If agent is required:

```
load agents/agent_execution.md
```



---

# 5. Agent Discovery

Agent selection is done by reading **descriptions**.

The process:

```
created_agents/
   agent_1/
   agent_2/
```

For each agent:

```
read description.md
```

Then choose the best match. 

After selecting:

```
read agent.md
read output_format.md
```

Then execute the instructions.

---

# 6. Standalone Agent Mode

Your system also supports **direct agent execution** without the router.

The prompt:

```
RUN_STANDALONE_AGENT_PROMPT
```

provides:

```
agent_name
execution_id
execution_path
```

The agent must:

```
read agent.md
produce output.json
update metadata.json
```

inside:

```
agent_executions/{agent}/{execution_id}
```

This effectively creates **file-based execution artifacts**. 

---

# 7. Execution Artifact Design

Each run produces:

```
agent_executions/
   agent_name/
      execution_id/
          metadata.json
          logs.json
          output.json
```

This is a good design decision.

It enables:

* replayability
* auditability
* debugging

---

# 8. What Your System Really Is

Architecturally, your system is closest to:

```
Filesystem Agent Runtime
```

where:

```
Markdown = workflow instructions
Codex = reasoning engine
Filesystem = shared state
```

This is similar in philosophy to:

* AutoGPT classic
* OpenAI DevAgent
* GitHub Copilot Workspace agents

but implemented much more cleanly.

---

# 9. Major Strengths

### 1. Extremely simple orchestration layer

You avoided complex frameworks.

### 2. Markdown agents

Agents are easy to edit and version.

### 3. Streaming observability

Your thinking logs are very useful.

### 4. Artifact-based execution

The execution folder structure is strong.

---

# 10. Weak Points (Current System)

These are architectural observations—not redesign yet.

### Router is unconstrained

The router is pure LLM reasoning.

That means it may:

* pick wrong agent
* misinterpret tasks
* hallucinate paths

---

### Agent discovery is O(N)

Each run requires reading:

```
description.md
```

for every agent.

This will not scale to:

```
>50 agents
```

---

### No deterministic execution engine

The LLM decides:

```
execution order
file reads
file writes
```

Ideally:

```
LLM → plan
Python → execute
```

---

### No input schema enforcement

Agents rely on natural language instructions.

This will break when:

```
agents expect structured inputs
```

--