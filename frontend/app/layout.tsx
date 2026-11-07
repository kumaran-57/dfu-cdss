import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "DFU-XAI Clinical Decision Support",
  description:
    "An Integrated Self-Supervised, Domain-Adaptive and Explainable AI Framework for Calibrated Longitudinal Diabetic Foot Ulcer Assessment",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-slate-50 antialiased">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
          <p>© 2026 DFU-XAI Academic Research Consortium. Decision-support prototype only. Not for autonomous diagnosis.</p>
        </footer>
      </body>
    </html>
  );
}
