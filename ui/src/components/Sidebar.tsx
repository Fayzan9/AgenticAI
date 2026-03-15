"use client";

import { PlusIcon, SettingsIcon, BotIcon } from "./icons";
import Link from "next/link";
import { usePathname } from "next/navigation";

const RECENT_CHATS = [
  { title: "Project Brainstorming", preview: "How should we approach..." },
  { title: "Technical Roadmap", preview: "Discussing the architecture..." },
  { title: "Code Review Refactor", preview: "Optimizing the main loop..." },
];

interface SidebarProps {
  collapsed: boolean;
  onNewChat?: () => void;
}

export function Sidebar({ collapsed, onNewChat }: SidebarProps) {
  const pathname = usePathname();
  return (
    <aside
      className="sidebar-transition h-full bg-gray-50 border-r border-gray-100 flex flex-col shrink-0 overflow-hidden"
      style={{ width: collapsed ? 0 : "18rem" }}
      data-purpose="navigation-sidebar"
    >
      <div className={`${collapsed ? "opacity-0 pointer-events-none" : ""} w-72 flex flex-col h-full min-w-0`}>
        <div className="p-4">
          <button
            type="button"
            onClick={onNewChat}
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
          {RECENT_CHATS.map((chat, i) => (
            <button
              key={chat.title}
              type="button"
              className={`w-full flex flex-col text-left px-3 py-3 rounded-lg transition-all group ${
                i === 0 ? "bg-white border border-gray-200 shadow-sm" : "hover:bg-gray-100"
              }`}
            >
              <span className={`text-sm font-medium truncate ${i === 0 ? "text-gray-800" : "text-gray-700"}`}>
                {chat.title}
              </span>
              <span className="text-xs text-gray-400 truncate">{chat.preview}</span>
            </button>
          ))}
        </div>
        <div className="p-4 border-t border-gray-100 space-y-1" data-purpose="quick-actions">
          <Link
            href="/agents"
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
              pathname === "/agents" ? "bg-gray-200 text-gray-900" : "text-gray-600 hover:bg-gray-200"
            }`}
          >
            <BotIcon className="w-5 h-5 text-gray-400" />
            <span>Agents</span>
          </Link>
          <button
            type="button"
            className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <SettingsIcon className="w-5 h-5 text-gray-400" />
            <span>Settings</span>
          </button>
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
