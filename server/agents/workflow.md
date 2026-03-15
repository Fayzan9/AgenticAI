# Agentic AI Workflow

## Overview

This workflow is the entry point for handling user requests.
The system decides whether to **respond directly** or **delegate the task to one or more agents**.

Agents are stored in the `created_agents/` directory and can be extended by adding new folders.

---

# Workflow

1. **Receive Request**

   The system receives a request from the user.

2. **Analyze Request**

   Determine:

   * The tasks required to fulfill the request
   * Whether any tasks require specialized agents
   * Whether the request contains **multiple tasks**

3. **Identify Relevant Agents**

   To determine which agents may help:

   * Read `description.md` from each agent folder.
   * Use the description to identify which agent is relevant.

   Do **not read `agent.md` or `output_format.md` yet**.

4. **Decide Execution Method**

   * **Direct Response**
     If no agent is required, respond directly.

   * **Use Agent(s)**
     If the task requires one or more agents, execute them as needed.

---

# Sequential Agent Execution

If multiple agents are required:

1. Execute agents **in sequence**.
2. The **output of one agent may be used as input for the next agent**.
3. Continue until all tasks are completed.

Examples:

* User asks for **multiple tasks**
  Example:
  *"Write an essay about AI and give a recipe for pasta."*

  Execution:

  1. Use `essay_writer`
  2. Use `recipe_agent`

* One task **depends on the result of another**
  Example:
  *"Write an essay and summarize it."*

  Execution:

  1. `essay_writer`
  2. `essay_summarizer` using the essay output

---

# Loading an Agent

Only when an agent is selected:

Load the agent from:

```
created_agents/<agent_name>/
```

Read:

* `agent.md`
* `output_format.md`

---

# Agent Registry

List available agents and their purpose.

| Agent        | Description                   |
| ------------ | ----------------------------- |
| essay_writer | Writes essays on given topics |
| recipe_agent | Generates recipes for dishes  |

To add a new agent, add a new row with the agent name and description.

---

# Response Rules

* If no agent is needed → respond directly.
* If an agent is used → follow that agent's instructions and output format.
* If multiple agents are used → execute them sequentially and combine the outputs clearly.

---

# Folder Structure

```
.
├── created_agents
│   ├── essay_writer
│   │   ├── agent.md
│   │   ├── description.md
│   │   └── output_format.md
│   └── recipe_agent
│       ├── agent.md
│       ├── description.md
│       └── output_format.md
└── workflow.md
```
