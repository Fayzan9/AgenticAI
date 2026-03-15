"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { BotIcon, MenuIcon, PlusIcon, ChevronLeftIcon, PlayIcon, XIcon } from "@/components/icons";
import { useLayout } from "@/components/Layout";

// ─── Run Modal ────────────────────────────────────────────────────────────────

interface RunModalProps {
  agentId: string;
  onClose: () => void;
}

function RunModal({ agentId, onClose }: RunModalProps) {
  const [prompt, setPrompt] = useState("");
  const [inputHtml, setInputHtml] = useState<string | null>(null);
  const [loadingForm, setLoadingForm] = useState(true);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);

  // Fetch the agent's optional input.html
  useEffect(() => {
    fetch(`http://localhost:8000/api/agents/${agentId}/input-form`)
      .then((r) => r.json())
      .then((d) => setInputHtml(d.html ?? null))
      .catch(() => setInputHtml(null))
      .finally(() => setLoadingForm(false));
  }, [agentId]);

  // Write HTML into the iframe so it inherits no external styles
  useEffect(() => {
    if (!inputHtml || !iframeRef.current) return;
    const doc = iframeRef.current.contentDocument;
    if (!doc) return;
    doc.open();
    doc.write(inputHtml);
    doc.close();

    // Auto-resize the iframe to fit its content
    const resize = () => {
      if (iframeRef.current && doc.body) {
        iframeRef.current.style.height = doc.body.scrollHeight + "px";
      }
    };
    // Give the iframe a moment to render, then resize
    setTimeout(resize, 100);
  }, [inputHtml]);

  // Close on backdrop click
  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === overlayRef.current) onClose();
  };

  // Close on Escape key
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const handleRun = () => {
    // TODO: wire up actual run logic
    console.log("Running agent:", agentId, "with prompt:", prompt);
    onClose();
  };

  return (
    <div
      ref={overlayRef}
      onClick={handleOverlayClick}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm animate-in fade-in duration-200"
    >
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-xl mx-4 max-h-[90vh] overflow-y-auto animate-in slide-in-from-bottom-6 duration-300">
        {/* Header */}
        <div className="flex items-center justify-between px-6 pt-6 pb-4 border-b border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-accent/10 flex items-center justify-center">
              <PlayIcon className="w-4 h-4 text-accent ml-0.5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-gray-800">Run Agent</h2>
              <p className="text-xs text-gray-400 font-medium">{agentId}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-all"
          >
            <XIcon className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-5 space-y-5">
          {/* Prompt */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Prompt
            </label>
            <textarea
              autoFocus
              rows={4}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe what you want this agent to do…"
              className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all resize-none"
            />
          </div>

          {/* Additional Inputs (input.html) */}
          {!loadingForm && inputHtml && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <div className="h-px flex-1 bg-gray-100" />
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                  Additional Inputs
                </span>
                <div className="h-px flex-1 bg-gray-100" />
              </div>
              <div className="rounded-xl border border-gray-100 overflow-hidden">
                <iframe
                  ref={iframeRef}
                  title="Agent Input Form"
                  className="w-full border-0"
                  style={{ minHeight: "120px" }}
                  sandbox="allow-forms allow-scripts allow-same-origin"
                />
              </div>
            </div>
          )}

          {/* Loading state for form */}
          {loadingForm && (
            <div className="flex items-center justify-center py-4">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-accent" />
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 pb-6">
          <button
            onClick={onClose}
            className="px-5 py-2.5 bg-gray-100 text-gray-600 rounded-xl text-sm font-semibold hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleRun}
            disabled={!prompt.trim()}
            className="flex items-center gap-2 px-6 py-2.5 bg-accent text-white rounded-xl text-sm font-semibold hover:bg-accent-dark transition-all shadow-sm shadow-accent/20 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed disabled:active:scale-100"
          >
            <PlayIcon className="w-4 h-4" />
            Run Agent
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Agents Page ──────────────────────────────────────────────────────────────

export default function AgentsPage() {
  const [agents, setAgents] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [newAgentName, setNewAgentName] = useState("");
  const [runningAgent, setRunningAgent] = useState<string | null>(null);
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
              <div
                key={agent}
                className="group flex items-center justify-between p-5 bg-white border border-gray-100 rounded-2xl hover:border-accent hover:shadow-xl hover:shadow-accent/5 transition-all duration-300"
              >
                {/* Left: bot icon + name — clicking navigates to editor */}
                <Link
                  href={`/agents/${agent}`}
                  className="flex items-center gap-5 flex-1 min-w-0"
                >
                  <div className="w-14 h-14 rounded-2xl bg-gray-50 flex items-center justify-center group-hover:bg-accent/10 transition-colors flex-shrink-0">
                    <BotIcon className="w-7 h-7 text-gray-400 group-hover:text-accent" />
                  </div>
                  <div className="min-w-0">
                    <h3 className="text-lg font-bold text-gray-800 group-hover:text-accent transition-colors truncate">
                      {agent}
                    </h3>
                    <div className="flex items-center gap-3 mt-1">
                      <span className="text-xs font-medium text-gray-400 px-2 py-0.5 bg-gray-50 rounded group-hover:bg-accent/5 transition-colors">
                        Template-based
                      </span>
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-400">Active and ready</span>
                    </div>
                  </div>
                </Link>

                {/* Right: status + run button */}
                <div className="flex items-center gap-3 ml-4 flex-shrink-0">
                  <div className="hidden sm:flex flex-col items-end mr-2">
                    <span className="text-[10px] font-bold text-gray-300 uppercase tracking-widest leading-none mb-1">
                      Status
                    </span>
                    <span className="text-xs font-semibold text-green-500 flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                      Ready
                    </span>
                  </div>

                  {/* Run button */}
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      setRunningAgent(agent);
                    }}
                    className="flex items-center gap-2 px-4 py-2 bg-accent/10 text-accent rounded-xl text-sm font-semibold hover:bg-accent hover:text-white transition-all active:scale-95 shadow-sm"
                    title="Run agent"
                  >
                    <PlayIcon className="w-4 h-4" />
                    <span className="hidden sm:inline">Run</span>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Run modal */}
      {runningAgent && (
        <RunModal agentId={runningAgent} onClose={() => setRunningAgent(null)} />
      )}
    </div>
  );
}
