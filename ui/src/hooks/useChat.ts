"use client";

import { useCallback, useState } from "react";

export type Message = { role: "user"; text: string } | { role: "assistant"; text: string };

export interface ThoughtState {
  visible: boolean;
  subtitle: string;
  steps: string[];
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [thought, setThought] = useState<ThoughtState>({
    visible: false,
    subtitle: "Running Codex",
    steps: [],
  });

  const sendPrompt = useCallback(async (prompt: string) => {
    const trimmed = prompt.trim();
    if (!trimmed || streaming) return;

    setStreaming(true);
    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
    setThought({ visible: true, subtitle: "Running Codex", steps: [] });

    let currentAssistantText = "";

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: trimmed }),
      });
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
            if (data.stream !== "stdout" || !data.line) continue;
            const event = JSON.parse(data.line);
            if (event.type === "item.completed" && event.item) {
              const it = event.item;
              if (it.type === "agent_message" && it.text) {
                currentAssistantText = (currentAssistantText ? currentAssistantText + "\n\n" : "") + it.text;
              }
            } else if (event.type === "item.completed" && event.item?.type === "command_execution") {
              const cmd = event.item.command ?? "";
              const out = (event.item.aggregated_output ?? "").slice(0, 80);
              setThought((t) => ({
                ...t,
                steps: [...t.steps, "Ran: " + cmd + (out ? " → " + out : "")],
              }));
            } else if (event.type === "item.started" && event.item?.type === "command_execution") {
              const cmd = (event.item.command ?? "").replace(/^\/bin\/\w+ -lc '|'$/g, "").slice(0, 50);
              setThought((t) => ({
                ...t,
                subtitle: "Running: " + cmd,
                steps: [...t.steps, "Running: " + (event.item?.command ?? "").slice(0, 60)],
              }));
            }
          } catch {
            // ignore parse errors
          }
        }
      }

      if (currentAssistantText) {
        setMessages((prev) => [...prev, { role: "assistant", text: currentAssistantText }]);
      }
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Error: " + (e instanceof Error ? e.message : String(e)) },
      ]);
    } finally {
      setThought((t) => ({ ...t, visible: false }));
      setStreaming(false);
    }
  }, [streaming]);

  return { messages, streaming, thought, sendPrompt };
}
