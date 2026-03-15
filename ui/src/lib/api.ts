/**
 * api.ts: API client for thread management
 */

export interface Message {
  role: string;
  text: string;
  thinking_logs?: string[];
  timestamp: string;
}

export interface Thread {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

export interface ThreadListResponse {
  threads: Thread[];
}

/**
 * Create a new thread
 */
export async function createThread(title: string = "New Chat"): Promise<Thread> {
  console.log("[API] Creating thread with title:", title);
  const response = await fetch("/api/threads", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error("[API] Failed to create thread:", response.status, errorText);
    throw new Error(`Failed to create thread: ${response.statusText}`);
  }

  const thread = await response.json();
  console.log("[API] Thread created:", thread.id);
  return thread;
}

/**
 * Get all threads
 */
export async function getThreads(): Promise<Thread[]> {
  console.log("[API] Fetching threads...");
  const response = await fetch("/api/threads");

  if (!response.ok) {
    const errorText = await response.text();
    console.error("[API] Failed to fetch threads:", response.status, errorText);
    throw new Error(`Failed to fetch threads: ${response.statusText}`);
  }

  const data: ThreadListResponse = await response.json();
  console.log("[API] Fetched", data.threads.length, "threads");
  return data.threads;
}

/**
 * Get a specific thread by ID
 */
export async function getThread(threadId: string): Promise<Thread> {
  const response = await fetch(`/api/threads/${threadId}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch thread: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Add a message to a thread
 */
export async function addMessageToThread(
  threadId: string,
  role: string,
  text: string
): Promise<Thread> {
  const response = await fetch(`/api/threads/${threadId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role, text }),
  });

  if (!response.ok) {
    throw new Error(`Failed to add message: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Delete a thread
 */
export async function deleteThread(threadId: string): Promise<void> {
  const response = await fetch(`/api/threads/${threadId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Failed to delete thread: ${response.statusText}`);
  }
}
