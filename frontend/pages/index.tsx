import { useSession, signIn, signOut } from "next-auth/react";
import { useState } from "react";

export default function Home() {
  const { data: session } = useSession();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string>("");

  async function sendPrompt() {
    setLoading(true);
    setErr("");
    setAnswer("");

    try {
const API_BASE =
      process.env.NEXT_PUBLIC_API_BASE_URL ??
      "https://chat-vwg8.onrender.com";
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });


      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `Request failed: ${res.status}`);
      }

      const data = await res.json();
      setAnswer(data.response ?? "");
    } catch (e: unknown) {
      const message =
        e instanceof Error ? e.message : typeof e === "string" ? e : "Something went wrong";
      setErr(message);
    } finally {
      setLoading(false);
    }

  }

  if (session) {
    return (
      <div style={{ padding: 16 }}>
        <p>Signed in as {session.user?.email}</p>
        <button onClick={() => signOut()}>Sign out</button>

        <hr />

        <h2>Chat</h2>
        <textarea
          placeholder="Type a message..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={4}
          style={{ width: "100%" }}
        />
        <button disabled={loading || !prompt.trim()} onClick={sendPrompt}>
          {loading ? "Sending..." : "Send"}
        </button>

        {err && <p style={{ color: "red" }}>{err}</p>}
        {answer && (
          <div style={{ marginTop: 12, whiteSpace: "pre-wrap" }}>
            <strong>Response:</strong>
            <div>{answer}</div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div style={{ padding: 16 }}>
      <h1>Login</h1>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={() => signIn("credentials", { email, password })}>
        Sign in
      </button>
    </div>
  );
}
