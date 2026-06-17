import streamlit as st
import google.generativeai as genai
import requests
import os
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & SECRETS ---
st.set_page_config(page_title="AlishooX Pro Terminal", layout="wide")
st_autorefresh(interval=30 * 1000, key="data_sync")

try:
    FINNHUB_KEY = st.secrets["FINNHUB_API_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ API Keys Missing in Streamlit Secrets!")

# --- 2. FUTURISTIC CSS ---
st.markdown("""
<style>
    .stApp { background-color: #050508; color: #e0e0f0; }
    .neon-card {
        border: 1px solid #00e5ff33; border-radius: 12px; padding: 15px;
        background: rgba(13, 13, 20, 0.7); box-shadow: 0 0 10px #00e5ff11;
        margin-bottom: 10px; text-align: center;
    }
    .agent-label { color: #00e5ff; font-size: 0.7rem; font-weight: bold; letter-spacing: 1px; }
    .metric-val { font-size: 1.3rem; font-weight: bold; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIN ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown("<h1 style='text-align:center; color:#00e5ff;'>⚡ AlishooX PRO</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("Email")
        key = st.text_input("Security Key", type="password")
        if st.button("LAUNCH TERMINAL"):
            if email == "zainakram259525@gmail.com" and key == "akramtradingbot":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Access Denied")
else:
    # --- 4. DASHBOARD ---
    st.markdown("<h2 style='text-align:center; color:#00e5ff; margin-bottom:0;'>ALISHOOX COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:10px;'>BY TRADER AKRAM & HUSNAIN</p>", unsafe_allow_html=True)

    # TRADING VIEW
    st.components.v1.html("""
        <div id="tv" style="height:400px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({"width": "100%", "height": 400, "symbol": "OANDA:XAUUSD", "interval": "15", "theme": "dark", "container_id": "tv"});
        </script>
    """, height=400)

    # 8 AGENTS
    res = requests.get(f"https://finnhub.io/api/v1/quote?symbol=OANDA:XAU_USD&token={FINNHUB_KEY}").json()
    price = res.get('c', 2325.00)
    
    # 2 Rows of 4 Agents
    for row in [range(1,5), range(5,9)]:
        cols = st.columns(4)
        for i, col in enumerate(cols):
            agent_idx = row[i]
            with col:
                val = f"${price}" if agent_idx == 1 else "BULLISH" if agent_idx == 2 else "54.2" if agent_idx == 3 else "STABLE"
                if agent_idx > 4: val = "104.2" if agent_idx == 5 else "HIGH" if agent_idx == 6 else "NY OPEN" if agent_idx == 7 else "0.05"
                st.markdown(f"<div class='neon-card'><p class='agent-label'>AGENT-{agent_idx}</p><p class='metric-val'>{val}</p></div>", unsafe_allow_html=True)

    # JARVIS SIGNAL
    st.divider()
    if st.button("⚡ ACTIVATE JARVIS SCAN", use_container_width=True):
        with st.spinner("Analyzing..."):
            prompt = f"Gold price is {price}. Give professional SMC signal: ACTION, ENTRY, SL, TP. Professional Urdu/English."
            response = model.generate_content(prompt)
            st.markdown(f"<div style='border:2px solid #ffd700; padding:15px; border-radius:10px;'>{response.text}</div>", unsafe_allow_html=True)

    if st.sidebar.button("LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()
