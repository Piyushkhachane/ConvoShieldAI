import streamlit as st
import pandas as pd
import re
import json
import hashlib
from datetime import datetime
from collections import Counter
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ConvoShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:       #05080f;
    --surface:  #090e1a;
    --card:     #0d1424;
    --card2:    #111b30;
    --border:   #182030;
    --border2:  #1e2d45;
    --green:    #00ff88;
    --cyan:     #00d4ff;
    --amber:    #ffb300;
    --red:      #ff3b5c;
    --blue:     #3b82f6;
    --purple:   #a855f7;
    --text:     #dde6f5;
    --muted:    #3d5070;
    --muted2:   #5a7090;
    --radius:   12px;
    --mono:     'IBM Plex Mono', monospace;
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.main .block-container { padding: 0 2rem 5rem !important; max-width: 1300px; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.1rem 2rem !important; }

.sb-brand { display:flex; align-items:center; gap:.6rem; margin-bottom:.2rem; }
.sb-brand-icon {
    width:36px; height:36px; border-radius:9px; flex-shrink:0;
    background:linear-gradient(135deg,var(--cyan),var(--green));
    display:flex; align-items:center; justify-content:center; font-size:1rem;
    animation:shield-pulse 3s ease-in-out infinite;
}
@keyframes shield-pulse {
    0%,100%{box-shadow:0 0 12px rgba(0,212,255,.3);}
    50%{box-shadow:0 0 28px rgba(0,255,136,.45);}
}
.sb-name {
    font-family:var(--mono); font-size:1.1rem; font-weight:600; letter-spacing:1px;
    background:linear-gradient(90deg,var(--cyan),var(--green));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.sb-tagline { font-size:.68rem; color:var(--muted2); letter-spacing:.5px; margin-bottom:1.6rem; padding-left:44px; }
.sb-section {
    font-size:.62rem; font-weight:700; letter-spacing:2.5px; text-transform:uppercase;
    color:var(--muted); margin:1.1rem 0 .55rem;
    display:flex; align-items:center; gap:7px;
}
.sb-section::after { content:''; flex:1; height:1px; background:var(--border); }
.sb-stat {
    background:var(--card); border:1px solid var(--border);
    border-radius:8px; padding:.7rem .9rem; margin-bottom:.5rem;
    display:flex; align-items:center; justify-content:space-between;
}
.sb-stat-label { font-size:.72rem; color:var(--muted2); font-weight:500; }
.sb-stat-val   { font-family:var(--mono); font-size:1rem; font-weight:600; }
.sb-pill-row { display:flex; flex-wrap:wrap; gap:.35rem; margin-top:.5rem; }
.sb-pill { font-size:.65rem; font-weight:600; padding:2px 9px; border-radius:99px; letter-spacing:.3px; }
.sp-green  { background:rgba(0,255,136,.08);  color:var(--green);  border:1px solid rgba(0,255,136,.18); }
.sp-cyan   { background:rgba(0,212,255,.08);  color:var(--cyan);   border:1px solid rgba(0,212,255,.18); }
.sp-amber  { background:rgba(255,179,0,.08);  color:var(--amber);  border:1px solid rgba(255,179,0,.18); }
.sp-red    { background:rgba(255,59,92,.08);  color:var(--red);    border:1px solid rgba(255,59,92,.18); }

/* HERO */
.hero {
    position:relative; overflow:hidden;
    background:linear-gradient(155deg,#07111f 0%,#050c18 50%,#060f0a 100%);
    border-bottom:1px solid var(--border);
    padding:3rem 3rem 2.6rem; margin:0 -2rem 2.5rem;
}
.hero::before {
    content:''; position:absolute; inset:0;
    background-image:
        radial-gradient(ellipse 500px 350px at 85% 40%,rgba(0,212,255,.07) 0%,transparent 65%),
        radial-gradient(ellipse 400px 400px at 10% 75%,rgba(0,255,136,.06) 0%,transparent 65%);
    animation:hero-breathe 7s ease-in-out infinite;
}
@keyframes hero-breathe{0%,100%{opacity:.8;}50%{opacity:1.3;}}
.hero::after {
    content:''; position:absolute; inset:0;
    background-image:repeating-linear-gradient(0deg,rgba(0,212,255,.02) 0px,rgba(0,212,255,.02) 1px,transparent 1px,transparent 44px);
}
.hero-inner { position:relative; z-index:2; }
.hero-chip {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(0,212,255,.07); border:1px solid rgba(0,212,255,.18);
    border-radius:99px; padding:4px 14px 4px 8px;
    font-size:.7rem; font-weight:700; color:var(--cyan);
    letter-spacing:1px; text-transform:uppercase; margin-bottom:1rem;
    animation:fade-up .5s ease both;
}
.hero-chip-dot { width:6px; height:6px; border-radius:50%; background:var(--green); animation:blink 1.4s ease-in-out infinite; }
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.15;}}
.hero-title {
    font-family:var(--mono); font-size:3.8rem; font-weight:600;
    letter-spacing:-1px; line-height:1; margin:0 0 .9rem;
    animation:fade-up .6s .05s ease both;
}
.ht-white { display:block; color:#fff; }
.ht-grad  {
    display:block;
    background:linear-gradient(90deg,var(--cyan) 0%,var(--green) 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero-sub {
    font-size:.95rem; color:var(--muted2); line-height:1.7;
    max-width:500px; margin:0 0 1.8rem; font-weight:400;
    animation:fade-up .6s .1s ease both;
}
.hero-sub strong { color:var(--text); }
.hero-tags { display:flex; gap:.6rem; flex-wrap:wrap; animation:fade-up .6s .15s ease both; }
.hero-tag {
    padding:4px 13px; border-radius:6px; font-size:.76rem;
    font-weight:600; border:1px solid; letter-spacing:.3px; transition:transform .2s;
}
.hero-tag:hover{transform:translateY(-2px);}
.htg{color:var(--green); background:rgba(0,255,136,.07); border-color:rgba(0,255,136,.2);}
.htc{color:var(--cyan);  background:rgba(0,212,255,.07); border-color:rgba(0,212,255,.2);}
.hta{color:var(--amber); background:rgba(255,179,0,.07); border-color:rgba(255,179,0,.2);}
.htr{color:var(--red);   background:rgba(255,59,92,.07); border-color:rgba(255,59,92,.2);}
@keyframes fade-up{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}

/* KPI ROW */
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem;}
.kpi{
    background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
    padding:1.1rem 1.4rem;position:relative;overflow:hidden;transition:transform .2s,border-color .2s;
}
.kpi:hover{transform:translateY(-2px);border-color:var(--border2);}
.kpi::after{
    content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,var(--kpi-c,var(--cyan)),transparent);
}
.kpi-icon{font-size:1.3rem;margin-bottom:.5rem;display:block;}
.kpi-val {font-family:var(--mono);font-size:2.1rem;font-weight:600;line-height:1;color:var(--kpi-c,var(--cyan));margin-bottom:.2rem;}
.kpi-lbl {font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted2);}

/* SECTION HEADER */
.sec-hdr{display:flex;align-items:center;gap:.7rem;margin-bottom:1rem;}
.sec-line{flex:1;height:1px;background:var(--border);}
.sec-title{font-family:var(--mono);font-size:1rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--text);}
.sec-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.sd-green {background:var(--green); box-shadow:0 0 8px var(--green);}
.sd-cyan  {background:var(--cyan);  box-shadow:0 0 8px var(--cyan);}
.sd-amber {background:var(--amber); box-shadow:0 0 8px var(--amber);}
.sd-red   {background:var(--red);   box-shadow:0 0 8px var(--red);}
.sd-purple{background:var(--purple);box-shadow:0 0 8px var(--purple);}

/* INPUT */
.input-wrap {
    background:var(--card);border:1px solid var(--border);
    border-radius:var(--radius);padding:1.5rem 1.5rem .8rem;
    margin-bottom:.8rem;transition:border-color .3s;
}
.input-wrap:focus-within{border-color:rgba(0,212,255,.3);box-shadow:0 0 0 3px rgba(0,212,255,.05);}
.input-lbl {
    font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;
    color:var(--muted2);margin-bottom:.6rem;display:flex;align-items:center;gap:6px;
}
.lbl-dot{width:5px;height:5px;border-radius:50%;background:var(--green);animation:blink 1.4s ease-in-out infinite;}

div[data-testid="stTextArea"] textarea {
    background:#04060f !important;border:1px solid var(--border2) !important;
    border-radius:8px !important;color:var(--text) !important;
    font-family:var(--mono) !important;font-size:.88rem !important;
    line-height:1.7 !important;padding:1rem 1.1rem !important;
    transition:border-color .2s,box-shadow .2s !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color:rgba(0,212,255,.4) !important;
    box-shadow:0 0 0 3px rgba(0,212,255,.07) !important;outline:none !important;
}
div[data-testid="stTextArea"] textarea::placeholder{color:var(--muted) !important;font-style:italic;}

/* SCAN BUTTON */
div[data-testid="stButton"] > button {
    background:linear-gradient(135deg,rgba(0,212,255,.15),rgba(0,255,136,.15)) !important;
    color:var(--cyan) !important;font-family:var(--mono) !important;
    font-size:.9rem !important;font-weight:600 !important;letter-spacing:2px !important;
    border:1px solid rgba(0,212,255,.35) !important;border-radius:8px !important;
    padding:.7rem 2rem !important;width:100% !important;transition:all .2s !important;
    box-shadow:0 0 20px rgba(0,212,255,.1) !important;
}
div[data-testid="stButton"] > button:hover {
    background:linear-gradient(135deg,rgba(0,212,255,.25),rgba(0,255,136,.25)) !important;
    box-shadow:0 0 32px rgba(0,212,255,.22) !important;transform:translateY(-2px) !important;
    border-color:rgba(0,212,255,.6) !important;
}

/* RISK BANNER */
.risk-banner{
    border-radius:var(--radius);padding:1.5rem 2rem;margin-bottom:1.2rem;
    display:flex;align-items:center;justify-content:space-between;gap:1rem;
    animation:fade-up .4s ease both;
}
.rb-green{background:rgba(0,255,136,.06);border:1px solid rgba(0,255,136,.2);}
.rb-amber{background:rgba(255,179,0,.06);border:1px solid rgba(255,179,0,.2);}
.rb-red  {background:rgba(255,59,92,.07);border:1px solid rgba(255,59,92,.22);}
.rb-label{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:2px;opacity:.65;margin-bottom:.3rem;}
.rb-value{font-family:var(--mono);font-size:2.4rem;font-weight:600;line-height:1;}
.rb-green .rb-value{color:var(--green);}
.rb-amber .rb-value{color:var(--amber);}
.rb-red   .rb-value{color:var(--red);}
.rb-sub{font-size:.8rem;color:var(--muted2);margin-top:4px;}
.rb-score-num{font-family:var(--mono);font-size:3rem;font-weight:600;line-height:1;}
.rb-green .rb-score-num{color:var(--green);}
.rb-amber .rb-score-num{color:var(--amber);}
.rb-red   .rb-score-num{color:var(--red);}
.rb-score-lbl{font-size:.62rem;color:var(--muted2);text-transform:uppercase;letter-spacing:1px;}

/* FINDING CARDS */
.finding-card{
    background:var(--card);border:1px solid var(--border);
    border-radius:8px;padding:.85rem 1.1rem;margin-bottom:.55rem;
    display:flex;align-items:flex-start;gap:.9rem;transition:border-color .2s;
    animation:fade-up .3s ease both;
}
.finding-card:hover{border-color:var(--border2);}
.finding-icon{font-size:1.1rem;flex-shrink:0;margin-top:1px;}
.finding-type{font-family:var(--mono);font-size:.78rem;font-weight:600;color:var(--text);margin-bottom:2px;}
.finding-detail{font-size:.75rem;color:var(--muted2);}
.finding-badge{
    margin-left:auto;flex-shrink:0;font-size:.62rem;font-weight:700;
    padding:2px 9px;border-radius:99px;text-transform:uppercase;letter-spacing:.5px;
}
.fb-low     {background:rgba(0,212,255,.1); color:var(--cyan);  border:1px solid rgba(0,212,255,.2);}
.fb-medium  {background:rgba(255,179,0,.1); color:var(--amber); border:1px solid rgba(255,179,0,.2);}
.fb-high    {background:rgba(255,59,92,.1); color:var(--red);   border:1px solid rgba(255,59,92,.2);}
.fb-critical{background:rgba(168,85,247,.1);color:var(--purple);border:1px solid rgba(168,85,247,.2);}

/* REDACT BOX */
.redact-box{
    background:#04060f;border:1px solid var(--border2);border-radius:8px;
    padding:1rem 1.2rem;font-family:var(--mono);font-size:.84rem;line-height:1.8;
    color:var(--text);white-space:pre-wrap;word-break:break-word;
}
.redact-box .r-phone  {background:rgba(255,179,0,.18); color:var(--amber); padding:1px 5px;border-radius:3px;}
.redact-box .r-email  {background:rgba(0,212,255,.15); color:var(--cyan);  padding:1px 5px;border-radius:3px;}
.redact-box .r-upi    {background:rgba(0,255,136,.13); color:var(--green); padding:1px 5px;border-radius:3px;}
.redact-box .r-link   {background:rgba(59,130,246,.15);color:var(--blue);  padding:1px 5px;border-radius:3px;}
.redact-box .r-aadhaar{background:rgba(255,59,92,.15); color:var(--red);   padding:1px 5px;border-radius:3px;}
.redact-box .r-pan    {background:rgba(168,85,247,.15);color:var(--purple);padding:1px 5px;border-radius:3px;}
.redact-box .r-credit {background:rgba(255,59,92,.15); color:var(--red);   padding:1px 5px;border-radius:3px;}
.redact-box .r-flag   {background:rgba(255,59,92,.12); color:var(--red);   padding:1px 5px;border-radius:3px;text-decoration:underline wavy rgba(255,59,92,.5);}

/* CLEAN STATE */
.clean-banner{
    background:rgba(0,255,136,.04);border:1px solid rgba(0,255,136,.15);
    border-radius:var(--radius);padding:2rem;text-align:center;animation:fade-up .4s ease both;
}
.clean-icon {font-size:2.5rem;margin-bottom:.5rem;}
.clean-title{font-family:var(--mono);font-size:1.3rem;font-weight:600;color:var(--green);margin-bottom:.3rem;}
.clean-sub  {font-size:.85rem;color:var(--muted2);}

/* DOWNLOAD BUTTON */
div[data-testid="stDownloadButton"] > button {
    background:rgba(0,255,136,.08) !important;color:var(--green) !important;
    font-family:var(--mono) !important;font-size:.82rem !important;font-weight:600 !important;
    letter-spacing:1px !important;border:1px solid rgba(0,255,136,.22) !important;
    border-radius:7px !important;padding:.55rem 1.2rem !important;
    width:100% !important;transition:all .2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background:rgba(0,255,136,.15) !important;
    box-shadow:0 0 20px rgba(0,255,136,.15) !important;
}

/* TABS */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:var(--card) !important;border-radius:8px !important;
    border:1px solid var(--border) !important;gap:0 !important;
    padding:4px !important;margin-bottom:1.2rem !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    background:transparent !important;border-radius:6px !important;
    color:var(--muted2) !important;font-family:var(--mono) !important;
    font-size:.82rem !important;font-weight:600 !important;letter-spacing:1px !important;
    padding:.4rem 1.2rem !important;border:none !important;transition:all .2s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background:linear-gradient(135deg,rgba(0,212,255,.18),rgba(0,255,136,.18)) !important;
    color:var(--cyan) !important;border:1px solid rgba(0,212,255,.25) !important;
}

details{background:var(--card) !important;border:1px solid var(--border) !important;border-radius:8px !important;}
summary{color:var(--muted2) !important;font-size:.83rem !important;font-weight:600 !important;}
div[data-testid="stDataFrame"]{border-radius:8px !important;border:1px solid var(--border) !important;overflow:hidden !important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DETECTION ENGINE
# ─────────────────────────────────────────────
LEGAL_PHRASES = {
    "Illegal Activity":     ["cracked version","torrent","fake report","hack","forged doc","pirated","darkweb","dark web","exploit","bypass security","stolen data"],
    "Workplace Misconduct": ["lazy teammate","gossip","skip the task","blame her","blame him","fake sick","backstab","sabotage","frame colleague"],
    "Harassment":           ["idiot","loser","shut up","bully","moron","worthless","you're fired","threatening","harass","intimidate","abuse"],
    "Confidential Info":    ["password is","api key","private info","secret key","access token","bearer token","client secret","db password","database password"],
    "Inappropriate Offers": ["black money","cheat","leak this","bribe","under the table","off the books","insider tip","pay in cash","money laundering"],
    "Hate Speech":          ["racist","sexist","homophobic","slur","discriminate","xenophobic"],
    "Self-Harm / Crisis":   ["want to die","kill myself","end my life","suicide","self harm","no reason to live"],
}

SEVERITY_WEIGHTS = {
    "Illegal Activity": 4, "Confidential Info": 4, "Inappropriate Offers": 3,
    "Harassment": 3, "Hate Speech": 4, "Self-Harm / Crisis": 5, "Workplace Misconduct": 2,
}

RISK_ICONS = {
    "Illegal Activity":"⚖️","Workplace Misconduct":"🏢","Harassment":"😠",
    "Confidential Info":"🔑","Inappropriate Offers":"💸","Hate Speech":"🚫",
    "Self-Harm / Crisis":"🆘","Phone Number":"📞","Email":"📧","UPI ID":"💳",
    "External Link":"🔗","Aadhaar Number":"🪪","PAN Card":"📄",
    "Credit/Debit Card":"💳","IP Address":"🌐","Date of Birth":"📅","IFSC Code":"🏦",
}

PRIVACY_PATTERNS = [
    ("Phone Number",      r"\b[6-9]\d{9}\b",                                     "Medium",   "Avoid sharing Indian mobile numbers."),
    ("Email",             r"[\w.\-+]+@[\w.\-]+\.[a-zA-Z]{2,}",                   "Low",      "Avoid unnecessary email exposure."),
    ("UPI ID",            r"[\w.\-]+@[a-zA-Z]+",                                  "Medium",   "Never share UPI IDs openly."),
    ("External Link",     r"https?://[\w.\-/?=#&%+]+",                            "Low",      "Verify external links before sharing."),
    ("Aadhaar Number",    r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",                  "High",     "Aadhaar is highly sensitive — never share."),
    ("PAN Card",          r"\b[A-Z]{5}\d{4}[A-Z]\b",                             "High",     "PAN card is sensitive personal data."),
    ("Credit/Debit Card", r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",     "Critical", "Card numbers must never be shared."),
    ("IP Address",        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",             "Low",      "Sharing IPs may expose your network."),
    ("IFSC Code",         r"\b[A-Z]{4}0[A-Z0-9]{6}\b",                           "Medium",   "Bank IFSC codes are semi-sensitive."),
    ("Date of Birth",     r"\b(0?[1-9]|[12]\d|3[01])[\/\-](0?[1-9]|1[0-2])[\/\-]\d{2,4}\b","Low","Dates of birth can aid identity theft."),
]

def detect_privacy_risks(text):
    issues = []
    for name, pattern, severity, suggestion in PRIVACY_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            sample = matches[0] if isinstance(matches[0], str) else "".join(matches[0])
            issues.append({"type": name, "severity": severity, "suggestion": suggestion, "sample": sample, "count": len(matches)})
    return issues

def check_legal_ethics(text):
    lower = text.lower()
    findings = []
    for category, phrases in LEGAL_PHRASES.items():
        for phrase in phrases:
            if phrase in lower:
                findings.append({
                    "category": category, "phrase": phrase,
                    "severity": "Critical" if SEVERITY_WEIGHTS.get(category,3) >= 4 else "High",
                    "suggestion": "Review or remove this statement immediately.",
                    "icon": RISK_ICONS.get(category, "⚠️")
                })
    return findings

def compute_risk_score(privacy, legal):
    sev_map = {"Low":1,"Medium":2,"High":3,"Critical":4}
    score = sum(sev_map.get(p["severity"],1) for p in privacy)
    score += sum(SEVERITY_WEIGHTS.get(l["category"],3) for l in legal)
    return score

def build_annotated_html(text, privacy_issues, legal_flags):
    import html as hl
    safe = hl.escape(text)
    type_class = {
        "Phone Number":"r-phone","Email":"r-email","UPI ID":"r-upi",
        "External Link":"r-link","Aadhaar Number":"r-aadhaar","PAN Card":"r-pan",
        "Credit/Debit Card":"r-credit","IP Address":"r-link","IFSC Code":"r-upi","Date of Birth":"r-phone",
    }
    pat_map = {
        "Phone Number":      r"\b[6-9]\d{9}\b",
        "Email":             r"[\w.\-+]+@[\w.\-]+\.[a-zA-Z]{2,}",
        "External Link":     r"https?://[\w.\-/?=#&%+]+",
        "Aadhaar Number":    r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
        "PAN Card":          r"\b[A-Z]{5}\d{4}[A-Z]\b",
        "Credit/Debit Card": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
        "IP Address":        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        "IFSC Code":         r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
        "Date of Birth":     r"\b(0?[1-9]|[12]\d|3[01])[\/\-](0?[1-9]|1[0-2])[\/\-]\d{2,4}\b",
    }
    found_types = {p["type"] for p in privacy_issues}
    for ptype, pat in pat_map.items():
        if ptype not in found_types:
            continue
        cls   = type_class.get(ptype,"r-link")
        label = ptype.replace("Number","").replace("Card","").strip().upper()
        safe  = re.sub(pat, lambda m: f'<span class="{cls}">[{label}: {hl.escape(m.group())}]</span>', safe)
    for f in legal_flags:
        phrase = hl.escape(f["phrase"])
        safe   = re.sub(re.escape(phrase), f'<span class="r-flag">{phrase}</span>', safe, flags=re.IGNORECASE)
    return safe

def generate_report(text, privacy, legal, score, risk_level, scan_id, ts):
    sep = "─" * 55
    lines = [
        "╔══════════════════════════════════════════════════════╗",
        "║         ConvoShield AI — Security Scan Report        ║",
        "╚══════════════════════════════════════════════════════╝",
        f"Scan ID   : {scan_id}",
        f"Timestamp : {ts}",
        f"Risk Level: {risk_level}  (Score: {score})",
        sep, "ORIGINAL TEXT", sep, text,
        sep, "PRIVACY RISKS DETECTED", sep,
    ]
    if privacy:
        for p in privacy:
            lines += [f"  [{p['severity']:8s}]  {p['type']} — found {p['count']}x",
                      f"             ↳ Sample : {p['sample']}", f"             ↳ Advice : {p['suggestion']}"]
    else:
        lines.append("  ✅  None detected.")
    lines += [sep, "LEGAL / ETHICAL FLAGS", sep]
    if legal:
        for l in legal:
            lines += [f"  [{l['severity']:8s}]  {l['category']}",
                      f"             ↳ Trigger: \"{l['phrase']}\"", f"             ↳ Advice : {l['suggestion']}"]
    else:
        lines.append("  ✅  None detected.")
    lines += [sep, "Generated by ConvoShield AI · Created by Piyush Khachane"]
    return "\n".join(lines)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-icon">🛡️</div>
        <div class="sb-name">ConvoShield</div>
    </div>
    <div class="sb-tagline">AI Privacy &amp; Ethics Scanner</div>
    """, unsafe_allow_html=True)

    history = st.session_state.scan_history
    total   = st.session_state.total_scans
    flagged = sum(1 for h in history if h["score"] > 0)

    st.markdown('<div class="sb-section">Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sb-stat"><span class="sb-stat-label">Total Scans</span><span class="sb-stat-val" style="color:var(--cyan);">{total}</span></div>
    <div class="sb-stat"><span class="sb-stat-label">Flagged</span><span class="sb-stat-val" style="color:var(--amber);">{flagged}</span></div>
    <div class="sb-stat"><span class="sb-stat-label">Clean</span><span class="sb-stat-val" style="color:var(--green);">{total - flagged}</span></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-pill-row">
        <span class="sb-pill sp-cyan">📞 Phone</span><span class="sb-pill sp-cyan">📧 Email</span>
        <span class="sb-pill sp-green">🪪 Aadhaar</span><span class="sb-pill sp-green">📄 PAN</span>
        <span class="sb-pill sp-amber">💳 Card</span><span class="sb-pill sp-amber">💳 UPI</span>
        <span class="sb-pill sp-red">⚖️ Legal</span><span class="sb-pill sp-red">🆘 Crisis</span>
        <span class="sb-pill sp-cyan">🌐 IP</span><span class="sb-pill sp-cyan">🏦 IFSC</span>
    </div>
    """, unsafe_allow_html=True)

    if history:
        st.markdown('<div class="sb-section">Recent Scans</div>', unsafe_allow_html=True)
        for h in reversed(history[-5:]):
            col = "var(--green)" if h["score"]==0 else ("var(--amber)" if h["score"]<8 else "var(--red)")
            icon = "🟢" if h["score"]==0 else ("🟡" if h["score"]<8 else "🔴")
            st.markdown(f"""
            <div class="sb-stat">
                <span class="sb-stat-label" style="font-family:var(--mono);font-size:.65rem;">{h['id'][:10]}…</span>
                <span class="sb-stat-val" style="font-size:.85rem;color:{col};">{icon} {h['level']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:.72rem;color:var(--muted2);line-height:1.7;">
        Scans text for PII leaks, legal risks<br>&amp; ethical violations using regex + rule-based NLP.<br><br>
        <span style="color:var(--muted);">Created by Piyush Khachane</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-inner">
        <div class="hero-chip"><span class="hero-chip-dot"></span>Real-time · Privacy · Ethics · Compliance</div>
        <div class="hero-title">
            <span class="ht-white">ConvoShield</span>
            <span class="ht-grad">AI Scanner</span>
        </div>
        <p class="hero-sub">
            Detect <strong>privacy leaks</strong>, <strong>legal risks</strong> and
            <strong>ethical violations</strong> in any text — emails, chats, posts or documents.
            10 PII categories. Inline annotation. Instant report.
        </p>
        <div class="hero-tags">
            <span class="hero-tag htg">🔒 Privacy Detection</span>
            <span class="hero-tag htc">🌐 10 PII Types</span>
            <span class="hero-tag hta">⚖️ Legal Flags</span>
            <span class="hero-tag htr">🆘 Crisis Signals</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────
total_scans_now = st.session_state.total_scans
flagged_now     = sum(1 for h in st.session_state.scan_history if h["score"]>0)
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi" style="--kpi-c:var(--cyan);">
        <span class="kpi-icon">🔍</span><div class="kpi-val">10</div><div class="kpi-lbl">PII Types</div>
    </div>
    <div class="kpi" style="--kpi-c:var(--green);">
        <span class="kpi-icon">⚖️</span><div class="kpi-val">7</div><div class="kpi-lbl">Ethics Categories</div>
    </div>
    <div class="kpi" style="--kpi-c:var(--amber);">
        <span class="kpi-icon">📊</span><div class="kpi-val">{total_scans_now}</div><div class="kpi-lbl">Scans Run</div>
    </div>
    <div class="kpi" style="--kpi-c:var(--red);">
        <span class="kpi-icon">🛡️</span><div class="kpi-val">{flagged_now}</div><div class="kpi-lbl">Threats Found</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT
# ─────────────────────────────────────────────
st.markdown("""
<div class="sec-hdr">
    <span class="sec-dot sd-cyan"></span>
    <span class="sec-title">Input</span>
    <div class="sec-line"></div>
</div>
<div class="input-wrap">
    <div class="input-lbl"><span class="lbl-dot"></span>Paste text to scan — email, chat, post or document</div>
</div>
""", unsafe_allow_html=True)

input_text = st.text_area(
    "input", height=180,
    placeholder="Paste text here…\n\nExample: My Aadhaar is 1234 5678 9012, call me on 9876543210 or pay via user@upi",
    label_visibility="collapsed"
)

col_btn, col_opt1, col_opt2 = st.columns([1, 1, 1])
with col_btn:
    scan_clicked = st.button("⚡  SCAN NOW", use_container_width=True)
with col_opt1:
    redact_mode = st.checkbox("🔴 Annotated text preview", value=True)
with col_opt2:
    show_charts = st.checkbox("📊 Show risk charts", value=True)

# ─────────────────────────────────────────────
#  ANALYSIS
# ─────────────────────────────────────────────
if scan_clicked:
    if not input_text.strip():
        st.warning("⚠️  Please enter some text to scan.")
    else:
        with st.spinner("🔍 Scanning…"):
            privacy_issues = detect_privacy_risks(input_text)
            legal_flags    = check_legal_ethics(input_text)
            risk_score     = compute_risk_score(privacy_issues, legal_flags)

            if risk_score == 0:   risk_level, rb_cls = "SAFE",      "rb-green"
            elif risk_score < 8:  risk_level, rb_cls = "MODERATE",  "rb-amber"
            else:                 risk_level, rb_cls = "HIGH RISK", "rb-red"

            ts      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            scan_id = hashlib.md5((input_text + ts).encode()).hexdigest()[:12].upper()

            st.session_state.total_scans += 1
            st.session_state.scan_history.append({
                "id": scan_id, "score": risk_score, "level": risk_level, "ts": ts,
                "privacy": len(privacy_issues), "legal": len(legal_flags)
            })

        # ── RISK BANNER ──
        st.markdown(f"""
        <div class="risk-banner {rb_cls}">
            <div>
                <div class="rb-label">Overall Risk Level</div>
                <div class="rb-value">{risk_level}</div>
                <div class="rb-sub">Scan ID: <code style="font-family:var(--mono);font-size:.75rem;">{scan_id}</code> &nbsp;·&nbsp; {ts}</div>
            </div>
            <div style="text-align:center;">
                <div class="rb-score-num">{risk_score}</div>
                <div class="rb-score-lbl">Risk Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── TABS ──
        tab1, tab2, tab3, tab4 = st.tabs(["🔒  PRIVACY", "⚖️  ETHICS & LEGAL", "📝  TEXT PREVIEW", "📊  CHARTS"])

        with tab1:
            st.markdown('<div class="sec-hdr"><span class="sec-dot sd-cyan"></span><span class="sec-title">Privacy Risk Findings</span><div class="sec-line"></div></div>', unsafe_allow_html=True)
            if privacy_issues:
                for p in privacy_issues:
                    sev   = p["severity"].lower()
                    badge = f"fb-{sev}"
                    icon  = RISK_ICONS.get(p["type"],"🔍")
                    st.markdown(f"""
                    <div class="finding-card">
                        <div class="finding-icon">{icon}</div>
                        <div class="finding-body">
                            <div class="finding-type">{p['type']} <span style="color:var(--muted2);font-weight:400;">× {p['count']}</span></div>
                            <div class="finding-detail">
                                Sample: <code style="font-family:var(--mono);font-size:.75rem;color:var(--amber);">{str(p['sample'])[:45]}</code><br>
                                {p['suggestion']}
                            </div>
                        </div>
                        <span class="finding-badge {badge}">{p['severity']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="clean-banner"><div class="clean-icon">✅</div><div class="clean-title">No Privacy Risks</div><div class="clean-sub">No PII patterns found in the scanned text.</div></div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="sec-hdr"><span class="sec-dot sd-red"></span><span class="sec-title">Legal &amp; Ethical Flags</span><div class="sec-line"></div></div>', unsafe_allow_html=True)
            if legal_flags:
                for l in legal_flags:
                    sev   = l["severity"].lower()
                    badge = f"fb-{sev}"
                    st.markdown(f"""
                    <div class="finding-card">
                        <div class="finding-icon">{l['icon']}</div>
                        <div class="finding-body">
                            <div class="finding-type">{l['category']}</div>
                            <div class="finding-detail">
                                Trigger: <code style="font-family:var(--mono);font-size:.75rem;color:var(--red);">"{l['phrase']}"</code><br>
                                {l['suggestion']}
                            </div>
                        </div>
                        <span class="finding-badge {badge}">{l['severity']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="clean-banner"><div class="clean-icon">✅</div><div class="clean-title">No Legal / Ethical Flags</div><div class="clean-sub">No concerning phrases detected.</div></div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="sec-hdr"><span class="sec-dot sd-amber"></span><span class="sec-title">Annotated Text Preview</span><div class="sec-line"></div></div>', unsafe_allow_html=True)
            display_html = build_annotated_html(input_text, privacy_issues, legal_flags) if redact_mode else __import__('html').escape(input_text)
            st.markdown(f'<div class="redact-box">{display_html}</div>', unsafe_allow_html=True)
            if redact_mode:
                st.markdown("""
                <div style="font-size:.72rem;color:var(--muted2);margin-top:.6rem;display:flex;gap:1rem;flex-wrap:wrap;">
                    <span><span style="background:rgba(255,179,0,.18);color:var(--amber);padding:1px 6px;border-radius:3px;">PHONE</span></span>
                    <span><span style="background:rgba(0,212,255,.15);color:var(--cyan);padding:1px 6px;border-radius:3px;">EMAIL</span></span>
                    <span><span style="background:rgba(0,255,136,.13);color:var(--green);padding:1px 6px;border-radius:3px;">UPI</span></span>
                    <span><span style="background:rgba(255,59,92,.15);color:var(--red);padding:1px 6px;border-radius:3px;">AADHAAR</span></span>
                    <span><span style="background:rgba(168,85,247,.15);color:var(--purple);padding:1px 6px;border-radius:3px;">PAN</span></span>
                    <span><span style="background:rgba(255,59,92,.12);color:var(--red);padding:1px 6px;border-radius:3px;text-decoration:underline wavy;">ethics flag</span></span>
                </div>
                """, unsafe_allow_html=True)

        with tab4:
            if not privacy_issues and not legal_flags:
                st.markdown('<div class="clean-banner"><div class="clean-icon">📊</div><div class="clean-title">Nothing to Chart</div><div class="clean-sub">No risks found.</div></div>', unsafe_allow_html=True)
            else:
                col1, col2 = st.columns(2)
                with col1:
                    all_sevs  = [p["severity"] for p in privacy_issues] + [l["severity"] for l in legal_flags]
                    sev_count = Counter(all_sevs)
                    sev_order  = ["Low","Medium","High","Critical"]
                    sev_colors = {"Low":"#00d4ff","Medium":"#ffb300","High":"#ff3b5c","Critical":"#a855f7"}
                    labels = [s for s in sev_order if s in sev_count]
                    values = [sev_count[s] for s in labels]
                    colors = [sev_colors[s] for s in labels]
                    fig = go.Figure(go.Pie(
                        labels=labels, values=values, hole=0.62,
                        marker=dict(colors=colors, line=dict(color='#05080f',width=2)),
                        textinfo='label+value', textfont=dict(size=11,family='IBM Plex Mono'),
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>',
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#dde6f5',family='Manrope'),
                        title=dict(text="Severity Breakdown",font=dict(size=13,color='#3d5070'),x=0),
                        showlegend=True,legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size=10)),
                        margin=dict(l=0,r=0,t=40,b=0),height=280,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    cat_labels, cat_values, cat_colors_list = [], [], []
                    for p in privacy_issues:
                        cat_labels.append(p["type"])
                        cat_values.append({"Low":1,"Medium":2,"High":3,"Critical":4}.get(p["severity"],1))
                        cat_colors_list.append({"Low":"#00d4ff","Medium":"#ffb300","High":"#ff3b5c","Critical":"#a855f7"}.get(p["severity"],"#00d4ff"))
                    for l in legal_flags:
                        cat_labels.append(l["category"][:18])
                        cat_values.append(SEVERITY_WEIGHTS.get(l["category"],3))
                        cat_colors_list.append("#a855f7" if SEVERITY_WEIGHTS.get(l["category"],3)>=4 else "#ff3b5c")
                    fig2 = go.Figure(go.Bar(
                        y=cat_labels, x=cat_values, orientation='h',
                        marker=dict(color=cat_colors_list, line=dict(width=0)),
                        text=cat_values, textposition='outside',
                        textfont=dict(size=10,color='#dde6f5',family='IBM Plex Mono'),
                    ))
                    fig2.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#dde6f5',family='Manrope'),
                        title=dict(text="Risk Weight by Category",font=dict(size=13,color='#3d5070'),x=0),
                        xaxis=dict(showgrid=True,gridcolor='#182030',color='#3d5070'),
                        yaxis=dict(showgrid=False,color='#dde6f5',tickfont=dict(size=10)),
                        margin=dict(l=0,r=40,t=40,b=10),height=280,
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                # Gauge
                st.markdown('<div class="sec-hdr" style="margin-top:.5rem;"><span class="sec-dot sd-purple"></span><span class="sec-title">Risk Score Gauge</span><div class="sec-line"></div></div>', unsafe_allow_html=True)
                gauge_color = "#00ff88" if risk_score==0 else "#ffb300" if risk_score<8 else "#ff3b5c"
                fig3 = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=min(risk_score, 20),
                    gauge={
                        "axis": {"range":[0,20],"tickcolor":"#3d5070","tickfont":{"color":"#3d5070","size":10}},
                        "bar":  {"color":gauge_color,"thickness":0.25},
                        "bgcolor": "#0d1424","bordercolor":"#182030",
                        "steps": [
                            {"range":[0,4],  "color":"rgba(0,255,136,0.08)"},
                            {"range":[4,8],  "color":"rgba(255,179,0,0.08)"},
                            {"range":[8,20], "color":"rgba(255,59,92,0.08)"},
                        ],
                        "threshold":{"line":{"color":gauge_color,"width":3},"thickness":0.75,"value":min(risk_score,20)},
                    },
                    number={"font":{"size":40,"color":gauge_color,"family":"IBM Plex Mono"}},
                    title={"text":f"<b>{risk_level}</b>","font":{"size":14,"color":gauge_color}},
                ))
                fig3.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#dde6f5',family='Manrope'),
                    margin=dict(l=40,r=40,t=20,b=10),height=240,
                )
                st.plotly_chart(fig3, use_container_width=True)

        # ── DOWNLOAD REPORTS ──
        st.markdown('<div class="sec-hdr" style="margin-top:1.5rem;"><span class="sec-dot sd-green"></span><span class="sec-title">Download Report</span><div class="sec-line"></div></div>', unsafe_allow_html=True)
        report_txt = generate_report(input_text, privacy_issues, legal_flags, risk_score, risk_level, scan_id, ts)
        report_json = json.dumps({
            "scan_id":scan_id,"timestamp":ts,"risk_level":risk_level,"risk_score":risk_score,
            "privacy_issues":privacy_issues,"legal_flags":legal_flags,
        }, indent=2)
        csv_rows = (
            [{"source":"privacy","category":p["type"],"severity":p["severity"],"detail":str(p["sample"]),"suggestion":p["suggestion"]} for p in privacy_issues] +
            [{"source":"ethics","category":l["category"],"severity":l["severity"],"detail":l["phrase"],"suggestion":l["suggestion"]} for l in legal_flags]
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📄 TXT Report",  data=report_txt,  file_name=f"convoshield_{scan_id}.txt",  mime="text/plain",       use_container_width=True)
        with c2:
            st.download_button("🗂️ JSON Report", data=report_json, file_name=f"convoshield_{scan_id}.json", mime="application/json", use_container_width=True)
        with c3:
            if csv_rows:
                st.download_button("📊 CSV Report",  data=pd.DataFrame(csv_rows).to_csv(index=False), file_name=f"convoshield_{scan_id}.csv",  mime="text/csv", use_container_width=True)

else:
    st.markdown("""
    <div class="clean-banner" style="margin-top:1rem;">
        <div class="clean-icon">🛡️</div>
        <div class="clean-title">Ready to Scan</div>
        <div class="clean-sub">
            Paste any text above and click <strong style="color:#dde6f5;">⚡ SCAN NOW</strong><br>
            to detect privacy leaks, legal risks &amp; ethical violations instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid #182030;margin-top:2rem;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:.75rem;letter-spacing:2px;color:#3d5070;text-transform:uppercase;">
        ConvoShield AI · Privacy &amp; Ethics Scanner · Created by Piyush Khachane
    </div>
</div>
""", unsafe_allow_html=True)
