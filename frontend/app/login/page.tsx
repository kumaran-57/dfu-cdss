"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { ShieldCheck, UserCheck, Stethoscope, Eye } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("clinician@dfuxai.local");
  const [password, setPassword] = useState("ClinicianPass123!");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.login(email, password);
      router.push("/");
    } catch (err: any) {
      setError(err.message || "Failed to authenticate");
    } finally {
      setLoading(false);
    }
  };

  const setRoleCredentials = (roleEmail: string, rolePass: string) => {
    setEmail(roleEmail);
    setPassword(rolePass);
  };

  return (
    <div className="max-w-md mx-auto mt-12">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
        <div className="text-center mb-6">
          <div className="w-12 h-12 bg-teal-600 text-white rounded-xl flex items-center justify-center mx-auto text-xl font-bold mb-3 shadow">
            DFU
          </div>
          <h1 className="text-2xl font-bold text-slate-900">Clinical Portal Login</h1>
          <p className="text-sm text-slate-500 mt-1">
            Authenticate to access decision-support workflows
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 mb-1">
              Authorized Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-700 mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-teal-600 hover:bg-teal-700 text-white font-medium rounded-lg text-sm transition-colors shadow-sm disabled:opacity-50"
          >
            {loading ? "Authenticating..." : "Sign In"}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-slate-100">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 text-center">
            One-Click Research Test Roles
          </p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <button
              onClick={() => setRoleCredentials("clinician@dfuxai.local", "ClinicianPass123!")}
              className="p-2 border border-slate-200 hover:border-teal-500 rounded flex items-center gap-1.5 text-slate-700 hover:text-teal-700 font-medium"
            >
              <Stethoscope className="w-3.5 h-3.5 text-teal-600" />
              Clinician
            </button>
            <button
              onClick={() => setRoleCredentials("researcher@dfuxai.local", "ResearcherPass123!")}
              className="p-2 border border-slate-200 hover:border-teal-500 rounded flex items-center gap-1.5 text-slate-700 hover:text-teal-700 font-medium"
            >
              <UserCheck className="w-3.5 h-3.5 text-blue-600" />
              Researcher
            </button>
            <button
              onClick={() => setRoleCredentials("admin@dfuxai.local", "AdminPass123!")}
              className="p-2 border border-slate-200 hover:border-teal-500 rounded flex items-center gap-1.5 text-slate-700 hover:text-teal-700 font-medium"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-purple-600" />
              Administrator
            </button>
            <button
              onClick={() => setRoleCredentials("viewer@dfuxai.local", "ViewerPass123!")}
              className="p-2 border border-slate-200 hover:border-teal-500 rounded flex items-center gap-1.5 text-slate-700 hover:text-teal-700 font-medium"
            >
              <Eye className="w-3.5 h-3.5 text-slate-600" />
              Auditor / Viewer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
