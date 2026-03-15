import { SparkIcon } from "./icons";

export function AssistantMessage({ text, thinkingLogs = [] }: { text: string; thinkingLogs?: any[] }) {
  // Render structured logs
  const renderLog = (log: any, i: number) => {
    if (typeof log === "string") return <div key={i} className="font-mono text-[11px] text-gray-500 break-words">{log}</div>;
    if (log.type === "started") {
      return (
        <div key={i} className="font-mono text-[11px] text-gray-500 break-words">
          <span className="text-accent">›</span> <span>Running: <span className="font-semibold">{log.command}</span></span>
        </div>
      );
    }
    if (log.type === "completed") {
      return (
        <div key={i} className="font-mono text-[11px] text-gray-500 break-words">
          <span className="text-accent">›</span> <span>Ran: <span className="font-semibold">{log.command}</span>{log.output ? <span> <span className="text-gray-400">→</span> <span className="italic">{log.output}</span></span> : null}</span>
        </div>
      );
    }
    return <div key={i} className="font-mono text-[11px] text-gray-500 break-words">{JSON.stringify(log)}</div>;
  };
  return (
    <div className="flex gap-4 fade-in">
      <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center shrink-0">
        <SparkIcon className="w-5 h-5 text-gray-500" />
      </div>
      <div className="space-y-2 max-w-2xl">
        {thinkingLogs.length > 0 && (
          <details className="bg-gray-50/60 border border-gray-100 rounded-lg px-3 py-2">
            <summary className="text-xs font-medium text-gray-500 cursor-pointer select-none">
              Trace ({thinkingLogs.length} logs)
            </summary>
            <div className="mt-2 space-y-1.5">
              {thinkingLogs.map(renderLog)}
            </div>
          </details>
        )}
        <div className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{text}</div>
      </div>
    </div>
  );
}
