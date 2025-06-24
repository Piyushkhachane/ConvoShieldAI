import streamlit as st
import pandas as pd
import re

# Set page configuration
st.set_page_config(page_title="ConvoShield AI", layout="wide", page_icon="🔐")

# Sidebar: About
with st.sidebar:
    st.title("ℹ️ About ConvoShield AI")
    st.markdown("""
    Welcome to **ConvoShield AI** 🔐

    This app:
    - Detects privacy risks like phone numbers, emails, UPI, etc.
    - Flags unethical or illegal language
    - Summarizes message risk with a score and downloadable report

    **Created by:** Piyush Khachane
    """)

# LEGAL/ETHICAL PHRASES
LEGAL_PHRASES = {
    "Illegal": ["cracked version", "torrent", "fake report", "hack", "forged doc"],
    "Workplace Misconduct": ["lazy teammate", "gossip", "skip the task", "blame her"],
    "Harassment": ["idiot", "loser", "shut up", "bully"],
    "Confidential Info": ["password is", "API key", "private info"],
    "Inappropriate Offers": ["black money", "cheat", "leak this"]
}

# Privacy Detection (Regex Rules)
def detect_privacy_risks(text):
    issues = []
    if re.search(r"\b\d{10}\b", text):
        issues.append(["Phone Number", "Medium", "Avoid sharing personal numbers."])
    if re.search(r"[\w.-]+@[\w.-]+", text):
        issues.append(["Email", "Low", "Avoid unnecessary email exposure."])
    if re.search(r"[\w.-]+@ok[\w]+", text):
        issues.append(["UPI ID", "Medium", "Never share UPI openly."])
    if re.search(r"(http|https)://[\w./-]+", text):
        issues.append(["External Link", "Low", "Review external links."])
    return issues

# Legal & Ethical Check
def check_legal_ethics(text):
    text = text.lower()
    findings = []
    for category, phrases in LEGAL_PHRASES.items():
        for phrase in phrases:
            if phrase in text:
                findings.append([category, phrase, "High", "Review or rephrase this statement."])
    return findings

# Streamlit App UI
st.title("🔐 ConvoShield AI – Smart Privacy Risk Detector for Conversations")

input_text = st.text_area("Enter your message/email/post:", height=200)

if st.button("Analyze Message"):
    with st.spinner("Analyzing message..."):
        if not input_text.strip():
            st.warning("⚠ Please enter some text.")
        else:
            # Run analysis
            privacy_issues = detect_privacy_risks(input_text)
            legal_flags = check_legal_ethics(input_text)

            # Results
            with st.expander("📌 Privacy Risk Analysis", expanded=True):
                if privacy_issues:
                    st.table(pd.DataFrame(privacy_issues, columns=["Type", "Risk Level", "Suggestion"]))
                else:
                    st.success("✅ No privacy risk found.")

            with st.expander("⚖ Legal & Ethical Risk Flags", expanded=True):
                if legal_flags:
                    st.table(pd.DataFrame(legal_flags, columns=["Category", "Phrase", "Risk", "Suggestion"]))
                else:
                    st.success("✅ No legal/ethical risk detected.")

            # 🛡️ Risk Score Indicator
            risk_score = len(privacy_issues) * 2 + len(legal_flags) * 3
            if risk_score >= 8:
                risk_level = "High"
                color = "🔴"
            elif risk_score >= 4:
                risk_level = "Medium"
                color = "🟡"
            else:
                risk_level = "Low"
                color = "🟢"

            with st.expander("🛡️ Overall Risk Score", expanded=True):
                st.metric(label="Risk Score", value=f"{risk_score} / 10", delta=f"{color} {risk_level}")
                st.progress(min(risk_score / 10, 1.0))

            # 📥 Report Download
            with st.expander("📥 Download Full Report"):
                report_text = f"""
🧾 ConvoShield AI Report

📄 Original Text:
{input_text}

📌 Privacy Issues:
{privacy_issues if privacy_issues else 'None'}

⚖ Legal & Ethical Flags:
{legal_flags if legal_flags else 'None'}

🛡️ Risk Score: {risk_score} ({risk_level})
                """
                st.download_button("Download Report", report_text, file_name="convo_report.txt")
