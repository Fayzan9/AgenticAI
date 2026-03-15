# Agentic AI Workflow

## Overview

This workflow defines how the system processes a user request.
The system decides whether to **respond directly** or **delegate the task to one or more agents**.

Agents are stored in the `created_agents/` directory.

The workflow also supports loading conversation history using the provided function.

---

# Important Rule

Conversation history **must only be accessed using the provided function**.

```python
from services.history_loader import load_history

history = load_history(thread_id)
```

❌ **Do NOT read conversation files directly**.
Always use `load_history(thread_id)`.

---

# Workflow

## 1. Receive Request

The system receives:

* `user_request`
* `thread_id`

---

## 2. Load Message History

Load history using the provided function:

```python
from services.history_loader import load_history

history = load_history(thread_id)
```

History contains:

```
[
  {"role": "...", "text": "...", "timestamp": "..."}
]
```

Use this history for context.

---

## 3. Analyze Request

Determine:

* The task required
* Whether **multiple tasks** exist
* Whether a **specialized agent** is required

---

## 4. Identify Relevant Agents

### Step 1 — Determine if an Agent is Needed

First, decide whether the current request requires using any agent.

If **no agent is required**, continue the process without reading any agent files.

If **an agent is required**, proceed to Step 2.

### Step 2 — Check Available Agents

Look for available agents inside:

```
created_agents/
```

Identify which agent (if any) is relevant to the current request.

### Step 3 — Read the Agent Description

For the selected agent, read only:

```
description.md
```

Use the description to confirm that the agent is appropriate for the task.

### Important Rules

❗ **Do not read any agent files (including `description.md`) unless you have determined that an agent is required.**

⚠️ **Do not read the following files unless you are executing the agent:**

```
agent.md
output_format.md
```

---

## 5. Decide Execution Method

### Direct Response

If no agent is required → respond directly.

---

### Use Agent(s)

If an agent is needed → execute the relevant agent.

---

# Sequential Agent Execution

If multiple agents are required:

1. Execute agents **in sequence**
2. Pass the **output of one agent to the next** if needed

Example:

User request:

```
Write an essay and summarize it
```

Execution:

1. `essay_writer`
2. `essay_summarizer`

---

# Loading an Agent

When an agent is selected, load files from:

```
created_agents/<agent_name>/
```

Read:

```
agent.md
output_format.md
```

---

# Agent Registry

| Agent        | Description       |
| ------------ | ----------------- |
| essay_writer | Writes essays     |
| recipe_agent | Generates recipes |

To add a new agent:

1. Create a new folder in `created_agents/`
2. Add:

```
agent.md
description.md
output_format.md
```

---

# Response Rules

* If no agent is needed → respond directly
* If an agent is used → follow the agent instructions and output format
* If multiple agents are used → execute them sequentially and combine outputs

---

# Folder Structure that you can access

```
server
├── agents
│   ├── created_agents
│   │   ├── essay_writer
│   │   │   ├── agent.md
│   │   │   ├── description.md
│   │   │   └── output_format.md
│   │   └── recipe_agent
│   │       ├── agent.md
│   │       ├── description.md
│   │       └── output_format.md
│   └── workflow.md
└── services
    ├── history_loader.py
```
