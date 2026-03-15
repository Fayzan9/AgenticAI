"use client";

import { useState, createContext, useContext } from "react";
import { Sidebar } from "./Sidebar";

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

export function Layout({ children }: { children: React.ReactNode }) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const toggleSidebar = () => setSidebarCollapsed((prev) => !prev);

  return (
    <LayoutContext.Provider value={{ sidebarCollapsed, setSidebarCollapsed, toggleSidebar }}>
      <div className="flex h-full w-full overflow-hidden" data-purpose="app-root">
        <Sidebar
          collapsed={sidebarCollapsed}
          onNewChat={() => {
            setSidebarCollapsed(false);
            window.location.href = "/";
          }}
        />
        <main className="flex-1 flex flex-col min-w-0 bg-white relative transition-all duration-300 ease-in-out">
          {children}
        </main>
      </div>
    </LayoutContext.Provider>
  );
}
