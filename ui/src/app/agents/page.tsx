"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { BotIcon, MenuIcon, PlusIcon, ChevronLeftIcon } from "@/components/icons";
import { useLayout } from "@/components/Layout";

export default function AgentsPage() {
  const [agents, setAgents] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [newAgentName, setNewAgentName] = useState("");
  const { toggleSidebar } = useLayout();

  const fetchAgents = () => {
    setLoading(true);
    fetch("http://localhost:8000/api/agents")
      .then((res) => res.json())
      .then((data) => {
        setAgents(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch agents:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleCreateAgent = () => {
    if (!newAgentName.trim()) return;
    fetch("http://localhost:8000/api/agents", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newAgentName.trim() }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "ok") {
          setNewAgentName("");
          setCreating(false);
          fetchAgents();
        }
      });
  };

  return (
    <div className="flex-1 flex flex-col min-w-0 bg-white">
      <header className="h-16 flex items-center justify-between px-8 border-b border-gray-50 flex-shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 -ml-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all"
          >
            <MenuIcon className="w-5 h-5" />
          </button>
          <Link
            href="/"
            className="p-2 -ml-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all"
            title="Back to Chat"
          >
            <ChevronLeftIcon className="w-5 h-5" />
          </Link>
          <div className="h-6 w-px bg-gray-100 mx-1" />
          <h1 className="text-xl font-semibold text-gray-800 tracking-tight">Agents</h1>
        </div>
        
        <button
          onClick={() => setCreating(true)}
          className="flex items-center gap-2 px-6 py-2 bg-accent text-white rounded-xl text-sm font-semibold hover:bg-accent-dark transition-all shadow-sm shadow-accent/20 active:scale-95"
        >
          <PlusIcon className="w-4 h-4" />
          Create Agent
        </button>
      </header>
      
      <div className="flex-1 overflow-y-auto p-8 max-w-5xl w-full mx-auto">
        <div className="space-y-4">
          {creating && (
            <div className="p-6 bg-white border-2 border-accent rounded-2xl shadow-lg shadow-accent/5 animate-in fade-in slide-in-from-top-4 duration-300">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                <div className="flex-1">
                  <h3 className="text-base font-semibold text-gray-800">New Agent Name</h3>
                  <input
                    autoFocus
                    type="text"
                    value={newAgentName}
                    onChange={(e) => setNewAgentName(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleCreateAgent()}
                    placeholder="e.g. MySmartAgent"
                    className="w-full mt-3 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleCreateAgent}
                    className="px-6 py-2.5 bg-accent text-white rounded-xl text-sm font-semibold hover:bg-accent-dark transition-colors shadow-sm"
                  >
                    Create Agent
                  </button>
                  <button
                    onClick={() => {
                      setCreating(false);
                      setNewAgentName("");
                    }}
                    className="px-6 py-2.5 bg-gray-100 text-gray-600 rounded-xl text-sm font-semibold hover:bg-gray-200 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}

          {loading ? (
            <div className="flex flex-col items-center justify-center h-64 gap-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent" />
              <span className="text-sm font-medium text-gray-400">Loading agents...</span>
            </div>
          ) : agents.length === 0 && !creating ? (
            <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed border-gray-100 rounded-3xl">
              <div className="w-16 h-16 rounded-full bg-gray-50 flex items-center justify-center mb-4">
                <BotIcon className="w-8 h-8 text-gray-200" />
              </div>
              <h3 className="text-lg font-semibold text-gray-600">No agents yet</h3>
              <p className="text-sm text-gray-400 mt-1">Create your first agent to get started</p>
              <button
                onClick={() => setCreating(true)}
                className="mt-6 px-6 py-2 bg-accent/10 text-accent rounded-xl text-sm font-semibold hover:bg-accent/20 transition-all active:scale-95"
              >
                Create Agent
              </button>
            </div>
          ) : (
            agents.map((agent) => (
              <Link
                key={agent}
                href={`/agents/${agent}`}
                className="group flex items-center justify-between p-5 bg-white border border-gray-100 rounded-2xl hover:border-accent hover:shadow-xl hover:shadow-accent/5 transition-all duration-300"
              >
                <div className="flex items-center gap-5">
                  <div className="w-14 h-14 rounded-2xl bg-gray-50 flex items-center justify-center group-hover:bg-accent/10 transition-colors">
                    <BotIcon className="w-7 h-7 text-gray-400 group-hover:text-accent" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-800 group-hover:text-accent transition-colors">
                      {agent}
                    </h3>
                    <div className="flex items-center gap-3 mt-1">
                      <span className="text-xs font-medium text-gray-400 px-2 py-0.5 bg-gray-50 rounded group-hover:bg-accent/5 transition-colors">Template-based</span>
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-400">Active and ready</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="hidden sm:flex flex-col items-end mr-4">
                    <span className="text-[10px] font-bold text-gray-300 uppercase tracking-widest leading-none mb-1">Status</span>
                    <span className="text-xs font-semibold text-green-500 flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                      Ready
                    </span>
                  </div>
                  <div className="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center group-hover:bg-accent text-gray-400 group-hover:text-white transition-all shadow-sm">
                    <PlusIcon className="w-5 h-5 rotate-45" />
                  </div>
                </div>
              </Link>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
