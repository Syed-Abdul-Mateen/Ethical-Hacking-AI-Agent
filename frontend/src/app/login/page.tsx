"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Shield, Lock, User, ArrowRight, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        throw new Error("Invalid Authorization Credentials");
      }

      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      router.push("/");
    } catch (err: any) {
      setError(err.message || "Failed to authenticate with command center.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0f] text-white relative flex items-center justify-center overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 opacity-20 pointer-events-none"
        style={{ backgroundImage: "radial-gradient(circle at 50% 0%, #064e3b, transparent 50%), radial-gradient(circle at 50% 100%, #0e7490, transparent 50%)" }} />
      
      {/* Grid Pattern */}
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none" 
        style={{ backgroundImage: "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)", backgroundSize: "50px 50px" }} />

      <div className="relative z-10 w-full max-w-md p-8">
        
        {/* Header */}
        <div className="flex flex-col items-center mb-10">
          <div className="w-20 h-20 bg-emerald-500/10 rounded-2xl border border-emerald-500/20 flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(16,185,129,0.15)] relative">
            <div className="absolute inset-0 bg-emerald-500/20 blur-xl rounded-full animate-pulse" />
            <Shield className="w-10 h-10 text-emerald-400 relative z-10" />
          </div>
          <h1 className="text-3xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
            SYSTEM LOGIN
          </h1>
          <p className="text-white/40 text-sm mt-2 font-mono tracking-widest uppercase text-center">
            Restricted SOC Authorization Required
          </p>
        </div>

        {/* Login Form */}
        <div className="glass-panel p-8 rounded-3xl border border-emerald-500/10 shadow-2xl relative overflow-hidden">
          {/* Animated top border */}
          <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-emerald-500 to-transparent opacity-50" />
          
          <form onSubmit={handleLogin} className="space-y-6 relative z-10">
            
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-mono p-3 rounded-lg flex items-center gap-2">
                <Lock className="w-4 h-4 shrink-0" />
                {error}
              </div>
            )}

            <div className="space-y-4">
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-emerald-500/50" />
                <input
                  type="text"
                  placeholder="Operator ID (admin)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-black/40 border border-white/10 pl-11 pr-4 py-3 rounded-xl outline-none focus:border-emerald-500/60 transition-all text-emerald-100 placeholder:text-white/20 text-sm font-mono"
                  disabled={isLoading}
                  required
                />
              </div>

              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-emerald-500/50" />
                <input
                  type="password"
                  placeholder="Passcode (admin123)"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-black/40 border border-white/10 pl-11 pr-4 py-3 rounded-xl outline-none focus:border-emerald-500/60 transition-all text-emerald-100 placeholder:text-white/20 text-sm font-mono"
                  disabled={isLoading}
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading || !username || !password}
              className={cn(
                "w-full py-4 rounded-xl font-bold transition-all flex items-center justify-center gap-2 text-sm",
                isLoading || !username || !password
                  ? "bg-white/5 text-white/30 cursor-not-allowed border border-white/5"
                  : "bg-emerald-500 text-[#0a0a0f] hover:bg-emerald-400 hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_20px_rgba(16,185,129,0.3)] border border-emerald-400"
              )}
            >
              {isLoading ? (
                <>
                  <Zap className="w-4 h-4 animate-pulse" />
                  AUTHENTICATING...
                </>
              ) : (
                <>
                  INITIALIZE UPLINK
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>

        <div className="mt-8 text-center text-xs text-white/20 font-mono flex items-center justify-center gap-2">
          <span className="w-1 h-1 rounded-full bg-emerald-500/50 animate-ping" />
          SECURE CONNECTION ESTABLISHED
        </div>
      </div>
    </main>
  );
}
