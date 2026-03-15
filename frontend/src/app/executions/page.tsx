"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  MenuIcon, 
  ChevronLeftIcon, 
  ChevronRightIcon, 
  PlayIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon
} from "@/components/icons";
import { useLayout } from "@/components/Layout";

// ─── Types ────────────────────────────────────────────────────────────────────

interface ExecutionSummary {
  execution_id: string;
  prompt: string;
  status: string;
  started_at: string;
  completed_at: string | null;
  duration_seconds: number | null;
}

interface AgentExecutions {
  agent_name: string;
  execution_count: number;
  executions?: ExecutionSummary[];
  expanded?: boolean;
}

interface ExecutionLog {
  timestamp: string;
  type: string;
  content: string;
  details?: any;
}

interface ExecutionDetail {
  metadata: {
    execution_id: string;
    agent_name: string;
    prompt: string;
    status: string;
    return_code: number | null;
    started_at: string;
    completed_at: string | null;
    duration_seconds: number | null;
  };
  logs: ExecutionLog[];
}

// ─── Utilities ────────────────────────────────────────────────────────────────

function formatTimestamp(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleString();
}

function formatDuration(seconds: number | null): string {
  if (seconds === null) return "N/A";
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}m ${secs}s`;
}

function StatusIcon({ status }: { status: string }) {
  if (status === "completed") {
    return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
  } else if (status === "failed") {
    return <XCircleIcon className="w-5 h-5 text-red-500" />;
  } else {
    return <ClockIcon className="w-5 h-5 text-yellow-500 animate-pulse" />;
  }
}

// ─── Execution Detail Modal ───────────────────────────────────────────────────

interface ExecutionModalProps {
  agentName: string;
  executionId: string;
  onClose: () => void;
}

function ExecutionModal({ agentName, executionId, onClose }: ExecutionModalProps) {
  const [detail, setDetail] = useState<ExecutionDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/api/agent-executions/${agentName}/${executionId}`)
      .then((r) => r.json())
      .then((d) => setDetail(d))
      .catch((err) => console.error("Failed to fetch execution detail:", err))
      .finally(() => setLoading(false));
  }, [agentName, executionId]);

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm animate-in fade-in duration-200"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl mx-4 max-h-[90vh] overflow-hidden flex flex-col animate-in slide-in-from-bottom-6 duration-300"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100 flex-shrink-0">
          <div>
            <h2 className="text-lg font-bold text-gray-800">Execution Details</h2>
            {detail && (
              <p className="text-sm text-gray-500 mt-1">
                {agentName} • {formatTimestamp(detail.metadata.started_at)}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-all"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent" />
            </div>
          )}

          {!loading && detail && (
            <div className="space-y-6">
              {/* Metadata */}
              <div className="bg-gray-50 rounded-xl p-4 space-y-3">
                <div className="flex items-center gap-3">
                  <StatusIcon status={detail.metadata.status} />
                  <span className="font-semibold text-gray-700 capitalize">
                    {detail.metadata.status}
                  </span>
                  {detail.metadata.return_code !== null && (
                    <span className="text-sm text-gray-500">
                      (code: {detail.metadata.return_code})
                    </span>
                  )}
                  <span className="ml-auto text-sm text-gray-500">
                    {formatDuration(detail.metadata.duration_seconds)}
                  </span>
                </div>
                <div>
                  <div className="text-xs font-semibold text-gray-500 uppercase mb-1">
                    Prompt
                  </div>
                  <div className="text-sm text-gray-700">
                    {detail.metadata.prompt}
                  </div>
                </div>
              </div>

              {/* Logs */}
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-3">
                  Execution Logs ({detail.logs.length})
                </h3>
                <div className="bg-gray-900 rounded-xl p-4 space-y-2 max-h-96 overflow-y-auto">
                  {detail.logs.map((log, idx) => (
                    <div key={idx} className="text-xs font-mono">
                      <span className="text-gray-500">
                        [{new Date(log.timestamp).toLocaleTimeString()}]
                      </span>{" "}
                      <span
                        className={
                          log.type === "command_start"
                            ? "text-blue-400"
                            : log.type === "command_complete"
                            ? "text-green-400"
                            : log.type === "message"
                            ? "text-yellow-300"
                            : "text-gray-400"
                        }
                      >
                        [{log.type}]
                      </span>{" "}
                      <span className="text-gray-200">{log.content}</span>
                      {log.details?.output && (
                        <div className="text-gray-400 ml-8 mt-1">
                          → {log.details.output}
                        </div>
                      )}
                    </div>
                  ))}
                  {detail.logs.length === 0 && (
                    <div className="text-gray-500 text-center py-4">
                      No logs recorded
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end px-6 py-4 border-t border-gray-100 flex-shrink-0">
          <button
            onClick={onClose}
            className="px-5 py-2.5 bg-accent text-white rounded-xl text-sm font-semibold hover:bg-accent-dark transition-all"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function ExecutionsPage() {
  const [agents, setAgents] = useState<AgentExecutions[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedExecution, setSelectedExecution] = useState<{
    agent: string;
    id: string;
  } | null>(null);
  const { toggleSidebar } = useLayout();

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = () => {
    setLoading(true);
    fetch("http://localhost:8000/api/agent-executions")
      .then((res) => res.json())
      .then((data) => {
        setAgents(data.map((a: any) => ({ ...a, expanded: false })));
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch executions:", err);
        setLoading(false);
      });
  };

  const toggleAgent = (agentName: string) => {
    const agent = agents.find((a) => a.agent_name === agentName);
    if (!agent) return;

    if (agent.expanded) {
      // Collapse
      setAgents(
        agents.map((a) =>
          a.agent_name === agentName ? { ...a, expanded: false } : a
        )
      );
    } else {
      // Expand and fetch executions
      fetch(`http://localhost:8000/api/agent-executions/${agentName}`)
        .then((res) => res.json())
        .then((data) => {
          setAgents(
            agents.map((a) =>
              a.agent_name === agentName
                ? { ...a, expanded: true, executions: data.executions }
                : a
            )
          );
        })
        .catch((err) => console.error("Failed to fetch agent executions:", err));
    }
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
          <h1 className="text-xl font-semibold text-gray-800 tracking-tight">
            Agent Executions
          </h1>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-8 max-w-5xl w-full mx-auto">
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent" />
          </div>
        )}

        {!loading && agents.length === 0 && (
          <div className="text-center py-12">
            <PlayIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No agent executions yet</p>
            <Link
              href="/agents"
              className="inline-block mt-4 text-accent hover:underline"
            >
              Run an agent to get started
            </Link>
          </div>
        )}

        {!loading && agents.length > 0 && (
          <div className="space-y-3">
            {agents.map((agent) => (
              <div
                key={agent.agent_name}
                className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
              >
                {/* Agent Header */}
                <button
                  onClick={() => toggleAgent(agent.agent_name)}
                  className="w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center">
                      <PlayIcon className="w-5 h-5 text-accent" />
                    </div>
                    <div className="text-left">
                      <h3 className="font-semibold text-gray-800">
                        {agent.agent_name}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {agent.execution_count} execution
                        {agent.execution_count !== 1 ? "s" : ""}
                      </p>
                    </div>
                  </div>
                  <ChevronRightIcon
                    className={`w-5 h-5 text-gray-400 transition-transform ${
                      agent.expanded ? "rotate-90" : ""
                    }`}
                  />
                </button>

                {/* Executions List */}
                {agent.expanded && agent.executions && (
                  <div className="border-t border-gray-100">
                    {agent.executions.map((exec) => (
                      <button
                        key={exec.execution_id}
                        onClick={() =>
                          setSelectedExecution({
                            agent: agent.agent_name,
                            id: exec.execution_id,
                          })
                        }
                        className="w-full flex items-center justify-between px-6 py-3 hover:bg-gray-50 transition-colors text-left border-b border-gray-50 last:border-b-0"
                      >
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <StatusIcon status={exec.status} />
                            <span className="text-sm font-medium text-gray-700 truncate">
                              {exec.prompt}
                            </span>
                          </div>
                          <div className="text-xs text-gray-500">
                            {formatTimestamp(exec.started_at)} •{" "}
                            {formatDuration(exec.duration_seconds)}
                          </div>
                        </div>
                        <ChevronRightIcon className="w-4 h-4 text-gray-400 flex-shrink-0 ml-2" />
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedExecution && (
        <ExecutionModal
          agentName={selectedExecution.agent}
          executionId={selectedExecution.id}
          onClose={() => setSelectedExecution(null)}
        />
      )}
    </div>
  );
}
