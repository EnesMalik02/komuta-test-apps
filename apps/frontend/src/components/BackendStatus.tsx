"use client";

import { useEffect, useState } from "react";
import { fetchHealth, type HealthStatus } from "@/lib/api";

export function BackendStatus({ name, baseUrl }: { name: string; baseUrl: string }) {
  const [status, setStatus] = useState<HealthStatus | "loading" | "error">("loading");

  useEffect(() => {
    fetchHealth(baseUrl)
      .then(setStatus)
      .catch(() => setStatus("error"));
  }, [baseUrl]);

  return (
    <div className="rounded-lg border border-black/10 p-4 dark:border-white/15">
      <h2 className="font-semibold">{name}</h2>
      <p className="text-sm text-black/60 dark:text-white/60">{baseUrl}</p>
      {status === "loading" && <p>checking…</p>}
      {status === "error" && <p className="text-red-600">unreachable</p>}
      {typeof status === "object" && (
        <ul className="mt-2 text-sm">
          {Object.entries(status).map(([service, value]) => (
            <li key={service}>
              {service}: {value === "ok" ? "✅ ok" : `⚠️ ${value}`}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
