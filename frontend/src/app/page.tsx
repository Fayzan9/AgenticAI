"use client";

import { ChatArea } from "@/components/ChatArea";
import { useThreadContext } from "@/hooks/useThreadContext";

export default function Home() {
  const {
    messages,
    streaming,
    thought,
    sendPrompt,
    currentThreadTitle,
    currentThreadId,
    createNewThread
  } = useThreadContext();

  const handleUpload = async (files: File[]) => {
    let threadId = currentThreadId;

    if (!threadId) {
      const thread = await createNewThread();
      if (thread) {
        threadId = thread.id;
      }
    }

    if (!threadId) return;

    const formData = new FormData();
    formData.append("thread_id", threadId);

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const res = await fetch("http://localhost:8000/api/uploads", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to upload files");
      }

      console.log("Files uploaded successfully");
    } catch (error) {
      console.error("Error uploading files:", error);
    }
  };

  return (
    <ChatArea
      chatTitle={currentThreadTitle}
      messages={messages}
      thought={thought}
      streaming={streaming}
      onSendPrompt={sendPrompt}
      onUpload={handleUpload}
    />
  );
}
