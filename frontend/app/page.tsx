"use client";

import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";

type Mode = "signin" | "signup";

export default function HomePage() {
  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      setLoading(false);
    });
    const { data: listener } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession);
    });
    return () => listener.subscription.unsubscribe();
  }, []);

  if (loading) return <main className="center">Loading DocMind AI…</main>;
  return session ? <Dashboard email={session.user.email ?? ""} /> : <Auth />;
}

function Auth() {
  const [mode, setMode] = useState<Mode>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setMessage("");
    const result = mode === "signin"
      ? await supabase.auth.signInWithPassword({ email, password })
      : await supabase.auth.signUp({ email, password });

    if (result.error) {
      setMessage(result.error.message);
    } else if (mode === "signup") {
      setMessage("Account created. If email confirmation is enabled in Supabase, check your inbox before signing in.");
      setMode("signin");
    }
    setBusy(false);
  }

  return (
    <main className="center shell">
      <section className="auth-card">
        <h1 className="brand">DocMind AI</h1>
        <p className="subtitle">Your private AI knowledge assistant. Upload a PDF and ask questions grounded in its content.</p>
        <form onSubmit={submit}>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input id="password" type="password" autoComplete={mode === "signin" ? "current-password" : "new-password"} minLength={6} required value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <button className="primary" disabled={busy} type="submit">{busy ? "Please wait…" : mode === "signin" ? "Sign in" : "Create account"}</button>
        </form>
        {message && <p className={message.startsWith("Account") ? "success" : "error"}>{message}</p>}
        <div className="switch">
          {mode === "signin" ? "New to DocMind AI? " : "Already have an account? "}
          <button className="link" type="button" onClick={() => { setMode(mode === "signin" ? "signup" : "signin"); setMessage(""); }}>
            {mode === "signin" ? "Create an account" : "Sign in"}
          </button>
        </div>
      </section>
    </main>
  );
}

function Dashboard({ email }: { email: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState("");

  async function upload() {
    if (!file) return setStatus("Choose a PDF first.");
    if (file.type !== "application/pdf") return setStatus("Only PDF documents are supported.");
    setBusy(true);
    setStatus("Uploading and indexing your document…");

    try {
      const { data: { session } } = await supabase.auth.getSession();
      if (!session) throw new Error("Your session has expired. Please sign in again.");

      // Production backend. Keep the environment variable as an override for
      // future environments, but never fall back to localhost in production.
      const apiUrl =
        process.env.NEXT_PUBLIC_API_URL ||
        "https://docmind-ai-iyg7.onrender.com";

      const formData = new FormData();
      formData.append("file", file);

      let response: Response;
      try {
        response = await fetch(apiUrl.replace(/\/$/, "") + "/api/v1/documents/ingest", {
          method: "POST",
          headers: { Authorization: "Bearer " + session.access_token },
          body: formData,
        });
      } catch {
        throw new Error(
          "Cannot reach the DocMind API. Please refresh once and try again."
        );
      }

      const contentType = response.headers.get("content-type") ?? "";
      const data = contentType.includes("application/json")
        ? await response.json()
        : { detail: await response.text() };

      if (!response.ok) {
        throw new Error(data.detail ?? "Document ingestion failed.");
      }

      setStatus("Indexed successfully: " + (data.filename ?? file.name) + ". " + (data.chunk_count ?? 0) + " chunks are ready.");
      setFile(null);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Upload failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="dashboard shell">
      <header className="topbar">
        <div><h1 className="brand">DocMind AI</h1><p>{email}</p></div>
        <button className="secondary" onClick={() => supabase.auth.signOut()}>Sign out</button>
      </header>
      <section className="dashboard-grid">
        <article className="dashboard-card">
          <h2>Upload a document</h2>
          <div className="dropzone">
            <strong>PDF knowledge base</strong>
            <p>Your document is processed into searchable chunks and embeddings.</p>
            <input className="file-input" type="file" accept="application/pdf,.pdf" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
            <button className="primary" style={{ marginTop: 16 }} disabled={busy || !file} onClick={upload}>
              {busy ? "Processing…" : "Upload & index"}
            </button>
          </div>
          {status && <div className="status">{status}</div>}
        </article>
        <article className="dashboard-card">
          <h2>What happens next?</h2>
          <p className="subtitle">DocMind extracts each page, creates overlapping chunks, generates embeddings, and stores them in your private Supabase vector database.</p>
          <p className="subtitle">The next step will add your document library and grounded chat with page-level citations.</p>
        </article>
      </section>
    </main>
  );
}