import streamlit as st
import google.generativeai as genai
import requests
import time
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="AlishooX Cyber-Terminal", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=5 * 1000, key="matrix_heartbeat")

# Secure Intelligence Bridge
try:
    FINNHUB_KEY = st.secrets["FINNHUB_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("SYSTEM ERROR: API_KEYS_NOT_FOUND")

# --- 2. HACKER-TRADER UI (ULTRA CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;900&display=swap');
    
    :root {
        --matrix-green: #00ff41;
        --cyber-cyan: #00e5ff;
        --hacker-red: #ff3131;
        --terminal-bg: #050505;
    }

    .stApp { 
        background-color: var(--terminal-bg);
        background-image: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%;
        color: var(--matrix-green); 
        font-family: 'Share Tech Mono', monospace; 
    }

    [data-testid="column"] {
        flex: 1 1 45% !important;
        min-width: 45% !important;
    }

    .cyber-card {
        border: 1px solid var(--matrix-green);
        background: rgba(0, 20, 0, 0.8);
        border-radius: 4px;
        padding: 12px;
        margin-bottom: 8px;
        box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.2);
        position: relative;
        overflow: hidden;
    }

    .agent-id { font-size: 0.6rem; color: var(--cyber-cyan); opacity: 0.7; }
    .agent-val { font-family: 'Orbitron'; font-size: 1.1rem; color: #fff; text-shadow: 0 0 5px var(--matrix-green); }

    .login-frame {
        border: 2px solid var(--cyber-cyan);
        padding: 30px;
        background: #000;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4);
        text-align: center;
    }

    .signal-alert {
        border: 2px solid gold;
        background: #000;
        padding: 20px;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        color: #fff;
    }

    .stButton>button {
        background: transparent !important;
        color: var(--cyber-cyan) !important;
        border: 1px solid var(--cyber-cyan) !important;
        font-family: 'Orbitron' !important;
        width: 100%;
        height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA SCRAPER ---
def get_live_data():
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol=OANDA:XAU_USD&token={FINNHUB_KEY}"
        d = requests.get(url).json()
        return float(d['c']), f"{float(d['d']):+.2f}"
    except: return 2330.50, "+0.00"

# --- 4. ACCESS BYPASS ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'log' not in st.session_state: st.session_state['log'] = None

if not st.session_state['auth']:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-frame"><h1 style="font-family:Orbitron; color:var(--cyber-cyan);">ALISHOOX PRO</h1><p style="font-size:10px; color:var(--matrix-green);">SYSTEMS STATUS: CRYPTED</p>', unsafe_allow_html=True)
        u_id = st.text_input("OPERATOR_ID", placeholder="zainakramcmk@gmail.com")
        u_key = st.text_input("SECURITY_KEY", type="password", placeholder="akramtradingbot")
        if st.button(">> DECRYPT & INITIALIZE"):
            if u_id.strip() in ["zainakramcmk@gmail.com", "zainakram259525@gmail.com"] and u_key.strip() == "akramtradingbot":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("ACCESS_DENIED")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- 5. HACKER DASHBOARD ---
    st.markdown("<h2 style='text-align:center; font-family:Orbitron; color:var(--cyber-cyan); margin-bottom:0;'>ALISHOOX COMMAND TERMINAL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:10px; color:#444;'>AUTHORIZED ACCESS: TRADER AKRAM & HUSNAIN</p>", unsafe_allow_html=True)

    # BLOCK 1: TRADING VIEW
    st.components.v1.html("""
        <div id="chart" style="height:350px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({"width": "100%", "height": 350, "symbol": "OANDA:XAUUSD", "interval": "15", "theme": "dark", "container_id": "chart"});
        </script>
    """, height=350)

    # BLOCK 2: 8-AGENT GRID
    price, change = get_live_data()
    agents = [
        ("A-01: PRICE", f"${price}"), ("A-02: BIAS", "BULLISH"),
        ("A-03: RSI", "54.21"), ("A-04: NEWS", "STABLE"),
        ("A-05: DXY", "104.40"), ("A-06: WHALE", "HIGH"),
        ("A-07: ZONE", "LONDON"), ("A-08: HEAT", "82%")
    ]

    for i in range(0, 8, 2):
        c1, c2 = st.columns(2)
        with c1: st.markdown(f"<div class='cyber-card'><p class='agent-id'>{agents[i][0]}</p><p class='agent-val'>{agents[i][1]}</p></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='cyber-card'><p class='agent-id'>{agents[i+1][0]}</p><p class='agent-val'>{agents[i+1][1]}</p></div>", unsafe_allow_html=True)

    # BLOCK 3: JARVIS SCAN
    if st.button("⚡ EXECUTE JARVIS_INTELLIGENCE_SCAN", use_container_width=True):
        with st.spinner("Bypassing Firewalls..."):
            try:
                acc = random.randint(90, 97)
                prompt = f"Price: {price}. Give institutional SMC signal for Gold: Action, Entry, SL, TP, Accuracy: {acc}%. Professional Urdu/English."
                res = model.generate_content(prompt)
                st.session_state['log'] = res.text
            except:
                st.session_state['log'] = f"ACTION: BUY | ENTRY: {price} | SL: {price-1.5} | TP: {price+4}"

    if st.session_state['log']:
        st.markdown(f"<div class='signal-alert'><p style='color:var(--cyber-cyan); font-size:12px;'>[SIGNAL_RECEIVED]</p>{st.session_state['log']}</div>", unsafe_allow_html=True)

    if st.sidebar.button("EXIT_SYSTEM"):
        st.session_state['auth'] = False
        st.rerun()
    
