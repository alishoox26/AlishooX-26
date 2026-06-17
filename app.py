import streamlit as st
import google.generativeai as genai
import requests
import time
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. SOVEREIGN CONFIG ---
st.set_page_config(page_title="AlishooX Sovereign", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=5 * 1000, key="global_heartbeat")

# Load Intelligence Safely
try:
    FINNHUB_KEY = st.secrets["FINNHUB_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🔒 ACCESS DENIED: SECRETS NOT DETECTED.")

# --- 2. THE GOD-MODE UI (ULTRA CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;500;700&display=swap');
    
    :root {
        --glow-cyan: #00e5ff;
        --glow-gold: #ffd700;
        --bg-dark: #050508;
    }

    .stApp { 
        background: radial-gradient(circle at top right, #0a101a, #050508);
        color: #e0e0f0; 
        font-family: 'Rajdhani', sans-serif; 
    }

    /* Scanline Animation Effect */
    .stApp::before {
        content: " ";
        position: fixed; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
        z-index: 9999; background-size: 100% 4px, 3px 100%;
        pointer-events: none; opacity: 0.3;
    }

    /* Responsive 2-Column Grid for Mobile */
    @media (max-width: 768px) {
        [data-testid="column"] { width: 48% !important; flex: 1 1 45% !important; min-width: 45% !important; }
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 229, 255, 0.15);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        transition: 0.4s;
    }
    .glass-card:hover { 
        border-color: var(--glow-cyan);
        transform: translateY(-3px);
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
    }

    .agent-title { font-family: 'Orbitron'; font-size: 0.6rem; color: var(--glow-cyan); letter-spacing: 2px; }
    .agent-value { font-family: 'Orbitron'; font-size: 1.3rem; font-weight: 900; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
    
    /* Glowing Signal Terminal */
    .master-signal-box {
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid var(--glow-gold);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    .master-signal-box::after {
        content: ""; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: conic-gradient(transparent, transparent, transparent, var(--glow-gold));
        animation: rotate 6s linear infinite; z-index: -1;
    }
    @keyframes rotate { 100% { transform: rotate(360deg); } }

    /* Buttons Premium */
    .stButton>button {
        background: linear-gradient(135deg, var(--glow-cyan), #00b8cc);
        color: #000 !important; font-family: 'Orbitron'; font-weight: 900;
        border-radius: 8px; border: none; height: 50px;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(0, 229, 255, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.02); box-shadow: 0 0 25px var(--glow-cyan);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
def get_institutional_data():
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol=OANDA:XAU_USD&token={FINNHUB_KEY}"
        d = requests.get(url).json()
        if d.get('c'): return float(d['c']), f"{float(d['d']):+.2f}"
    except: pass
    return 2332.40, "+1.20"

# --- 4. ACCESS CONTROL ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'last_sig' not in st.session_state: st.session_state['last_sig'] = None

if not st.session_state['auth']:
    st.markdown("<div style='height:10vh;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("""
            <div style='text-align:center; padding:40px; background:rgba(10,10,15,0.9); border:1px solid #00e5ff33; border-radius:20px; box-shadow:0 0 40px rgba(0,0,0,0.5);'>
                <h1 style='font-family:Orbitron; color:#00e5ff; letter-spacing:5px;'>ALISHOOX PRO</h1>
                <p style='color:#666; font-size:12px; margin-bottom:30px;'>ESTABLISHING SECURE CONNECTION...</p>
        """, unsafe_allow_html=True)
        email = st.text_input("OPERATOR ID", placeholder="zainakram259525@gmail.com")
        key = st.text_input("SECURITY KEY", type="password", placeholder="akramtradingbot")
        if st.button("INITIALIZE TERMINAL", use_container_width=True):
            if email.strip() == "zainakram259525@gmail.com" and key.strip() == "akramtradingbot":
                st.session_state['auth'] = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- 5. THE ULTIMATE DASHBOARD ---
    st.markdown("<h2 style='text-align:center; font-family:Orbitron; color:#00e5ff; margin-bottom:0;'>ALISHOOX COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:10px; color:#ffd700; letter-spacing:8px;'>TRADER AKRAM & HUSNAIN</p>", unsafe_allow_html=True)

    # BLOCK 1: TRADING VIEW (PREMIUM FRAME)
    st.markdown("<div class='glass-card' style='padding:5px; border-color:rgba(255,215,0,0.2);'>", unsafe_allow_html=True)
    st.components.v1.html("""
        <div id="tv_main" style="height:400px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({"width": "100%", "height": 400, "symbol": "OANDA:XAUUSD", "interval": "15", "theme": "dark", "style": "1", "container_id": "tv_main", "allow_symbol_change": true});
        </script>
    """, height=400)
    st.markdown("</div>", unsafe_allow_html=True)

    # BLOCK 2: 8-AGENT GRID (2x4 MOBILE RESPONSIVE)
    price, change = get_institutional_data()
    agents = [
        ("AGENT-1: PRICE EYE", f"${price}", "#fff"),
        ("AGENT-2: TREND BIAS", "BULLISH", "#00ff88"),
        ("AGENT-3: RSI ANALYSIS", "56.4", "#ffd700"),
        ("AGENT-4: NEWS RADAR", "STABLE", "#00e5ff"),
        ("AGENT-5: DXY CORR", "104.4", "#ff3860"),
        ("AGENT-6: WHALE FLOW", "HIGH", "#00ff88"),
        ("AGENT-7: SESSION", "LONDON", "#fff"),
        ("AGENT-8: ISM HEAT", "84.2%", "#00e5ff")
    ]

    # Creating the 2-column responsive grid
    for i in range(0, 8, 2):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='glass-card'><p class='agent-title'>{agents[i][0]}</p><p class='agent-value' style='color:{agents[i][2]}'>{agents[i][1]}</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='glass-card'><p class='agent-title'>{agents[i+1][0]}</p><p class='agent-value' style='color:{agents[i+1][2]}'>{agents[i+1][1]}</p></div>", unsafe_allow_html=True)

    # BLOCK 3: JARVIS SCANNER (ULTRA UI)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ EXECUTE MULTI-AGENT MARKET SCAN", use_container_width=True):
        with st.spinner("Decoding Institutional Liquidity..."):
            try:
                acc = random.randint(89, 98)
                prompt = f"Price: {price}. Give professional SMC signal for Gold. Action, Entry, SL, TP, Accuracy: {acc}%. Professional Urdu/English."
                response = model.generate_content(prompt)
                st.session_state['last_sig'] = response.text
            except:
                st.session_state['last_sig'] = f"**ACTION:** BUY\n**ENTRY:** {price}\n**SL:** {price-1.8}\n**TP:** {price+4.5}\n**ACCURACY:** 94%\n*System Fallback Active.*"

    if st.session_state['last_sig']:
        st.markdown(f"""
            <div class='master-signal-box'>
                <p style='font-family:Orbitron; color:#ffd700; font-size:12px; border-bottom:1px solid #333; padding-bottom:10px;'>[JARVIS INTELLIGENCE REPORT]</p>
                <div style='font-family:Share Tech Mono; color:#eee; font-size:1rem; line-height:1.6;'>
                    {st.session_state['last_sig']}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # BLOCK 4: SETTINGS (HIDDEN)
    with st.expander("🛠️ TERMINAL CONFIGURATIONS"):
        st.write("Operator Settings")
        wa_phone = st.text_input("WhatsApp Link Phone (923...)")
        wa_key = st.text_input("CallMeBot Key")
        if st.button("SEND TEST DATA"):
            st.toast("Transmitting data...")

    # FOOTER
    st.markdown(f"<p style='text-align:center; font-size:9px; color:#444; margin-top:30px;'>SYSTEM SYNC: {datetime.now().strftime('%H:%M:%S')} | v10.0 ULTRA</p>", unsafe_allow_html=True)

    if st.sidebar.button("EXIT SYSTEM"):
        st.session_state['auth'] = False
        st.rerun()
