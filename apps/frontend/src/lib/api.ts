export const GO_API_URL = process.env.NEXT_PUBLIC_GO_API_URL ?? "http://localhost:8080";
export const PY_API_URL = process.env.NEXT_PUBLIC_PY_API_URL ?? "http://localhost:8000";

export type HealthStatus = Record<"postgres" | "valkey" | "rabbitmq", string>;

export async function fetchHealth(baseUrl: string): Promise<HealthStatus> {
  const res = await fetch(`${baseUrl}/health`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${baseUrl}/health -> ${res.status}`);
  return res.json();
}
