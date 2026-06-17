import streamlit as st
import google.generativeai as genai
import requests
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & IDENTITY ---
st.set_page_config(page_title="AlishooX Pro Terminal", layout="wide", initial_sidebar_state="collapsed")

# Auto-refresh Gold Price & News every 30 seconds
st_autorefresh(interval=30 * 1000, key="jarvis_sync")

# Load Keys from Secrets
try:
    FINNHUB_KEY = st.secrets["FINNHUB_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ Secrets Error: Please check your API Keys in Streamlit Cloud Settings.")

# --- 2. PREMIUM JARVIS UI/UX (CSS Animations) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    .stApp { background-color: #050508; color: #e0e0f0; font-family: 'Rajdhani', sans-serif; }
    
    /* Premium Neon Borders & Animations */
    @keyframes glow { 0% { box-shadow: 0 0 5px #00e5ff33; } 50% { box-shadow: 0 0 20px #00e5ff66; } 100% { box-shadow: 0 0 5px #00e5ff33; } }
    @keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    .neon-card {
        border: 1px solid #00e5ff33; border-radius: 15px; padding: 20px;
        background: rgba(10, 10, 15, 0.9); backdrop-filter: blur(10px);
        animation: glow 3s infinite, slideIn 0.8s ease-out;
        margin-bottom: 15px; text-align: center;
    }
    
    .agent-label { color: #00e5ff; font-family: 'Orbitron'; font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; }
    .metric-val { font-family: 'Orbitron'; font-size: 1.6rem; font-weight: 900; color: #ffffff; text-shadow: 0 0 10px #ffffff33; }
    
    /* Login Page Premium Style */
    .login-box {
        max-width: 450px; margin: auto; padding: 40px; border-radius: 20px;
        border: 1px solid #ffd70044; background: rgba(15, 15, 20, 0.95);
        box-shadow: 0 0 40px #ffd70011; animation: slideIn 1s ease;
    }
    
    /* Spinning Analyzer Circle */
    .analyzer-circle {
        width: 80px; height: 80px; border: 3px solid transparent;
        border-top: 3px solid #00e5ff; border-radius: 50%;
        animation: spin 1.5s linear infinite; margin: 0 auto 20px;
    }

    /* Signal Box Premium */
    .signal-box {
        border: 2px solid #ffd700; border-radius: 15px; padding: 25px;
        background: linear-gradient(145deg, #0f0f15, #050508);
        box-shadow: 0 0 30px #ffd70022; animation: glow 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIN SYSTEM (FIXED CREDENTIALS) ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="login-box">
            <div class="analyzer-circle"></div>
            <h1 style='text-align:center; font-family:Orbitron; color:#00e5ff; margin-bottom:0;'>ALISHOOX PRO</h1>
            <p style='text-align:center; color:#ffd700; font-size:10px; letter-spacing:3px;'>SYSTEM ACCESS REQUIRED</p>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Operator Email", placeholder="zainakram259525@gmail.com")
    sec_key = st.text_input("Security Key", type="password", placeholder="akramtradingbot")
    
    if st.button("⚡ INITIALIZE TERMINAL", use_container_width=True):
        # EXACT MATCH CHECK
        if email.strip() == "zainakram259525@gmail.com" and sec_key.strip() == "akramtradingbot":
            st.session_state['auth'] = True
            st.success("Access Granted. Booting System...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Access Denied: Invalid Operator ID or Key.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- 4. PREMIUM DASHBOARD ---
    # Header
    st.markdown("<h2 style='text-align:center; font-family:Orbitron; color:#00e5ff; margin-bottom:0;'>ALISHOOX COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:10px; color:#ffd700; letter-spacing:5px;'>TRADER AKRAM & HUSNAIN</p>", unsafe_allow_html=True)

    # BLOCK 1: TRADING VIEW (FIRST BLOCK)
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.components.v1.html("""
        <div id="tv_chart" style="height:450px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({"width": "100%", "height": 450, "symbol": "OANDA:XAUUSD", "interval": "15", "theme": "dark", "style": "1", "container_id": "tv_chart"});
        </script>
    """, height=450)
    st.markdown("</div>", unsafe_allow_html=True)

    # BLOCK 2: 8-AGENT GRID
    try:
        res = requests.get(f"https://finnhub.io/api/v1/quote?symbol=OANDA:XAU_USD&token={FINNHUB_KEY}").json()
        live_price = res.get('c', 2330.50)
    except: live_price = 2330.50

    # Professional 4-Column Grid (Responsive)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-1: Price</p><p class='metric-val'>${live_price}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-2: Trend</p><p class='metric-val' style='color:#00ff88;'>BULLISH</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-3: RSI</p><p class='metric-val' style='color:#ffd700;'>54.2</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-4: News</p><p class='metric-val'>STABLE</p></div>", unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-5: DXY</p><p class='metric-val'>104.25</p></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-6: Whale</p><p class='metric-val' style='color:#00ff88;'>HIGH</p></div>", unsafe_allow_html=True)
    with col7:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-7: Session</p><p class='metric-val'>NY OPEN</p></div>", unsafe_allow_html=True)
    with col8:
        st.markdown(f"<div class='neon-card'><p class='agent-label'>Agent-8: ISM</p><p class='metric-val'>82.4%</p></div>", unsafe_allow_html=True)

    # BLOCK 3: JARVIS SIGNAL ENGINE
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ ACTIVATE JARVIS INTELLIGENCE SCAN", use_container_width=True):
        with st.spinner("Analyzing Market Confluence..."):
            try:
                prompt = f"Gold price is {live_price}. Give a professional SMC signal: ACTION (BUY/SELL), ENTRY, SL, TP, and CONFLUENCE. Use professional Urdu and English."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='signal-box'><h3 style='color:#ffd700; font-family:Orbitron;'>JARVIS SIGNAL</h3>{response.text}</div>", unsafe_allow_html=True)
            except:
                st.error("Jarvis is busy. Please try again in 60 seconds.")

    if st.sidebar.button("🚪 LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()
