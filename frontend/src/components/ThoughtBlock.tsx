"use client";

import { SpinnerIcon } from "./icons";

interface ThoughtBlockProps {
  visible: boolean;
  subtitle: string;
  steps: any[];
}

export function ThoughtBlock({ visible, subtitle, steps }: ThoughtBlockProps) {
  if (!visible) return null;
  const renderStep = (step: any, i: number) => {
    if (typeof step === "string") return (
      <div key={i} className="flex gap-2"><span className="text-accent shrink-0">›</span><span>{step}</span></div>
    );
    if (step.type === "started") {
      return (
        <div key={i} className="flex gap-2">
          <span className="text-blue-500 shrink-0">›</span>
          <span className="text-blue-700">Running: <span className="font-semibold">{step.command}</span></span>
        </div>
      );
    }
    if (step.type === "completed") {
      return (
        <div key={i} className="flex gap-2">
          <span className="text-green-500 shrink-0">›</span>
          <span className="text-green-700">Ran: <span className="font-semibold">{step.command}</span>{step.output ? <span> <span className="text-gray-400">→</span> <span className="italic">{step.output}</span></span> : null}</span>
        </div>
      );
    }
    return (
      <div key={i} className="flex gap-2"><span className="text-accent shrink-0">›</span><span>{JSON.stringify(step)}</span></div>
    );
  };
  return (
    <div className="flex gap-4 fade-in" data-purpose="ai-thought-process">
      <div className="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center shrink-0 border border-gray-100">
        <SpinnerIcon className="w-4 h-4 text-gray-400 animate-spin" />
      </div>
      <div className="flex-1 max-w-2xl">
        <div className="bg-gray-50/50 border border-gray-100 rounded-xl overflow-hidden transition-all duration-300">
          <div className="w-full flex items-center justify-between px-4 py-2.5 text-left">
            <div className="flex items-center gap-2.5">
              <span className="text-xs font-medium text-gray-500">Thinking...</span>
              <span className="text-[11px] text-gray-400 italic">{subtitle}</span>
            </div>
          </div>
          <div className="px-4 pb-4 space-y-2 border-t border-gray-100/50 pt-3">
            <div className="font-mono text-[11px] text-gray-500 space-y-1.5">
              {steps.map(renderStep)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
