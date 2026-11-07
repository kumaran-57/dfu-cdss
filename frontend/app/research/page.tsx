"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import {
  BarChart3,
  Download,
  CheckCircle2,
  Clock,
  FileSpreadsheet,
  Cpu,
  Layers,
  Activity,
  AlertTriangle,
} from "lucide-react";

export default function ResearchPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    api.getResearchMetrics().then(setMetrics).catch(console.error);
  }, []);

  const handleExportCSV = async () => {
    setDownloading(true);
    try {
      const blob = await api.exportCSV();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "dfu_xai_cohort_export.csv";
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      alert(err.message || "Export failed");
    } finally {
      setDownloading(false);
    }
  };

  const experimentMatrix = [
    { id: "E1", title: "Self-Supervised Representation", comp: "ImageNet vs DINOv2 vs SimCLR vs MAE", metric: "Macro-F1, ROC-AUC", status: "Harness Configured" },
    { id: "E2", title: "Boundary Segmentation", comp: "U-Net baseline vs SegFormer-B0 candidate", metric: "Dice (DSC), IoU, HD95", status: "Verified" },
    { id: "E3", title: "Label Efficiency", comp: "10%, 25%, 50%, 100% annotation budget", metric: "Δ Dice Score", status: "Configured" },
    { id: "E4", title: "Domain Adaptation", comp: "Source-only vs Pseudo-label adaptation", metric: "Target-site generalization gap", status: "Configured" },
    { id: "E5", title: "Geometric Scale Calibration", comp: "Uncalibrated pixels vs mm scale factor", metric: "Area MAE (cm²), ICC(2,1)", status: "Verified" },
    { id: "E6", title: "Tissue Composition Contribution", comp: "Outer wound margin vs Granulation/Slough/Necrosis", metric: "Multi-class Mean IoU", status: "Verified" },
    { id: "E7", title: "Multimodal Clinical Fusion", comp: "Image-only vs Clinical-only vs Fused", metric: "Brier Score, SHAP Rankings", status: "Harness Ready" },
    { id: "E8", title: "Longitudinal Rate Trajectory", comp: "Single visit snapshot vs Mixed-effects slope", metric: "Area change rate (cm²/week)", status: "Verified" },
    { id: "E9", title: "Calibrated Epistemic Uncertainty", comp: "Deterministic baseline vs MC Dropout ensemble", metric: "ECE, Risk-Coverage Curve", status: "Verified" },
    { id: "E10", title: "Deployment Benchmarking", comp: "PyTorch native vs ONNX Runtime CPU latency", metric: "Inference Latency (ms), Peak RAM", status: "Verified" },
  ];

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Research Evaluation &amp; Benchmark Leaderboard
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Controlled comparisons across self-supervised representation, segmentation, and multimodal clinical fusion
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          disabled={downloading}
          className="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white font-medium text-sm rounded-lg shadow-sm transition-colors disabled:opacity-50"
        >
          <Download className="w-4 h-4" />
          {downloading ? "Exporting..." : "Download De-identified CSV"}
        </button>
      </div>

      {/* Cohort Stats Summary */}
      {metrics && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <span className="text-xs text-slate-500 uppercase font-semibold block">Total Participants</span>
            <span className="text-xl font-bold text-slate-900 mt-1 block">{metrics.total_participants}</span>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <span className="text-xs text-slate-500 uppercase font-semibold block">Serial Visits</span>
            <span className="text-xl font-bold text-slate-900 mt-1 block">{metrics.total_visits}</span>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <span className="text-xs text-slate-500 uppercase font-semibold block">Predictions</span>
            <span className="text-xl font-bold text-slate-900 mt-1 block">{metrics.total_predictions}</span>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <span className="text-xs text-slate-500 uppercase font-semibold block">Review Rate</span>
            <span className="text-xl font-bold text-teal-600 mt-1 block">{metrics.review_rate_percentage}%</span>
          </div>
        </div>
      )}

      {/* Experiments Matrix */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200">
          <h2 className="font-bold text-slate-900 text-base">Formal Experiment Protocol (E1 through E10)</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Strict patient-level data partitions. Held-out test sets are unblinded only after hyperparameter freeze.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 text-xs uppercase font-semibold text-slate-500 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3">ID</th>
                <th className="px-6 py-3">Experiment Focus</th>
                <th className="px-6 py-3">Controlled Comparison</th>
                <th className="px-6 py-3">Key Metrics</th>
                <th className="px-6 py-3 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {experimentMatrix.map((exp) => (
                <tr key={exp.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4 font-mono font-bold text-teal-700">{exp.id}</td>
                  <td className="px-6 py-4 font-semibold text-slate-900">{exp.title}</td>
                  <td className="px-6 py-4 text-xs text-slate-600">{exp.comp}</td>
                  <td className="px-6 py-4 text-xs font-mono text-slate-500">{exp.metric}</td>
                  <td className="px-6 py-4 text-right">
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      {exp.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
