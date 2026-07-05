import streamlit as st
import requests
import json

# 1. Dynamic Extension-to-Language Mapping Function
def detect_programming_language(filename: str) -> str:
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    extension_map = {
        'py': 'python',
        'java': 'java',
        'js': 'javascript',
        'ts': 'typescript',
        'c': 'c',
        'cpp': 'cpp',
        'cc': 'cpp',
        'h': 'c',
        'cs': 'csharp',
        'go': 'go',
        'rs': 'rust',
        'rb': 'ruby',
        'php': 'php',
        'html': 'html',
        'css': 'css',
        'sh': 'bash',
        'sql': 'sql',
        'kt': 'kotlin',
        'swift': 'swift'
    }
    return extension_map.get(ext, 'plaintext')


# 2. Advanced Page Setup
st.set_page_config(
    page_title="QUANTUM_SHIELD // AI Code Auditor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Injecting Custom Glamorous Cyber-Glassmorphism CSS Engine
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;900&family=Plus+Jakarta+Sans:wght@300;500;700&display=swap');
    
    /* Global Background Override with Shimmering Core Mesh */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1a103c 0%, #060814 60%, #020308 100%) !important;
        color: #f1f5f9 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Core Dynamic Glassmorphic Panel Structure with Internal Diamond Reflection */
    div[data-testid="stVerticalBlock"] > div:has(div.glass-card), .glass-card {
        background: rgba(10, 15, 30, 0.45) !important;
        backdrop-filter: blur(24px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 20px !important;
        padding: 28px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 
                    inset 0 0 30px rgba(0, 240, 255, 0.05) !important;
        margin-bottom: 24px;
        transition: all 0.4s ease-in-out;
    }
    
    .glass-card:hover {
        border-color: rgba(255, 0, 127, 0.3) !important;
        box-shadow: 0 25px 60px rgba(255, 0, 127, 0.1), 
                    inset 0 0 40px rgba(255, 0, 127, 0.05) !important;
    }

    /* Glamorous Cyber Title - Diamond Bright Neon Text */
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #00f0ff 10% , #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0px 0px 15px rgba(0, 240, 255, 0.4));
        margin-bottom: 5px;
    }

    /* Futuristic Animated Flowing Current Waves Banner */
    .wave-container {
        position: relative;
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, #00f0ff, #ff007f, #9d4edd, #00f0ff);
        background-size: 400% 400%;
        border-radius: 3px;
        margin-bottom: 30px;
        animation: cyberWaveFlow 8s ease infinite;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
    }
    
    @keyframes cyberWaveFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Customized Shiny High-Tech Metric Shells */
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Dynamic Cyber Status Badges */
    .badge-high {
        background: linear-gradient(135deg, #ff2a54 0%, #99001d 100%);
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 0 12px rgba(255, 42, 84, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .badge-med {
        background: linear-gradient(135deg, #ff9f0a 0%, #b36b00 100%);
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 0 12px rgba(2ff, 159, 10, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .badge-low {
        background: linear-gradient(135deg, #0bf 0%, #005580 100%);
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 0 12px rgba(0, 187, 255, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Custom Shimmering Submit Button Override */
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 50%, #ff007f 100%) !important;
        background-size: 200% auto !important;
        color: white !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        box-shadow: 0 4px 20px rgba(0, 240, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-position: right center !important;
        box-shadow: 0 4px 30px rgba(255, 0, 127, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Code Editor Viewport Customizations */
    textarea, input {
        background-color: rgba(5, 7, 15, 0.7) !important;
        color: #00f0ff !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        font-family: 'Fira Code', monospace !important;
        border-radius: 10px !important;
    }
    textarea:focus, input:focus {
        border-color: #ff007f !important;
        box-shadow: 0 0 10px rgba(255, 0, 127, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000/api"

# 4. Sidebar Log Architecture
with st.sidebar:
    st.markdown('<h2 class="cyber-title">🛡️ CYBER_SHIELD</h2>', unsafe_allow_html=True)
    st.caption("MULTI-AGENT SWARM CORE ENGINE")
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-family:Orbitron; font-size:15px; color:#00f0ff;'>🕒 QUANTUM LEDGER LOGS</h3>", unsafe_allow_html=True)
    try:
        response = requests.get(f"{BACKEND_URL}/history", timeout=5)
        if response.status_code == 200:
            history_data = response.json()
            if not history_data:
                st.info("No logs populated locally.")
            for log in history_data:
                score = log.get('quality_score', 0)
                score_color = "🟢" if score >= 80 else ("🟡" if score >= 50 else "🔴")
                st.markdown(f"**{score_color} {log.get('filename', 'Unknown')}** \nHealth Matrix: `{score}%` | ID: `#{log.get('id', 'N/A')}`")
                st.markdown("<div style='border-bottom:1px solid rgba(0,240,255,0.1); margin-bottom:10px;'></div>", unsafe_allow_html=True)
        else:
            st.error("Engine pipeline data synchronization mismatch.")
    except Exception:
        st.warning("Relational SQLite Ledger Service Offline.")

# 5. Main Control Console Header Layout
st.markdown('<h1 class="cyber-title">QUANTUM ENGINE CODE REVIEWER</h1>', unsafe_allow_html=True)
st.markdown("<p style='color:#a4b3c6; margin-top:-10px;'>Orchestrating autonomous security engineers and static compilation emulators concurrently via FastAPI & CrewAI.</p>", unsafe_allow_html=True)
st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)

col_input, col_output = st.columns([5, 7], gap="large")

# Left Workspace Column: Operational Input Control
with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:Orbitron; font-size:18px; color:#ffffff; margin-bottom:15px;'>🛰️ SECURE DIRECTIVE INPUT</h3>", unsafe_allow_html=True)
    
    filename = st.text_input("Target File Vector Name", value="vulnerable_script.py")
    
    default_code = """# Paste target validation code source here
def execute_query(user_id):
    query = f"SELECT * FROM accounts WHERE id = '{user_id}'"
    db.execute(query) # Vulnerable injection loop node
"""
    code_content = st.text_area("Source Manifest Content", value=default_code, height=320)
    
    submit_btn = st.button("ENGAGE SWARM ANALYSIS PIPELINE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# Right Workspace Column: Realtime Swarm Extraction Output
with col_output:
    if submit_btn:
        if not code_content.strip():
            st.warning("Please provide valid source code inputs.")
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            with st.spinner("⚡ CRIT_ENG_AGENT_COGNITION: Processing matrix loops..."):
                try:
                    payload = {"filename": filename, "content": code_content}
                    res = requests.post(f"{BACKEND_URL}/review", json=payload, timeout=60)
                    
                    if res.status_code == 200:
                        response_data = res.json()
                        
                        # Shiny Metric Layout Display
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(label="Calculated Health Score", value=f"{response_data.get('quality_score', 100)}%")
                        with col2:
                            st.metric(label="Active Vulnerabilities", value=len(response_data.get("vulnerabilities", [])))
                        with col3:
                            st.metric(label="Logical Quality Bugs", value=len(response_data.get("bugs", [])))

                        st.markdown("<div style='margin: 20px 0; border-bottom:1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)
                        
                        # --- SECTION A: SECURITY VULNERABILITIES SWEEP ---
                        st.markdown("<h3 style='font-family:Orbitron; font-size:16px; color:#ff007f;'>🔥 THREAT_REPORT_VULNERABILITIES</h3>", unsafe_allow_html=True)
                        vulnerabilities = response_data.get('vulnerabilities', [])
                        
                        if not vulnerabilities:
                            st.success("No structural security breaches isolated by the auditor.")
                        else:
                            for vuln in vulnerabilities:
                                severity = str(vuln.get('severity', 'Medium')).strip().capitalize()
                                if severity == "High":
                                    badge_cls, border_color = "badge-high", "#ff2a54"
                                elif severity == "Low":
                                    badge_cls, border_color = "badge-low", "#0bf"
                                else:
                                    badge_cls, border_color = "badge-med", "#ff9f0a"
                                    
                                st.markdown(f"""
                                <div style="background:rgba(255,255,255,0.02); padding:16px; border-radius:12px; margin-bottom:12px; border-left:4px solid {border_color}; box-shadow: inset 0 0 15px rgba({int(border_color[1:3],16) if len(border_color)==4 else 255},0,0,0.05);">
                                    <div style="display:flex; justify-content:between; align-items:center; gap:20px;">
                                        <span style="color:#ffffff; font-weight:700; font-size:14px; flex-grow:1;">🛡️ {vuln.get('title', 'Unknown Issue')}</span>
                                        <span class="{badge_cls}">{severity}</span>
                                    </div>
                                    <p style="font-size:13px; color:#cbd5e1; margin: 10px 0; line-height:1.5;">{vuln.get('description', '')}</p>
                                    <div style="margin-top:4px; font-size:12px; color:#00f0ff; font-family:monospace;">
                                        <strong>Location Cluster:</strong> Line {vuln.get('line_number', 'N/A')} | Scope: {vuln.get('location', 'Global')}
                                    </div>
                                    <div style="background:rgba(0,240,255,0.03); border:1px dashed rgba(0,240,255,0.2); padding:12px; border-radius:8px; margin-top:10px;">
                                        <small style="color:#00f0ff; font-weight:bold; display:block; margin-bottom:4px; font-family:Orbitron;">⚙️ REQUIRED REMEDIATION MATRIX:</small>
                                        <small style="color:#e2e8f0; font-size:12.5px; line-height:1.4;">{vuln.get('remediation', 'No execution correction logged.')}</small>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                        st.markdown("<div style='margin: 25px 0; border-bottom:1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)
                        
                        # --- SECTION B: LOGICAL COMPILER & QUALITY SWEEP ---
                        st.markdown("<h3 style='font-family:Orbitron; font-size:16px; color:#00f0ff;'>🪲 STRUCTURAL_LOOPS_AND_LOGIC</h3>", unsafe_allow_html=True)
                        bugs = response_data.get('bugs', [])
                        
                        if not bugs:
                            st.success("No static compilation blocks isolated by pre-commit checkers.")
                        else:
                            uploaded_filename = response_data.get("filename", "code.txt")
                            render_lang = detect_programming_language(uploaded_filename)
                            
                            # Fixed iterative loop closure targeting all items in arrays
                            for bug in bugs:
                                impact = str(bug.get('impact', 'Medium')).strip().capitalize()
                                title = bug.get('bug_type') or "Code Logic Bug"
                                line = bug.get('line_number', '0')
                                desc = bug.get('description', 'No descriptive diagnostic logged.')
                                fix_code = bug.get('fix_suggestion') or "// No correction payload."
                                
                                if "Compilation" in impact or "Error" in impact:
                                    bug_border, bug_badge = "#ff007f", "badge-high"
                                else:
                                    bug_border, bug_badge = "#ff9f0a", "badge-med"
                                    
                                st.markdown(f"""
                                <div style="background:rgba(255,255,255,0.02); padding:16px; border-radius:12px 12px 0 0; margin-top:16px; border-left:4px solid {bug_border}; border-bottom:1px solid rgba(255,255,255,0.05);">
                                    <div style="display:flex; justify-content:space-between; align-items:center; gap:20px;">
                                        <span style="font-family: monospace; font-weight:700; font-size:13.5px; color:#ffffff;">💥 Vector: {title} (Line {line})</span>
                                        <span class="{bug_badge}">{impact}</span>
                                    </div>
                                    <p style="font-size:13px; color:#cbd5e1; margin: 10px 0 0 0; line-height:1.5;">{desc}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Render patch code blocks cleanly matching outer theme variables
                                with st.expander(f"🛠️ DEPLOY STRUCTURAL PATCH FOR LINE {line}"):
                                    st.code(fix_code, language=render_lang)
                                    
                    else:
                        st.error(f"❌ Backend Processing Failure (Status Code: {res.status_code})")
                        with st.expander("View Backend Crash Logs"):
                            st.code(res.text, language="json")
                            
                except requests.exceptions.Timeout:
                    st.error("⏳ Pipeline request timed out. The multi-agent workspace verification processing cycle broke 60 seconds.")
                except Exception as e:
                    st.error(f"🔗 Connection Error: Target FastAPI node at {BACKEND_URL} is unreachable.")
                    st.caption(f"Details: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Standby Initialization State Displays
        st.markdown('<div class="glass-card" style="text-align:center; padding:60px !important; border-style:dashed !important; border-color: rgba(0,240,255,0.2) !important;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#64748b; font-family:Orbitron; font-size:16px; letter-spacing:1px;'>🛰️ SYSTEM_IDLE // MONITORING_MODE</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#475569; font-size:13px; max-width:400px; margin:10px auto;'>Input targeted script components in the operational workspace dashboard terminal to trigger asynchronous processing loops.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)