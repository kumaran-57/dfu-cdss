"use client";

import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import {
  Camera,
  Upload,
  CheckCircle,
  AlertTriangle,
  ArrowRight,
  ArrowLeft,
  Sparkles,
  Sliders,
} from "lucide-react";

export default function VisitCapturePage() {
  const params = useParams();
  const router = useRouter();
  const visitId = params?.id as string;

  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [imageRecord, setImageRecord] = useState<any>(null);
  const [calibrationRecord, setCalibrationRecord] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Calibration inputs
  const [markerType, setMarkerType] = useState("circle_10mm");
  const [knownDim, setKnownDim] = useState(10.0);
  const [calibrating, setCalibrating] = useState(false);

  const handleUpload = async (fileToUpload?: File) => {
    const targetFile = fileToUpload || file;
    if (!targetFile) return;

    setError(null);
    setUploading(true);
    try {
      const res = await api.uploadImage(visitId, targetFile, true);
      setImageRecord(res);
    } catch (err: any) {
      setError(err.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleCalibrate = async () => {
    if (!imageRecord) return;
    setCalibrating(true);
    setError(null);
    try {
      const res = await api.calibrateImage(imageRecord.id, {
        marker_type: markerType,
        known_dimension_mm: knownDim,
      });
      setCalibrationRecord(res);
    } catch (err: any) {
      setError(err.message || "Calibration failed");
    } finally {
      setCalibrating(false);
    }
  };

  // Helper to load synthetic demo image directly
  const loadSyntheticDemo = async (type: "sharp" | "blurry") => {
    setError(null);
    setUploading(true);
    try {
      // Create a canvas-rendered test image file in memory
      const canvas = document.createElement("canvas");
      canvas.width = 600;
      canvas.height = 600;
      const ctx = canvas.getContext("2d")!;
      
      // Skin tone
      ctx.fillStyle = "#e0b59b";
      ctx.fillRect(0, 0, 600, 600);

      // Marker
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(100, 100, 45, 0, 2 * Math.PI);
      ctx.fill();
      ctx.fillStyle = "#222222";
      ctx.beginPath();
      ctx.arc(100, 100, 35, 0, 2 * Math.PI);
      ctx.fill();

      // Wound
      ctx.fillStyle = type === "blurry" ? "#888888" : "#992222";
      ctx.beginPath();
      ctx.arc(300, 300, 110, 0, 2 * Math.PI);
      ctx.fill();

      // Slough center
      ctx.fillStyle = "#d4c88a";
      ctx.beginPath();
      ctx.arc(300, 300, 50, 0, 2 * Math.PI);
      ctx.fill();

      canvas.toBlob(async (blob) => {
        if (!blob) return;
        const demoFile = new File([blob], `synthetic_${type}.jpg`, { type: "image/jpeg" });
        await handleUpload(demoFile);
      }, "image/jpeg");

    } catch (err: any) {
      setError(err.message || "Failed to load demo");
      setUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <button
          onClick={() => router.back()}
          className="p-2 border border-slate-200 rounded-lg text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Standardized Image Ingestion &amp; Calibration</h1>
          <p className="text-xs text-slate-500">
            Automated quality checks (blur &amp; exposure) and geometric scale calibration
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl">
          {error}
        </div>
      )}

      {/* Step 1: Upload / Capture */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Camera className="w-5 h-5 text-teal-600" />
          Step 1: Wound Photographic Capture
        </h2>

        <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center space-y-3 hover:border-teal-500 transition-colors">
          <Upload className="w-8 h-8 text-slate-400 mx-auto" />
          <div>
            <p className="text-sm font-semibold text-slate-700">Choose photograph or drag and drop</p>
            <p className="text-xs text-slate-400">JPEG, PNG up to 25MB • EXIF metadata stripped automatically</p>
          </div>
          <input
            type="file"
            accept="image/jpeg,image/png"
            onChange={(e) => {
              if (e.target.files?.[0]) {
                setFile(e.target.files[0]);
                handleUpload(e.target.files[0]);
              }
            }}
            className="text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100 cursor-pointer"
          />
        </div>

        {/* Quick Demo Watermark Fixture Loaders */}
        <div className="pt-2 flex items-center justify-between">
          <span className="text-xs text-slate-500 font-medium">Or test with procedural synthetic phantoms:</span>
          <div className="flex gap-2">
            <button
              onClick={() => loadSyntheticDemo("sharp")}
              disabled={uploading}
              className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg flex items-center gap-1 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5 text-teal-600" />
              Load Valid Synthetic Wound
            </button>
            <button
              onClick={() => loadSyntheticDemo("blurry")}
              disabled={uploading}
              className="px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-semibold rounded-lg flex items-center gap-1 transition-colors"
            >
              <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
              Load Blurry Wound (Rejection Test)
            </button>
          </div>
        </div>
      </div>

      {/* Step 2: Quality Check Status */}
      {imageRecord && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-teal-600" />
            Step 2: Automated Image Quality Inspection
          </h2>

          <div className="grid grid-cols-3 gap-4">
            <div className="p-3 bg-slate-50 rounded-lg">
              <span className="text-xs text-slate-500 block">Sharpness / Blur Score</span>
              <span className="text-base font-bold text-slate-900 mt-1 block">
                {imageRecord.blur_score ? imageRecord.blur_score.toFixed(1) : "—"}
              </span>
              <span className="text-[11px] text-slate-400">Laplacian Variance (&gt;40 required)</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg">
              <span className="text-xs text-slate-500 block">Exposure Status</span>
              <span className="text-base font-bold text-slate-900 mt-1 capitalize block">
                {imageRecord.exposure_status}
              </span>
              <span className="text-[11px] text-slate-400">Mean Luminance Inspection</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg">
              <span className="text-xs text-slate-500 block">Quality Decision Gate</span>
              <span className={`text-base font-bold mt-1 block ${
                imageRecord.quality_passed ? "text-emerald-600" : "text-amber-600"
              }`}>
                {imageRecord.quality_passed ? "✓ Passed Quality Gate" : "⚠ Recapture Advised"}
              </span>
              <span className="text-[11px] text-slate-400">Clinical Usability Gate</span>
            </div>
          </div>

          {/* Step 3: Planar Scale Calibration */}
          <div className="pt-4 border-t border-slate-100 space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
              <Sliders className="w-4 h-4 text-teal-600" />
              Step 3: Geometric Scale Calibration
            </h3>
            <p className="text-xs text-slate-500">
              Calibrate pixel-to-millimeter ratio using the reference marker to compute surface area in metric cm².
            </p>

            <div className="flex flex-wrap items-center gap-3">
              <select
                value={markerType}
                onChange={(e) => setMarkerType(e.target.value)}
                className="px-3 py-1.5 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500"
              >
                <option value="circle_10mm">Standard Circular 10mm Marker</option>
                <option value="checkerboard_20mm">Checkerboard 20mm Grid</option>
                <option value="manual_reference">Manual 2-Point Caliper</option>
              </select>

              <button
                onClick={handleCalibrate}
                disabled={calibrating}
                className="px-4 py-1.5 bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors"
              >
                {calibrating ? "Estimating Scale..." : "Perform Calibration"}
              </button>

              {calibrationRecord && (
                <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
                  Scale: {calibrationRecord.mm_per_pixel} mm/px (Confidence: {calibrationRecord.calibration_confidence * 100}%)
                </span>
              )}
            </div>
          </div>

          {/* Step 4: Proceed to AI Assessment */}
          <div className="pt-4 border-t border-slate-100 flex justify-end">
            <Link
              href={`/visits/${visitId}/assessment`}
              className="flex items-center gap-2 px-5 py-2.5 bg-teal-600 hover:bg-teal-700 text-white font-semibold text-sm rounded-lg shadow transition-colors"
            >
              Proceed to AI Assessment &amp; Clinician Review
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
