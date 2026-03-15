"use client";

import { useRef, useEffect, useState } from "react";
import { PaperclipIcon, SendIcon, XIcon } from "./icons";

interface ChatInputProps {
  onSend: (text: string) => void;
  onUpload?: (files: File[]) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({ onSend, onUpload, disabled, placeholder = "Ask anything..." }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleSend = () => {
    const el = textareaRef.current;
    if (!el) return;
    const text = el.value.trim();
    
    if (disabled) return;
    if (!text && selectedFiles.length === 0) return;

    if (selectedFiles.length > 0 && onUpload) {
      onUpload(selectedFiles);
      setSelectedFiles([]);
    }

    if (text) {
      onSend(text);
      el.value = "";
      el.style.height = "auto";
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFiles(prev => [...prev, ...Array.from(e.target.files!)]);
      e.target.value = "";
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
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
        
        {/* File Previews */}
        {selectedFiles.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-2 relative z-10 px-2">
            {selectedFiles.map((file, i) => (
              <div key={i} className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-lg px-2 py-1 text-xs text-gray-600">
                <span className="truncate max-w-[150px]">{file.name}</span>
                <button 
                  onClick={() => removeFile(i)}
                  className="p-0.5 hover:bg-gray-200 rounded-full transition-colors"
                >
                  <XIcon className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="relative bg-white border border-gray-200 rounded-2xl shadow-sm flex flex-col focus-within:border-accent/40 transition-all">
          <div className="flex items-center px-4 py-3">
            <input 
              type="file" 
              ref={fileInputRef} 
              className="hidden" 
              multiple 
              onChange={handleFileChange} 
            />
            <button
              type="button"
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Attach"
              onClick={() => fileInputRef.current?.click()}
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
              disabled={disabled || (!textareaRef.current?.value.trim() && selectedFiles.length === 0)}
              className="ml-2 w-10 h-10 bg-accent text-white rounded-xl flex items-center justify-center hover:bg-accent/90 transition-all shadow-lg shadow-accent/20 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="Send"
            >
              <SendIcon className="w-5 h-5" />
            </button>
          </div>
        </div>
        <p className="text-[10px] text-center text-gray-400 mt-3 font-medium">
          AI can make mistakes. Verify important information.
        </p>
      </div>
    </div>
  );
}
