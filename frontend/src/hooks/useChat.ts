"use client";

import { useCallback, useState, useEffect } from "react";
import { createThread, getThread } from "@/lib/api";

export type Message =
  | { role: "user"; text: string }
  | { role: "assistant"; text: string; thinkingLogs?: any[] };

export interface ThoughtState {
  visible: boolean;
  subtitle: string;
  steps: any[];
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null);
  const [currentThreadTitle, setCurrentThreadTitle] = useState<string>("New Chat");
  const [threadUpdateTrigger, setThreadUpdateTrigger] = useState(0);
  const [thought, setThought] = useState<ThoughtState>({
    visible: false,
    subtitle: "Running Codex",
    steps: [],
  });

  const createNewThread = useCallback(async () => {
    try {
      console.log("Creating new thread...");
      const thread = await createThread();
      console.log("Thread created:", thread.id);
      setCurrentThreadId(thread.id);
      setCurrentThreadTitle(thread.title);
      setMessages([]);
      setThreadUpdateTrigger(prev => prev + 1);
      return thread;
    } catch (error) {
      console.error("Failed to create thread:", error);
      return null;
    }
  }, []);

  const loadThread = useCallback(async (threadId: string) => {
    try {
      console.log("Loading thread:", threadId);
      const thread = await getThread(threadId);
      console.log("Thread loaded:", thread.title, "messages:", thread.messages.length);
      setCurrentThreadId(thread.id);
      setCurrentThreadTitle(thread.title);
      setThreadUpdateTrigger(prev => prev + 1);
      setMessages(
        thread.messages.map((m) =>
          m.role === "assistant"
            ? ({ role: "assistant", text: m.text, thinkingLogs: m.thinking_logs ?? [] } as Message)
            : ({ role: "user", text: m.text } as Message)
        )
      );
      return thread;
    } catch (error) {
      console.error("Failed to load thread:", error);
      return null;
    }
  }, []);

  const sendPrompt = useCallback(async (prompt: string) => {
    const trimmed = prompt.trim();
    if (!trimmed || streaming) return;

    // Create thread if doesn't exist
    let threadId = currentThreadId;
    if (!threadId) {
      const thread = await createNewThread();
      if (thread) {
        threadId = thread.id;
      }
    }

    setStreaming(true);
    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
    // Hide the ThoughtBlock before starting a new process
    setThought({ visible: false, subtitle: "Running Codex", steps: [] });
    // Show it again as soon as streaming starts
    setTimeout(() => setThought({ visible: true, subtitle: "Running Codex", steps: [] }), 0);

    let currentAssistantText = "";
    let currentThoughtSteps: any[] = [];

    try {
      console.log("Sending message to thread:", threadId);
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: trimmed, thread_id: threadId }),
      });
      console.log("Chat request sent, response status:", res.status);
      if (!res.ok) throw new Error(res.statusText);

      const reader = res.body!.getReader();
      const dec = new TextDecoder();
      let buf = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const parts = buf.split("\n\n");
        buf = parts.pop() ?? "";
        for (const part of parts) {
          const m = part.match(/^data:\s*(.+)/m);
          if (!m) continue;
          try {
            const data = JSON.parse(m[1]);
            if (data.type === "returncode") continue;
            if (data.stream !== "stdout" || !data.data) continue;
            const event = JSON.parse(data.data);
            if (event.type === "item.completed" && event.item) {
              const it = event.item;
              if (it.type === "agent_message" && it.text) {
                // Keep only the latest assistant message as the final answer.
                currentAssistantText = it.text;
              } else if (it.type === "command_execution") {
                const cmd = it.command ?? "";
                const out = (it.aggregated_output ?? "").slice(0, 80);
                const logObj = { type: "completed", command: cmd, output: out };
                currentThoughtSteps = [...currentThoughtSteps, logObj];
                setThought((t) => ({
                  ...t,
                  steps: [...t.steps, logObj],
                }));
              }
            } else if (event.type === "item.started" && event.item?.type === "command_execution") {
              const cmd = (event.item.command ?? "").replace(/^\/bin\/\w+ -lc '\|'$/g, "").slice(0, 50);
              const logObj = { type: "started", command: event.item?.command ?? "" };
              currentThoughtSteps = [...currentThoughtSteps, logObj];
              setThought((t) => ({
                ...t,
                subtitle: "Running: " + cmd,
                steps: [...t.steps, logObj],
              }));
            }
          } catch {
            // ignore parse errors
          }
        }
      }

      if (currentAssistantText) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", text: currentAssistantText, thinkingLogs: currentThoughtSteps },
        ]);
      }

      // Reload thread to get updated title
      if (threadId) {
        console.log("Reloading thread after message completion:", threadId);
        const thread = await getThread(threadId);
        if (thread) {
          console.log("Thread title updated:", thread.title);
          setThreadUpdateTrigger(prev => prev + 1);
          setCurrentThreadTitle(thread.title);
        }
      }
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Error: " + (e instanceof Error ? e.message : String(e)) },
      ]);
    } finally {
      // Hide the global ThoughtBlock after response; trace is already shown in the assistant message
      setThought({ visible: false, subtitle: "Running Codex", steps: [] });
      setStreaming(false);
    }
  }, [streaming, currentThreadId, createNewThread]);

  return { 
    messages, 
    streaming, 
    thought, 
    sendPrompt, 
    currentThreadId, 
    threadUpdateTrigger,
    currentThreadTitle,
    createNewThread, 
    loadThread 
  };
}
