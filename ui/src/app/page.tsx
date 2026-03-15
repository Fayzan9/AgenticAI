"use client";

import { ChatArea } from "@/components/ChatArea";
import { useThreadContext } from "@/hooks/useThreadContext";

export default function Home() {
  const { 
    messages, 
    streaming, 
    thought, 
    sendPrompt, 
    currentThreadTitle
  } = useThreadContext();

  return (
    <ChatArea
      chatTitle={currentThreadTitle}
      messages={messages}
      thought={thought}
      streaming={streaming}
      onSendPrompt={sendPrompt}
    />
  );
}
