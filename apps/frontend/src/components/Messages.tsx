"use client";

import { useCallback, useEffect, useState } from "react";
import { GO_API_URL, PY_API_URL } from "@/lib/api";

type Message = { id: number; text: string; status: string };

export function Messages() {
  const [text, setText] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [processed, setProcessed] = useState(0);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    try {
      const [m, s] = await Promise.all([
        fetch(`${PY_API_URL}/messages`, { cache: "no-store" }).then((r) => r.json()),
        fetch(`${GO_API_URL}/stats`, { cache: "no-store" }).then((r) => r.json()),
      ]);
      setMessages(m);
      setProcessed(s.processed);
    } catch {
      setError("backend unreachable");
    }
  }, []);

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 2000);
    return () => clearInterval(t);
  }, [refresh]);

  async function send(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    const res = await fetch(`${PY_API_URL}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) return setError(`send failed (${res.status})`);
    setText("");
    refresh();
  }

  return (
    <div className="rounded-lg border border-black/10 p-4 dark:border-white/15">
      <h2 className="font-semibold">messages (python → rabbitmq → go)</h2>
      <p className="text-sm text-black/60 dark:text-white/60">processed (valkey): {processed}</p>
      <form onSubmit={send} className="mt-2 flex gap-2">
        <input
          required
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="flex-1 rounded border border-black/20 px-2 py-1 dark:bg-transparent"
        />
        <button className="rounded bg-black px-3 py-1 text-white dark:bg-white dark:text-black">send</button>
      </form>
      {error && <p className="text-red-600">{error}</p>}
      <ul className="mt-2 text-sm">
        {messages.map((m) => (
          <li key={m.id}>
            #{m.id} {m.text} — {m.status === "processed" ? "✅ processed" : "⏳ pending"}
          </li>
        ))}
      </ul>
    </div>
  );
}
