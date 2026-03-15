"use client";

import { useRef, useEffect } from "react";
import { PaperclipIcon, SendIcon } from "./icons";

interface ChatInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({ onSend, disabled, placeholder = "Ask anything..." }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const el = textareaRef.current;
    if (!el) return;
    const text = el.value.trim();
    if (!text || disabled) return;
    onSend(text);
    el.value = "";
    el.style.height = "auto";
  };

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    const onInput = () => {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + "px";
    };
    el.addEventListener("input", onInput);
    return () => el.removeEventListener("input", onInput);
  }, []);

  return (
    <div className="p-6 md:pb-10 bg-white" data-purpose="input-container">
      <div className="max-w-3xl mx-auto relative group">
        <div className="absolute inset-0 bg-gray-100 rounded-2xl blur-sm opacity-0 group-focus-within:opacity-40 transition-opacity" />
        <div className="relative bg-white border border-gray-200 rounded-2xl shadow-sm flex items-center px-4 py-3 focus-within:border-accent/40 transition-all">
          <button
            type="button"
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Attach"
          >
            <PaperclipIcon className="w-5 h-5" />
          </button>
          <textarea
            ref={textareaRef}
            disabled={disabled}
            placeholder={placeholder}
            rows={1}
            className="flex-1 border-none focus:ring-0 text-sm py-2 resize-none bg-transparent placeholder-gray-400 min-h-[40px] max-h-[200px]"
            style={{ minHeight: 40, maxHeight: 200 }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button
            type="button"
            onClick={handleSend}
            disabled={disabled}
            className="ml-2 w-10 h-10 bg-accent text-white rounded-xl flex items-center justify-center hover:bg-accent/90 transition-all shadow-lg shadow-accent/20 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Send"
          >
            <SendIcon className="w-5 h-5" />
          </button>
        </div>
        <p className="text-[10px] text-center text-gray-400 mt-3 font-medium">
          AI can make mistakes. Verify important information.
        </p>
      </div>
    </div>
  );
}
