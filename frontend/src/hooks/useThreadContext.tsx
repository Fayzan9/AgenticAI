"use client";

import { createContext, useContext, ReactNode, useEffect } from "react";
import { useChat } from "./useChat";

interface ThreadContextType {
  messages: ReturnType<typeof useChat>["messages"];
  streaming: boolean;
  thought: ReturnType<typeof useChat>["thought"];
  sendPrompt: (prompt: string) => Promise<void>;
  currentThreadId: string | null;
  currentThreadTitle: string;
  threadUpdateTrigger: number;
  createNewThread: () => Promise<any>;
  loadThread: (threadId: string) => Promise<any>;
}

const ThreadContext = createContext<ThreadContextType | undefined>(undefined);

export function useThreadContext() {
  const context = useContext(ThreadContext);
  if (!context) {
    throw new Error("useThreadContext must be used within ThreadProvider");
  }
  return context;
}

export function ThreadProvider({ children }: { children: ReactNode }) {
  const chatState = useChat();

  useEffect(() => {
    console.log("ThreadProvider mounted");
    console.log("Current thread ID:", chatState.currentThreadId);
    console.log("Current thread title:", chatState.currentThreadTitle);
  }, [chatState.currentThreadId, chatState.currentThreadTitle]);

  return (
    <ThreadContext.Provider value={chatState}>
      {children}
    </ThreadContext.Provider>
  );
}
