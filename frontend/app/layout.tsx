import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DocMind AI — Private AI Knowledge Assistant",
  description: "Ask questions over your documents with grounded answers and page-level citations.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}