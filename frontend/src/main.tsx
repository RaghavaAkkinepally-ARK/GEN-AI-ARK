import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

interface Citation {
  source: string;
  passage: string;
  score: number;
}

type View = "chat" | "profile" | "history" | "evaluations" | "privacy";

interface FarmProfile {
  farmName: string;
  location: string;
  soilType: string;
  irrigation: string;
  crop: string;
  acreage: string;
  season: string;
}

interface ChatRecord {
  id: number;
  question: string;
  answer: string;
  status: string;
  citations: Citation[];
  imageName?: string;
  createdAt: string;
}

interface Account {
  name: string;
  email: string;
}

const defaultProfile: FarmProfile = {
  farmName: "",
  location: "",
  soilType: "Loam",
  irrigation: "Rainfed",
  crop: "Rice",
  acreage: "",
  season: "Kharif",
};

function readProfile(): FarmProfile {
  try {
    return { ...defaultProfile, ...JSON.parse(localStorage.getItem("agriculturegpt-profile") || "{}") };
  } catch {
    return defaultProfile;
  }
}

function readHistory(): ChatRecord[] {
  try {
    return JSON.parse(localStorage.getItem("agriculturegpt-history") || "[]");
  } catch {
    return [];
  }
}

function readAccount(): Account | null {
  try {
    return JSON.parse(localStorage.getItem("agriculturegpt-account") || "null");
  } catch {
    return null;
  }
}

function viewFromHash(): View {
  const hash = window.location.hash.replace("#", "");
  return ["chat", "profile", "history", "evaluations", "privacy"].includes(hash)
    ? hash as View
    : "chat";
}

function Icon({ name }: { name: string }) {
  const icons: Record<string, React.ReactNode> = {
    chat: <svg viewBox="0 0 24 24"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v7a2.5 2.5 0 0 1-2.5 2.5H10l-5 4v-4.2A2.5 2.5 0 0 1 3 12.5v-7Z"/></svg>,
    profile: <svg viewBox="0 0 24 24"><path d="M12 13a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm-8 8a8 8 0 0 1 16 0"/></svg>,
    history: <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 3-6.7L3 8m0-5v5h5M12 7v5l3 2"/></svg>,
    evaluation: <svg viewBox="0 0 24 24"><path d="M4 20V10m5 10V4m6 16v-7m5 7V7"/></svg>,
    privacy: <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Zm-3-10 2 2 4-5"/></svg>,
    image: <svg viewBox="0 0 24 24"><path d="M4 5h16v14H4V5Zm0 11 4-4 3 3 3-4 6 5M8.5 9.5h.01"/></svg>,
  };
  return <span className="icon">{icons[name]}</span>;
}

function App() {
  const [view, setView] = useState<View>(viewFromHash());
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [status, setStatus] = useState("Ready");
  const [busy, setBusy] = useState(false);
  const [profile, setProfile] = useState<FarmProfile>(readProfile);
  const [history, setHistory] = useState<ChatRecord[]>(readHistory);
  const [account, setAccount] = useState<Account | null>(readAccount);
  const [authOpen, setAuthOpen] = useState(false);
  const [authMode, setAuthMode] = useState<"signin" | "signup">("signin");
  const [authName, setAuthName] = useState("");
  const [authEmail, setAuthEmail] = useState("");
  const [authPassword, setAuthPassword] = useState("");
  const [saved, setSaved] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState("");

  useEffect(() => {
    const onHashChange = () => setView(viewFromHash());
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  function navigate(nextView: View) {
    window.location.hash = nextView;
    setView(nextView);
  }

  function chooseImage(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      setStatus("Please choose an image");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setStatus("Image must be under 10 MB");
      return;
    }
    setImageFile(file);
    setStatus("Image ready");
    const reader = new FileReader();
    reader.onload = () => setImagePreview(String(reader.result));
    reader.readAsDataURL(file);
  }

  async function submitQuery(event: React.FormEvent) {
    event.preventDefault();
    if ((!query.trim() && !imageFile) || busy) return;
    setBusy(true);
    setStatus(imageFile ? "Analyzing image..." : "Searching evidence...");
    setAnswer("");
    setCitations([]);
    try {
      let data: Record<string, unknown>;
      if (imageFile) {
        const base64 = await new Promise<string>((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(String(reader.result).split(",")[1] || "");
          reader.onerror = () => reject(new Error("Unable to read the image."));
          reader.readAsDataURL(imageFile);
        });
        const response = await fetch("/api/advisory/diagnose", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            filename: imageFile.name,
            content_type: imageFile.type,
            size: imageFile.size,
            image_base64: base64,
            question: query,
          }),
        });
        if (!response.ok) throw new Error("The image service is unavailable.");
        data = await response.json();
      } else {
        const response = await fetch("/api/rag/query", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query, k: 4 }),
        });
        if (!response.ok) throw new Error("The advisory service is unavailable.");
        data = await response.json();
      }
      const nextCitations = (data.citations as Citation[]) ?? [];
      setAnswer(String(data.answer));
      setCitations(nextCitations);
      setStatus(String(data.evidence_status || data.status));
      const record: ChatRecord = {
        id: Date.now(),
        question: query || `Crop image: ${imageFile?.name}`,
        answer: String(data.answer),
        status: String(data.evidence_status || data.status),
        citations: nextCitations,
        imageName: imageFile?.name,
        createdAt: new Date().toISOString(),
      };
      const nextHistory = [record, ...history].slice(0, 100);
      setHistory(nextHistory);
      localStorage.setItem("agriculturegpt-history", JSON.stringify(nextHistory));
      setImageFile(null);
      setImagePreview("");
    } catch (error) {
      setAnswer(error instanceof Error ? error.message : "Unable to retrieve advisory.");
      setStatus("service_error");
    } finally {
      setBusy(false);
    }
  }

  function saveProfile(event: React.FormEvent) {
    event.preventDefault();
    localStorage.setItem("agriculturegpt-profile", JSON.stringify(profile));
    setSaved("Farm profile saved on this device.");
  }

  function createAccount(event: React.FormEvent) {
    event.preventDefault();
    if (!authEmail.trim() || authPassword.length < 6) return;
    const nextAccount = {
      name: authName.trim() || authEmail.split("@")[0],
      email: authEmail.trim(),
    };
    localStorage.setItem("agriculturegpt-account", JSON.stringify(nextAccount));
    setAccount(nextAccount);
    setAuthOpen(false);
    setAuthPassword("");
  }

  function signOut() {
    localStorage.removeItem("agriculturegpt-account");
    setAccount(null);
  }

  const navItems: { id: View; label: string; icon: string }[] = [
    { id: "chat", label: "AI Advisory", icon: "chat" },
    { id: "profile", label: "Farm Profile", icon: "profile" },
    { id: "history", label: "History", icon: "history" },
    { id: "evaluations", label: "Evaluations", icon: "evaluation" },
    { id: "privacy", label: "Privacy", icon: "privacy" },
  ];

  return (
    <main className="app-shell">
      <aside>
        <button className="brand" onClick={() => navigate("chat")} aria-label="Go to AI advisory">
          <span className="brand-mark">A</span>
          <span><strong>Agriculture</strong>GPT</span>
        </button>
        <nav aria-label="Main navigation">
          {navItems.map((item) => (
            <a key={item.id} className={view === item.id ? "active" : ""} href={`#${item.id}`}>
              <Icon name={item.icon} />{item.label}
            </a>
          ))}
        </nav>
        <div className="aside-footer">
          {account ? (
            <button className="account" onClick={signOut} title="Sign out">
              <span className="avatar">{account.name.slice(0, 1).toUpperCase()}</span>
              <span><strong>{account.name}</strong><small>{account.email}</small></span>
            </button>
          ) : (
            <button className="account sign-in" onClick={() => setAuthOpen(true)}>
              <span className="avatar">?</span><span><strong>Sign in</strong><small>Save your farm workspace</small></span>
            </button>
          )}
        </div>
      </aside>

      {view === "chat" && (
        <section className="workspace">
          <header className="topbar">
            <div><p className="eyebrow">Precision crop assistant</p><h1>Ask about your crops</h1></div>
            <div className="top-actions">
              <button className="new-chat" onClick={() => { setQuery(""); setAnswer(""); setCitations([]); setStatus("Ready"); }}>+ New query</button>
              {account && <button className="avatar-button" onClick={() => setAuthOpen(true)}>{account.name.slice(0, 1).toUpperCase()}</button>}
            </div>
          </header>

          <div className="context-strip">
            <span className="live-dot"></span>
            <span>{profile.crop || "Crop"} advisor</span>
            <span>{profile.location || "Location not set"}</span>
            <button onClick={() => navigate("profile")}>Edit profile</button>
          </div>

          <form onSubmit={submitQuery} className={`composer ${imagePreview ? "with-image" : ""}`}>
            {imagePreview && (
              <div className="image-preview">
                <img src={imagePreview} alt="Crop upload preview" />
                <button type="button" onClick={() => { setImageFile(null); setImagePreview(""); setStatus("Ready"); }} aria-label="Remove image">×</button>
                <span>{imageFile?.name}</span>
              </div>
            )}
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Ask about pests, irrigation, soil, fertilizer, or crop health..."
              aria-label="Agricultural question"
            />
            <div className="composer-actions">
              <label className="image-button" title="Upload a crop image">
                <Icon name="image" /><input type="file" accept="image/jpeg,image/png,image/webp" onChange={chooseImage} />
              </label>
              <span className={`status ${status.toLowerCase().replace(/[^a-z]/g, "_")}`}>{status}</span>
              <button type="submit" disabled={busy || (!query.trim() && !imageFile)}>
                {busy ? "Processing..." : "Send"}
                <span>↑</span>
              </button>
            </div>
          </form>

          {(answer || citations.length > 0) && (
            <section className="result-grid">
              {answer && (
                <article className="answer-card">
                  <div className="answer-heading"><span className="answer-mark">A</span><p>AgricultureGPT</p><span className="verified">Evidence assisted</span></div>
                  <p className="answer-text">{answer}</p>
                  <p className="notice">Verify pesticide, fertilizer and irrigation decisions with a qualified local agricultural expert.</p>
                </article>
              )}
              {citations.length > 0 && (
                <aside className="sources-card">
                  <h2>Sources <span>{citations.length}</span></h2>
                  {citations.map((citation, index) => (
                    <article key={`${citation.source}-${index}`}>
                      <strong>{citation.source}</strong><p>{citation.passage}</p>
                    </article>
                  ))}
                </aside>
              )}
            </section>
          )}
        </section>
      )}

      {view !== "chat" && (
        <section className="workspace">
          {view === "profile" && (
            <>
              <header className="topbar"><div><p className="eyebrow">Farm settings</p><h1>Farm profile</h1></div></header>
              <form className="panel-form" onSubmit={saveProfile}>
                <label>Farm name<input value={profile.farmName} onChange={(e) => setProfile({...profile, farmName: e.target.value})} placeholder="Example: Green Valley Farm" /></label>
                <label>Location<input value={profile.location} onChange={(e) => setProfile({...profile, location: e.target.value})} placeholder="Village, district or region" /></label>
                <label>Primary crop<select value={profile.crop} onChange={(e) => setProfile({...profile, crop: e.target.value})}><option>Rice</option><option>Wheat</option><option>Maize</option><option>Cotton</option><option>Beans</option><option>Tomato</option><option>Potato</option><option>Other</option></select></label>
                <label>Soil type<select value={profile.soilType} onChange={(e) => setProfile({...profile, soilType: e.target.value})}><option>Loam</option><option>Clay</option><option>Sandy</option><option>Silt</option><option>Black soil</option><option>Red soil</option></select></label>
                <label>Irrigation<select value={profile.irrigation} onChange={(e) => setProfile({...profile, irrigation: e.target.value})}><option>Rainfed</option><option>Drip</option><option>Sprinkler</option><option>Canal</option><option>Borewell</option><option>Flood</option></select></label>
                <label>Farm area (acres)<input type="number" min="0" step="0.1" value={profile.acreage} onChange={(e) => setProfile({...profile, acreage: e.target.value})} placeholder="0.0" /></label>
                <label>Growing season<select value={profile.season} onChange={(e) => setProfile({...profile, season: e.target.value})}><option>Kharif</option><option>Rabi</option><option>Zaid</option><option>Year-round</option></select></label>
                <div className="form-actions"><button type="button" className="secondary" onClick={() => { setProfile(defaultProfile); localStorage.removeItem("agriculturegpt-profile"); setSaved("Farm profile cleared."); }}>Clear</button><button type="submit">Save profile</button></div>
                {saved && <p className="saved">{saved}</p>}
              </form>
            </>
          )}
          {view === "history" && (
            <>
              <header className="topbar"><div><p className="eyebrow">Recent activity</p><h1>Advisory history</h1></div>{history.length > 0 && <button className="danger" onClick={() => { setHistory([]); localStorage.removeItem("agriculturegpt-history"); }}>Clear history</button>}</header>
              {history.length === 0 ? <div className="empty-state"><span className="empty-icon"><Icon name="history" /></span><h2>No questions yet</h2><p>Start a conversation with your crop assistant.</p><button onClick={() => navigate("chat")}>Ask a question</button></div> :
                <div className="history-list">{history.map((record) => <article key={record.id} className="history-card"><div className="history-meta"><span>{new Date(record.createdAt).toLocaleString()}</span><span className={`status ${record.status}`}>{record.status}</span></div>{record.imageName && <span className="image-tag">Image: {record.imageName}</span>}<h2>{record.question}</h2><p>{record.answer}</p></article>)}</div>}
            </>
          )}
          {view === "evaluations" && (
            <>
              <header className="topbar"><div><p className="eyebrow">System quality</p><h1>Evaluations</h1></div></header>
              <div className="metric-grid"><article><span>Questions asked</span><strong>{history.length}</strong></article><article><span>Grounded answers</span><strong>{history.filter((item) => item.status === "grounded").length}</strong></article><article><span>Evidence sources</span><strong>{history.reduce((total, item) => total + item.citations.length, 0)}</strong></article><article><span>Safety mode</span><strong>Active</strong></article></div>
              <article className="panel"><h2>Evaluation scope</h2><p>The local system reports retrieval activity and prompt-safety behavior. Image diagnosis is currently a safe preview and does not provide a confirmed crop disease result.</p><ul><li>Prompt and sensitive-data screening</li><li>Evidence-grounding status</li><li>Source citation presence</li><li>Local profile and history controls</li></ul></article>
            </>
          )}
          {view === "privacy" && (
            <>
              <header className="topbar"><div><p className="eyebrow">Your data</p><h1>Privacy and data</h1></div></header>
              <article className="panel"><h2>Local-first workspace</h2><p>Your farm profile and question history are stored in this browser. Uploaded images are processed by the local backend request and are not persisted by the server.</p><div className="privacy-row"><div><strong>Farm profile</strong><p>{profile.farmName || "No profile"} saved locally</p></div><button className="secondary" onClick={() => { setProfile(defaultProfile); localStorage.removeItem("agriculturegpt-profile"); }}>Delete profile</button></div><div className="privacy-row"><div><strong>Advisory history</strong><p>{history.length} item(s) saved locally</p></div><button className="danger" onClick={() => { setHistory([]); localStorage.removeItem("agriculturegpt-history"); }}>Delete history</button></div></article>
            </>
          )}
        </section>
      )}

      {authOpen && (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setAuthOpen(false); }}>
          <form className="auth-modal" onSubmit={createAccount}>
            <button type="button" className="modal-close" onClick={() => setAuthOpen(false)}>×</button>
            <div className="auth-brand"><span className="brand-mark">A</span><strong>AgricultureGPT</strong></div>
            <h2>{authMode === "signin" ? "Welcome back" : "Create your workspace"}</h2>
            <p>{authMode === "signin" ? "Continue with your local farm workspace." : "Set up a local profile for this browser."}</p>
            {authMode === "signup" && <label>Full name<input value={authName} onChange={(e) => setAuthName(e.target.value)} placeholder="Your name" /></label>}
            <label>Email<input type="email" required value={authEmail} onChange={(e) => setAuthEmail(e.target.value)} placeholder="you@example.com" /></label>
            <label>Password<input type="password" required minLength={6} value={authPassword} onChange={(e) => setAuthPassword(e.target.value)} placeholder="At least 6 characters" /></label>
            <button className="auth-submit" type="submit">{authMode === "signin" ? "Sign in" : "Create account"}</button>
            <button type="button" className="auth-switch" onClick={() => setAuthMode(authMode === "signin" ? "signup" : "signin")}>{authMode === "signin" ? "New here? Create an account" : "Already have an account? Sign in"}</button>
          </form>
        </div>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);
