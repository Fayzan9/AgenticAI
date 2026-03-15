export function UserMessage({ text }: { text: string }) {
  return (
    <div className="flex gap-4 flex-row-reverse fade-in">
      <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center shrink-0">
        <span className="text-[10px] font-bold text-white">You</span>
      </div>
      <div className="space-y-2 max-w-2xl text-right">
        <div className="inline-block text-sm bg-gray-50 border border-gray-100 px-4 py-2.5 rounded-2xl text-gray-800 leading-relaxed text-left">
          {text}
        </div>
      </div>
    </div>
  );
}
