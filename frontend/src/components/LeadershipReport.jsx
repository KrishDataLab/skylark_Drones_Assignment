import React, { useState } from 'react';
import { FileText, Copy, Download, X, Check } from 'lucide-react';

export default function LeadershipReport({ isOpen, onClose }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/export/leadership-update');
      const data = await res.json();
      setReport(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    if (isOpen && !report) {
      fetchReport();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const copyToClipboard = () => {
    if (report?.markdown_content) {
      navigator.clipboard.writeText(report.markdown_content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl w-full max-w-3xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden glass-panel">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/80">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold font-heading text-slate-100">Executive Leadership Update Report</h2>
              <p className="text-xs text-slate-400">One-click synthesized summary for board meetings and updates</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto flex-1 font-sans text-sm text-slate-300 space-y-4">
          {loading ? (
            <div className="py-12 text-center text-slate-400">
              <div className="animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto mb-3"></div>
              Generating Executive Leadership Report...
            </div>
          ) : (
            <pre className="whitespace-pre-wrap font-sans bg-slate-950/60 p-4 rounded-xl border border-slate-800 text-slate-200 leading-relaxed">
              {report?.markdown_content}
            </pre>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-slate-800 bg-slate-900/80">
          <span className="text-xs text-slate-400">Formatted in Markdown</span>
          <div className="flex items-center gap-3">
            <button 
              onClick={copyToClipboard}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium flex items-center gap-2 transition"
            >
              {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              {copied ? "Copied!" : "Copy Report"}
            </button>
            <button 
              onClick={onClose}
              className="px-4 py-2 glow-button text-white rounded-lg text-xs font-medium"
            >
              Done
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
