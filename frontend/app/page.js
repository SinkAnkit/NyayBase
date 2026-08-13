"use client";
import { useState, useEffect, useRef, useMemo } from "react";
import styles from "./page.module.css";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

/* ---- Icons loaded from Lucide CDN (no inline SVGs) ---- */
const LUCIDE_CDN = "https://cdn.jsdelivr.net/npm/lucide-static@0.460.0/icons";
const Ico = (name) => (p) => <img {...p} src={`${LUCIDE_CDN}/${name}.svg`} alt="" draggable="false" />;

const Icons = {
  Scale: Ico("scale"),
  Search: Ico("search"),
  Shield: Ico("shield"),
  Clock: Ico("clock"),
  Book: Ico("book-open"),
  Alert: Ico("alert-triangle"),
  Check: Ico("check"),
  ArrowLeft: Ico("arrow-left"),
  ChevRight: Ico("chevron-right"),
  Home: Ico("home"),
  FileText: Ico("file-text"),
  Car: Ico("truck"),
  Heart: Ico("heart"),
  ShoppingBag: Ico("shopping-bag"),
  Gavel: Ico("gavel"),
  Users: Ico("users"),
  Globe: Ico("globe"),
  Lock: Ico("lock"),
  DollarSign: Ico("indian-rupee"),
  Lightbulb: Ico("lightbulb"),
  Map: Ico("map-pin"),
  Layers: Ico("layers"),
  Settings: Ico("settings"),
  BarChart: Ico("bar-chart-3"),
  TrendingUp: Ico("trending-up"),
  Award: Ico("award"),
  MessageCircle: Ico("message-circle"),
  Send: Ico("send"),
  X: Ico("x"),
  Bot: Ico("bot"),
  StopSquare: Ico("square"),
};

const ICON_MAP = {
  property_dispute: Icons.Home, cheque_bounce: Icons.FileText, motor_accident: Icons.Car,
  divorce: Icons.Heart, consumer_complaint: Icons.ShoppingBag, criminal_offense: Icons.Gavel,
  labor_employment: Icons.Users, cyber_crime: Icons.Globe, tax_dispute: Icons.DollarSign,
  ipr_dispute: Icons.Lightbulb, land_acquisition: Icons.Map, writ_petition: Icons.Layers,
  custom: Icons.Settings,
};

const SAMPLES = [
  {
    label: "Cheque Bounce - Rs 5 Lakh Loan",
    data: {
      case_type: "cheque_bounce", jurisdiction: "Delhi",
      facts: "I am a businessman. The accused issued me a cheque of Rs 5,00,000 towards repayment of a loan. The cheque was presented to my bank but was dishonoured due to 'insufficient funds'. I sent a registered demand notice within 15 days of dishonour. The accused received the notice but failed to make payment within 15 days. I have the original cheque, bank return memo, postal receipt and acknowledgement of the demand notice. The loan was documented with a promissory note signed by the accused.",
      sections: "Section 138, 139, 141, 142 NI Act",
    }
  },
  {
    label: "Property Encroachment - Land Dispute",
    data: {
      case_type: "property_dispute", jurisdiction: "Bangalore",
      facts: "My father purchased a plot of land in 1995 through a registered sale deed. He has been paying property tax and has all revenue records in his name. In 2020, a neighbour encroached upon 500 sq ft of our land by extending their compound wall. We have the original sale deed, survey records showing clear boundaries, property tax receipts for 28 years, and photographs showing the encroachment. The neighbour claims the land was always theirs but has no documents.",
      sections: "Section 54 Transfer of Property Act, Section 5 Specific Relief Act",
    }
  },
  {
    label: "Motor Accident - Spinal Injury Claim",
    data: {
      case_type: "motor_accident", jurisdiction: "Mumbai",
      facts: "My husband was riding his motorcycle when a speeding truck hit him from behind. He sustained severe spinal injuries and is permanently disabled with 70% disability. The truck driver was driving recklessly and fled the scene. An FIR was filed and a charge sheet submitted. My husband was earning Rs 45,000 per month as a software engineer, age 32 at the time. We have FIR copy, medical records showing 8 months treatment costing Rs 15 lakh, disability certificate from the medical board, and the charge sheet.",
      sections: "Section 166, 140 Motor Vehicles Act",
    }
  },
  {
    label: "Divorce - Mental Cruelty",
    data: {
      case_type: "divorce", jurisdiction: "Chennai",
      facts: "I have been married for 8 years. My spouse has been subjecting me to continuous mental cruelty including verbal abuse, isolation from family, and financial control. There are documented incidents including police complaints, messages showing threats, and counseling records. We have two children aged 5 and 3. I am seeking divorce with custody of children and appropriate maintenance. I am currently employed earning Rs 35,000 per month while my spouse earns Rs 1,20,000 per month.",
      sections: "Section 13(1)(ia) Hindu Marriage Act, Section 125 CrPC",
    }
  },
  {
    label: "Employment - Wrongful Termination",
    data: {
      case_type: "employment_dispute", jurisdiction: "Hyderabad",
      facts: "I was employed as a Senior Manager at an IT company for 6 years with consistently excellent performance reviews. I was abruptly terminated without notice or any show cause notice. The company cited 'restructuring' but hired new employees for the same role within a month of my termination. I was not paid my 3 months notice period salary, earned leave encashment, or gratuity of Rs 4.5 lakh. I have my appointment letter, performance appraisals, termination letter, and evidence of new hiring for the same position from LinkedIn.",
      sections: "Section 25F Industrial Disputes Act, Payment of Gratuity Act",
    }
  },
  {
    label: "Consumer Complaint - Defective Vehicle",
    data: {
      case_type: "consumer_dispute", jurisdiction: "Pune",
      facts: "I purchased a new car worth Rs 12 lakh from an authorized dealer. Within 2 months, the engine started giving problems with frequent overheating and loss of power. I visited the service center 5 times but the issue persists. The dealer is now saying the warranty does not cover this defect claiming it is due to 'customer misuse' without any evidence. I have all service records, purchase invoice, warranty card, multiple complaint emails, and a third-party mechanic's report confirming a manufacturing defect in the engine cooling system.",
      sections: "Section 2(1)(c), Section 2(1)(g), Section 2(1)(r) Consumer Protection Act 2019",
    }
  },
];

const fmtNum = (n) => {
  if (n >= 10000000) return (n / 10000000).toFixed(1) + " Cr";
  if (n >= 100000) return (n / 100000).toFixed(1) + " L";
  if (n >= 1000) return (n / 1000).toFixed(1) + "K";
  return n.toLocaleString("en-IN");
};

const CHAT_SAMPLES = [
  "How do I file an FIR?",
  "What are my rights if arrested?",
  "How to file an RTI application?",
  "What is the procedure for bail?",
  "How to file a consumer complaint?",
  "What are tenant rights in India?",
  "How to get a restraining order?",
  "What is anticipatory bail?",
];

/* --- Section Auto-Suggest Map --- */
const SECTION_MAP = {
  cheque_bounce: ["S.138 NI Act", "S.139 NI Act (Presumption)", "S.142 NI Act (Jurisdiction)"],
  property_dispute: ["S.5 Transfer of Property Act", "S.54 TPA (Sale)", "Specific Relief Act S.12"],
  criminal_case: ["S.302 BNS", "S.304 BNS", "S.103 BNS (Right of Private Defence)"],
  family_divorce: ["S.13 Hindu Marriage Act", "S.125 CrPC (Maintenance)", "Domestic Violence Act S.12"],
  consumer_dispute: ["S.2(1)(c) CPA 2019", "S.35 CPA 2019 (Filing)", "S.39 CPA 2019 (Appeal)"],
  labor_dispute: ["S.25F Industrial Disputes Act", "Payment of Gratuity Act", "S.2(s) ID Act"],
  land_acquisition: ["Right to Fair Compensation Act 2013", "Article 300A (Right to Property)", "S.24 RFCTLARR Act"],
  rent_dispute: ["State Rent Control Act", "S.106 Transfer of Property Act", "Model Tenancy Act 2021"],
  cybercrime: ["S.66 IT Act", "S.43 IT Act (Penalty)", "S.72 IT Act (Breach of Privacy)"],
  tax_dispute: ["S.143(3) Income Tax Act", "S.246A ITA (Appeal)", "S.271(1)(c) Penalty"],
  custom: [],
};

/* --- Evidence Strength Meter --- */
const EVIDENCE_KEYWORDS = {
  strong: ["agreement", "contract", "receipt", "invoice", "fir", "witness", "cctv", "video", "recording",
    "notarized", "stamp paper", "affidavit", "bank statement", "photograph", "medical report", "postmortem",
    "forensic", "dna", "email proof", "whatsapp", "screenshot", "digital evidence", "certified copy"],
  moderate: ["document", "letter", "notice", "proof", "evidence", "copy", "statement", "record", "report",
    "certificate", "id card", "aadhaar", "pan", "passport", "license"],
  dates: /\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}|\d{4})\b/gi,
  money: /₹\s*[\d,]+|rs\.?\s*[\d,]+|lakh|crore|rupee/gi,
};

function computeEvidenceStrength(text) {
  if (!text || text.length < 20) return { score: 0, label: "Too Short", color: "#6b7280" };
  const lower = text.toLowerCase();
  let score = Math.min(20, text.length / 10); // Base: length (max 20)
  const strongHits = EVIDENCE_KEYWORDS.strong.filter(k => lower.includes(k)).length;
  const modHits = EVIDENCE_KEYWORDS.moderate.filter(k => lower.includes(k)).length;
  const dateHits = (text.match(EVIDENCE_KEYWORDS.dates) || []).length;
  const moneyHits = (text.match(EVIDENCE_KEYWORDS.money) || []).length;
  score += strongHits * 12 + modHits * 6 + dateHits * 5 + moneyHits * 5;
  score = Math.min(100, score);
  if (score >= 70) return { score, label: "Very Strong", color: "#22c55e" };
  if (score >= 45) return { score, label: "Strong", color: "#4ade80" };
  if (score >= 25) return { score, label: "Fair", color: "#f59e0b" };
  return { score, label: "Weak", color: "#ef4444" };
}

export default function Home() {
  /* ---- Routing: hash-based so refresh + back/forward work ---- */
  const VALID_VIEWS = ["landing", "form", "analyzing", "results", "stats", "courts", "news"];
  const getHashView = () => {
    const h = window.location.hash.replace("#", "");
    return VALID_VIEWS.includes(h) ? h : "landing";
  };
  const [view, _setView] = useState("landing");
  const [mounted, setMounted] = useState(false);
  const setView = (v) => {
    _setView(v);
    const hash = v === "landing" ? "" : v;
    const current = window.location.hash.replace("#", "");
    if (current !== hash) {
      window.history.pushState({ view: v }, "", hash ? `#${hash}` : window.location.pathname);
    }
  };

  // Read hash after hydration + listen for back/forward
  useEffect(() => {
    _setView(getHashView());
    setMounted(true);
    const onPop = () => _setView(getHashView());
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);
  const [caseTypes, setCaseTypes] = useState([]);
  const [jurisdictions, setJurisdictions] = useState([]);
  const [form, setForm] = useState({ case_type: "", facts: "", jurisdiction: "", sections: "", custom_case_type: "", adverse_party: "", legal_representation: "" });
  const [results, setResults] = useState(null);
  const [animGauge, setAnimGauge] = useState(false);
  const [error, setError] = useState("");
  const [stats, setStats] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  /* ---- Courts state ---- */
  const [courtsQuery, setCourtsQuery] = useState("");
  const [courtsResults, setCourtsResults] = useState([]);
  const [courtsFilter, setCourtsFilter] = useState("all");
  const [activeCourt, setActiveCourt] = useState(null);
  const [courtsSearched, setCourtsSearched] = useState(false);
  const [courtsIsNearest, setCourtsIsNearest] = useState(false);
  const [courtsSearchLat, setCourtsSearchLat] = useState(null);
  const [courtsSearchLng, setCourtsSearchLng] = useState(null);
  const courtsMapRef = useRef(null);
  const courtsMapInstance = useRef(null);

  /* ---- Chatbot state ---- */
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const chatEndRef = useRef(null);
  const chatInputRef = useRef(null);
  const chatAbortRef = useRef(null);

  /* ---- News state ---- */
  const [newsArticles, setNewsArticles] = useState([]);
  const [newsLoading, setNewsLoading] = useState(false);
  const [newsError, setNewsError] = useState("");
  const [newsFilter, setNewsFilter] = useState("all");
  const [nextRefreshAt, setNextRefreshAt] = useState(null);
  const [countdown, setCountdown] = useState("");

  /* ---- Mobile nav ---- */
  const [mobileNav, setMobileNav] = useState(false);

  /* ---- Case History + Premium Features ---- */
  const [caseHistory, setCaseHistory] = useState([]);
  const [copied, setCopied] = useState(false);

  // Load case history from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem("nyaybase_history");
      if (saved) setCaseHistory(JSON.parse(saved));
    } catch { }
  }, []);

  // Save result to history after analysis
  const saveToHistory = (data) => {
    const entry = {
      id: Date.now(),
      case_type: data.case_type,
      jurisdiction: data.jurisdiction,
      probability: data.win_probability?.probability || 0,
      strength: data.win_probability?.strength || "N/A",
      date: new Date().toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }),
    };
    const updated = [entry, ...caseHistory].slice(0, 10); // Keep last 10
    setCaseHistory(updated);
    try { localStorage.setItem("nyaybase_history", JSON.stringify(updated)); } catch { }
  };

  const clearHistory = () => {
    setCaseHistory([]);
    try { localStorage.removeItem("nyaybase_history"); } catch { }
  };

  // Evidence strength meter (real-time)
  const evidenceStrength = useMemo(() => computeEvidenceStrength(form.facts), [form.facts]);

  // Section suggestions based on case type
  const sectionSuggestions = useMemo(() => SECTION_MAP[form.case_type] || [], [form.case_type]);

  // Copy analysis summary to clipboard
  const copyAnalysis = () => {
    if (!results) return;
    const wp = results.win_probability || {};
    let text = `NyayBase Case Analysis Report\n`;
    text += `================================\n`;
    text += `Case Type: ${results.case_type}\n`;
    text += `Jurisdiction: ${results.jurisdiction}\n`;
    text += `Win Probability: ${wp.probability}% (${wp.strength})\n`;
    text += `Range: ${wp.lower_bound}% - ${wp.upper_bound}%\n`;
    text += `\nKey Arguments:\n`;
    (results.key_arguments || []).forEach((a, i) => {
      text += `${i + 1}. ${a.argument} (${a.strength}%) - ${a.section}\n`;
    });
    text += `\nTimeline: ${results.timeline?.estimated_months || 0} months est.\n`;
    text += `\nRisk Factors:\n`;
    (results.risk_factors || []).forEach((r, i) => {
      text += `${i + 1}. ${r.risk} (${r.severity}) - ${r.mitigation}\n`;
    });
    text += `\n================================\nGenerated by NyayBase - Legal Case Analysis`;
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  // Download PDF report
  const downloadPDF = () => {
    if (!results) return;
    const wp = results.win_probability || {};
    let html = `<html><head><meta charset="utf-8"><title>NyayBase Report - ${results.case_type}</title>
    <style>body{font-family:'Inter','Segoe UI',Tahoma,sans-serif;max-width:800px;margin:0 auto;padding:40px;color:#111827;line-height:1.6}
    h1{color:#059669;border-bottom:3px solid #059669;padding-bottom:10px}h2{color:#047857;margin-top:30px;border-bottom:1px solid #e5e7eb;padding-bottom:6px}
    .badge{display:inline-block;padding:4px 12px;border-radius:12px;font-size:13px;font-weight:700;margin:4px}
    .green{background:#dcfce7;color:#166534}.red{background:#fee2e2;color:#991b1b}.amber{background:#fef3c7;color:#92400e}
    .prob-box{text-align:center;padding:24px;margin:20px 0;background:#ecfdf5;border-radius:16px;border:2px solid #059669}
    .prob-num{font-size:56px;font-weight:800;color:#059669}.prob-str{font-size:18px;color:#047857;font-weight:600}
    .arg{background:#f8fafc;border-left:4px solid #059669;padding:12px 16px;margin:10px 0;border-radius:0 8px 8px 0}
    .risk{background:#fef2f2;border-left:4px solid #ef4444;padding:12px 16px;margin:10px 0;border-radius:0 8px 8px 0}
    table{width:100%;border-collapse:collapse;margin:10px 0}td,th{padding:8px 12px;text-align:left;border-bottom:1px solid #e5e7eb}
    .footer{margin-top:40px;padding-top:20px;border-top:2px solid #e5e7eb;text-align:center;color:#6b7280;font-size:12px}</style></head><body>`;
    html += `<h1>NyayBase - Case Analysis Report</h1>`;
    html += `<table><tr><td><strong>Case Type</strong></td><td>${results.case_type}</td></tr>`;
    html += `<tr><td><strong>Jurisdiction</strong></td><td>${results.jurisdiction}</td></tr>`;
    if (results.relevant_acts?.length) html += `<tr><td><strong>Applicable Laws</strong></td><td>${results.relevant_acts.join(", ")}</td></tr>`;
    html += `</table>`;
    html += `<div class="prob-box"><div class="prob-num">${wp.probability}%</div><div class="prob-str">${wp.strength} Case</div>`;
    html += `<p>Range: ${wp.lower_bound}% - ${wp.upper_bound}% | Base Rate: ${wp.base_rate}% | Adjustment: ${wp.adjustment >= 0 ? "+" : ""}${wp.adjustment}%</p></div>`;
    if (wp.reasoning) html += `<p><em>${wp.reasoning}</em></p>`;
    html += `<h2>Key Arguments (${(results.key_arguments || []).length})</h2>`;
    (results.key_arguments || []).forEach(a => { html += `<div class="arg"><strong>${a.argument}</strong> <span class="badge ${a.strength >= 70 ? 'green' : a.strength >= 50 ? 'amber' : 'red'}">${a.strength}%</span><br><small>${a.section}</small><p>${a.description}</p></div>`; });
    html += `<h2>Expected Timeline</h2><p><strong>${results.timeline?.estimated_months || 0} months</strong> (${results.timeline?.min_months || 0} - ${results.timeline?.max_months || 0} months range)</p>`;
    if (results.timeline?.recommendation) html += `<p>${results.timeline.recommendation}</p>`;
    html += `<h2>Mediation</h2><p><strong>${results.mediation?.recommendation || "N/A"}</strong> - Success Rate: ${results.mediation?.success_rate || 0}%, Avg Settlement: ${results.mediation?.avg_settlement_months || 0} months</p>`;
    if ((results.similar_cases || []).length) {
      html += `<h2>Similar Landmark Cases</h2>`;
      results.similar_cases.forEach(c => { html += `<div class="arg"><strong>${c.case_name}</strong> ${c.year ? `(${c.year})` : ''} ${c.relevance_score ? `<span class="badge green">${c.relevance_score}%</span>` : ''}<p>${c.summary || c.outcome || ''}</p></div>`; });
    }
    html += `<h2>Risk Factors</h2>`;
    (results.risk_factors || []).forEach(r => { html += `<div class="risk"><strong>${r.risk}</strong> <span class="badge ${r.severity === 'High' ? 'red' : r.severity === 'Medium' ? 'amber' : 'green'}">${r.severity}</span><p>${r.description}</p><p><strong>Mitigation:</strong> ${r.mitigation}</p></div>`; });
    html += `<div class="footer"><p><strong>Disclaimer:</strong> This is an AI-generated analysis based on historical court data. This is not legal advice. Consult a qualified advocate.</p><p>Generated by NyayBase - ${new Date().toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" })}</p></div></body></html>`;
    const blob = new Blob([html], { type: "text/html;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const printWin = window.open(url, "_blank");
    printWin.addEventListener("load", () => { printWin.print(); });
  };

  useEffect(() => {
    if (chatEndRef.current) chatEndRef.current.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages, chatLoading]);

  const sendChat = async (msg) => {
    const message = (msg || chatInput).trim();
    if (!message || chatLoading) return;
    const userMsg = { role: "user", content: message };
    setChatMessages(prev => [...prev, userMsg]);
    setChatInput("");
    setChatLoading(true);

    const controller = new AbortController();
    chatAbortRef.current = controller;

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history: [...chatMessages, userMsg].slice(-8) }),
        signal: controller.signal,
      });
      const data = await res.json();
      setChatMessages(prev => [...prev, { role: "bot", content: data.reply || "Sorry, I couldn't generate a response. Please try again." }]);
    } catch (err) {
      if (err.name === "AbortError") {
        // User cancelled - don't add error message
      } else {
        setChatMessages(prev => [...prev, { role: "bot", content: "Connection error. Please check if the server is running and try again." }]);
      }
    }
    chatAbortRef.current = null;
    setChatLoading(false);
    setTimeout(() => chatInputRef.current?.focus(), 100);
  };

  const stopChat = () => {
    if (chatAbortRef.current) {
      chatAbortRef.current.abort();
      chatAbortRef.current = null;
    }
    setChatLoading(false);
    setTimeout(() => chatInputRef.current?.focus(), 100);
  };

  useEffect(() => {
    fetch(`${API}/case-types`).then(r => r.json()).then(d => setCaseTypes(d.case_types || [])).catch(() => { });
    fetch(`${API}/jurisdictions`).then(r => r.json()).then(d => setJurisdictions(d.jurisdictions || [])).catch(() => { });
    fetch(`${API}/stats`).then(r => r.json()).then(d => setStats(d)).catch(() => { });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.case_type || !form.jurisdiction || form.facts.length < 20) {
      setError("Please fill all required fields. Case facts must be at least 20 characters.");
      return;
    }
    setError("");
    setView("analyzing");
    setAnalyzing(true);
    try {
      const res = await fetch(`${API}/analyze`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (data.success) {
        setResults(data.data);
        saveToHistory(data.data);
        setTimeout(() => { setView("results"); setTimeout(() => setAnimGauge(true), 200); setAnalyzing(false); }, 2200);
      } else {
        setError(data.error || "Analysis failed"); setView("form"); setAnalyzing(false);
      }
    } catch {
      setError("Cannot connect to backend. Ensure the server is running on port 8000."); setView("form"); setAnalyzing(false);
    }
  };

  const reset = () => { setView("landing"); setResults(null); setAnimGauge(false); setForm({ case_type: "", facts: "", jurisdiction: "", sections: "", custom_case_type: "", adverse_party: "", legal_representation: "" }); setError(""); setAnalyzing(false); };
  const goToForm = () => { setResults(null); setAnimGauge(false); setForm({ case_type: "", facts: "", jurisdiction: "", sections: "", custom_case_type: "", adverse_party: "", legal_representation: "" }); setError(""); setView("form"); setAnalyzing(false); };
  const loadSample = (s) => { setForm({ ...s.data, custom_case_type: "", adverse_party: "", legal_representation: "" }); };
  const I = (name, cls) => { const Ic = Icons[name]; return Ic ? <Ic className={`${styles.icon} ${cls || ""}`} /> : null; };
  const CaseIcon = ({ type }) => { const Ic = ICON_MAP[type] || Icons.Gavel; return <Ic className={styles.caseIcon} />; };

  /* ------ NAV BAR (shared across all views) ------ */
  const NavBar = ({ active }) => (
    <nav className={styles.nav}>
      <div className={styles.navInner}>
        <div className={styles.logo} onClick={reset} style={{ cursor: "pointer" }}><Icons.Scale className={styles.logoSvg} /><span>Nyay<b>Base</b></span></div>
        <button className={styles.hamburger} onClick={() => setMobileNav(!mobileNav)} aria-label="Menu">
          <span /><span /><span />
        </button>
        <div className={`${styles.navTabs} ${mobileNav ? styles.navTabsOpen : ""}`}>
          <button className={`${styles.navTab} ${active === "home" ? styles.navTabActive : ""}`} onClick={() => { reset(); setMobileNav(false); }}>{I("Home")} Home</button>
          <button className={`${styles.navTab} ${(active === "analyze" || active === "form") ? styles.navTabActive : ""}`} onClick={() => { goToForm(); setMobileNav(false); }}>{I("Search")} Analyze</button>
          <button className={`${styles.navTab} ${active === "stats" ? styles.navTabActive : ""}`} onClick={() => { setView("stats"); setMobileNav(false); }}>{I("BarChart")} Statistics</button>
          <button className={`${styles.navTab} ${active === "courts" ? styles.navTabActive : ""}`} onClick={() => { setView("courts"); setMobileNav(false); }}>{I("Map")} Courts</button>
          <button className={`${styles.navTab} ${active === "news" ? styles.navTabActive : ""}`} onClick={() => { setView("news"); setMobileNav(false); }}>{I("Globe")} News</button>
        </div>
      </div>
    </nav>
  );

  /* ------ LANDING ------ */
  let renderView = null;
  if (view === "landing") renderView = (
    <main className={styles.page}>
      <NavBar active="home" />
      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <div className={styles.heroTag}>
            <span className={styles.heroPing}></span>
            <span>Legal Case Analysis Platform</span>
          </div>
          <h1 className={styles.heroH1}>Predict Your Case<br /><span className={styles.gold}>Outcome with AI</span></h1>
          <p className={styles.heroP}>Analyze patterns from <strong>1.2 million+</strong> Indian court judgments. Get win probability, winning arguments, strategic timelines, and recommended next steps.</p>
          <div className={styles.heroBtns}>
            <button className={styles.btnPrimary} onClick={goToForm}>{I("Search")} Analyze Your Case</button>
            <button className={styles.btnSecondary} onClick={() => setView("stats")}>{I("BarChart")} View Statistics</button>
          </div>
          <div className={styles.statsBar}>
            <div className={styles.stat}><div className={styles.statV}>25+</div><div className={styles.statL}>Courts Covered All Over India</div></div>
            <div className={styles.stat}><div className={styles.statV}>Multiple</div><div className={styles.statL}>Case Types Analysed & Covered</div></div>
          </div>
        </div>
      </section>

      {/* Decorative section divider */}
      <hr style={{ border: "none", borderTop: "1px solid var(--border)", margin: "0 auto", maxWidth: "800px" }} />

      <section className={styles.section}>
        <span className={styles.secLabel}>How It Works</span>
        <h2 className={styles.secTitle}>How NyayBase Works</h2>
        <div className={styles.grid4}>
          {[["Search", "Input Case Details", "Enter your case type, key facts, jurisdiction, and relevant legal sections for precise analysis."],
          ["Shield", "Pattern Matching", "Our engine cross-references patterns from millions of past court judgments in real time."],
          ["Book", "Strategic Insights", "Receive win probability, winning arguments, case timeline, and landmark case precedents."],
          ["Clock", "Save Years of Effort", "Make informed legal decisions before investing time and resources in lengthy litigation."]
          ].map(([ic, t, d], i) => (
            <div key={i} className={styles.card}><div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "8px" }}><div className={styles.cardIcon} style={{ margin: 0 }}>{I(ic)}</div><h3 style={{ margin: 0 }}>{t}</h3></div><p>{d}</p></div>
          ))}
        </div>
      </section>

      <hr style={{ border: "none", borderTop: "1px solid var(--border)", margin: "0 auto", maxWidth: "800px" }} />

      <section className={styles.section}>
        <span className={styles.secLabel}>Case Categories</span>
        <h2 className={styles.secTitle}>Supported Case Types</h2>
        <div className={styles.grid3}>
          {(caseTypes.length > 0 ? caseTypes : Object.entries(ICON_MAP).map(([id]) => ({ id, name: id.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()), description: "", avg_win_rate: 0, avg_duration_months: 0 }))).filter(c => c.id !== "custom").map((ct, i) => (
            <div key={i} className={styles.card} onClick={() => { setForm(f => ({ ...f, case_type: ct.id })); setView("form"); }} style={{ cursor: "pointer" }}>
              <CaseIcon type={ct.id} />
              <h3>{ct.name}</h3>
              <p className={styles.cardDesc}>{ct.description}</p>
              {ct.avg_win_rate > 0 && <div className={styles.cardMeta}>
                <span>Win Rate: <b className={styles.gold}>{ct.avg_win_rate}%</b></span>
                <span>Avg: <b className={styles.gold}>{ct.avg_duration_months}mo</b></span>
              </div>}
            </div>
          ))}
        </div>
      </section>

      {/* Trust Section */}
      <section className={styles.trustSection}>
        <div className={styles.trustInner}>
          <div className={styles.trustItem}>{I("Shield")} <span>Data Encrypted & Secure</span></div>
                    <div className={styles.trustItem}>{I("Lock")} <span>No Data Stored</span></div>
                    <div className={styles.trustItem}>{I("Award")} <span>AI-Verified Analysis</span></div>
        </div>
      </section>

      {caseHistory.length > 0 && (
        <section className={styles.historySection}>
          <h3>{I("Clock")} Recent Analyses <button className={styles.suggestChip} onClick={clearHistory} style={{ marginLeft: 12, cursor: "pointer" }}>Clear All</button></h3>
          <div className={styles.historyGrid}>
            {caseHistory.map((h) => (
              <div key={h.id} className={styles.historyCard} onClick={goToForm}>
                <div className={styles.historyCardTop}>
                  <span className={styles.historyType}>{h.case_type}</span>
                  <span className={styles.historyProb} style={{ background: h.probability >= 60 ? "rgba(34,197,94,0.15)" : h.probability >= 40 ? "rgba(245,158,11,0.15)" : "rgba(239,68,68,0.15)", color: h.probability >= 60 ? "#22c55e" : h.probability >= 40 ? "#f59e0b" : "#ef4444" }}>{h.probability}%</span>
                </div>
                <div className={styles.historyJur}>{h.jurisdiction} - {h.strength}</div>
                <div className={styles.historyDate}>{h.date}</div>
              </div>
            ))}
          </div>
        </section>
      )}

      <footer className={styles.footer}>
        <p>NyayBase - Legal Case Analysis for India</p>
        <p className={styles.muted}>Data sourced from National Judicial Data Grid (NJDG) and court records.</p>
        <a href="mailto:ankitsingh92004@gmail.com?subject=NyayBase Feedback" className={styles.contactLink}>{I("MessageCircle")} Contact Us</a>
      </footer>
    </main>
  );

  /* ------ FORM ------ */
  if (view === "form") renderView = (
    <main className={styles.page}>
      <NavBar active="analyze" />
      <section className={styles.formSection}>
        <div className={styles.formHeader}>
          <h1>{I("Scale")} Analyze Your Case</h1>
          <p>Enter your case details below for analysis</p>
        </div>
        {error && <div className={styles.errorBar}>{I("Alert")} {error}</div>}
        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.formRow}>
            <label>Case Type *</label>
            <select value={form.case_type} onChange={e => setForm(f => ({ ...f, case_type: e.target.value }))} required>
              <option value="">Select case type...</option>
              {caseTypes.map(ct => <option key={ct.id} value={ct.id}>{ct.name}</option>)}
            </select>
          </div>
          {form.case_type === "custom" && (
            <div className={styles.formRow}>
              <label>Custom Case Type</label>
              <input type="text" placeholder="e.g. Domestic Violence, Bail Application..." value={form.custom_case_type} onChange={e => setForm(f => ({ ...f, custom_case_type: e.target.value }))} />
            </div>
          )}
          <div className={styles.formRow}>
            <label>Jurisdiction *</label>
            <select value={form.jurisdiction} onChange={e => setForm(f => ({ ...f, jurisdiction: e.target.value }))} required>
              <option value="">Select jurisdiction...</option>
              {jurisdictions.map(j => <option key={j.id} value={j.id}>{j.name}</option>)}
            </select>
          </div>
          <div className={styles.formRow}>
            <label>Case Facts *</label>
            <textarea rows={6} placeholder="Describe the facts of your case in detail. Include: what happened, who is involved, dates, evidence you have, and what outcome you seek..." value={form.facts} onChange={e => setForm(f => ({ ...f, facts: e.target.value }))} required minLength={20} />
            {form.facts.length >= 10 && (
              <div className={styles.evidenceMeter}>
                <div className={styles.evidenceMeterLabel}>
                  <span>Evidence Strength</span>
                  <span className={styles.evidenceStrength} style={{ color: evidenceStrength.color }}>{evidenceStrength.label}</span>
                </div>
                <div className={styles.evidenceBar}>
                  <div className={styles.evidenceFill} style={{ width: `${evidenceStrength.score}%`, background: evidenceStrength.color }} />
                </div>
              </div>
            )}
          </div>
          <div className={styles.formRow}>
            <label>Relevant Sections (Optional)</label>
            <input type="text" placeholder="e.g. Section 138 NI Act, Section 420 IPC..." value={form.sections} onChange={e => setForm(f => ({ ...f, sections: e.target.value }))} />
            {sectionSuggestions.length > 0 && !form.sections && (
              <div className={styles.autoSuggest}>
                {sectionSuggestions.map((s, i) => (
                  <button key={i} type="button" className={styles.suggestChip} onClick={() => setForm(f => ({ ...f, sections: f.sections ? f.sections + ", " + s : s }))}>{s}</button>
                ))}
              </div>
            )}
          </div>
          <div className={styles.formRow}>
            <label>Your Legal Representation (Optional)</label>
            <select value={form.legal_representation} onChange={e => setForm(f => ({ ...f, legal_representation: e.target.value }))}>
              <option value="">Select your legal backing...</option>
              <option value="self">Self (No Lawyer)</option>
              <option value="individual_lawyer">Individual / Private Lawyer</option>
              <option value="government_lawyer">Government / Legal Aid Lawyer</option>
              <option value="law_firm">Reputed Law Firm</option>
              <option value="organization">Organization / NGO / Institution Backing</option>
            </select>
            <span className={styles.muted} style={{ fontSize: 11, marginTop: 4 }}>Who is representing you? This helps gauge your legal strength.</span>
          </div>
          <div className={styles.formRow}>
            <label>Adverse Party Information (Optional)</label>
            <textarea rows={3} placeholder="Describe who you're up against. E.g., 'A large real estate developer company', 'A government municipal authority', 'My neighbor who is an individual', 'A group of people involved in illegal activities'..." value={form.adverse_party} onChange={e => setForm(f => ({ ...f, adverse_party: e.target.value }))} />
            <span className={styles.muted} style={{ fontSize: 11, marginTop: 4 }}>This helps us assess the strength of opposition and adjust the analysis accordingly.</span>
          </div>
          <button type="submit" className={`${styles.btnPrimary} ${analyzing ? styles.btnLoading : ""}`} style={{ width: "100%", marginTop: 12 }} disabled={analyzing}>
            {analyzing ? <><span className={styles.btnSpinner}></span> Analyzing...</> : <>{I("Search")} Analyze Case</>}
          </button>
        </form>
        <div className={styles.sampleSection}>
          <p className={styles.muted} style={{ marginBottom: 8 }}>Or try a sample case:</p>
          <div className={styles.sampleGrid}>
            {SAMPLES.map((s, i) => (
              <button key={i} className={styles.sampleBtn} onClick={() => loadSample(s)}>{s.label}</button>
            ))}
          </div>
        </div>
      </section>
    </main>
  );

  /* ------ ANALYZING ------ */
  if (view === "analyzing") renderView = (
    <main className={styles.page}>
      <NavBar active="analyze" />
      <section className={styles.analyzing}>
        <div className={styles.analyzeInner}>
          <div className={styles.spinner}></div>
          <h2>Analyzing Your Case</h2>
          <p className={styles.muted}>Processing against 1.2M+ court judgments...</p>
          <div className={styles.steps}>
            {["Matching case patterns...", "Calculating win probability...", "Extracting winning arguments...", "Finding similar landmark cases...", "Estimating timeline...", "Assessing mediation options..."].map((s, i) => (
              <div key={i} className={styles.stepItem} style={{ animationDelay: `${i * 0.3}s` }}>{I("Check")} {s}</div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );

  /* ------ STATISTICS ------ */
  if (view === "stats") renderView = (
    <main className={styles.page}>
      <NavBar active="stats" />
      <section className={styles.statsSection}>
        <div className={styles.formHeader}>
          <h1>{I("BarChart")} Indian Judiciary Statistics</h1>
          <p>Comprehensive overview of the Indian judicial system - pendency, disposal rates, and case analytics</p>
        </div>

        {stats ? (
          <>
            {/* Highlight Cards */}
            <div className={styles.grid4} style={{ marginBottom: 32 }}>
              <div className={styles.statCard}>
                <div className={styles.statCardValue} style={{ color: "#ef4444" }}>{fmtNum(stats.highlights.total_pending)}</div>
                <div className={styles.statCardLabel}>Total Pending Cases</div>
                <div className={styles.muted} style={{ fontSize: 12 }}>Across Supreme Court + High Courts</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statCardValue} style={{ color: "#f59e0b" }}>{stats.highlights.total_judges_working}</div>
                <div className={styles.statCardLabel}>Working Judges</div>
                <div className={styles.muted} style={{ fontSize: 12 }}>{stats.highlights.judge_vacancy} vacancies of {stats.highlights.total_judges_sanctioned} sanctioned</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statCardValue} style={{ color: "#22c55e" }}>{fmtNum(stats.highlights.annual_cases_disposed)}</div>
                <div className={styles.statCardLabel}>Cases Disposed / Year</div>
                <div className={styles.muted} style={{ fontSize: 12 }}>{fmtNum(stats.highlights.annual_cases_filed)} new cases filed annually</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statCardValue} style={{ color: "#059669" }}>{stats.highlights.courts_covered}</div>
                <div className={styles.statCardLabel}>Courts Covered</div>
                <div className={styles.muted} style={{ fontSize: 12 }}>Supreme Court + {stats.highlights.courts_covered - 1} High Courts</div>
              </div>
            </div>

            {/* Court-wise Pendency Table */}
            <div className={styles.resultCard} style={{ marginBottom: 32 }}>
              <h2 className={styles.cardH}>{I("Gavel")} Court-wise Pendency & Performance</h2>
              <div className={styles.tableWrap}>
                <table className={styles.dataTable}>
                  <thead>
                    <tr>
                      <th>Court</th>
                      <th>Pending Cases</th>
                      <th>Civil</th>
                      <th>Criminal</th>
                      <th>Judges</th>
                      <th>Disposal Rate</th>
                      <th>Avg Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.court_stats.map((c, i) => (
                      <tr key={i}>
                        <td><strong>{c.name}</strong><br /><span className={styles.muted}>{c.state}</span></td>
                        <td><strong>{fmtNum(c.pending_total)}</strong></td>
                        <td>{fmtNum(c.pending_civil)}</td>
                        <td>{fmtNum(c.pending_criminal)}</td>
                        <td>{c.judges_working}/{c.judges_sanctioned}</td>
                        <td>
                          <div className={styles.miniBar}>
                            <div className={styles.miniBarFill} style={{ width: `${c.disposal_rate}%`, background: c.disposal_rate >= 80 ? "#22c55e" : c.disposal_rate >= 60 ? "#f59e0b" : "#ef4444" }}></div>
                          </div>
                          <span className={styles.muted}>{c.disposal_rate}%</span>
                        </td>
                        <td>{c.avg_disposal_months} mo</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Case Type Profiles */}
            <div className={styles.resultCard} style={{ marginBottom: 32 }}>
              <h2 className={styles.cardH}>{I("Layers")} Case Type Profiles - National Overview</h2>
              <div className={styles.tableWrap}>
                <table className={styles.dataTable}>
                  <thead>
                    <tr>
                      <th>Case Type</th>
                      <th>Pending Nationally</th>
                      <th>Avg Duration</th>
                      <th>Win Rate</th>
                      <th>Settlement Rate</th>
                      <th>Appeal Rate</th>
                      <th>Limitation (yrs)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.case_profiles.map((p, i) => (
                      <tr key={i}>
                        <td><strong>{p.name}</strong></td>
                        <td><strong>{fmtNum(p.pending_nationally)}</strong></td>
                        <td>{p.avg_duration_months} months</td>
                        <td>
                          <span style={{ color: p.win_rate >= 50 ? "#22c55e" : "#f59e0b", fontWeight: 600 }}>{p.win_rate}%</span>
                        </td>
                        <td>{p.settlement_rate}%</td>
                        <td>{p.appeal_rate}%</td>
                        <td>{p.limitation_years} yrs</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Case Type Win Rates Visual */}
            <div className={styles.resultCard} style={{ marginBottom: 32 }}>
              <h2 className={styles.cardH}>{I("TrendingUp")} Case Type Win Rates & Duration</h2>
              <div className={styles.winRateGrid}>
                {stats.case_type_stats.map((ct, i) => (
                  <div key={i} className={styles.winRateItem}>
                    <div className={styles.winRateBar}>
                      <div className={styles.winRateBarFill} style={{ width: `${ct.avg_win_rate}%`, background: ct.avg_win_rate >= 60 ? "#22c55e" : ct.avg_win_rate >= 40 ? "#f59e0b" : "#ef4444" }}>
                        <span>{ct.avg_win_rate}%</span>
                      </div>
                    </div>
                    <div className={styles.winRateLabel}>{ct.name}</div>
                    <div className={styles.muted} style={{ fontSize: 11 }}>{ct.avg_duration_months} mo avg | {ct.landmark_cases_count} landmark cases</div>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ textAlign: "center", paddingBottom: 40 }}>
              <button className={styles.btnPrimary} onClick={goToForm}>{I("Search")} Analyze Your Case Now</button>
            </div>
          </>
        ) : (
          <div className={styles.analyzing}>
            <div className={styles.spinner}></div>
            <p>Loading statistics...</p>
          </div>
        )}
      </section>
      <footer className={styles.footer}>
        <p>NyayBase - Legal Case Analysis for India</p>
        <p className={styles.muted}>Data sourced from National Judicial Data Grid (NJDG) and court records.</p>
        <a href="mailto:ankitsingh92004@gmail.com?subject=NyayBase Feedback" className={styles.contactLink}>{I("MessageCircle")} Contact Us</a>
      </footer>
    </main>
  );

  /* ------ COURTS LOCATOR ------ */
  const searchCourts = async (q) => {
    const query = (q || courtsQuery).trim();
    if (!query) return;
    try {
      const res = await fetch(`${API}/courts/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setCourtsResults(data.courts || []);
      setCourtsSearched(true);
      setCourtsIsNearest(data.is_nearest || false);
      setCourtsSearchLat(data.search_lat || null);
      setCourtsSearchLng(data.search_lng || null);
      setActiveCourt(null);
      setCourtsFilter("all");
    } catch {
      setCourtsResults([]);
      setCourtsSearched(true);
      setCourtsIsNearest(false);
    }
  };

  const COURT_TYPE_LABEL = { supreme_court: "Supreme Court", high_court: "High Court", district_court: "District Court", consumer_forum: "Consumer Forum" };
  const COURT_TYPE_STYLE = { supreme_court: styles.courtTypeSC, high_court: styles.courtTypeHC, district_court: styles.courtTypeDC, consumer_forum: styles.courtTypeCF };
  const COURT_TYPE_COLOR = { supreme_court: "#eab308", high_court: "#059669", district_court: "#0ea5e9", consumer_forum: "#22c55e" };

  const filteredCourts = courtsFilter === "all" ? courtsResults : courtsResults.filter(c => c.type === courtsFilter);

  // Leaflet map effect
  useEffect(() => {
    if (view !== "courts" || filteredCourts.length === 0 || !courtsMapRef.current) return;

    // Dynamically load Leaflet CSS + JS
    const loadLeaflet = async () => {
      if (!document.getElementById("leaflet-css")) {
        const link = document.createElement("link");
        link.id = "leaflet-css";
        link.rel = "stylesheet";
        link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
        document.head.appendChild(link);
      }
      if (!window.L) {
        await new Promise((resolve) => {
          const script = document.createElement("script");
          script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
          script.onload = resolve;
          document.head.appendChild(script);
        });
      }

      const L = window.L;

      // Destroy previous map
      if (courtsMapInstance.current) {
        courtsMapInstance.current.remove();
        courtsMapInstance.current = null;
      }

      const map = L.map(courtsMapRef.current, { zoomControl: true, scrollWheelZoom: true });
      courtsMapInstance.current = map;

      L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
        maxZoom: 18,
      }).addTo(map);

      const bounds = [];
      filteredCourts.forEach((court) => {
        if (!court.lat || !court.lng) return;
        const color = COURT_TYPE_COLOR[court.type] || "#059669";
        const marker = L.circleMarker([court.lat, court.lng], {
          radius: court.type === "supreme_court" ? 10 : court.type === "high_court" ? 8 : 6,
          fillColor: color,
          color: color,
          weight: 2,
          opacity: 0.9,
          fillOpacity: 0.6,
        }).addTo(map);

        marker.bindPopup(`<div style="font-family:system-ui;min-width:180px">
          <b style="font-size:13px;color:#1a1a2e">${court.name}</b><br>
          <span style="font-size:11px;color:#6b7280">${COURT_TYPE_LABEL[court.type] || court.type}</span><br>
          <span style="font-size:11px;color:#4b5563">${court.address}</span><br>
          <span style="font-size:11px;color:#4b5563">${court.phone}</span>
        </div>`);

        marker.on("click", () => setActiveCourt(court.name));
        bounds.push([court.lat, court.lng]);
      });

      if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [30, 30], maxZoom: 12 });
      }

      // Add "Your Location" marker
      if (courtsSearchLat && courtsSearchLng) {
        const locIcon = L.divIcon({
          className: "",
          html: `<div style="position:relative;width:24px;height:24px">
            <div style="position:absolute;top:0;left:0;width:24px;height:24px;border-radius:50%;background:rgba(239,68,68,0.25);animation:locPulse 2s infinite"></div>
            <div style="position:absolute;top:6px;left:6px;width:12px;height:12px;border-radius:50%;background:#ef4444;border:2px solid #fff;box-shadow:0 0 6px rgba(239,68,68,0.6)"></div>
          </div>
          <style>@keyframes locPulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.8);opacity:0}}</style>`,
          iconSize: [24, 24],
          iconAnchor: [12, 12],
        });
        const locMarker = L.marker([courtsSearchLat, courtsSearchLng], { icon: locIcon }).addTo(map);
        locMarker.bindPopup(`<div style="font-family:system-ui;text-align:center">
          <b style="font-size:13px;color:#ef4444">Your Location</b><br>
          <span style="font-size:11px;color:#6b7280">${courtsQuery}</span>
        </div>`);
        bounds.push([courtsSearchLat, courtsSearchLng]);
        if (bounds.length > 1) map.fitBounds(bounds, { padding: [30, 30], maxZoom: 12 });
      }
    };

    loadLeaflet();

    return () => {
      if (courtsMapInstance.current) {
        courtsMapInstance.current.remove();
        courtsMapInstance.current = null;
      }
    };
  }, [view, filteredCourts]);

  if (view === "courts") renderView = (
    <main className={styles.page}>
      <NavBar active="courts" />
      <section className={styles.courtsSection}>
        <div className={styles.courtsHeader}>
          <h1>{I("Map")} Court Locator</h1>
          <p>Find District Courts, High Courts, and Consumer Forums across India</p>
          <div className={styles.courtsSearchBar}>
            <input
              className={styles.courtsSearchInput}
              placeholder="Enter city name or pincode (e.g. Delhi, Mumbai, 110001)"
              value={courtsQuery}
              onChange={(e) => setCourtsQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && searchCourts()}
            />
            <button className={styles.courtsSearchBtn} onClick={() => searchCourts()}>
              {I("Search")} Search
            </button>
          </div>
        </div>

        {courtsSearched && courtsResults.length > 0 && (
          <>
            <div className={styles.courtsFilters}>
              {["all", "supreme_court", "high_court", "district_court", "consumer_forum"].map(f => (
                <button key={f} className={`${styles.courtFilterBtn} ${courtsFilter === f ? styles.courtFilterActive : ""}`} onClick={() => setCourtsFilter(f)}>
                  {f === "all" ? "All" : COURT_TYPE_LABEL[f]}
                  {f !== "all" && ` (${courtsResults.filter(c => c.type === f).length})`}
                </button>
              ))}
            </div>
            <div className={styles.courtsCount}>
              {courtsIsNearest
                ? <><b>{filteredCourts.length}</b> nearest court{filteredCourts.length !== 1 ? "s" : ""} to <b>{courtsQuery}</b></>
                : <>Showing <b>{filteredCourts.length}</b> court{filteredCourts.length !== 1 ? "s" : ""} in <b>{courtsQuery}</b></>
              }
            </div>
            <div className={styles.courtsBody}>
              <div className={styles.courtsList}>
                {filteredCourts.map((court, i) => (
                  <div key={i} className={`${styles.courtCard} ${activeCourt === court.name ? styles.courtCardActive : ""}`} onClick={() => setActiveCourt(court.name)}>
                    <div className={styles.courtCardTop}>
                      <div className={styles.courtCardName}>{court.name}</div>
                      <span className={`${styles.courtTypeBadge} ${COURT_TYPE_STYLE[court.type] || ""}`}>
                        {COURT_TYPE_LABEL[court.type] || court.type}
                      </span>
                    </div>
                    <div className={styles.courtCardDetails}>
                      <div className={styles.courtDetail}>{I("Map")} {court.address}</div>
                      <div className={styles.courtDetail}>{I("Clock")} {court.hours}</div>
                      <div className={styles.courtDetail}>{I("Shield")} {court.phone}{court.helpline && court.helpline !== court.phone ? ` | Helpline: ${court.helpline}` : ""}</div>
                    </div>
                    {court.website && (
                      <a href={court.website} target="_blank" rel="noopener noreferrer" className={styles.courtWebLink} onClick={(e) => e.stopPropagation()}>
                        {I("Globe")} Official Website
                      </a>
                    )}
                  </div>
                ))}
              </div>
              <div className={styles.courtsMapWrap}>
                <div ref={courtsMapRef} style={{ width: "100%", height: "100%", minHeight: 400 }} />
              </div>
            </div>
          </>
        )}

        {courtsSearched && courtsResults.length === 0 && (
          <div className={styles.courtsEmpty}>
            {I("Map")}
            <h3>No courts found</h3>
            <p>Try searching with a different city name or pincode</p>
          </div>
        )}

        {!courtsSearched && (
          <div className={styles.courtsEmpty}>
            {I("Map")}
            <h3>Search for courts near you</h3>
            <p>Enter a city name like Delhi, Mumbai, Bengaluru or a pincode to find nearby courts</p>
          </div>
        )}

        <div style={{ textAlign: "center", padding: "20px 0", marginTop: 20 }}>
          <div style={{ display: "flex", gap: 20, justifyContent: "center", flexWrap: "wrap" }}>
            <a href="https://services.ecourts.gov.in/" target="_blank" rel="noopener noreferrer" className={styles.courtWebLink}>eCourts Services</a>
            <a href="https://njdg.ecourts.gov.in/" target="_blank" rel="noopener noreferrer" className={styles.courtWebLink}>National Judicial Data Grid</a>
            <a href="https://main.sci.gov.in/" target="_blank" rel="noopener noreferrer" className={styles.courtWebLink}>Supreme Court of India</a>
            <a href="https://nalsa.gov.in/" target="_blank" rel="noopener noreferrer" className={styles.courtWebLink}>Free Legal Aid (NALSA)</a>
          </div>
        </div>
      </section>
    </main>
  );

  /* ------ LEGAL NEWS ------ */
  const fetchNews = () => {
    setNewsLoading(true);
    setNewsError("");
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    fetch(`${API}/legal-news`, { signal: controller.signal })
      .then(r => r.json())
      .then(d => {
        clearTimeout(timeout);
        setNewsArticles(d.articles || []);
        if (d.next_refresh) setNextRefreshAt(d.next_refresh);
        setNewsLoading(false);
      })
      .catch((err) => {
        clearTimeout(timeout);
        setNewsLoading(false);
        setNewsError(err.name === "AbortError" ? "Request timed out. The server may be starting up - try again in a moment." : "Could not connect to the news server. Make sure the backend is running.");
      });
  };

  // Fetch news on tab visit
  useEffect(() => {
    if (view !== "news") return;
    fetchNews();
  }, [view]);

  // Countdown timer - ticks every second
  useEffect(() => {
    if (!nextRefreshAt) return;
    const tick = () => {
      const now = Math.floor(Date.now() / 1000);
      const diff = nextRefreshAt - now;
      if (diff <= 0) {
        setCountdown("New articles available!");
        return;
      }
      const h = Math.floor(diff / 3600);
      const m = Math.floor((diff % 3600) / 60);
      const s = diff % 60;
      setCountdown(`${String(h).padStart(2, "0")}h ${String(m).padStart(2, "0")}m ${String(s).padStart(2, "0")}s`);
    };
    tick();
    const interval = setInterval(tick, 1000);
    return () => clearInterval(interval);
  }, [nextRefreshAt]);

  const NEWS_CATEGORIES = ["all", ...new Set(newsArticles.map(a => a.category))];
  const filteredNews = newsFilter === "all" ? newsArticles : newsArticles.filter(a => a.category === newsFilter);

  const CATEGORY_COLORS = {
    "Supreme Court": "#eab308", "High Court": "#059669", "Legislation": "#0ea5e9",
    "Criminal": "#ef4444", "Property": "#22c55e", "Family Law": "#f472b6",
    "Consumer": "#06b6d4", "Cyber Law": "#047857", "Tax": "#f59e0b", "Legal News": "#94a3b8",
  };

  if (view === "news") renderView = (
    <main className={styles.page}>
      <NavBar active="news" />
      <section className={styles.newsSection}>
        <div className={styles.newsHeader}>
          <h1>{I("Globe")} Legal News & Updates</h1>
          <p>Latest developments in Indian law - Supreme Court judgments, High Court orders, and legislative updates</p>
          <div className={styles.newsRefreshBar}>
            <button className={styles.newsRefreshBtn} onClick={fetchNews} disabled={newsLoading}>
              {I("Clock")} {newsLoading ? "Refreshing..." : "Refresh"}
            </button>
            {countdown && (
              <div className={styles.newsTimer}>
                {I("Clock")} Next update in: <b>{countdown}</b>
              </div>
            )}
          </div>
        </div>

        {newsLoading ? (
          <div className={styles.analyzing} style={{ minHeight: 300 }}>
            <div className={styles.spinner}></div>
            <p>Fetching latest legal news...</p>
          </div>
        ) : newsError ? (
          <div className={styles.courtsEmpty}>
            {I("Globe")}
            <h3>Unable to load news</h3>
            <p>{newsError}</p>
            <button className={styles.btnPrimary} onClick={fetchNews} style={{ marginTop: 16 }}>{I("Clock")} Try Again</button>
          </div>
        ) : (
          <>
            <div className={styles.newsFilters}>
              {NEWS_CATEGORIES.map(cat => (
                <button key={cat} className={`${styles.courtFilterBtn} ${newsFilter === cat ? styles.courtFilterActive : ""}`}
                  onClick={() => setNewsFilter(cat)}>
                  {cat === "all" ? "All" : cat}
                </button>
              ))}
            </div>
            <div className={styles.newsCount}>
              Showing <b>{filteredNews.length}</b> article{filteredNews.length !== 1 ? "s" : ""}
              {newsFilter !== "all" && <> in <b>{newsFilter}</b></>}
            </div>
            <div className={styles.newsGrid}>
              {filteredNews.map((article, i) => (
                <a key={i} href={article.link} target="_blank" rel="noopener noreferrer" className={styles.newsCard}>
                  <div className={styles.newsCardImg}>
                    {article.image ? (
                      <img src={article.image} alt="" onError={(e) => { e.target.style.display = "none"; e.target.nextSibling.style.display = "flex"; }} />
                    ) : null}
                    <div className={styles.newsPlaceholder} style={article.image ? { display: "none" } : {}}>
                      <img src={`${LUCIDE_CDN}/scale.svg`} alt="" style={{ width: 48, height: 48, opacity: 0.25 }} />
                    </div>
                  </div>
                  <div className={styles.newsCardBody}>
                    <div className={styles.newsCardMeta}>
                      <span className={styles.newsCategory} style={{ background: `${CATEGORY_COLORS[article.category] || "#94a3b8"}20`, color: CATEGORY_COLORS[article.category] || "#94a3b8" }}>
                        {article.category}
                      </span>
                      <span className={styles.newsSource}>{article.source}</span>
                    </div>
                    <h3 className={styles.newsCardTitle}>{article.title}</h3>
                    {article.summary && <p className={styles.newsCardSummary}>{article.summary.substring(0, 150)}{article.summary.length > 150 ? "..." : ""}</p>}
                    <div className={styles.newsCardFooter}>
                      <span>{article.date}</span>
                      <span className={styles.newsReadMore}>Read More {I("ChevRight")}</span>
                    </div>
                  </div>
                </a>
              ))}
            </div>
            {filteredNews.length === 0 && (
              <div className={styles.courtsEmpty}>
                {I("Globe")}
                <h3>No articles found</h3>
                <p>Try a different category filter</p>
              </div>
            )}
          </>
        )}
      </section>
      <footer className={styles.footer}>
        <p>News sourced from LiveLaw, Bar & Bench, and Google News India.</p>
        <p className={styles.muted}>Updates every 24 hours at 12 AM IST sharp.</p>
        <a href="mailto:ankitsingh92004@gmail.com?subject=NyayBase Feedback" className={styles.contactLink}>{I("MessageCircle")} Contact Us</a>
      </footer>
    </main>
  );

  /* ------ RESULTS ------ */
  if (view === "results" && results) {
    /* Invalid Input Screen */
    if (results.is_invalid_input || results.is_weak_input) renderView = (
      <main className={styles.page}>
        <NavBar active="analyze" />
        <section className={styles.formSection}>
          <div className={styles.invalidBox}>
            <div className={styles.invalidIcon}>{I("Alert")}</div>
            <h2>{results.is_invalid_input ? "Invalid Input Detected" : "Insufficient Case Details"}</h2>
            <p className={styles.invalidMsg}>{results.error_message || results.win_probability?.reasoning || "Your case description does not contain enough specific information for a meaningful analysis."}</p>
            {(results.suggestions || results.improvement_tips) && (results.suggestions || results.improvement_tips).length > 0 && (
              <ul className={styles.invalidList}>
                {(results.suggestions || results.improvement_tips).map((s, i) => <li key={i}>{I("Check")} {s}</li>)}
              </ul>
            )}
            {results.example_input && <div className={styles.invalidExample}><strong>Example:</strong> {results.example_input}</div>}
            <button className={styles.btnPrimary} onClick={goToForm}>{I("ArrowLeft")} Go Back & Enter Detailed Case Facts</button>
          </div>
        </section>
      </main>
    );
    else {
      const wp = results.win_probability || {};
      renderView = (
        <main className={styles.page}>
          <NavBar active="analyze" />
          <section className={styles.resultsSection}>
            <div className={styles.resultsHeader}>
              <h1>{I("Scale")} Case Analysis Results</h1>
              <div className={styles.resultsMeta}>
                <span className={styles.badge}>{results.case_type}</span>
                <span className={styles.badge}>{results.jurisdiction}</span>
              </div>
            </div>

            {results.relevant_acts?.length > 0 && (
              <div className={styles.actsBar}>{I("Book")} <strong>Applicable Laws:</strong> {results.relevant_acts.join(" | ")}</div>
            )}

            {/* Action Buttons */}
            <div className={styles.actionRow}>
              <button className={`${styles.actionBtn} ${copied ? styles.actionBtnSuccess : ""}`} onClick={copyAnalysis}>
                {copied ? <>{I("Check")} Copied!</> : <>{I("Book")} Copy Summary</>}
              </button>
              <button className={styles.actionBtn} onClick={downloadPDF}>
                {I("Award")} Download Report
              </button>
            </div>

            <div className={styles.resultsGrid}>
              {/* Win Probability Card */}
              <div className={`${styles.resultCard} ${styles.resultCardAnim}`} style={{ animationDelay: "0s" }}>
                <h2 className={styles.cardH}>{I("Shield")} Win Probability</h2>
                <div className={styles.gaugeWrap}>
                  <svg viewBox="0 0 200 120" className={styles.gaugeSvg}>
                    <path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="#1e1e2f" strokeWidth="18" strokeLinecap="round" />
                    <path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke={wp.strength_color || "#d4af37"} strokeWidth="18" strokeLinecap="round"
                      strokeDasharray={`${(animGauge ? (wp.probability || 0) : 0) * 2.51} 999`}
                      style={{ transition: "stroke-dasharray 1.2s cubic-bezier(.4,0,.2,1)" }} />
                    <text x="100" y="80" textAnchor="middle" fill="#fff" fontSize="32" fontWeight="bold">{wp.probability || 0}%</text>
                    <text x="100" y="100" textAnchor="middle" fill={wp.strength_color || "#d4af37"} fontSize="13" fontWeight="600">{wp.strength || "N/A"}</text>
                  </svg>
                </div>
                <div className={styles.gaugeRange}>
                  <span>Low: {wp.lower_bound || 0}%</span>
                  <span>High: {wp.upper_bound || 0}%</span>
                </div>
                <div className={styles.gaugeDetails}>
                  <div><span className={styles.muted}>Base Rate</span><b>{wp.base_rate || 0}%</b></div>
                  <div><span className={styles.muted}>Adjustment</span><b style={{ color: (wp.adjustment || 0) >= 0 ? "#22c55e" : "#ef4444" }}>{(wp.adjustment || 0) >= 0 ? "+" : ""}{wp.adjustment || 0}%</b></div>
                  <div><span className={styles.muted}>Factors</span><b>{wp.factors_detected || 0}</b></div>
                </div>
                {wp.reasoning && <p className={styles.reasoning}>{wp.reasoning}</p>}
              </div>

              {/* Key Arguments */}
              <div className={`${styles.resultCard} ${styles.resultCardAnim}`} style={{ animationDelay: "0.15s" }}>
                <h2 className={styles.cardH}>{I("Book")} Key Arguments</h2>
                {(results.key_arguments || []).map((a, i) => (
                  <div key={i} className={styles.argItem}>
                    <div className={styles.argTop}><h4>{a.argument}</h4><span className={`${styles.badge} ${a.strength >= 80 ? styles.badgeG : a.strength >= 60 ? styles.badgeA : styles.badgeR}`}>{a.strength}%</span></div>
                    <div className={styles.muted} style={{ fontSize: 12 }}>{a.section}</div>
                    <p>{a.description}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.resultsGrid}>
              {/* Timeline */}
              <div className={`${styles.resultCard} ${styles.resultCardAnim}`} style={{ animationDelay: "0.3s" }}>
                <h2 className={styles.cardH}>{I("Clock")} Expected Timeline</h2>
                <div className={styles.timelineMain}>
                  <div className={styles.timelineNumber}>{results.timeline?.estimated_months || 0}<span>months (est.)</span></div>
                  <div className={styles.timelineRange}>{results.timeline?.min_months || 0} - {results.timeline?.max_months || 0} months range</div>
                </div>
                {(results.timeline?.stages || []).map((s, i) => (
                  <div key={i} className={styles.stageItem}>
                    <span>{s.court}</span>
                    <div className={styles.stageBar}>
                      <div className={styles.stageBarFill} style={{ width: `${Math.min(100, s.avg_months * 2)}%` }}></div>
                    </div>
                    <span className={styles.muted}>{s.avg_months}mo • {s.win_rate}%</span>
                  </div>
                ))}
                {results.timeline?.recommendation && <p className={styles.reasoning}>{results.timeline.recommendation}</p>}
              </div>

              {/* Mediation */}
              <div className={`${styles.resultCard} ${styles.resultCardAnim}`} style={{ animationDelay: "0.45s" }}>
                <h2 className={styles.cardH}>{I("Users")} Mediation Assessment</h2>
                <div className={styles.medMain}>
                  <div className={styles.medBadge} style={{ background: results.mediation?.color || "#6b7280" }}>{results.mediation?.recommendation || "N/A"}</div>
                  <div className={styles.medStats}>
                    <div><span className={styles.muted}>Success Rate</span><b>{results.mediation?.success_rate || 0}%</b></div>
                    <div><span className={styles.muted}>Avg Settlement</span><b>{results.mediation?.avg_settlement_months || 0} months</b></div>
                  </div>
                </div>
                {results.mediation?.reasoning && <p className={styles.reasoning}>{results.mediation.reasoning}</p>}
              </div>
            </div>

            {/* Similar Cases */}
            {(results.similar_cases || []).length > 0 && (
              <div className={`${styles.resultCard} ${styles.resultCardAnim}`} style={{ animationDelay: "0.6s" }}>
                <h2 className={styles.cardH}>{I("Book")} Similar Landmark Cases ({(results.similar_cases || []).length})</h2>
                {results.similar_cases.map((c, i) => (
                  <div key={i} className={styles.caseItem}>
                    <div className={styles.caseTop}>
                      <h4>{c.case_name}</h4>
                      <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                        {c.relevance_score && <span className={`${styles.badge} ${c.relevance_score >= 70 ? styles.badgeG : c.relevance_score >= 40 ? styles.badgeA : styles.badgeR}`}>{c.relevance_score}%</span>}
                        {c.year && <span className={styles.badge}>{c.year}</span>}
                      </div>
                    </div>
                    {c.citation && <div className={styles.muted} style={{ fontSize: 12 }}>{c.citation}{c.court ? ` - ${c.court}` : ""}</div>}
                    <p>{c.summary || c.outcome}</p>
                    {c.source_url && (
                      <a href={c.source_url} target="_blank" rel="noopener noreferrer" className={styles.sourceLink}>
                        {I("Book")} View on Indian Kanoon
                      </a>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Risk Factors */}
            {(results.risk_factors || []).length > 0 && (
              <div className={`${styles.resultCard} ${styles.resultCardAnim}`} style={{ animationDelay: "0.75s" }}>
                <h2 className={styles.cardH}>{I("Alert")} Risk Factors</h2>
                {results.risk_factors.map((r, i) => (
                  <div key={i} className={styles.riskItem}>
                    <div className={styles.riskTop}><h4>{r.risk}</h4><span className={`${styles.badge} ${r.severity === "High" ? styles.badgeR : r.severity === "Medium" ? styles.badgeA : styles.badgeG}`}>{r.severity}</span></div>
                    <p className={styles.muted}>{r.description}</p>
                    <div className={styles.mitigation}><strong>Mitigation:</strong> {r.mitigation}</div>
                  </div>
                ))}
              </div>
            )}

            <div className={styles.disclaimer}><p><strong>Disclaimer:</strong> NyayBase provides informational analysis based on historical court judgment patterns. This is not legal advice. Consult a qualified advocate for your specific case.</p></div>
            <div style={{ textAlign: "center", paddingBottom: 40 }}><button className={styles.btnPrimary} onClick={goToForm}>{I("Search")} Analyze Another Case</button></div>
          </section>
        </main>
      );
    }
  }

  /* ---- Floating Chatbot Widget (always visible) ---- */
  const chatWidget = (
    <>
      {chatOpen && (
        <div className={styles.chatPanel}>
          <div className={styles.chatHeader}>
            <div className={styles.chatHeaderLeft}>
              <Icons.Bot className={styles.chatBotIcon} />
              <div>
                <h3>NyayBase Assistant</h3>
                <span className={styles.chatOnline}>Online</span>
              </div>
            </div>
            <button className={styles.chatCloseBtn} onClick={() => setChatOpen(false)}>
              <Icons.X className={styles.chatCloseIcon} />
            </button>
          </div>

          <div className={styles.chatBody}>
            {chatMessages.length === 0 && (
              <div className={styles.chatWelcome}>
                <Icons.Scale className={styles.chatWelcomeIcon} />
                <h4>Welcome to NyayBase Assistant</h4>
                <p>Ask me anything about Indian law - rights, procedures, legal advice, and more.</p>
                <div className={styles.chatSamples}>
                  {CHAT_SAMPLES.map((q, i) => (
                    <button key={i} className={styles.chatSampleChip} onClick={() => sendChat(q)}>
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}
            {chatMessages.map((m, i) => (
              <div key={i} className={`${styles.chatMsg} ${m.role === "user" ? styles.chatMsgUser : styles.chatMsgBot}`}>
                {m.role === "bot" && <Icons.Bot className={styles.chatMsgAvatar} />}
                <div className={styles.chatBubble}>
                  {m.content.split("\n").map((line, j) => <span key={j}>{line}<br /></span>)}
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className={`${styles.chatMsg} ${styles.chatMsgBot}`}>
                <Icons.Bot className={styles.chatMsgAvatar} />
                <div className={`${styles.chatBubble} ${styles.chatTyping}`}>
                  <span className={styles.chatDot}></span>
                  <span className={styles.chatDot}></span>
                  <span className={styles.chatDot}></span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className={styles.chatFooter}>
            <input
              ref={chatInputRef}
              className={styles.chatInput}
              placeholder={chatLoading ? "Generating response..." : "Ask a legal question..."}
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !chatLoading && sendChat()}
              disabled={chatLoading}
            />
            {chatLoading ? (
              <button className={`${styles.chatSendBtn} ${styles.chatStopBtn}`} onClick={stopChat} title="Stop generating">
                <Icons.StopSquare className={styles.chatSendIcon} />
              </button>
            ) : (
              <button className={styles.chatSendBtn} onClick={() => sendChat()} disabled={!chatInput.trim()}>
                <Icons.Send className={styles.chatSendIcon} />
              </button>
            )}
          </div>
        </div>
      )}
      <button className={`${styles.chatFab} ${chatOpen ? styles.chatFabOpen : ""}`} onClick={() => setChatOpen(!chatOpen)}>
        {chatOpen ? <Icons.X className={styles.chatFabIcon} /> : <Icons.MessageCircle className={styles.chatFabIcon} />}
      </button>
    </>
  );

  return mounted ? (
    <>
      {renderView}
      {chatWidget}
    </>
  ) : null;
}
