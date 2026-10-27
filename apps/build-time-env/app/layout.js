export const metadata = { title: "build-time-env" };

export default function RootLayout({ children }) {
  return (
    <html lang="tr">
      <body style={{ fontFamily: "system-ui, sans-serif", padding: 24 }}>{children}</body>
    </html>
  );
}
