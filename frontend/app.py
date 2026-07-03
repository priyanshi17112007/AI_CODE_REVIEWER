import streamlit as st
import requests
import json

# 1. Page Configuration
st.set_page_config(
    page_title="Agentic AI Code Reviewer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injecting Custom Dynamic Glassmorphism CSS Global Styles
st.markdown("""
    <style>
    /* Dark Cyber Theme Core Background override */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #11131c 0%, #0a0b10 100%);
        color: #e2e8f0;
    }
    
    /* Global Glassmorphic Panel Implementation */
    div[data-testid="stVerticalBlock"] > div:has(div.glass-card), .glass-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        margin-bottom: 20px;
    }

    /* Cyber Title Neon Accents */
    .cyber-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, #00f0ff 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    /* Custom Indicator Badges */
    .badge-high {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 11px;
    }
    .badge-med {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 11px;
    }
    
    /* Code block stylings */
    code, pre {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000/api"

# 3. Sidebar Log Management Panel
with st.sidebar:
    st.markdown('<h2 class="cyber-title">🛡️ CYBER_SHIELD</h2>', unsafe_allow_html=True)
    st.caption("MULTI-AGENT AI CODE AUDITOR")
    st.markdown("---")
    
    st.markdown("### 🕒 Recent Run History")
    try:
        response = requests.get(f"{BACKEND_URL}/history", timeout=5)
        if response.status_code == 200:
            history_data = response.json()
            if not history_data:
                st.info("No logs populated locally.")
            for log in history_data:
                score_color = "🟢" if log.get('quality_score', 0) >= 80 else "🟡"
                st.markdown(f"**{score_color} {log.get('filename', 'Unknown')}** \nScore: `{log.get('quality_score', 0)}%` | ID: #{log.get('id', 'N/A')}")
                st.markdown("<div style='border-bottom:1px solid rgba(255,255,255,0.05); margin-bottom:8px;'></div>", unsafe_allow_html=True)
        else:
            st.error("Engine pipeline unreachable.")
    except Exception:
        st.warning("Backend service offline.")

# 4. Main Panel Workspace Architecture
st.markdown('<h1 class="cyber-title">Agentic Code Review Engine</h1>', unsafe_allow_html=True)
st.write("Orchestrating concurrent security and performance agents via FastAPI + CrewAI.")

col_input, col_output = st.columns([5, 7], gap="large")

# Left Column Workspace: User Inputs
with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🤖 Control Console Input")
    
    filename = st.text_input("Target Filename", value="vulnerable_script.py")
    
    default_code = """# Paste target validation code source here
def execute_query(user_id):
    query = f"SELECT * FROM accounts WHERE id = '{user_id}'"
    db.execute(query) # Vulnerable loop node
"""
    code_content = st.text_area("Source Code Snippet", value=default_code, height=280)
    
    submit_btn = st.button("ENGAGE AGENT SWARM", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Right Column Workspace: Output Visualization
with col_output:
    if submit_btn:
        if not code_content.strip():
            st.warning("Please provide valid source code inputs.")
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            with st.spinner("⚡ CRIT_ENG_AGENT_COGNITION: Running multi-agent auditing..."):
                try:
                    payload = {"filename": filename, "content": code_content}
                    res = requests.post(f"{BACKEND_URL}/review", json=payload, timeout=60)
                    
                    if res.status_code == 200:
                        report = res.json()
                        
                        # Metrics Layout Display
                        m_col1, m_col2, m_col3 = st.columns(3)
                        m_col1.metric("Health Score", f"{report.get('quality_score', 0)}%")
                        m_col2.metric("Security Exploits", len(report.get('vulnerabilities', [])))
                        m_col3.metric("Loop Flaws", len(report.get('bugs', [])))
                        
                        st.markdown("---")
                        
                        # Section: Security Auditor Bugs
                        st.markdown("### 🔥 THREAT_REPORT_VULNERABILITIES")
                        vulnerabilities = report.get('vulnerabilities', [])
                        if not vulnerabilities:
                            st.success("No critical vulnerabilities detected by the swarm.")
                        for vuln in vulnerabilities:
                            badge_cls = "badge-high" if vuln.get('severity') == "High" else "badge-med"
                            st.markdown(f"""
                            <div style="background:rgba(255,255,255,0.02); padding:14px; border-radius:10px; margin-bottom:10px; border-left:4px solid #ff007f;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <strong>{vuln.get('title', 'Unknown Issue')}</strong>
                                    <span class="{badge_cls}">{vuln.get('severity', 'Medium')}</span>
                                </div>
                                <p style="font-size:13px; color:#a0aec0; margin: 6px 0 2px 0;">{vuln.get('description', '')}</p>
                                <small style="color:#00f0ff; font-family: monospace;">Location: {vuln.get('location', 'N/A')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        # Section: Logic & Data Loops
                        st.markdown("### 🪲 STRUCTURAL_LOOPS_AND_LOGIC")
                        bugs = report.get('bugs', [])
                        if not bugs:
                            st.success("No structural loop anomalies detected.")
                        for bug in bugs:
                            st.markdown(f"""
                            <div style="background:rgba(255,255,255,0.02); padding:14px; border-radius:10px; margin-bottom:10px; border-left:4px solid #f59e0b;">
                                <div style="display:flex; justify-content:space-between;">
                                    <span style="font-family: monospace; font-size:13px; font-weight:bold;">{bug.get('bug_type', 'Logic Flaw')}</span>
                                    <span style="color:#f59e0b; font-size:12px;">Impact: {bug.get('impact', 'Medium')}</span>
                                </div>
                                <div style="margin-top:8px; background:rgba(0,0,0,0.3); padding:8px; border-radius:6px; font-size:12px; border:1px solid rgba(255,255,255,0.05);">
                                    <span style="color:#00f0ff; font-weight:bold;">Fix Suggestion:</span> {bug.get('fix_suggestion', 'No fix specified.')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    else:
                        # NEW DIAGNOSTIC UPGRADE: Prints the real error on screen instead of hiding it!
                        st.error(f"❌ Backend Processing Failure (Status Code: {res.status_code})")
                        with st.expander("View Backend Crash Logs"):
                            st.code(res.text, language="json")
                            
                except requests.exceptions.Timeout:
                    st.error("⏳ Pipeline request timed out. The CrewAI agent swarm took over 60 seconds to respond.")
                except Exception as e:
                    st.error(f"🔗 Connection Error: Could not reach the FastAPI server at {BACKEND_URL}. Check your Uvicorn terminal.")
                    st.caption(f"Details: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # System Idle State Display
        st.markdown('<div class="glass-card" style="text-align:center; padding:50px !important; border-style:dashed !important;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#718096; font-family:monospace;'>SYSTEM_IDLE</h3>", unsafe_allow_html=True)
        st.write("Submit code structural files using the control console input panel to inspect real-time vulnerabilities.")
        st.markdown('</div>', unsafe_allow_html=True)