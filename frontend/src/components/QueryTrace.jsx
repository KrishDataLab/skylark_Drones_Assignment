import React, { useState } from 'react';
import { Terminal, ChevronDown, ChevronRight, CheckCircle2 } from 'lucide-react';

export default function QueryTrace({ trace }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!trace || trace.length === 0) return null;

  return (
    <div className="mt-3 border border-slate-800 rounded-lg overflow-hidden glass-panel">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-2 bg-slate-900/60 hover:bg-slate-900 flex items-center justify-between text-xs text-slate-400 font-mono transition-colors"
      >
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <span>Agent Execution Trace ({trace.length} steps)</span>
        </div>
        {isOpen ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
      </button>

      {isOpen && (
        <div className="p-3 bg-slate-950/80 font-mono text-xs text-slate-300 space-y-1 border-t border-slate-800/80">
          {trace.map((step, idx) => (
            <div key={idx} className="flex items-start gap-2 py-0.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
              <span>{step}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
