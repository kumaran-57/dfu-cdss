"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import {
  Calendar,
  Camera,
  Activity,
  ArrowLeft,
  Plus,
  AlertCircle,
  TrendingDown,
  TrendingUp,
  Minus,
  CheckCircle,
  Clock,
} from "lucide-react";

export default function ParticipantDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;

  const [participant, setParticipant] = useState<any>(null);
  const [visits, setVisits] = useState<any[]>([]);
  const [progression, setProgression] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showAddVisit, setShowAddVisit] = useState(false);

  // New visit form
  const [visitCode, setVisitCode] = useState("V01");
  const [followUpDay, setFollowUpDay] = useState(0);
  const [woundSide, setWoundSide] = useState("left");
  const [anatomicalLocation, setAnatomicalLocation] = useState("plantar_forefoot");
  const [notes, setNotes] = useState("");

  const loadAll = async () => {
    setLoading(true);
    try {
      const [p, v, prog] = await Promise.all([
        api.getParticipant(id),
        api.listVisits(id),
        api.getProgression(id).catch(() => null),
      ]);
      setParticipant(p);
      setVisits(v.items || []);
      setProgression(prog);
      setVisitCode(`V0${(v.items?.length || 0) + 1}`);
      setFollowUpDay((v.items?.length || 0) * 14);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) loadAll();
  }, [id]);

  const handleCreateVisit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createVisit(id, {
        visit_code: visitCode,
        follow_up_day: followUpDay,
        wound_side: woundSide,
        anatomical_location: anatomicalLocation,
        notes,
      });
      setShowAddVisit(false);
      loadAll();
    } catch (err: any) {
      alert(err.message || "Failed to create visit");
    }
  };

  if (loading && !participant) {
    return <div className="p-8 text-center text-slate-500">Loading participant timeline...</div>;
  }

  if (!participant) {
    return <div className="p-8 text-center text-red-500">Participant not found.</div>;
  }

  return (
    <div className="space-y-8">
      {/* Top Breadcrumb & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link
            href="/participants"
            className="p-2 border border-slate-200 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold font-mono text-slate-900">{participant.study_id}</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full font-semibold bg-teal-100 text-teal-800">
                {participant.enrollment_status}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Demographics: {participant.biological_sex || "undisclosed"} • {participant.age_at_enrollment || "—"} years old
            </p>
          </div>
        </div>

        <button
          onClick={() => setShowAddVisit(true)}
          className="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white font-medium text-sm rounded-lg shadow-sm transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Consultation Visit
        </button>
      </div>

      {/* Longitudinal Trajectory Card */}
      {progression && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Activity className="w-5 h-5 text-teal-600" />
              Longitudinal Wound Trajectory Analysis
            </h2>
            <div className="flex items-center gap-2">
              {progression.healing_trajectory_trend === "improving" && (
                <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                  <TrendingDown className="w-3.5 h-3.5" />
                  Area Reduction (Improving)
                </span>
              )}
              {progression.healing_trajectory_trend === "deteriorating" && (
                <span className="inline-flex items-center gap-1 text-xs font-bold text-red-700 bg-red-50 px-2.5 py-1 rounded-full border border-red-200">
                  <TrendingUp className="w-3.5 h-3.5" />
                  Area Expansion (Clinician Review Required)
                </span>
              )}
              {progression.healing_trajectory_trend === "stalled" && (
                <span className="inline-flex items-center gap-1 text-xs font-bold text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200">
                  <Minus className="w-3.5 h-3.5" />
                  Stalled Trajectory
                </span>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="p-3 bg-slate-50 rounded-lg">
              <span className="text-xs text-slate-500 block">Baseline Surface Area</span>
              <span className="text-lg font-bold text-slate-900 mt-1 block">
                {progression.baseline_area_cm2 ? `${progression.baseline_area_cm2} cm²` : "Uncalibrated"}
              </span>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg">
              <span className="text-xs text-slate-500 block">Latest Surface Area</span>
              <span className="text-lg font-bold text-slate-900 mt-1 block">
                {progression.latest_area_cm2 ? `${progression.latest_area_cm2} cm²` : "Uncalibrated"}
              </span>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg">
              <span className="text-xs text-slate-500 block">Total Area Change</span>
              <span className={`text-lg font-bold mt-1 block ${
                (progression.total_area_change_percentage ?? 0) < 0 ? "text-emerald-600" : "text-slate-900"
              }`}>
                {progression.total_area_change_percentage !== null
                  ? `${progression.total_area_change_percentage}%`
                  : "—"}
              </span>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg">
              <span className="text-xs text-slate-500 block">Weekly Rate of Change</span>
              <span className="text-lg font-bold text-slate-900 mt-1 block">
                {progression.healing_rate_cm2_per_week !== null
                  ? `${progression.healing_rate_cm2_per_week} cm²/wk`
                  : "—"}
              </span>
            </div>
          </div>

          <p className="text-xs text-slate-400 italic pt-2 border-t border-slate-100">
            {progression.clinical_notice}
          </p>
        </div>
      )}

      {/* Serial Visits Timeline */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-slate-900">Serial Consultation Encounters</h2>

        {visits.length === 0 ? (
          <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-slate-400">
            No clinical visits recorded. Click &quot;Add Consultation Visit&quot; to begin serial tracking.
          </div>
        ) : (
          <div className="space-y-3">
            {visits.map((v) => (
              <div
                key={v.id}
                className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-teal-300 transition-colors"
              >
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-teal-50 border border-teal-200 text-teal-700 flex flex-col items-center justify-center font-bold">
                    <span className="text-xs uppercase">Day</span>
                    <span className="text-base leading-none">{v.follow_up_day}</span>
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900 text-base">{v.visit_code}</span>
                      <span className="text-xs text-slate-400">
                        {new Date(v.visit_date).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 mt-0.5">
                      Location: <span className="font-medium capitalize">{v.anatomical_location.replace("_", " ")}</span> ({v.wound_side} foot)
                    </p>
                    {v.notes && <p className="text-xs text-slate-500 mt-1">{v.notes}</p>}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    href={`/visits/${v.id}/capture`}
                    className="flex items-center gap-1.5 px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition-colors"
                  >
                    <Camera className="w-3.5 h-3.5" />
                    Capture / Upload
                  </Link>
                  <Link
                    href={`/visits/${v.id}/assessment`}
                    className="flex items-center gap-1.5 px-3.5 py-2 bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors"
                  >
                    <Activity className="w-3.5 h-3.5" />
                    AI Assessment &amp; Review
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Visit Modal */}
      {showAddVisit && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 border border-slate-200">
            <h2 className="text-lg font-bold text-slate-900 mb-1">Add Consultation Visit</h2>
            <p className="text-xs text-slate-500 mb-4">
              Create a new encounter for serial assessment and wound photography.
            </p>

            <form onSubmit={handleCreateVisit} className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
                    Visit Code
                  </label>
                  <input
                    type="text"
                    value={visitCode}
                    onChange={(e) => setVisitCode(e.target.value)}
                    required
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm font-mono focus:ring-2 focus:ring-teal-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
                    Follow-Up Day
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={followUpDay}
                    onChange={(e) => setFollowUpDay(parseInt(e.target.value))}
                    required
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
                    Wound Side
                  </label>
                  <select
                    value={woundSide}
                    onChange={(e) => setWoundSide(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                  >
                    <option value="left">Left Foot</option>
                    <option value="right">Right Foot</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
                    Anatomical Site
                  </label>
                  <select
                    value={anatomicalLocation}
                    onChange={(e) => setAnatomicalLocation(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                  >
                    <option value="plantar_forefoot">Plantar Forefoot</option>
                    <option value="plantar_heel">Plantar Heel</option>
                    <option value="plantar_hallux">Plantar Hallux</option>
                    <option value="dorsal_aspect">Dorsal Aspect</option>
                    <option value="lateral_malleolus">Lateral Malleolus</option>
                    <option value="medial_malleolus">Medial Malleolus</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
                  Encounter Notes / Clinical Findings
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Clinical observation, offloading compliance, wound bed condition..."
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                />
              </div>

              <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddVisit(false)}
                  className="px-4 py-2 border border-slate-300 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-teal-600 text-white text-sm font-medium rounded-lg hover:bg-teal-700"
                >
                  Save Encounter
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
