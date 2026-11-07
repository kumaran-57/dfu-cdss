"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api, getSession, UserSession } from "@/lib/api";
import {
  Users,
  Calendar,
  AlertCircle,
  FileCheck2,
  TrendingDown,
  ArrowRight,
  ShieldAlert,
  Camera,
} from "lucide-react";

export default function DashboardPage() {
  const [session, setSessionState] = useState<UserSession | null>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [participants, setParticipants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const curr = getSession();
    setSessionState(curr);

    async function loadData() {
      try {
        const [m, p] = await Promise.all([
          api.getResearchMetrics().catch(() => null),
          api.listParticipants(0, 5).catch(() => ({ items: [] })),
        ]);
        setMetrics(m);
        setParticipants(p.items || []);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Clinician Assessment Dashboard
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Standardized diabetic foot ulcer monitoring, scale calibration, and longitudinal analysis
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/participants"
            className="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white font-medium text-sm rounded-lg shadow-sm transition-colors"
          >
            <Users className="w-4 h-4" />
            Manage Participants
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
              Enrolled Cohort
            </span>
            <span className="text-2xl font-bold text-slate-900 mt-1 block">
              {metrics ? metrics.total_participants : "—"}
            </span>
            <span className="text-xs text-slate-400 mt-0.5 block">Coded Study IDs</span>
          </div>
          <div className="w-11 h-11 bg-teal-50 text-teal-600 rounded-lg flex items-center justify-center">
            <Users className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
              Total Encounters
            </span>
            <span className="text-2xl font-bold text-slate-900 mt-1 block">
              {metrics ? metrics.total_visits : "—"}
            </span>
            <span className="text-xs text-slate-400 mt-0.5 block">Serial Clinical Visits</span>
          </div>
          <div className="w-11 h-11 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center">
            <Calendar className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
              Calibrated AI Predictions
            </span>
            <span className="text-2xl font-bold text-slate-900 mt-1 block">
              {metrics ? metrics.total_predictions : "—"}
            </span>
            <span className="text-xs text-teal-600 mt-0.5 block">Metric cm² Computed</span>
          </div>
          <div className="w-11 h-11 bg-emerald-50 text-emerald-600 rounded-lg flex items-center justify-center">
            <FileCheck2 className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
              Flagged for Review
            </span>
            <span className="text-2xl font-bold text-amber-600 mt-1 block">
              {metrics ? metrics.flagged_for_clinician_review : "—"}
            </span>
            <span className="text-xs text-slate-400 mt-0.5 block">Uncertainty &gt; 0.35</span>
          </div>
          <div className="w-11 h-11 bg-amber-50 text-amber-600 rounded-lg flex items-center justify-center">
            <AlertCircle className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Cohort Overview Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 className="font-bold text-slate-900 text-base">Active Research Participants</h2>
          <Link
            href="/participants"
            className="text-xs font-semibold text-teal-600 hover:text-teal-700 flex items-center gap-1"
          >
            View All <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 text-xs uppercase font-semibold text-slate-500 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3">Study ID</th>
                <th className="px-6 py-3">Biological Sex</th>
                <th className="px-6 py-3">Enrollment Age</th>
                <th className="px-6 py-3">Consent Status</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {participants.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-slate-400">
                    No participants registered yet. Use the button above to add a participant.
                  </td>
                </tr>
              ) : (
                participants.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 font-mono font-semibold text-slate-900">{p.study_id}</td>
                    <td className="px-6 py-4 capitalize">{p.biological_sex || "undisclosed"}</td>
                    <td className="px-6 py-4">{p.age_at_enrollment ? `${p.age_at_enrollment} yrs` : "—"}</td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800">
                        {p.consent_status} ({p.consent_version})
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-700">
                        {p.enrollment_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        href={`/participants/${p.id}`}
                        className="text-teal-600 hover:text-teal-800 font-medium text-xs inline-flex items-center gap-1"
                      >
                        Longitudinal View <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
