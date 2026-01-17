"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowUpRight, TrendingUp, Activity, Target, BarChart3, Clock,
  AlertTriangle, Info, ChevronDown, ChevronUp, Shield, Zap, TrendingDown,
  Brain, Scale, AlertCircle, Eye, FileText, Volume2, VolumeX, Sparkles,
  BookOpen, Microscope, Globe, Binary, History, Lock, Unlock
} from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { getMarketPrediction } from "./actions";

const ASSETS = [
  { symbol: "BTC-USD", name: "Bitcoin" },
  { symbol: "AAPL", name: "Apple Inc." },
  { symbol: "TSLA", name: "Tesla Inc." },
  { symbol: "MSFT", name: "Microsoft" },
  { symbol: "^NSEI", name: "Nifty 50" },
  { symbol: "^NSEBANK", name: "Bank Nifty" },
];

export default function FinancialIntelligenceApp() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [batchData, setBatchData] = useState<any[]>([]); // For multi-asset results
  const [selectedTicker, setSelectedTicker] = useState("BTC-USD");
  const [selectedName, setSelectedName] = useState("Bitcoin");
  const [loadingStatus, setLoadingStatus] = useState("");
  const [showDisclaimer, setShowDisclaimer] = useState(true);
  const [expandedSections, setExpandedSections] = useState({
    why: true,
    mtf: false,
    health: false,
    omega: true,
    transcendent: true
  });

  const runAnalysis = async (ticker: string, name: string) => {
    setLoading(true);

    // Simulate system process updates for better UX
    const steps = [
      `Establishing Secure Uplink to ${name}...`,
      "Fetching Institutional Market Data...",
      "Initializing LSTM Neural Network...",
      "Analysing FinBERT Sentiment Streams...",
      "Synthesizing Omega & Elite Signals...",
      "Finalizing Transcendent Output..."
    ];
    let stepIndex = 0;
    setLoadingStatus(steps[0]);

    const intervalId = setInterval(() => {
      stepIndex = (stepIndex + 1) % steps.length;
      setLoadingStatus(steps[stepIndex]);
    }, 800);

    try {
      const result = await getMarketPrediction(ticker, name);

      if (result.error) {
        console.error("Analysis Error:", result.error);
        alert("Error: " + result.error);
      } else {
        setData(result);
        setSelectedTicker(ticker); // Ensure header updates
        setSelectedName(name);
        setShowDisclaimer(false);
      }
    } catch (error) {
      console.error("Failed to run analysis:", error);
      alert("Failed to run analysis.");
    } finally {
      clearInterval(intervalId);
      setLoading(false);
      setLoadingStatus("");
    }
  };

  const runBatchAnalysis = async () => {
    setLoading(true);
    const results = [];
    setShowDisclaimer(false);

    for (const asset of ASSETS) {
      setLoadingStatus(`Analyzing ${asset.name}...`);
      try {
        const result = await getMarketPrediction(asset.symbol, asset.name);
        if (!result.error) {
          results.push(result);
        }
      } catch (e) {
        console.error(`Failed to analyze ${asset.name}`, e);
      }
    }

    setBatchData(results);
    setLoading(false);
    setLoadingStatus("");
  };

  const getBiasColor = (bias: string) => {
    if (bias?.includes("Bullish")) return "text-emerald-400";
    if (bias?.includes("Bearish")) return "text-rose-400";
    if (bias?.includes("Silent") || bias?.includes("Suppressed")) return "text-neutral-500";
    return "text-neutral-400";
  };

  const getStrengthColor = (strength: string) => {
    if (strength === "High") return "bg-emerald-500";
    if (strength === "Medium") return "bg-amber-500";
    if (strength === "None") return "bg-neutral-700";
    return "bg-neutral-500";
  };

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section as keyof typeof prev] }));
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-white selection:bg-emerald-500/30 font-sans">
      {/* Disclaimer Modal */}
      <AnimatePresence>
        {showDisclaimer && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-6"
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="max-w-2xl w-full bg-neutral-900 border border-purple-500/30 rounded-[2.5rem] p-10 shadow-2xl shadow-purple-500/10"
            >
              <div className="flex items-center gap-4 mb-8">
                <div className="h-16 w-16 rounded-3xl bg-gradient-to-br from-purple-500 to-blue-500 p-0.5">
                  <div className="h-full w-full rounded-[1.4rem] bg-neutral-900 flex items-center justify-center">
                    <Sparkles className="h-8 w-8 text-purple-400" />
                  </div>
                </div>
                <div>
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                    Transcendent Intelligence
                  </h2>
                  <p className="text-neutral-500 text-sm">v4.0.0 Experimental Living Organism</p>
                </div>
              </div>

              <div className="space-y-5 text-neutral-300 text-sm mb-10">
                <p className="flex items-start gap-3 p-4 rounded-2xl bg-white/5 border border-white/5">
                  <AlertTriangle className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                  <span><strong>Beyond Prediction:</strong> This system models "unknown unknowns" and uses epistemic humility. It is a research organism, not a financial advisor.</span>
                </p>
                <p className="flex items-start gap-3 p-4 rounded-2xl bg-white/5 border border-white/5">
                  <Shield className="h-5 w-5 text-cyan-500 mt-0.5 flex-shrink-0" />
                  <span><strong>Moral Responsibility:</strong> AI may withhold insights if market fragility or risk amplification is detected.</span>
                </p>
                <p className="flex items-start gap-3 p-4 rounded-2xl bg-white/5 border border-white/5">
                  <History className="h-5 w-5 text-purple-500 mt-0.5 flex-shrink-0" />
                  <span><strong>Legacy Memory:</strong> Analysis is grounded in generational market patterns (2008, 2020, 2022).</span>
                </p>
              </div>

              <button
                onClick={() => setShowDisclaimer(false)}
                className="w-full py-5 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl font-bold text-lg hover:shadow-lg hover:shadow-purple-500/20 active:scale-[0.98] transition-all"
              >
                Assemble Intelligence
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <div className="border-b border-white/5 bg-neutral-950/80 backdrop-blur-2xl sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-black tracking-tight text-white uppercase italic">
                SENTINEL <span className="text-purple-500">INTELLIGENCE</span>
              </h1>
              <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                <p className="text-[10px] text-neutral-500 font-medium uppercase tracking-[0.2em]">When insight matters.</p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-6">
            {data?.transcendent?.budget && (
              <div className="px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center gap-2">
                <Clock className="h-3.5 w-3.5 text-purple-400" />
                <span className="text-[10px] uppercase font-bold text-purple-400 leading-none">
                  Budget: {data.transcendent.budget.remaining}/{data.transcendent.budget.totalBudget}
                </span>
              </div>
            )}
            <div className="text-right hidden sm:block">
              <p className="text-[10px] uppercase tracking-widest text-neutral-500 font-bold mb-0.5">{selectedName} ({selectedTicker})</p>
              <p className="text-xs font-mono text-neutral-400">Epistemic Sync: Active</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-10">
        {batchData.length > 0 ? (
          <div className="space-y-8">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-black uppercase tracking-tight">Multi-Asset Intelligence</h2>
              <button
                onClick={() => setBatchData([])}
                className="px-6 py-2 rounded-xl bg-neutral-900 border border-white/10 text-xs font-bold uppercase hover:bg-white/5"
              >
                Reset Scanner
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {batchData.map((result, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  onClick={() => { setData(result); setBatchData([]); setSelectedName(result.name); setSelectedTicker(result.ticker); }}
                  className="group cursor-pointer p-8 rounded-[2rem] bg-neutral-900 border border-white/5 hover:border-purple-500/50 transition-all hover:-translate-y-1 relative overflow-hidden"
                >
                  <div className="absolute top-0 right-0 p-6 opacity-50 group-hover:opacity-100 transition-opacity">
                    <ArrowUpRight className="h-6 w-6 text-purple-500" />
                  </div>
                  <div className="mb-6">
                    <p className="text-xs font-black uppercase tracking-widest text-neutral-500 mb-1">{result.name}</p>
                    <p className="text-2xl font-black font-mono">${result.currentPrice?.toLocaleString()}</p>
                  </div>
                  <div className="space-y-2">
                    <p className={cn("text-lg font-black italic", getBiasColor(result.recommendation))}>
                      {result.actionVerb}
                    </p>
                    <p className="text-xs text-neutral-400 font-medium line-clamp-2">{result.explanation?.summary}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        ) : !data ? (
          <div className="flex flex-col items-center justify-center min-h-[70vh]">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="text-center w-full max-w-4xl"
            >
              <div className="relative h-32 w-32 mx-auto mb-10">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  className="absolute inset-0 rounded-full border-2 border-dashed border-purple-500/30"
                />
                <motion.div
                  animate={{ rotate: -360 }}
                  transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                  className="absolute inset-2 rounded-full border border-blue-500/20"
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <Brain className="h-14 w-14 text-purple-500" />
                </div>
              </div>
              <h2 className="text-5xl font-black mb-4 tracking-tighter">Transcendent Tier</h2>
              <p className="text-neutral-500 mb-12 max-w-lg mx-auto text-lg leading-relaxed">
                Select a target asset for deep structural analysis or initiate a full market scan.
              </p>

              {/* ASSET SELECTOR */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8 max-w-2xl mx-auto">
                {ASSETS.map((asset) => (
                  <button
                    key={asset.symbol}
                    onClick={() => { setSelectedTicker(asset.symbol); setSelectedName(asset.name); }}
                    className={cn(
                      "p-4 rounded-xl border text-left transition-all",
                      selectedTicker === asset.symbol
                        ? "bg-purple-500 text-white border-purple-500 ring-2 ring-purple-500/30"
                        : "bg-neutral-900 border-white/5 text-neutral-400 hover:border-white/20 hover:text-white"
                    )}
                  >
                    <span className="block text-xs font-black uppercase tracking-wider opacity-70 mb-1">{asset.symbol}</span>
                    <span className="block font-bold text-sm">{asset.name}</span>
                  </button>
                ))}
              </div>

              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <button
                  onClick={() => runAnalysis(selectedTicker, selectedName)}
                  disabled={loading}
                  className="w-full sm:w-auto px-10 py-5 bg-white text-black rounded-2xl font-black text-xl overflow-hidden active:scale-[0.95] transition-all disabled:opacity-50 relative group"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-blue-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                  <span className="relative z-10 group-hover:text-white transition-colors">
                    {loading ? loadingStatus || "ANALYZING..." : "ANALYZE TARGET"}
                  </span>
                </button>

                <button
                  onClick={runBatchAnalysis}
                  disabled={loading}
                  className="w-full sm:w-auto px-10 py-5 bg-neutral-900 text-neutral-400 border border-white/10 rounded-2xl font-bold text-lg hover:bg-neutral-800 hover:text-white transition-all disabled:opacity-50"
                >
                  {loading ? "SCANNING..." : "SCAN MKT (ALL)"}
                </button>
              </div>

            </motion.div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* LEFT COLUMN: Main Prediction & Narrative */}
            <div className="lg:col-span-3 space-y-8">

              {/* MORAL LAYER ALERT */}
              {data.transcendent?.moral?.moralRestraint === "Active" && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="p-6 rounded-[2rem] bg-rose-500/10 border border-rose-500/30 flex items-center gap-4 border-l-[6px] border-l-rose-500"
                >
                  <Lock className="h-8 w-8 text-rose-500" />
                  <div>
                    <h3 className="text-lg font-black uppercase text-rose-500">Moral Restraint Active</h3>
                    <p className="text-sm text-rose-400/80">{data.transcendent.moral.message}</p>
                  </div>
                </motion.div>
              )}

              {/* EPISTEMIC ALERT */}
              {data.transcendent?.epistemic?.boundariesDetected && (
                <div className="p-6 rounded-[2rem] bg-purple-500/10 border border-purple-500/30 flex items-center gap-4">
                  <Unlock className="h-8 w-8 text-purple-400" />
                  <div>
                    <h3 className="text-lg font-black uppercase text-purple-400">{data.transcendent.epistemic.message}</h3>
                    <p className="text-sm text-purple-300/60">Forecasting suppressed due to high structural uncertainty.</p>
                  </div>
                </div>
              )}

              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                className="relative overflow-hidden p-10 rounded-[3rem] bg-neutral-900 border border-white/5"
              >
                {/* Background Sparkle */}
                <div className="absolute -top-24 -right-24 h-64 w-64 bg-purple-500/10 blur-[80px] rounded-full" />

                {/* Header Row */}
                <div className="flex flex-wrap items-end justify-between gap-8 mb-12 relative z-10">
                  <div className="space-y-1">
                    <p className="text-neutral-500 text-xs font-black uppercase tracking-[0.3em] mb-2 px-1">Current State</p>
                    <div className="flex items-baseline gap-3">
                      <p className="text-6xl font-black font-mono tracking-tighter">${data.currentPrice?.toLocaleString()}</p>
                      <span className="text-neutral-600 font-mono text-xl">USD</span>
                    </div>
                  </div>
                  <div className="space-y-1 text-right">
                    <p className="text-neutral-500 text-xs font-black uppercase tracking-[0.3em] mb-2">Hypothesis Outcome (7D)</p>
                    <p className="text-3xl font-black font-mono text-neutral-400 tabular-nums">
                      ${data.rangeLow?.toLocaleString()} - ${data.rangeHigh?.toLocaleString()}
                    </p>
                  </div>
                </div>

                {/* Primary Narrative */}
                <div className="mb-14 relative z-10">
                  <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 mb-6">
                    <History className="h-3.5 w-3.5 text-purple-400" />
                    <span className="text-[10px] font-black uppercase tracking-widest text-neutral-400">Living Narrative Engine</span>
                  </div>
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className={cn("text-7xl font-black tracking-[-0.04em] leading-[0.9] mb-8 uppercase italic", getBiasColor(data.recommendation))}
                  >
                    {data.actionVerb || data.recommendation}
                  </motion.p>

                  <div className="max-w-2xl">
                    <p className="text-xl text-neutral-300 leading-relaxed font-medium">
                      {data.transcendent?.narrative?.content || data.explanation?.summary}
                    </p>
                  </div>
                </div>

                {/* Transcendent Insights Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
                  {/* Hypothesis Testing */}
                  <div className="p-6 rounded-3xl bg-white/5 border border-white/5">
                    <div className="flex items-center gap-2 mb-4 text-purple-400">
                      <Microscope className="h-4 w-4" />
                      <span className="text-[10px] font-black uppercase tracking-widest text-purple-400">Hypothesis State</span>
                    </div>
                    <p className="text-lg font-bold mb-1">{data.transcendent?.hypothesis?.status || "Stable"}</p>
                    <div className="flex items-center gap-2">
                      <div className="h-1.5 w-full bg-neutral-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-purple-500"
                          style={{ width: `${(data.transcendent?.hypothesis?.evidenceScore || 5) * 10}%` }}
                        />
                      </div>
                      <span className="text-[10px] font-mono font-bold text-neutral-500">{data.transcendent?.hypothesis?.evidenceScore}/10</span>
                    </div>
                  </div>

                  {/* Research Question */}
                  <div className="p-6 rounded-3xl bg-white/5 border border-white/5">
                    <div className="flex items-center gap-2 mb-4 text-cyan-400">
                      <BookOpen className="h-4 w-4" />
                      <span className="text-[10px] font-black uppercase tracking-widest text-cyan-400">Research Pivot</span>
                    </div>
                    <p className="text-sm font-bold text-neutral-200 leading-snug">
                      "{data.transcendent?.research?.activeQuestion || "Is liquidity behavior normal?"}"
                    </p>
                  </div>

                  {/* Cross-Domain Coherence */}
                  <div className="p-6 rounded-3xl bg-white/5 border border-white/5">
                    <div className="flex items-center gap-2 mb-4 text-emerald-400">
                      <Globe className="h-4 w-4" />
                      <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">Field Coherence</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <p className="text-lg font-bold">{data.transcendent?.crossDomain?.domainAlignment || "Aligned"}</p>
                      <span className="text-2xl font-black text-emerald-500/50">{data.transcendent?.crossDomain?.coherenceScore}%</span>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* TRANSCENDENT DASHBOARD: THE CEILING */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Epistemic Awareness Card */}
                <div className="p-8 rounded-[2.5rem] bg-gradient-to-br from-neutral-900 to-purple-950/20 border border-purple-500/10">
                  <div className="flex items-center justify-between mb-8">
                    <div className="h-12 w-12 rounded-2xl bg-purple-500/10 flex items-center justify-center">
                      <Binary className="h-6 w-6 text-purple-400" />
                    </div>
                    <span className="text-[10px] font-black tracking-[0.2em] text-purple-500 uppercase">Epistemic Scan</span>
                  </div>
                  <h4 className="text-xl font-black mb-4 uppercase tracking-tight">Boundary Analysis</h4>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-neutral-500">Unknown Unknowns Risk</span>
                      <span className="font-bold text-purple-400">{data.transcendent?.epistemic?.unknownUnknownsRisk}</span>
                    </div>
                    <div className="space-y-2">
                      <span className="text-[10px] font-black text-neutral-600 uppercase">Data Blindness Matrix</span>
                      <div className="flex flex-wrap gap-2">
                        {data.transcendent?.epistemic?.dataBlindness?.map((item: string, i: number) => (
                          <span key={i} className="px-3 py-1 rounded-lg bg-black text-[10px] font-bold text-neutral-400 border border-white/5">
                            {item}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Legacy Memory Card */}
                <div className="p-8 rounded-[2.5rem] bg-gradient-to-br from-neutral-900 to-blue-950/20 border border-blue-500/10">
                  <div className="flex items-center justify-between mb-8">
                    <div className="h-12 w-12 rounded-2xl bg-blue-500/10 flex items-center justify-center">
                      <History className="h-6 w-6 text-blue-400" />
                    </div>
                    <span className="text-[10px] font-black tracking-[0.2em] text-blue-500 uppercase">Generational Learning</span>
                  </div>
                  <h4 className="text-xl font-black mb-4 uppercase tracking-tight">Institutional Memory</h4>
                  <div className="space-y-4">
                    <div>
                      <p className="text-[10px] font-black text-neutral-600 uppercase mb-1">Historical Parallel</p>
                      <p className="text-lg font-bold text-blue-400">{data.transcendent?.legacy?.historicalParallel}</p>
                    </div>
                    <div>
                      <p className="text-[10px] font-black text-neutral-600 uppercase mb-1">Pattern Relevance</p>
                      <p className="text-sm font-medium text-neutral-300 leading-snug">
                        {data.transcendent?.legacy?.lessonsLearned}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Observer Effect & Intelligence Budget */}
              <div className="flex flex-wrap gap-6">
                <div className="flex-1 min-w-[300px] p-6 rounded-3xl bg-white/5 border border-white/5 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-2xl bg-amber-500/10 flex items-center justify-center">
                      <Eye className="h-6 w-6 text-amber-500" />
                    </div>
                    <div>
                      <p className="text-[10px] font-black text-neutral-600 uppercase">Observer Effect</p>
                      <p className="text-sm font-bold text-neutral-200">Reflexivity: {data.transcendent?.observer?.reflexivityIndex}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] font-black text-neutral-600 uppercase">Crowding Risk</p>
                    <p className="text-sm font-bold text-amber-500">{data.transcendent?.observer?.crowdingRisk}</p>
                  </div>
                </div>

                <div className="flex-1 min-w-[300px] p-6 rounded-3xl bg-neutral-900 border border-purple-500/20 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-2xl bg-purple-500/10 flex items-center justify-center">
                      <Target className="h-6 w-6 text-purple-400" />
                    </div>
                    <div>
                      <p className="text-[10px] font-black text-neutral-600 uppercase">Intelligence Budget</p>
                      <p className="text-sm font-bold text-neutral-200">{data.transcendent?.budget?.message}</p>
                    </div>
                  </div>
                  <div className="h-2 w-24 bg-neutral-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-purple-500"
                      style={{ width: `${(data.transcendent?.budget?.remaining / data.transcendent?.budget?.totalBudget) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* RIGHT SIDEBAR: SYSTEM HEALTH & GOVERNANCE */}
            <div className="space-y-8">
              {/* Bayesian Brain */}
              {data.bayesianBeliefs && (
                <div className="p-8 rounded-[2.5rem] bg-neutral-900 border border-white/5 text-center">
                  <Brain className="h-10 w-10 text-purple-500 mx-auto mb-6" />
                  <h3 className="text-sm font-black uppercase tracking-widest text-neutral-500 mb-6">Bayesian Distribution</h3>
                  <div className="flex flex-col gap-6">
                    {Object.entries(data.bayesianBeliefs.beliefs || {}).map(([key, value]: [string, any]) => (
                      <div key={key}>
                        <div className="flex justify-between text-[11px] font-black uppercase mb-2">
                          <span className="text-neutral-500">{key}</span>
                          <span className="text-white">{value}%</span>
                        </div>
                        <div className="h-1.5 w-full bg-neutral-800 rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${value}%` }}
                            className={cn("h-full",
                              key === "Bullish" ? "bg-emerald-500" :
                                key === "Bearish" ? "bg-rose-500" : "bg-purple-500"
                            )}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Active Governance (Omega) */}
              <div className="p-8 rounded-[2.5rem] bg-gradient-to-br from-neutral-900 to-neutral-800 border border-white/5">
                <div className="flex items-center justify-between mb-8">
                  <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-neutral-500">Active Governance</h3>
                  <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                </div>

                <div className="space-y-6">
                  {/* Governance Items */}
                  {[
                    { label: "Silence", status: data.silenceIntelligence?.worthy ? "Proceed" : "Silent", color: data.silenceIntelligence?.worthy ? "text-emerald-400" : "text-neutral-500" },
                    { label: "Humility", status: data.humility?.enforcementNeeded ? "Enforced" : "Nominal", color: "text-blue-400" },
                    { label: "Trust", status: data.trustDebt?.severity || "Nominal", color: data.trustDebt?.severity === "None" ? "text-emerald-400" : "text-rose-400" },
                    { label: "Ethics", status: data.constitution?.active ? "Active" : "Stable", color: "text-cyan-400" }
                  ].map((item, i) => (
                    <div key={i} className="flex items-center justify-between">
                      <span className="text-sm font-black text-neutral-600 uppercase tracking-tighter">{item.label}</span>
                      <span className={cn("text-sm font-mono font-bold", item.color)}>{item.status}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Honors & Integrity */}
              <div className="p-8 rounded-[2.5rem] bg-white/5 border border-white/10 text-center">
                <p className="text-[10px] font-black uppercase tracking-[0.3em] text-neutral-600 mb-2">AI Honesty Grade</p>
                <p className="text-7xl font-black italic text-white mb-2">{data.honestyIndex?.grade || "A"}</p>
                <div className="flex justify-center gap-1">
                  {[1, 2, 3, 4, 5].map(i => (
                    <div key={i} className={cn("h-1 w-4 rounded-full", i <= 4 ? "bg-purple-500" : "bg-neutral-800")} />
                  ))}
                </div>
              </div>

              {/* Regime Context */}
              <div className="p-8 rounded-[2.5rem] bg-neutral-900 border border-white/5">
                <h3 className="text-sm font-black mb-4 tracking-tight uppercase">Regime Logic</h3>
                <div className="p-4 rounded-2xl bg-black border border-white/5 mb-4">
                  <p className="text-xs text-neutral-500 mb-1 uppercase font-bold tracking-widest">Market State</p>
                  <p className="text-lg font-black">{data.regime?.type}</p>
                </div>
                <p className="text-[11px] text-neutral-500 leading-relaxed font-medium">
                  {data.regime?.description}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer (v4.0.0 Stage) */}
      <div className="border-t border-white/5 bg-neutral-950/80 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-12 flex flex-wrap justify-between items-center gap-8">
          <div className="space-y-2">
            <h2 className="text-lg font-black uppercase tracking-tighter italic">Transcendent <span className="text-purple-500">Tier</span></h2>
            <p className="text-[10px] text-neutral-600 font-bold uppercase tracking-[0.3em]">Institutional Grade • 35 Systemic Features</p>
          </div>
          <div className="flex gap-12">
            {[
              { label: "Core", state: "Stable" },
              { label: "Elite", state: "Nominal" },
              { label: "Omega", state: "Enforced" },
              { label: "Transcendent", state: "Syncing" }
            ].map((tier, i) => (
              <div key={i} className="space-y-1">
                <p className="text-[9px] font-black uppercase text-neutral-700 tracking-widest">{tier.label}</p>
                <p className="text-[11px] font-bold text-neutral-400">{tier.state}</p>
              </div>
            ))}
          </div>
          <p className="text-[10px] text-neutral-700 font-medium max-w-[200px] text-right">
            Proprietary self-studying organism. Not for financial advice. Built by NFS Programming.
          </p>
        </div>
      </div>
    </div>
  );
}
