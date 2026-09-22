import { BackendStatus } from "@/components/BackendStatus";
import { GO_API_URL, PY_API_URL } from "@/lib/api";

export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex w-full max-w-3xl flex-col gap-6 py-16 px-8">
        <h1 className="text-2xl font-semibold">komuta-test-apps</h1>
        <div className="grid gap-4 sm:grid-cols-2">
          <BackendStatus name="backend-go" baseUrl={GO_API_URL} />
          <BackendStatus name="backend-python" baseUrl={PY_API_URL} />
        </div>
      </main>
    </div>
  );
}
