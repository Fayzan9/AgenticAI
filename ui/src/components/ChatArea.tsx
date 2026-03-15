"use client";

import { useRef, useEffect } from "react";
import { MenuIcon } from "./icons";
import { WelcomeMessage } from "./WelcomeMessage";
import { UserMessage } from "./UserMessage";
import { AssistantMessage } from "./AssistantMessage";
import { ThoughtBlock } from "./ThoughtBlock";
import { ChatInput } from "./ChatInput";
import type { Message } from "@/hooks/useChat";
import type { ThoughtState } from "@/hooks/useChat";
import { useLayout } from "@/components/Layout";

interface ChatAreaProps {
  chatTitle?: string;
  messages: Message[];
  thought: ThoughtState;
  streaming: boolean;
  onSendPrompt: (text: string) => void;
}

export function ChatArea({
  chatTitle = "Project Brainstorming",
  messages,
  thought,
  streaming,
  onSendPrompt,
}: ChatAreaProps) {
  const { toggleSidebar } = useLayout();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, thought.visible]);

  return (
    <main className="flex-1 flex flex-col relative bg-white min-w-0 h-full" data-purpose="chat-interface">
      <header className="h-16 flex items-center justify-between px-6 border-b border-gray-50 shrink-0">
        <div className="flex items-center gap-3">
          <button
            type="button"
            aria-label="Toggle Sidebar"
            onClick={toggleSidebar}
            className="p-2 -ml-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all"
          >
            <MenuIcon className="w-5 h-5" />
          </button>
          <h1 className="text-sm font-semibold text-gray-700">{chatTitle}</h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-xs text-gray-400 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-green-400" />
            System Ready
          </span>
        </div>
      </header>

      <section
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 max-w-4xl mx-auto w-full pb-28 md:pb-36"
        data-purpose="chat-messages"
      >
        {messages.length === 0 && <WelcomeMessage />}
        {messages.map((msg, i) =>
          msg.role === "user" ? (
            <UserMessage key={i} text={msg.text} />
          ) : (
            <AssistantMessage key={i} text={msg.text} thinkingLogs={msg.thinkingLogs} />
          )
        )}
        <ThoughtBlock visible={thought.visible} subtitle={thought.subtitle} steps={thought.steps} />
      </section>

      <div className="sticky bottom-0 left-0 right-0 bg-white z-10 border-t border-gray-100">
        <ChatInput onSend={onSendPrompt} disabled={streaming} />
      </div>
    </main>
  );
}
