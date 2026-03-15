# Workflow Router

This file is the entry point for all user requests.

The system receives:

- user_request
- thread_id

---

## Step 1 — Load Conversation History

Conversation history must be loaded using:

from services.history_loader import load_history

history = load_history(thread_id)

Do not access conversation files directly.

---

## Step 2 — Analyze Request

Determine:

- the user's intent
- whether the request requires specialized processing
- whether multiple tasks exist

---

## Step 3 — Decide Execution Path

### Case 1 — Direct Response

If the request is simple or conversational:

Respond directly using:
- user_request
- conversation history

No agents should be loaded.

---

### Case 2 — Agent Required

If the task requires specialized processing:

Load the agent execution workflow:

agents/agent_execution.md