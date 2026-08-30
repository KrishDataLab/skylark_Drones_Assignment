import React, { useState, useEffect } from 'react';
import { Activity, FileText, Database, ShieldCheck } from 'lucide-react';
import MetricCards from './components/MetricCards';
import ChatInterface from './components/ChatInterface';
import LeadershipReport from './components/LeadershipReport';

const INITIAL_SUMMARY_METRICS = {
  total_revenue_excl_gst: 211649409.21,
  total_pipeline_value: 688152293.17,
  open_deals_count: 49,
  open_deals: 49,
  delayed_count: 1,
  delayed_work_orders: 1,
  weighted_pipeline_value: 268356618.51
};

export default function App() {
  const [health, setHealth] = useState(null);
  const [summaryMetrics, setSummaryMetrics] = useState(INITIAL_SUMMARY_METRICS);
  const [isReportOpen, setIsReportOpen] = useState(false);

  useEffect(() => {
    // Fetch Health
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(err => console.error(err));

    // Fetch initial summary metrics from BI agent engine
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'general summary' })
    })
      .then(res => res.json())
      .then(data => {
        if (data.key_numbers && data.key_numbers.total_revenue_excl_gst) {
          setSummaryMetrics(data.key_numbers);
        }
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="min-h-screen flex flex-col p-4 md:p-8 max-w-7xl mx-auto">
      
      {/* Top Navbar */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8 pb-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <Activity className="w-6 h-6 text-slate-950 font-bold" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-heading tracking-tight text-white flex items-center gap-2">
              Skylark Drones <span className="text-indigo-400 font-normal text-base">| Monday.com BI Agent</span>
            </h1>
            <p className="text-xs text-slate-400">Founder Business Intelligence & Operational Decision Engine</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Health Badge */}
          <div className="px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs flex items-center gap-2 text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Mode: {health?.monday_integration?.mode === 'live_graphql' ? 'Monday GraphQL API' : 'Seed Data Layer'}</span>
          </div>

          {/* Leadership Report Trigger */}
          <button 
            onClick={() => setIsReportOpen(true)}
            className="px-4 py-2 bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition"
          >
            <FileText className="w-4 h-4 text-indigo-400" />
            <span>Leadership Update</span>
          </button>
        </div>
      </header>

      {/* KPI Cards */}
      <MetricCards metrics={summaryMetrics} />

      {/* Main Chat Interface */}
      <main className="flex-1">
        <ChatInterface />
      </main>

      {/* Leadership Update Modal */}
      <LeadershipReport 
        isOpen={isReportOpen} 
        onClose={() => setIsReportOpen(false)} 
      />

      {/* Footer */}
      <footer className="mt-8 pt-4 border-t border-slate-900 text-center text-xs text-slate-500 flex flex-col md:flex-row items-center justify-between gap-2">
        <div>Skylark Drones Business Intelligence Agent — Deterministic BI Engine</div>
        <div className="flex items-center gap-4 text-slate-400">
          <span className="flex items-center gap-1"><ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /> Deterministic Math</span>
          <span className="flex items-center gap-1"><Database className="w-3.5 h-3.5 text-cyan-400" /> Monday.com Schema</span>
        </div>
      </footer>

    </div>
  );
}
