import React, { useState } from 'react';
import { Send, Bot, User, AlertTriangle, Sparkles, PieChart, Layers } from 'lucide-react';
import QueryTrace from './QueryTrace';

const SUGGESTED_QUERIES = [
  "What is our total revenue in mining sector?",
  "How's our pipeline looking for energy sector this quarter?",
  "Which work orders are delayed?",
  "Which customers generated the most revenue?",
  "Show me pipeline by deal stage"
];

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      sender: 'agent',
      text: "Hello! I am your Monday.com Business Intelligence Agent. Ask me any natural-language question about Skylark Drones' sales pipeline, revenue, delayed work orders, or sectoral performance.",
      isIntro: true
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (queryText) => {
    const q = queryText || input;
    if (!q.trim() || loading) return;

    const userMsg = { sender: 'user', text: q };
    setMessages(prev => [...prev, userMsg]);
    if (!queryText) setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q })
      });
      const data = await res.json();
      
      const agentMsg = {
        sender: 'agent',
        data: data
      };
      setMessages(prev => [...prev, agentMsg]);
    } catch (err) {
      setMessages(prev => [...prev, {
        sender: 'agent',
        error: "I couldn't retrieve the latest Monday.com data. Please try again."
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[680px] rounded-2xl glass-panel border border-slate-800/80 overflow-hidden shadow-2xl">
      
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-800/80 bg-slate-900/60 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold font-heading text-slate-100">BI Conversation Agent</h2>
            <p className="text-xs text-slate-400">Grounded & Deterministic Monday.com BI Intelligence</p>
          </div>
        </div>
      </div>

      {/* Suggested Query Chips */}
      <div className="px-6 py-3 bg-slate-950/40 border-b border-slate-800/60 flex items-center gap-2 overflow-x-auto no-scrollbar">
        <Sparkles className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
        <span className="text-xs text-slate-400 font-medium shrink-0">Try asking:</span>
        {SUGGESTED_QUERIES.map((sq, i) => (
          <button 
            key={i} 
            onClick={() => handleSend(sq)}
            className="px-3 py-1 bg-slate-800/60 hover:bg-indigo-600/30 hover:border-indigo-500/50 border border-slate-700/60 rounded-full text-xs text-slate-300 transition shrink-0"
          >
            {sq}
          </button>
        ))}
      </div>

      {/* Messages Scroll View */}
      <div className="flex-1 p-6 overflow-y-auto space-y-6">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {m.sender === 'agent' && (
              <div className="w-8 h-8 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-indigo-400" />
              </div>
            )}

            <div className={`max-w-[82%] ${m.sender === 'user' ? 'bg-indigo-600/90 text-white rounded-2xl rounded-tr-none px-4 py-3 shadow-lg' : 'space-y-3'}`}>
              {m.sender === 'user' ? (
                <p className="text-sm">{m.text}</p>
              ) : m.isIntro ? (
                <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 text-sm text-slate-200">
                  {m.text}
                </div>
              ) : m.error ? (
                <div className="bg-rose-950/40 border border-rose-800/60 rounded-2xl p-4 text-sm text-rose-300">
                  {m.error}
                </div>
              ) : (
                <div className="bg-slate-900/90 border border-slate-800/90 rounded-2xl p-5 shadow-xl text-sm text-slate-200 space-y-4">
                  
                  {/* Direct Answer */}
                  <div className="p-4 bg-indigo-950/40 border-l-4 border-indigo-500 rounded-r-xl">
                    <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">Direct Answer</div>
                    <p className="text-slate-100 leading-relaxed text-sm font-medium">{m.data.direct_answer}</p>
                  </div>

                  {/* Clarification prompt if any */}
                  {m.data.intent?.needs_clarification && (
                    <div className="flex items-center gap-2 text-xs text-indigo-300 bg-indigo-900/30 p-3 rounded-lg border border-indigo-700/40">
                      <Sparkles className="w-4 h-4 text-indigo-400" />
                      <span>{m.data.intent.clarification_question}</span>
                    </div>
                  )}

                  {/* Contextual Insights */}
                  {m.data.insights?.length > 0 && (
                    <div className="space-y-2">
                      <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <PieChart className="w-3.5 h-3.5 text-cyan-400" /> Key Insights & Supporting Metrics
                      </div>
                      <ul className="space-y-1.5 pl-1">
                        {m.data.insights.map((ins, i) => (
                          <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                            <span className="text-cyan-400 font-bold">•</span>
                            <span>{ins}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Data Quality Warning Note */}
                  {m.data.data_notes?.length > 0 && (
                    <div className="p-3 bg-amber-950/20 border border-amber-500/30 rounded-xl text-xs text-amber-300 flex items-start gap-2">
                      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                      <div>
                        <span className="font-semibold block mb-0.5">Data Quality Note:</span>
                        {m.data.data_notes.map((note, nIdx) => (
                          <div key={nIdx}>• {note}</div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Trace Execution View */}
                  <QueryTrace trace={m.data.execution_trace} />

                </div>
              )}
            </div>

            {m.sender === 'user' && (
              <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
                <User className="w-4 h-4 text-slate-300" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 text-xs text-slate-400 flex items-center gap-3">
              <div className="animate-spin w-4 h-4 border-2 border-indigo-500 border-t-transparent rounded-full"></div>
              Parsing Intent & Executing Deterministic Monday Math...
            </div>
          </div>
        )}
      </div>

      {/* Input Box */}
      <div className="p-4 bg-slate-900/80 border-t border-slate-800">
        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a business query (e.g. What is our revenue in mining sector?)"
            className="flex-1 query-input rounded-xl px-4 py-3 text-sm transition"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="glow-button px-5 py-3 text-white rounded-xl font-medium text-sm flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
            <span>Ask</span>
          </button>
        </form>
      </div>

    </div>
  );
}
