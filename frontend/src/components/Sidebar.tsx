"use client";

import { PlusIcon, SettingsIcon, BotIcon, TrashIcon, ClockIcon } from "./icons";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { getThreads, deleteThread, Thread } from "@/lib/api";

interface SidebarProps {
  collapsed: boolean;
  onNewChat?: () => void;
  onThreadClick?: (threadId: string) => void;
  currentThreadId?: string | null;
  refreshTrigger?: number;
}

export function Sidebar({
  collapsed,
  onNewChat,
  onThreadClick,
  currentThreadId,
  refreshTrigger,
}: SidebarProps) {
  const pathname = usePathname();
  const [threads, setThreads] = useState<Thread[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadThreads();
  }, [refreshTrigger]);

  const loadThreads = async () => {
    try {
      setLoading(true);
      const fetchedThreads = await getThreads();
      setThreads(fetchedThreads);
    } catch (error) {
      console.error("Failed to load threads:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = async () => {
    if (onNewChat) {
      await onNewChat();
    }
  };

  const handleThreadClick = (threadId: string) => {
    if (onThreadClick) {
      onThreadClick(threadId);
    }
  };

  const handleDeleteThread = async (
    e: React.MouseEvent,
    threadId: string
  ) => {
    e.stopPropagation();

    const confirmed = confirm("Delete this conversation?");
    if (!confirmed) return;

    try {
      await deleteThread(threadId);

      // optimistic update
      setThreads((prev) => prev.filter((t) => t.id !== threadId));
    } catch (error) {
      console.error("Failed to delete thread:", error);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return "Today";
    if (days === 1) return "Yesterday";
    if (days < 7) return `${days} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <aside
      className="sidebar-transition h-full bg-gray-50 border-r border-gray-100 flex flex-col shrink-0 overflow-hidden"
      style={{ width: collapsed ? 0 : "18rem" }}
      data-purpose="navigation-sidebar"
    >
      <div
        className={`${collapsed ? "opacity-0 pointer-events-none" : ""} w-72 flex flex-col h-full min-w-0`}
      >
        <div className="p-4">
          <button
            type="button"
            onClick={handleNewChat}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-100 transition-colors shadow-sm"
          >
            <PlusIcon className="w-4 h-4" />
            <span>New Chat</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3 space-y-1" data-purpose="recent-chats">
          <p className="px-3 py-2 text-[10px] font-semibold text-gray-400 uppercase tracking-widest">
            Recent Chats
          </p>

          {loading ? (
            <div className="px-3 py-4 text-xs text-gray-400 text-center">
              Loading threads...
            </div>
          ) : threads.length === 0 ? (
            <div className="px-3 py-4 text-xs text-gray-400 text-center">
              No conversations yet
            </div>
          ) : (
            threads.map((thread) => (
              <div
                key={thread.id}
                className={`w-full flex items-center justify-between px-3 py-3 rounded-lg transition-all group ${
                  currentThreadId === thread.id
                    ? "bg-white border border-gray-200 shadow-sm"
                    : "hover:bg-gray-100"
                }`}
              >
                <button
                  type="button"
                  onClick={() => handleThreadClick(thread.id)}
                  className="flex flex-col text-left flex-1"
                >
                  <span
                    className={`text-sm font-medium truncate ${
                      currentThreadId === thread.id
                        ? "text-gray-800"
                        : "text-gray-700"
                    }`}
                  >
                    {thread.title}
                  </span>

                  <span className="text-xs text-gray-400 truncate">
                    {formatDate(thread.updated_at)}
                  </span>
                </button>

                <button
                  onClick={(e) => handleDeleteThread(e, thread.id)}
                  className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-50 transition"
                >
                  <TrashIcon className="w-4 h-4 text-gray-400 hover:text-red-500" />
                </button>
              </div>
            ))
          )}
        </div>

        <div className="p-4 border-t border-gray-100 space-y-1" data-purpose="quick-actions">
          <Link
            href="/agents"
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
              pathname === "/agents"
                ? "bg-gray-200 text-gray-900"
                : "text-gray-600 hover:bg-gray-200"
            }`}
          >
            <BotIcon className="w-5 h-5 text-gray-400" />
            <span>Agents</span>
          </Link>

          <Link
            href="/executions"
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
              pathname === "/executions"
                ? "bg-gray-200 text-gray-900"
                : "text-gray-600 hover:bg-gray-200"
            }`}
          >
            <ClockIcon className="w-5 h-5 text-gray-400" />
            <span>Executions</span>
          </Link>

          <Link
            href="/settings"
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
              pathname === "/settings"
                ? "bg-gray-200 text-gray-900"
                : "text-gray-600 hover:bg-gray-200"
            }`}
          >
            <SettingsIcon className="w-5 h-5 text-gray-400" />
            <span>Settings</span>
          </Link>

          <button
            type="button"
            className="w-full flex items-center justify-between px-3 py-2 text-sm text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-accent/10 flex items-center justify-center text-[10px] font-bold text-accent">
                JD
              </div>
              <span>Profile</span>
            </div>
          </button>
        </div>
      </div>
    </aside>
  );
}