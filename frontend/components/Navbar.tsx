"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import { getSession, setSession, UserSession } from "@/lib/api";
import { Activity, Users, BarChart3, ShieldCheck, LogOut, LogIn, AlertTriangle } from "lucide-react";

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [session, setCurrentSession] = useState<UserSession | null>(null);

  useEffect(() => {
    setCurrentSession(getSession());
  }, [pathname]);

  const handleLogout = () => {
    setSession(null);
    setCurrentSession(null);
    router.push("/login");
  };

  const navItems = [
    { label: "Dashboard", href: "/", icon: Activity },
    { label: "Participants", href: "/participants", icon: Users },
    { label: "Research Benchmarks", href: "/research", icon: BarChart3 },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
      {/* Mandatory Clinical Decision-Support Disclaimer Banner */}
      <div className="bg-amber-500 text-slate-950 px-4 py-1.5 text-xs font-semibold flex items-center justify-center gap-2 border-b border-amber-600 tracking-wide text-center">
        <AlertTriangle className="w-4 h-4 shrink-0 text-slate-950" />
        <span>
          RESEARCH DECISION-SUPPORT PROTOTYPE • NOT FOR AUTONOMOUS DIAGNOSIS OR TREATMENT • ALL CLINICAL ACTIONS REQUIRE LICENSED PRACTITIONER SUPERVISION
        </span>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-teal-600 flex items-center justify-center text-white font-bold text-lg shadow-sm">
              DFU
            </div>
            <div>
              <span className="font-bold text-slate-900 text-base tracking-tight">DFU-XAI</span>
              <span className="text-xs text-slate-500 block -mt-0.5">Clinical Decision Support</span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-md text-sm font-medium transition-colors ${
                    active
                      ? "bg-teal-50 text-teal-700"
                      : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          {session ? (
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs font-medium text-slate-700 block">{session.email}</span>
                <span className="inline-block text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-teal-100 text-teal-800">
                  {session.role}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 text-slate-500 hover:text-red-600 hover:bg-slate-100 rounded-md transition-colors"
                title="Log out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="flex items-center gap-1.5 px-4 py-2 bg-teal-600 text-white rounded-md text-sm font-medium hover:bg-teal-700 transition-colors shadow-sm"
            >
              <LogIn className="w-4 h-4" />
              Sign In
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
