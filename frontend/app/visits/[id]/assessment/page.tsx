"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import {
  Activity,
  CheckCircle,
  AlertTriangle,
  Sliders,
  FileCheck2,
  ArrowLeft,
  Sparkles,
  ShieldCheck,
} from "lucide-react";

export default function AssessmentPage() {
  const params = useParams();
  const router = useRouter();
  const visitId = params?.id as string;

  const [images, setImages] = useState<any[]>([]);
  const [selectedImage, setSelectedImage] = useState<any>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [modelName, setModelName] = useState("segformer-b0");
  const [loading, setLoading] = useState(false);
  const [reviewSubmitted, setReviewSubmitted] = useState(false);

  // Review override states
  const [overrideArea, setOverrideArea] = useState<string>("");
  const [reviewNotes, setReviewNotes] = useState("");
  const [submittingReview, setSubmittingReview] = useState(false);

  useEffect(() => {
    async function loadImages() {
      try {
        const res = await api.listVisits(visitId);
      } catch {}
      // Fetch images for this visit via API
      try {
        const session = api;
        const res = await fetch(`http://localhost:8000/api/v1/visits/${visitId}/images`);
        if (res.ok) {
          const data = await res.json();
          setImages(data);
          if (data.length > 0) setSelectedImage(data[0]);
        }
      } catch (e) {
        console.error(e);
      }
    }
    loadImages();
  }, [visitId]);

  const handleRunInference = async () => {
    if (!selectedImage) return;
    setLoading(true);
    try {
      const res = await api.runAssessment(selectedImage.id, modelName);
      setPrediction(res);
      if (res.calibrated_area_cm2) {
        setOverrideArea(String(res.calibrated_area_cm2));
      }
    } catch (err: any) {
      alert(err.message || "Inference failed");
    } finally {
      setLoading(false);
    }
  };

  const handleReviewSubmit = async (approved: boolean) => {
    if (!prediction) return;
    setSubmittingReview(true);
    try {
      await api.submitReview(prediction.id, {
        approved,
        override_area_cm2: overrideArea ? parseFloat(overrideArea) : undefined,
        notes: reviewNotes || "Clinician sign-off completed.",
      });
      setReviewSubmitted(true);
    } catch (err: any) {
      alert(err.message || "Failed to submit clinician review");
    } finally {
      setSubmittingReview(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <button
          onClick={() => router.back()}
          className="p-2 border border-slate-200 rounded-lg text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-slate-900">AI Wound Segmentation &amp; Clinician Verification</h1>
          <p className="text-xs text-slate-500">
            Compare SegFormer-B0 vs U-Net baselines with calibrated metric measurements
          </p>
        </div>
      </div>

      {/* Model Selection Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-slate-700 uppercase">Architecture:</span>
          <div className="flex gap-2">
            <button
              onClick={() => setModelName("segformer-b0")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                modelName === "segformer-b0"
                  ? "bg-teal-600 text-white shadow-sm"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              SegFormer-B0 (Hierarchical ViT)
            </button>
            <button
              onClick={() => setModelName("unet-baseline")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                modelName === "unet-baseline"
                  ? "bg-teal-600 text-white shadow-sm"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              U-Net (Convolutional Baseline)
            </button>
          </div>
        </div>

        <button
          onClick={handleRunInference}
          disabled={loading || !selectedImage}
          className="px-5 py-2 bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold rounded-lg shadow transition-colors flex items-center gap-2 disabled:opacity-50"
        >
          <Sparkles className="w-4 h-4" />
          {loading ? "Running Segmentation..." : "Execute AI Assessment"}
        </button>
      </div>

      {/* Visualizer & Metric Panels */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Visualizer Card */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-900">Wound Bed Visualizer &amp; Mask Overlay</h2>
            {prediction && (
              <span className="text-[11px] font-semibold text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                {prediction.model_name} (v{prediction.model_version})
              </span>
            )}
          </div>

          <div className="relative aspect-square bg-slate-900 rounded-lg overflow-hidden flex items-center justify-center border border-slate-300">
            {/* Visual Canvas Display */}
            <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-400 p-6 text-center">
              <div className="w-48 h-48 rounded-full border-4 border-teal-500 bg-red-950/60 flex items-center justify-center relative shadow-lg">
                <div className="w-24 h-24 rounded-full bg-amber-500/50 border-2 border-amber-400 flex items-center justify-center">
                  <div className="w-8 h-8 rounded-full bg-stone-900"></div>
                </div>
                <span className="absolute -top-3 px-2 py-0.5 bg-teal-600 text-[10px] text-white font-mono font-bold rounded">
                  {prediction ? `${prediction.calibrated_area_cm2 || "Uncalibrated"} cm²` : "Calibrated Mask"}
                </span>
              </div>
            </div>

            {/* Watermark Label */}
            <div className="absolute bottom-2 left-2 right-2 text-center bg-black/80 text-[10px] text-amber-400 py-1 font-mono rounded">
              DECISION-SUPPORT VISUALIZATION • NOT FOR AUTONOMOUS SURGICAL MARGIN
            </div>
          </div>

          {/* Tissue Breakdown Legend */}
          {prediction && (
            <div className="space-y-2 pt-2">
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span>Tissue Composition Breakdown</span>
                <span className="text-slate-400">Multi-Class Sub-Segmentation</span>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center text-xs">
                <div className="p-2 bg-red-50 border border-red-200 rounded-lg">
                  <span className="text-red-700 font-bold block">{prediction.granulation_percentage}%</span>
                  <span className="text-[10px] text-slate-500 uppercase tracking-wide">Granulation</span>
                </div>
                <div className="p-2 bg-amber-50 border border-amber-200 rounded-lg">
                  <span className="text-amber-800 font-bold block">{prediction.slough_percentage}%</span>
                  <span className="text-[10px] text-slate-500 uppercase tracking-wide">Slough</span>
                </div>
                <div className="p-2 bg-stone-100 border border-stone-300 rounded-lg">
                  <span className="text-stone-800 font-bold block">{prediction.necrotic_percentage}%</span>
                  <span className="text-[10px] text-slate-500 uppercase tracking-wide">Necrotic</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Calibrated Measurements & Review Form */}
        <div className="space-y-6">
          {/* Calibrated Metrics Table */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3">
            <h2 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
              <FileCheck2 className="w-4 h-4 text-teal-600" />
              Calibrated Metric Measurements
            </h2>

            {prediction ? (
              <div className="space-y-2.5">
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-lg">
                  <span className="text-xs text-slate-600 font-medium">Calibrated Surface Area</span>
                  <span className="text-base font-bold text-teal-700 font-mono">
                    {prediction.calibrated_area_cm2 !== null ? `${prediction.calibrated_area_cm2} cm²` : "Calibration Missing"}
                  </span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-lg">
                  <span className="text-xs text-slate-600 font-medium">Feret Maximum Length</span>
                  <span className="text-sm font-bold text-slate-900 font-mono">
                    {prediction.major_length_mm ? `${prediction.major_length_mm} mm` : "—"}
                  </span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-lg">
                  <span className="text-xs text-slate-600 font-medium">Feret Perpendicular Width</span>
                  <span className="text-sm font-bold text-slate-900 font-mono">
                    {prediction.minor_width_mm ? `${prediction.minor_width_mm} mm` : "—"}
                  </span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-lg">
                  <span className="text-xs text-slate-600 font-medium">Epistemic Uncertainty</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded font-mono ${
                    prediction.uncertainty_score > 0.35 ? "bg-amber-100 text-amber-800" : "bg-emerald-100 text-emerald-800"
                  }`}>
                    {prediction.uncertainty_score.toFixed(2)} ({prediction.uncertainty_score > 0.35 ? "Review Required" : "Calibrated"})
                  </span>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400 py-6 text-center">
                Click &quot;Execute AI Assessment&quot; above to compute calibrated measurements.
              </p>
            )}
          </div>

          {/* Clinician Review & Override Form */}
          {prediction && (
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-teal-600" />
                  Clinician Adjudication &amp; Sign-off
                </h2>
                {reviewSubmitted && (
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    ✓ Verified &amp; Signed
                  </span>
                )}
              </div>

              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
                    Verified Surface Area (cm²)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={overrideArea}
                    onChange={(e) => setOverrideArea(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm font-mono focus:ring-2 focus:ring-teal-500 focus:outline-none"
                  />
                  <span className="text-[11px] text-slate-400 block mt-0.5">
                    Clinicians may adjust the metric boundary area based on direct inspection.
                  </span>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
                    Clinical Justification / Review Notes
                  </label>
                  <textarea
                    value={reviewNotes}
                    onChange={(e) => setReviewNotes(e.target.value)}
                    placeholder="Wound margins confirmed. Tissue viability consistent with current offloading plan..."
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                  />
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    onClick={() => handleReviewSubmit(true)}
                    disabled={submittingReview || reviewSubmitted}
                    className="flex-1 py-2 bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold rounded-lg shadow-sm transition-colors disabled:opacity-50"
                  >
                    {submittingReview ? "Submitting..." : "Approve & Sign Verification"}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
