"use client";

import { useState, useEffect } from "react";
import { getConfig, updateConfig, getWorkflowFiles, updateWorkflowFile, ConfigValue, WorkflowFile } from "@/lib/api";

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<"config" | "workflow">("config");
  const [configs, setConfigs] = useState<ConfigValue>({});
  const [workflowFiles, setWorkflowFiles] = useState<WorkflowFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [configData, workflowData] = await Promise.all([
        getConfig(),
        getWorkflowFiles(),
      ]);
      setConfigs(configData);
      setWorkflowFiles(workflowData);
    } catch (error) {
      showMessage("error", "Failed to load settings");
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (type: "success" | "error", text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 3000);
  };

  const handleConfigUpdate = async (key: string, value: any) => {
    try {
      setSaving(true);
      await updateConfig(key, value);
      setConfigs({ ...configs, [key]: value });
      showMessage("success", "Configuration updated successfully");
    } catch (error) {
      showMessage("error", "Failed to update configuration");
    } finally {
      setSaving(false);
    }
  };

  const handleWorkflowUpdate = async (filename: string, content: string) => {
    try {
      setSaving(true);
      await updateWorkflowFile(filename, content);
      setWorkflowFiles(
        workflowFiles.map((file) =>
          file.name === filename ? { ...file, content } : file
        )
      );
      showMessage("success", "Workflow file updated successfully");
    } catch (error) {
      showMessage("error", "Failed to update workflow file");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">Loading settings...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-8 py-6">
        <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
        <p className="text-sm text-gray-500 mt-1">
          Manage your application configuration and workflow templates
        </p>
      </div>

      {/* Notification */}
      {message && (
        <div
          className={`mx-8 mt-4 p-4 rounded-lg ${
            message.type === "success"
              ? "bg-green-50 text-green-800 border border-green-200"
              : "bg-red-50 text-red-800 border border-red-200"
          }`}
        >
          {message.text}
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200 px-8">
        <div className="flex space-x-8">
          <button
            onClick={() => setActiveTab("config")}
            className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === "config"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Configuration
          </button>
          <button
            onClick={() => setActiveTab("workflow")}
            className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === "workflow"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Workflow Templates
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto px-8 py-6">
        {activeTab === "config" ? (
          <ConfigEditor
            configs={configs}
            onUpdate={handleConfigUpdate}
            saving={saving}
          />
        ) : (
          <WorkflowEditor
            files={workflowFiles}
            onUpdate={handleWorkflowUpdate}
            saving={saving}
          />
        )}
      </div>
    </div>
  );
}

interface ConfigEditorProps {
  configs: ConfigValue;
  onUpdate: (key: string, value: any) => void;
  saving: boolean;
}

function ConfigEditor({ configs, onUpdate, saving }: ConfigEditorProps) {
  const [editingKey, setEditingKey] = useState<string | null>(null);
  const [editValue, setEditValue] = useState<string>("");

  const handleEdit = (key: string, value: any) => {
    setEditingKey(key);
    setEditValue(typeof value === "string" ? value : JSON.stringify(value, null, 2));
  };

  const handleSave = () => {
    if (!editingKey) return;

    try {
      // Try to parse as JSON, otherwise use as string
      let parsedValue;
      try {
        parsedValue = JSON.parse(editValue);
      } catch {
        parsedValue = editValue;
      }

      onUpdate(editingKey, parsedValue);
      setEditingKey(null);
    } catch (error) {
      alert("Invalid value format");
    }
  };

  const handleCancel = () => {
    setEditingKey(null);
  };

  const isLargeValue = (value: any) => {
    const str = typeof value === "string" ? value : JSON.stringify(value);
    return str.length > 100 || str.includes("\n");
  };

  return (
    <div className="max-w-4xl">
      <div className="space-y-4">
        {Object.entries(configs).map(([key, value]) => (
          <div key={key} className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-900">{key}</h3>
              {editingKey !== key && (
                <button
                  onClick={() => handleEdit(key, value)}
                  disabled={saving}
                  className="text-sm text-blue-600 hover:text-blue-700 font-medium disabled:opacity-50"
                >
                  Edit
                </button>
              )}
            </div>

            {editingKey === key ? (
              <div className="space-y-3">
                {isLargeValue(value) ? (
                  <textarea
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    rows={15}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                ) : (
                  <input
                    type="text"
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                )}
                <div className="flex space-x-3">
                  <button
                    onClick={handleSave}
                    disabled={saving}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
                  >
                    {saving ? "Saving..." : "Save"}
                  </button>
                  <button
                    onClick={handleCancel}
                    disabled={saving}
                    className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 disabled:opacity-50"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-sm text-gray-600">
                {isLargeValue(value) ? (
                  <pre className="bg-gray-50 p-3 rounded border border-gray-200 overflow-auto max-h-40 font-mono text-xs">
                    {typeof value === "string" ? value : JSON.stringify(value, null, 2)}
                  </pre>
                ) : (
                  <code className="bg-gray-50 px-2 py-1 rounded font-mono text-xs">
                    {typeof value === "string" ? value : JSON.stringify(value)}
                  </code>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

interface WorkflowEditorProps {
  files: WorkflowFile[];
  onUpdate: (filename: string, content: string) => void;
  saving: boolean;
}

function WorkflowEditor({ files, onUpdate, saving }: WorkflowEditorProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(
    files.length > 0 ? files[0].name : null
  );
  const [editContent, setEditContent] = useState<string>("");
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (selectedFile) {
      const file = files.find((f) => f.name === selectedFile);
      if (file) {
        setEditContent(file.content);
      }
    }
  }, [selectedFile, files]);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    if (selectedFile) {
      onUpdate(selectedFile, editContent);
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    const file = files.find((f) => f.name === selectedFile);
    if (file) {
      setEditContent(file.content);
    }
    setIsEditing(false);
  };

  const currentFile = files.find((f) => f.name === selectedFile);

  return (
    <div className="max-w-6xl">
      <div className="grid grid-cols-4 gap-6">
        {/* File list */}
        <div className="col-span-1">
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
              <h3 className="text-sm font-semibold text-gray-900">Files</h3>
            </div>
            <div className="divide-y divide-gray-200">
              {files.map((file) => (
                <button
                  key={file.name}
                  onClick={() => {
                    setSelectedFile(file.name);
                    setIsEditing(false);
                  }}
                  className={`w-full px-4 py-3 text-left text-sm hover:bg-gray-50 transition-colors ${
                    selectedFile === file.name
                      ? "bg-blue-50 text-blue-700 font-medium"
                      : "text-gray-700"
                  }`}
                >
                  <div className="truncate">{file.name}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* File editor */}
        <div className="col-span-3">
          {currentFile ? (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  {currentFile.name}
                </h3>
                {!isEditing && (
                  <button
                    onClick={handleEdit}
                    disabled={saving}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
                  >
                    Edit
                  </button>
                )}
              </div>

              {isEditing ? (
                <div className="space-y-3">
                  <textarea
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                    rows={25}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="flex space-x-3">
                    <button
                      onClick={handleSave}
                      disabled={saving}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
                    >
                      {saving ? "Saving..." : "Save Changes"}
                    </button>
                    <button
                      onClick={handleCancel}
                      disabled={saving}
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 disabled:opacity-50"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <pre className="bg-gray-50 p-4 rounded-lg border border-gray-200 overflow-auto font-mono text-sm text-gray-800 max-h-[600px]">
                  {currentFile.content}
                </pre>
              )}
            </div>
          ) : (
            <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
              <p className="text-gray-500">Select a file to view or edit</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
