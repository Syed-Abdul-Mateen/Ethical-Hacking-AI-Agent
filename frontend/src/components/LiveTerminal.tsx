"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface Log {
  message: string;
  level: string;
  timestamp: string;
}

export default function LiveTerminal({ logs }: { logs: Log[] }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="glass-panel h-64 overflow-hidden flex flex-col border border-white/10">
      <div className="bg-white/5 px-4 py-2 flex items-center justify-between border-b border-white/10">
        <span className="text-xs font-bold uppercase tracking-widest text-emerald-500">Live Operation Logs</span>
        <div className="flex gap-1.5">
          <div className="w-2 h-2 rounded-full bg-red-500/50" />
          <div className="w-2 h-2 rounded-full bg-yellow-500/50" />
          <div className="w-2 h-2 rounded-full bg-green-500/50" />
        </div>
      </div>
      <div 
        ref={scrollRef}
        className="flex-1 p-4 overflow-y-auto terminal-text text-sm space-y-1 bg-black/40"
      >
        {logs.length === 0 && (
          <div className="text-white/20 animate-pulse">Waiting for mission start...</div>
        )}
        {logs.map((log, i) => (
          <div key={i} className="flex gap-3">
            <span className="text-white/30 shrink-0">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
            <span className={cn(
              "break-all",
              log.level === "ERROR" ? "text-red-400" : 
              log.level === "SUCCESS" ? "text-emerald-400" : 
              "text-blue-300"
            )}>
              {log.message}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
