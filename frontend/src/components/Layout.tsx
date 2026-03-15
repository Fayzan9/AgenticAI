"use client";

import { useState, createContext, useContext } from "react";
import { Sidebar } from "./Sidebar";
import { ThreadProvider, useThreadContext } from "@/hooks/useThreadContext";

interface LayoutContextType {
  sidebarCollapsed: boolean;
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleSidebar: () => void;
}

const LayoutContext = createContext<LayoutContextType | undefined>(undefined);

export function useLayout() {
  const context = useContext(LayoutContext);
  if (!context) {
    throw new Error("useLayout must be used within a LayoutProvider");
  }
  return context;
}

function LayoutInner({ children }: { children: React.ReactNode }) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const { createNewThread, loadThread, currentThreadId, threadUpdateTrigger } = useThreadContext();

  const toggleSidebar = () => setSidebarCollapsed((prev) => !prev);

  const handleNewChat = async () => {
    setSidebarCollapsed(false);
    await createNewThread();
  };

  const handleThreadClick = async (threadId: string) => {
    await loadThread(threadId);
  };

  return (
    <LayoutContext.Provider value={{ sidebarCollapsed, setSidebarCollapsed, toggleSidebar }}>
      <div className="flex h-screen w-full overflow-hidden" data-purpose="app-root">
        <Sidebar
          collapsed={sidebarCollapsed}
          onNewChat={handleNewChat}
          onThreadClick={handleThreadClick}
          currentThreadId={currentThreadId}
          refreshTrigger={threadUpdateTrigger}
        />
        <main className="flex-1 flex flex-col min-w-0 bg-white relative overflow-hidden transition-all duration-300 ease-in-out">
          {children}
        </main>
      </div>
    </LayoutContext.Provider>
  );
}

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <ThreadProvider>
      <LayoutInner>{children}</LayoutInner>
    </ThreadProvider>
  );
}
