"use client";

import { useEffect, useState, use, useMemo, useRef } from "react";
import { FolderIcon, FileIcon, BotIcon, MenuIcon, PlusIcon, TrashIcon, ChevronLeftIcon, PencilIcon } from "@/components/icons";
import { useLayout } from "@/components/Layout";
import Link from "next/link";

interface FileNode {
  name: string;
  path: string;
  type: "file" | "directory";
  children?: FileNode[];
}

export default function AgentEditPage({ params }: { params: Promise<{ agentId: string }> }) {
  const { agentId } = use(params);
  const { toggleSidebar } = useLayout();
  
  // States
  const [files, setFiles] = useState<FileNode[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  const [managementAction, setManagementAction] = useState<{ type: "file" | "folder" | "rename"; path: string } | null>(null);
  const [newPathName, setNewPathName] = useState("");
  const [explorerWidth, setExplorerWidth] = useState(260);
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; node: FileNode | null } | null>(null);
  const [resizing, setResizing] = useState(false);
  const [saveStatus, setSaveStatus] = useState<"saved" | "saving" | "unsaved">("saved");
  const [isRenamingAgent, setIsRenamingAgent] = useState(false);
  const [tempAgentName, setTempAgentName] = useState(agentId);
  /** In-session edits: path -> content. Persisted in browser until "Save Changes". */
  const [sessionEdits, setSessionEdits] = useState<Record<string, string>>({});

  // Refs
  const isResizing = useRef(false);
  const explorerRef = useRef<HTMLDivElement>(null);

  const toggleFolder = (path: string) => {
    setExpandedFolders((prev) => {
      const next = new Set(prev);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return next;
    });
  };

  useEffect(() => {
    fetchFiles();

    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing.current || !explorerRef.current) return;
      const containerLeft = explorerRef.current.getBoundingClientRect().left;
      const newWidth = Math.max(160, Math.min(600, e.clientX - containerLeft));
      setExplorerWidth(newWidth);
    };

    const handleMouseUp = () => {
      isResizing.current = false;
      setResizing(false);
      document.body.style.cursor = "default";
      document.body.style.userSelect = "auto";
    };

    const handleClickOutside = () => setContextMenu(null);

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    window.addEventListener("click", handleClickOutside);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      window.removeEventListener("click", handleClickOutside);
    };
  }, [agentId]);

  // Derive unsaved state from session edits (manual save only; no auto-save)
  const hasUnsavedEdits = Object.keys(sessionEdits).length > 0;
  useEffect(() => {
    setSaveStatus(hasUnsavedEdits ? "unsaved" : "saved");
  }, [hasUnsavedEdits]);

  const fetchFiles = () => {
    fetch(`http://localhost:8000/api/agents/${agentId}/files`)
      .then((res) => res.json())
      .then((data) => {
        setFiles(data);
        setLoading(false);
      });
  };

  const loadFileContent = (path: string) => {
    // Persist current file's content to session edits before switching
    if (selectedFile) {
      setSessionEdits((prev) => ({ ...prev, [selectedFile]: fileContent }));
    }
    setSelectedFile(path);
    const edited = sessionEdits[path];
    if (edited !== undefined) {
      setFileContent(edited);
      return;
    }
    fetch(`http://localhost:8000/api/agents/${agentId}/files/${path}`)
      .then((res) => res.json())
      .then((data) => {
        setFileContent(data.content);
      });
  };

  /** Save all in-session edits to the server at once (manual save). */
  const saveAllChanges = () => {
    const paths = Object.keys(sessionEdits);
    if (paths.length === 0) return;
    setSaving(true);
    setSaveStatus("saving");
    Promise.all(
      paths.map((filePath) =>
        fetch(`http://localhost:8000/api/agents/${agentId}/files/${filePath}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: sessionEdits[filePath] }),
        })
      )
    )
      .then((results) => {
        const allOk = results.every((r) => r.ok);
        if (allOk) {
          setSessionEdits({});
          setSaveStatus("saved");
        } else {
          setSaveStatus("unsaved");
        }
        setSaving(false);
      })
      .catch(() => {
        setSaving(false);
        setSaveStatus("unsaved");
      });
  };

  const handleAgentRename = () => {
    const trimmedName = tempAgentName.trim();
    if (!trimmedName || trimmedName === agentId) {
      setIsRenamingAgent(false);
      return;
    }

    fetch(`http://localhost:8000/api/agents/${agentId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: trimmedName }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "ok") {
          window.location.href = `/agents/${data.name}`;
        } else {
          setIsRenamingAgent(false);
          setTempAgentName(agentId);
        }
      });
  };

  const handleManagePath = () => {
    if (!managementAction || !newPathName.trim()) return;
    
    if (managementAction.type === "rename") {
      const oldPath = managementAction.path;
      const parts = oldPath.split("/");
      parts[parts.length - 1] = newPathName.trim();
      const newPath = parts.join("/");

      fetch(`http://localhost:8000/api/agents/${agentId}/files/rename`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ old_path: oldPath, new_path: newPath }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status === "ok") {
            if (selectedFile === oldPath) setSelectedFile(newPath);
            setSessionEdits((prev) => {
              if (prev[oldPath] === undefined) return prev;
              const next = { ...prev };
              next[newPath] = next[oldPath];
              delete next[oldPath];
              return next;
            });
            setNewPathName("");
            setManagementAction(null);
            fetchFiles();
          }
        });
      return;
    }

    const path = managementAction.path ? `${managementAction.path}/${newPathName.trim()}` : newPathName.trim();
    fetch(`http://localhost:8000/api/agents/${agentId}/files/manage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        path,
        type: managementAction.type === "folder" ? "directory" : "file",
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "ok") {
          setNewPathName("");
          setManagementAction(null);
          // If we added inside a folder, expand it
          if (managementAction.path) {
            setExpandedFolders(prev => new Set(Array.from(prev).concat(managementAction.path)));
          }
          fetchFiles();
        }
      });
  };

  const handleDeletePath = (path: string) => {
    fetch(`http://localhost:8000/api/agents/${agentId}/files/${path}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "ok") {
          if (selectedFile === path) setSelectedFile(null);
          fetchFiles();
        }
      });
  };

  const filteredFiles = useMemo(() => {
    const filter = (nodes: FileNode[]): FileNode[] => {
      return nodes
        .map((node) => ({ ...node }))
        .filter((node) => {
          if (node.type === "directory" && node.children) {
            node.children = filter(node.children);
            return node.children.length > 0 || node.name.toLowerCase().includes(searchQuery.toLowerCase());
          }
          return node.name.toLowerCase().includes(searchQuery.toLowerCase());
        });
    };
    return filter(files);
  }, [files, searchQuery]);

  const renderFileExplorer = (nodes: FileNode[], depth = 0) => {
    return (
      <div className="space-y-0.5">
        {nodes.map((node) => {
          const isExpanded = expandedFolders.has(node.path) || searchQuery.length > 0;
          const isInlineRenaming = managementAction?.type === "rename" && managementAction?.path === node.path;
          
          return (
            <div key={node.path}>
              {isInlineRenaming ? (
                <div 
                  className="flex items-center gap-2 px-3 py-1.5"
                  style={{ paddingLeft: `${depth * 1.5 + 0.75}rem` }}
                >
                  {node.type === "directory" ? <FolderIcon className="w-4 h-4 text-accent" /> : <FileIcon className="w-4 h-4 text-accent" />}
                  <input
                    autoFocus
                    className="flex-1 bg-white border border-accent rounded px-1.5 py-0.5 text-sm focus:outline-none"
                    value={newPathName}
                    onChange={(e) => setNewPathName(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleManagePath();
                      if (e.key === "Escape") setManagementAction(null);
                    }}
                    onBlur={() => setManagementAction(null)}
                  />
                </div>
              ) : (
                <button
                  onClick={() => node.type === "file" ? loadFileContent(node.path) : toggleFolder(node.path)}
                  onDoubleClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    setManagementAction({ type: "rename", path: node.path });
                    setNewPathName(node.name);
                  }}
                  onContextMenu={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    setContextMenu({ x: e.clientX, y: e.clientY, node });
                  }}
                  className={`w-full flex items-center gap-2 px-3 py-1.5 text-sm rounded-lg transition-colors group ${
                    selectedFile === node.path ? "bg-accent/10 text-accent font-medium" : "text-gray-600 hover:bg-gray-50"
                  }`}
                  style={{ paddingLeft: `${depth * 1.5 + 0.75}rem` }}
                >
                  {node.type === "directory" ? (
                    <div className="flex items-center gap-1.5 min-w-0">
                      <svg
                        className={`w-3 h-3 text-gray-400 transition-transform ${isExpanded ? "rotate-90" : ""}`}
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} />
                      </svg>
                      <FolderIcon className="w-4 h-4 text-gray-400" />
                    </div>
                  ) : (
                    <FileIcon className="w-4 h-4 text-gray-400 group-hover:text-accent ml-4" />
                  )}
                  <span className="truncate">{node.name}</span>
                </button>
              )}
              
              {node.type === "directory" && managementAction?.type !== "rename" && managementAction?.path === node.path && (
                <div 
                  className="flex items-center gap-2 px-3 py-1.5"
                  style={{ paddingLeft: `${(depth + 1) * 1.5 + 0.75}rem` }}
                >
                  {managementAction.type === "folder" ? <FolderIcon className="w-4 h-4 text-accent" /> : <FileIcon className="w-4 h-4 text-accent" />}
                  <input
                    autoFocus
                    className="flex-1 bg-white border border-accent rounded px-1.5 py-0.5 text-sm focus:outline-none"
                    placeholder={`New ${managementAction.type}...`}
                    value={newPathName}
                    onChange={(e) => setNewPathName(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleManagePath();
                      if (e.key === "Escape") setManagementAction(null);
                    }}
                    onBlur={() => setManagementAction(null)}
                  />
                </div>
              )}
              
              {node.type === "directory" && node.children && isExpanded && renderFileExplorer(node.children, depth + 1)}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full bg-white">
      <header className="h-16 flex items-center justify-between px-8 border-b border-gray-50 shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 -ml-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all"
          >
            <MenuIcon className="w-5 h-5" />
          </button>
          <Link
            href="/agents"
            className="p-2 -ml-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all"
            title="Back to Agents"
          >
            <ChevronLeftIcon className="w-5 h-5" />
          </Link>
          <div className="h-6 w-px bg-gray-100 mx-1" />
          <div className="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center">
            <BotIcon className="w-5 h-5 text-gray-400" />
          </div>
          
          {isRenamingAgent ? (
            <input
              autoFocus
              className="text-sm font-semibold text-gray-700 bg-white border border-accent rounded px-2 py-0.5 focus:outline-none"
              value={tempAgentName}
              onChange={(e) => setTempAgentName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleAgentRename();
                if (e.key === "Escape") { setIsRenamingAgent(false); setTempAgentName(agentId); }
              }}
              onBlur={handleAgentRename}
            />
          ) : (
            <h1 
              onDoubleClick={() => setIsRenamingAgent(true)}
              className="text-sm font-semibold text-gray-700 truncate cursor-pointer hover:text-accent transition-colors"
              title="Double click to rename agent"
            >
              {agentId}
            </h1>
          )}
        </div>
        <div className="flex items-center gap-3">
          <div className="text-xs font-medium text-gray-400 mr-2 flex items-center gap-2">
            {saveStatus === "saving" && (
              <>
                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse" />
                Saving...
              </>
            )}
            {saveStatus === "saved" && (
              <>
                <div className="w-2 h-2 bg-green-500 rounded-full" />
                All changes saved
              </>
            )}
            {saveStatus === "unsaved" && (
              <>
                <div className="w-2 h-2 bg-gray-300 rounded-full" />
                Unsaved changes
              </>
            )}
          </div>
        </div>
      </header>

      <div className="flex-1 flex min-h-0">
        <aside 
          ref={explorerRef}
          className="border-r border-gray-100 flex flex-col bg-gray-50/30 overflow-hidden shrink-0 relative"
          style={{ width: explorerWidth }}
        >
          <div className="p-4 border-b border-gray-50 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">File Explorer</span>
            </div>
            <div className="relative">
              <input
                type="text"
                placeholder="Search files..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs focus:outline-none focus:ring-1 focus:ring-accent transition-all"
              />
              <svg
                className="w-3.5 h-3.5 text-gray-400 absolute left-2.5 top-1/2 -translate-y-1/2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} />
              </svg>
            </div>
          </div>
          <div 
            className="flex-1 overflow-y-auto p-2"
            onDoubleClick={(e) => {
              if (e.target === e.currentTarget) {
                e.preventDefault();
                setContextMenu({ x: e.clientX, y: e.clientY, node: null });
              }
            }}
            onContextMenu={(e) => {
              if (e.target === e.currentTarget) {
                e.preventDefault();
                setContextMenu({ x: e.clientX, y: e.clientY, node: null });
              }
            }}
          >
            {managementAction && managementAction.path === "" && (
              <div className="px-3 py-2 border-b border-gray-100 bg-gray-50/50 mb-2 rounded-lg">
                <div className="text-[10px] font-bold text-accent uppercase mb-2">
                  New {managementAction.type}
                </div>
                <input
                  autoFocus
                  type="text"
                  placeholder="Name..."
                  value={newPathName}
                  onChange={(e) => setNewPathName(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleManagePath()}
                  className="w-full px-2 py-1 bg-white border border-gray-200 rounded text-xs focus:outline-none focus:border-accent"
                />
              </div>
            )}
            {loading ? (
              <div className="flex items-center justify-center py-10">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-900" />
              </div>
            ) : (
              renderFileExplorer(filteredFiles)
            )}
          </div>

          {/* Save Status & Button (optional for quick save) */}
          {selectedFile && (
            <div className="p-4 border-t border-gray-50 bg-white">
              <button
                onClick={saveAllChanges}
                disabled={saving || !hasUnsavedEdits}
                className={`w-full h-10 rounded-xl text-sm font-semibold transition-all shadow-sm active:scale-[0.98] flex items-center justify-center gap-2 ${
                  !hasUnsavedEdits
                    ? "bg-gray-50 text-gray-400 border border-gray-100 cursor-default"
                    : "bg-accent text-white hover:bg-accent-dark"
                }`}
              >
                {saveStatus === "saving" && (
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                )}
                {saveStatus === "saving" ? "Saving..." : saveStatus === "saved" ? "Saved" : "Save Changes"}
              </button>
            </div>
          )}

          {/* Resize Handle */}
          <div
            className={`absolute top-0 right-0 w-1 px-0.5 h-full cursor-col-resize hover:bg-accent/40 transition-colors z-[60] ${resizing ? 'bg-accent/50' : ''}`}
            onMouseDown={(e) => {
              e.preventDefault();
              isResizing.current = true;
              setResizing(true);
              document.body.style.cursor = "col-resize";
              document.body.style.userSelect = "none";
            }}
          />
        </aside>

        {/* Resize Overlay to capture mouse moves during dragging */}
        {resizing && (
          <div 
            className="fixed inset-0 z-[1000] cursor-col-resize"
            style={{ userSelect: 'none' }}
          />
        )}

        <main className="flex-1 flex flex-col bg-white">
          {selectedFile ? (
            <div className="flex-1 flex flex-col">
              <div className="px-6 py-2 border-b border-gray-50 bg-gray-50/50 flex items-center justify-between">
                <span className="text-xs font-mono text-gray-400">{selectedFile}</span>
                <span className="text-[10px] font-bold text-accent uppercase tracking-wider bg-accent/10 px-2 py-0.5 rounded">
                  Live Editing
                </span>
              </div>
              <textarea
                value={fileContent}
                onChange={(e) => {
                  const v = e.target.value;
                  setFileContent(v);
                  if (selectedFile) {
                    setSessionEdits((prev) => ({ ...prev, [selectedFile]: v }));
                  }
                }}
                className="flex-1 w-full p-8 font-mono text-sm text-gray-800 focus:outline-none resize-none leading-relaxed bg-white"
                spellCheck={false}
                placeholder="Start typing..."
              />
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-gray-400">
              <FileIcon className="w-12 h-12 mb-4 opacity-10" />
              <p className="text-sm">Select a file from the explorer to begin editing</p>
            </div>
          )}
        </main>
      </div>

      {/* Context Menu */}
      {contextMenu && (
        <div 
          className="fixed bg-white border border-gray-200 rounded-xl shadow-2xl py-1.5 z-[100] min-w-[160px] animate-in fade-in zoom-in duration-100"
          style={{ top: contextMenu.y, left: contextMenu.x }}
          onClick={(e) => e.stopPropagation()}
        >
          {!contextMenu.node ? (
            <>
              <button
                onClick={() => { setManagementAction({ type: "file", path: "" }); setNewPathName(""); setContextMenu(null); }}
                className="w-full text-left px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-50 flex items-center gap-2"
              >
                <FileIcon className="w-3.5 h-3.5" />
                New File
              </button>
              <button
                onClick={() => { setManagementAction({ type: "folder", path: "" }); setNewPathName(""); setContextMenu(null); }}
                className="w-full text-left px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-50 flex items-center gap-2"
              >
                <FolderIcon className="w-3.5 h-3.5" />
                New Folder
              </button>
            </>
          ) : (
            <>
              {contextMenu.node.type === "directory" && (
                <>
                  <button
                    onClick={() => { setManagementAction({ type: "file", path: contextMenu.node!.path }); setNewPathName(""); setContextMenu(null); }}
                    className="w-full text-left px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-50 flex items-center gap-2"
                  >
                    <FileIcon className="w-3.5 h-3.5" />
                    New File
                  </button>
                  <button
                    onClick={() => { setManagementAction({ type: "folder", path: contextMenu.node!.path }); setNewPathName(""); setContextMenu(null); }}
                    className="w-full text-left px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-50 flex items-center gap-2"
                  >
                    <FolderIcon className="w-3.5 h-3.5" />
                    New Folder
                  </button>
                  <div className="my-1 border-t border-gray-100" />
                </>
              )}
              {contextMenu.node.type === "file" && (
                <button
                  onClick={() => { loadFileContent(contextMenu.node!.path); setContextMenu(null); }}
                  className="w-full text-left px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-50 flex items-center gap-2"
                >
                  <FileIcon className="w-3.5 h-3.5" />
                  Open File
                </button>
              )}
              <button
                onClick={() => { setManagementAction({ type: "rename", path: contextMenu.node!.path }); setNewPathName(contextMenu.node!.name); setContextMenu(null); }}
                className="w-full text-left px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-50 flex items-center gap-2"
              >
                <PencilIcon className="w-3.5 h-3.5" />
                Rename
              </button>
              <button
                onClick={() => { handleDeletePath(contextMenu.node!.path); setContextMenu(null); }}
                className="w-full text-left px-4 py-1.5 text-xs text-red-500 hover:bg-red-50 flex items-center gap-2"
              >
                <TrashIcon className="w-3.5 h-3.5" />
                Delete
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
