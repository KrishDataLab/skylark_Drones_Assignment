import React from 'react';
import { DollarSign, TrendingUp, AlertTriangle, Briefcase } from 'lucide-react';

export default function MetricCards({ metrics }) {
  if (!metrics) return null;

  const openDealsCount = metrics.open_deals_count !== undefined ? metrics.open_deals_count : (metrics.open_deals !== undefined ? metrics.open_deals : 0);
  const delayedCount = metrics.delayed_count !== undefined ? metrics.delayed_count : (metrics.delayed_work_orders !== undefined ? metrics.delayed_work_orders : 0);

  const cards = [
    {
      title: "Total Revenue (excl GST)",
      value: `₹${(metrics.total_revenue_excl_gst || 0).toLocaleString('en-IN')}`,
      subtext: "From work orders",
      icon: DollarSign,
      color: "from-emerald-500/20 to-teal-500/10 border-emerald-500/30 text-emerald-400"
    },
    {
      title: "Active Sales Pipeline",
      value: `₹${(metrics.total_pipeline_value || 0).toLocaleString('en-IN')}`,
      subtext: `${openDealsCount} open deals`,
      icon: TrendingUp,
      color: "from-indigo-500/20 to-cyan-500/10 border-indigo-500/30 text-indigo-400"
    },
    {
      title: "Delayed Work Orders",
      value: delayedCount,
      subtext: "Requires billing update",
      icon: AlertTriangle,
      color: "from-amber-500/20 to-rose-500/10 border-amber-500/30 text-amber-400"
    },
    {
      title: "Weighted Pipeline Value",
      value: `₹${(metrics.weighted_pipeline_value || 0).toLocaleString('en-IN')}`,
      subtext: "Probability adjusted",
      icon: Briefcase,
      color: "from-sky-500/20 to-blue-500/10 border-sky-500/30 text-sky-400"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {cards.map((c, i) => {
        const Icon = c.icon;
        return (
          <div key={i} className={`p-4 rounded-xl glass-card bg-gradient-to-br ${c.color} border`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium uppercase tracking-wider text-slate-400">{c.title}</span>
              <Icon className="w-5 h-5 opacity-80" />
            </div>
            <div className="text-2xl font-bold font-heading text-slate-100 mb-1">{c.value}</div>
            <div className="text-xs text-slate-400">{c.subtext}</div>
          </div>
        );
      })}
    </div>
  );
}
