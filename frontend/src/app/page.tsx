"use client";

import { useState, useEffect, useRef } from "react";
import { io, Socket } from "socket.io-client";
import axios from "axios";
import { useRouter } from "next/navigation";
import {
  Shield, Target, Activity, AlertTriangle,
  FileText, Zap, Clock, CheckCircle, XCircle,
  Download, ChevronDown, ChevronUp, Globe, LogOut
} from "lucide-react";
import LiveTerminal from "@/components/LiveTerminal";
import { cn } from "@/lib/utils";

const API_BASE = "http://localhost:8000";

// Configure Axios Interceptor for JWT
axios.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

interface Finding {
  id: number;
  title: string;
  severity: string;
  description: string;
  endpoint?: string;
  payload?: string;
  remediation?: string;
}

interface ScanMetrics {
  total_endpoints: number;
  total_forms: number;
  critical_findings: number;
  high_findings: number;
}

interface HistoryScan {
  id: string;
  target_url: string;
  status: string;
  critical_findings: number;
  high_findings: number;
  created_at: string;
}

export default function Dashboard() {
  const [url, setUrl] = useState("");
  const [isScanning, setIsScanning] = useState(false);
  const [scanId, setScanId] = useState<string | null>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [status, setStatus] = useState<any>({ phase: "Idle", progress: 0, message: "Ready for mission" });
  const [socket, setSocket] = useState<Socket | null>(null);
  const [metrics, setMetrics] = useState<ScanMetrics>({ total_endpoints: 0, total_forms: 0, critical_findings: 0, high_findings: 0 });
  const [findings, setFindings] = useState<Finding[]>([]);
  const [history, setHistory] = useState<HistoryScan[]>([]);
  const [expandedFinding, setExpandedFinding] = useState<number | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const scanIdRef = useRef<string | null>(null);
  const router = useRouter();

  // Authentication & History Load
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    axios.get(`${API_BASE}/scans/history`)
      .then(r => setHistory(r.data))
      .catch((err) => {
        if (err.response?.status === 401) {
          localStorage.removeItem("token");
          router.push("/login");
        }
      });
  }, [router]);

  // WebSocket connection
  useEffect(() => {
    const s = io(API_BASE, { transports: ["websocket", "polling"] });
    s.on("connect", () => console.log("WebSocket connected successfully"));
    s.on("connect_error", (e) => console.error("WebSocket error:", e));

    s.on("scan_log", (data) => {
      if (data.scan_id === scanIdRef.current) {
        setLogs((prev) => [...prev, data]);
      }
    });

    s.on("scan_status", (data) => {
      if (data.scan_id === scanIdRef.current) {
        setStatus(data);
        if (data.progress === 100) {
          setIsScanning(false);
          // Fetch full results when complete
          fetchScanResults(data.scan_id);
          axios.get(`${API_BASE}/scans/history`).then(r => setHistory(r.data)).catch(() => {});
        }
      }
    });

    setSocket(s);
    return () => { s.disconnect(); };
  }, []);

  const fetchScanResults = async (id: string) => {
    try {
      const resp = await axios.get(`${API_BASE}/scan/${id}`);
      setMetrics(resp.data.metrics || {});
      setFindings(resp.data.findings || []);
    } catch (err) {
      console.error("Failed to fetch scan results:", err);
    }
  };

  const startScan = async () => {
    if (!url) return;
    setIsScanning(true);
    setLogs([]);
    setFindings([]);
    setMetrics({ total_endpoints: 0, total_forms: 0, critical_findings: 0, high_findings: 0 });
    setStatus({ phase: "Initializing", progress: 5, message: "Contacting command center..." });

    try {
      const resp = await axios.post(`${API_BASE}/scan/start?target_url=${encodeURIComponent(url)}`);
      const newScanId = resp.data.scan_id;
      setScanId(newScanId);
      scanIdRef.current = newScanId;
    } catch (err) {
      console.error(err);
      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        router.push("/login");
        return;
      }
      setIsScanning(false);
      setStatus({ phase: "Failed", progress: 0, message: "Backend unreachable or unauthorized." });
    }
  };

  const downloadReport = async (format: "pdf" | "sarif") => {
    if (!scanId) return;
    setIsDownloading(true);
    try {
      const resp = await axios.get(`${API_BASE}/scan/${scanId}/report/${format}`, { responseType: "blob" });
      const ext = format === "pdf" ? "pdf" : "sarif.json";
      const blobUrl = window.URL.createObjectURL(new Blob([resp.data]));
      const link = document.createElement("a");
      link.href = blobUrl;
      link.setAttribute("download", `security_report_${scanId.slice(0, 8)}.${ext}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch {
      alert("Report not yet available. Please wait for the scan to complete.");
    } finally {
      setIsDownloading(false);
    }
  };

  const getSeverityColor = (sev: string) => ({
    critical: "text-red-400 bg-red-500/10 border-red-500/30",
    high: "text-orange-400 bg-orange-500/10 border-orange-500/30",
    medium: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30",
    low: "text-blue-400 bg-blue-500/10 border-blue-500/30",
  }[sev.toLowerCase()] || "text-gray-400 bg-gray-500/10 border-gray-500/30");

  const getStatusIcon = (s: string) => {
    if (s === "completed") return <CheckCircle className="w-4 h-4 text-emerald-400" />;
    if (s === "failed") return <XCircle className="w-4 h-4 text-red-400" />;
    return <Clock className="w-4 h-4 text-yellow-400 animate-spin" />;
  };

  return (
    <main className="min-h-screen bg-[#0a0a0f] text-white relative overflow-hidden">
      {/* Animated top accent line */}
      <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-emerald-500 to-transparent shadow-[0_0_15px_rgba(16,185,129,0.5)]" />

      {/* Background grain */}
      <div className="absolute inset-0 opacity-10 pointer-events-none"
        style={{ backgroundImage: "radial-gradient(circle at 20% 50%, #064e3b22, transparent 50%), radial-gradient(circle at 80% 20%, #0e7490aa, transparent 50%)" }} />

      <div className="max-w-7xl mx-auto p-6 md:p-10 relative z-10">

        {/* Header */}
        <header className="mb-10">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <h1 className="text-4xl font-extrabold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 flex items-center gap-3">
                <Shield className="w-10 h-10 text-emerald-500 shrink-0" />
                ETHICAL HACKING AI AGENT
              </h1>
              <div className="flex items-center gap-4 mt-1">
                <p className="text-white/40 text-sm font-medium tracking-widest uppercase">
                  Autonomous Security Operation Center v2.0
                </p>
                <button 
                  onClick={() => { localStorage.removeItem("token"); router.push("/login"); }}
                  className="text-xs flex items-center gap-1 text-red-400/70 hover:text-red-400 transition-colors"
                >
                  <LogOut className="w-3 h-3" />
                  DISCONNECT
                </button>
              </div>
            </div>

            {/* Target Input */}
            <div className="flex gap-3 w-full md:w-auto">
              <div className="relative flex-1 md:w-96">
                <Globe className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && !isScanning && startScan()}
                  placeholder="https://target.com"
                  className="w-full bg-white/5 border border-white/10 pl-10 pr-4 py-3 rounded-full outline-none focus:border-emerald-500/60 transition-all text-emerald-100 placeholder:text-white/20 text-sm"
                  disabled={isScanning}
                />
              </div>
              <button
                onClick={startScan}
                disabled={isScanning || !url}
                className={cn(
                  "px-6 py-3 rounded-full font-bold transition-all flex items-center gap-2 text-sm shrink-0",
                  isScanning || !url
                    ? "bg-white/5 text-white/30 cursor-not-allowed"
                    : "bg-emerald-500 text-[#0a0a0f] hover:bg-emerald-400 hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(16,185,129,0.3)]"
                )}
              >
                <Zap className={cn("w-4 h-4", isScanning && "animate-pulse")} />
                {isScanning ? "OPERATING..." : "INITIATE ATTACK"}
              </button>
            </div>
          </div>
        </header>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* Left: Mission Control + Terminal */}
          <div className="lg:col-span-2 space-y-6">

            {/* Mission Control Progress */}
            <div className="glass-panel p-6 border border-emerald-500/10 rounded-2xl">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold flex items-center gap-2 text-emerald-400">
                  <Activity className="w-5 h-5" /> Mission Control
                </h3>
                <span className="text-xs font-mono text-white/30 uppercase tracking-widest">
                  OP: {scanId ? scanId.slice(0, 8).toUpperCase() : "IDLE"}
                </span>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-end">
                  <span className="text-3xl font-black tracking-tighter">{status.phase}</span>
                  <span className="text-emerald-400 font-mono text-lg">{status.progress}%</span>
                </div>
                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden border border-white/5">
                  <div
                    className="h-full bg-gradient-to-r from-emerald-700 to-emerald-400 rounded-full transition-all duration-700 shadow-[0_0_10px_rgba(16,185,129,0.5)]"
                    style={{ width: `${status.progress}%` }}
                  />
                </div>
                <p className="text-white/50 text-sm flex items-center gap-2">
                  <span className={cn("w-1.5 h-1.5 rounded-full", isScanning ? "bg-emerald-500 animate-ping" : "bg-white/20")} />
                  {status.message}
                </p>
              </div>
            </div>

            {/* Live Terminal */}
            <LiveTerminal logs={logs} />

            {/* Findings Table (shown after scan) */}
            {findings.length > 0 && (
              <div className="glass-panel border border-red-500/10 rounded-2xl overflow-hidden">
                <div className="p-4 border-b border-white/5 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-red-400" />
                  <h3 className="font-bold">Vulnerability Intelligence ({findings.length} findings)</h3>
                </div>
                <div className="divide-y divide-white/5">
                  {findings.map((f) => (
                    <div key={f.id} className="p-4">
                      <button
                        className="w-full text-left flex justify-between items-start gap-4"
                        onClick={() => setExpandedFinding(expandedFinding === f.id ? null : f.id)}
                      >
                        <div className="flex items-center gap-3 flex-1">
                          <span className={cn("text-xs font-bold px-2 py-0.5 rounded border uppercase shrink-0", getSeverityColor(f.severity))}>
                            {f.severity}
                          </span>
                          <span className="font-semibold text-sm">{f.title}</span>
                        </div>
                        {expandedFinding === f.id
                          ? <ChevronUp className="w-4 h-4 text-white/30 shrink-0" />
                          : <ChevronDown className="w-4 h-4 text-white/30 shrink-0" />}
                      </button>

                      {expandedFinding === f.id && (
                        <div className="mt-4 space-y-3 text-sm text-white/60 pl-4 border-l border-white/10">
                          {f.endpoint && (
                            <div><span className="text-white/30 uppercase text-xs tracking-widest block mb-1">Endpoint</span>
                              <code className="text-emerald-400 font-mono text-xs">{f.endpoint}</code></div>
                          )}
                          <div><span className="text-white/30 uppercase text-xs tracking-widest block mb-1">Description</span>
                            <p>{f.description}</p></div>
                          {f.payload && (
                            <div><span className="text-white/30 uppercase text-xs tracking-widest block mb-1">Payload Used</span>
                              <code className="bg-black/30 px-2 py-1 rounded text-red-400 font-mono text-xs block">{f.payload}</code></div>
                          )}
                          {f.remediation && (
                            <div><span className="text-white/30 uppercase text-xs tracking-widest block mb-1">AI Remediation</span>
                              <p className="text-emerald-300">{f.remediation}</p></div>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right: Stats Sidebar */}
          <div className="space-y-5">

            {/* Threat Profile */}
            <div className="glass-panel p-5 border border-red-500/10 rounded-2xl">
              <div className="flex items-center gap-2 mb-4">
                <AlertTriangle className="w-5 h-5 text-red-500" />
                <h3 className="font-bold text-sm">Threat Profile</h3>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-red-500/5 p-4 rounded-xl border border-red-500/20">
                  <span className="text-xs block text-red-400 uppercase font-bold tracking-widest mb-1">Critical</span>
                  <span className="text-3xl font-black">{metrics.critical_findings}</span>
                </div>
                <div className="bg-orange-500/5 p-4 rounded-xl border border-orange-500/20">
                  <span className="text-xs block text-orange-400 uppercase font-bold tracking-widest mb-1">High Risk</span>
                  <span className="text-3xl font-black">{metrics.high_findings}</span>
                </div>
              </div>
            </div>

            {/* Target Intelligence */}
            <div className="glass-panel p-5 border border-emerald-500/10 rounded-2xl">
              <div className="flex items-center gap-2 mb-4">
                <Target className="w-5 h-5 text-emerald-500" />
                <h3 className="font-bold text-sm">Target Intelligence</h3>
              </div>
              <div className="space-y-2 text-sm">
                {[
                  { label: "Endpoints", val: metrics.total_endpoints },
                  { label: "Forms Found", val: metrics.total_forms },
                  { label: "Total Findings", val: findings.length },
                ].map(({ label, val }) => (
                  <div key={label} className="flex justify-between py-2 border-b border-white/5">
                    <span className="text-white/40">{label}</span>
                    <span className="font-mono text-emerald-400">{val}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Export Reports */}
            <div className="glass-panel p-5 border border-white/5 rounded-2xl space-y-3">
              <h3 className="font-bold text-sm flex items-center gap-2">
                <Download className="w-4 h-4 text-emerald-500" /> Export Intelligence
              </h3>
              <button
                onClick={() => downloadReport("pdf")}
                disabled={!scanId || status.progress < 100 || isDownloading}
                className={cn(
                  "w-full flex items-center justify-center gap-2 py-3 rounded-xl border text-sm font-bold transition-all",
                  scanId && status.progress === 100
                    ? "border-red-500/30 text-red-400 hover:bg-red-500/10 active:scale-95"
                    : "border-white/5 text-white/20 cursor-not-allowed"
                )}
              >
                <FileText className="w-4 h-4" />
                Download PDF Report
              </button>
              <button
                onClick={() => downloadReport("sarif")}
                disabled={!scanId || status.progress < 100 || isDownloading}
                className={cn(
                  "w-full flex items-center justify-center gap-2 py-3 rounded-xl border text-sm font-bold transition-all",
                  scanId && status.progress === 100
                    ? "border-blue-500/30 text-blue-400 hover:bg-blue-500/10 active:scale-95"
                    : "border-white/5 text-white/20 cursor-not-allowed"
                )}
              >
                <FileText className="w-4 h-4" />
                Export SARIF (CI/CD)
              </button>
              {(!scanId || status.progress < 100) && (
                <p className="text-white/20 text-xs text-center">Available after scan completes</p>
              )}
            </div>

            {/* Scan History */}
            {history.length > 0 && (
              <div className="glass-panel p-5 border border-white/5 rounded-2xl">
                <h3 className="font-bold text-sm mb-4 flex items-center gap-2">
                  <Clock className="w-4 h-4 text-white/40" /> Recent Operations
                </h3>
                <div className="space-y-2">
                  {history.slice(0, 5).map((scan) => (
                    <div key={scan.id} className="flex items-center gap-3 py-2 border-b border-white/5 text-xs">
                      {getStatusIcon(scan.status)}
                      <div className="flex-1 min-w-0">
                        <p className="text-white/70 truncate font-mono">{scan.target_url}</p>
                        <p className="text-white/30">{new Date(scan.created_at).toLocaleString()}</p>
                      </div>
                      <div className="text-right shrink-0">
                        <span className="text-red-400 font-bold">{scan.critical_findings}C</span>
                        <span className="text-white/20 mx-1">/</span>
                        <span className="text-orange-400 font-bold">{scan.high_findings}H</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
