import { SparkIcon } from "./icons";

export function WelcomeMessage() {
  return (
    <div className="flex gap-4 fade-in" id="welcome-msg">
      <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center shrink-0">
        <SparkIcon className="w-5 h-5 text-gray-500" />
      </div>
      <div className="space-y-2 max-w-2xl">
        <div className="text-sm text-gray-800 leading-relaxed">
          Hello! I&apos;m your Codex assistant. Send a prompt and I&apos;ll run it in your workspace (e.g.
          list files, edit code, run commands).
        </div>
      </div>
    </div>
  );
}
