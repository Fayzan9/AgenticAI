"use client";

import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ChatArea } from "@/components/ChatArea";
import { useChat } from "@/hooks/useChat";

export default function Home() {
  const { messages, streaming, thought, sendPrompt } = useChat();

  return (
    <ChatArea
      messages={messages}
      thought={thought}
      streaming={streaming}
      onSendPrompt={sendPrompt}
    />
  );
}
