// NEXT_PUBLIC_* values are inlined by `next build`; runtime env has no effect.
const checks = [
  { name: "NEXT_PUBLIC_TEST_ONE", expected: "komuta-one", actual: process.env.NEXT_PUBLIC_TEST_ONE },
  { name: "NEXT_PUBLIC_TEST_TWO", expected: "komuta-two", actual: process.env.NEXT_PUBLIC_TEST_TWO },
];

export default function Home() {
  const allOk = checks.every((c) => c.actual === c.expected);
  return (
    <main>
      <h1>{allOk ? "✅ Build-time env DOĞRU" : "❌ Build-time env YANLIŞ"}</h1>
      <ul>
        {checks.map((c) => (
          <li key={c.name}>
            {c.actual === c.expected ? "✅" : "❌"} <code>{c.name}</code> — gelen:{" "}
            <code>{c.actual ?? "(yok)"}</code>, beklenen: <code>{c.expected}</code>
          </li>
        ))}
      </ul>
    </main>
  );
}
