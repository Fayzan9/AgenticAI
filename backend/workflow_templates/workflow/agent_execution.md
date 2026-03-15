# Agent Execution Workflow

This workflow runs when the router determines that an agent is required.

---

## Step 1 — Discover Available Agents

Agents exist inside:

created_agents/

Each folder represents a single agent.

Example:

created_agents/
   agent_1/
   agent_2/
   agent_3/

---

## Step 2 — Read Agent Descriptions

For each candidate agent read only:

created_agents/<agent_name>/description.md

Use this file to determine if the agent is appropriate.

Do not read other files yet.

---

## Step 3 — Select Agent

Choose the agent whose description best matches the task.

---

## Step 4 — Load Agent Instructions

Once an agent is selected, load:

created_agents/<agent_name>/agent.md  
created_agents/<agent_name>/output_format.md

---

## Step 5 — Execute Agent

Follow instructions in `agent.md`.

Generate output using the format defined in `outputs/output.md`.

---

## Step 6 — Multi-Agent Tasks

If multiple agents are required:

1. determine execution order
2. run agents sequentially
3. pass output from one agent to the next