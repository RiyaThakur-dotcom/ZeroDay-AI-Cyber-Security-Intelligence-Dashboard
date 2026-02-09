import streamlit as st
import requests
import random
import time
import pandas as pd
import pydeck as pdk
import pyttsx3
from streamlit_autorefresh import st_autorefresh

# ================= CONFIG =================
API_KEY = "AIzaSyBVhwaLirG2jv4VYUDe9HntioVbig4RZ3M"  

# ================= GEMINI FUNCTIONS =================
def ask_gemini(prompt):
    """Real Gemini API call with error handling"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents":[{"parts":[{"text": prompt}]}]}
    
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        r.raise_for_status()
        result = r.json()

        candidates = result.get("candidates")
        if not candidates:
            return f"❌ Error: No candidates returned. Response: {result}"

        content_parts = candidates[0].get("content", {}).get("parts")
        if not content_parts:
            return f"❌ Error: No content parts found. Response: {result}"

        return content_parts[0].get("text", "❌ No text returned")
    
    except requests.exceptions.HTTPError as e:
        if r.status_code == 429:
            return "❌ Error: Rate limit exceeded. Try again in a few minutes."
        return f"❌ Error: HTTP request failed. {e}"
    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. Check your network."
    except requests.exceptions.RequestException as e:
        return f"❌ Error: HTTP request failed. {e}"
    except Exception as e:
        return f"❌ Error: Unexpected issue. {e}"

@st.cache_data(ttl=60)
def ask_gemini_cached(prompt):
    """Cached Gemini API call to reduce repeated requests"""
    return ask_gemini(prompt)

def ask_gemini_mock(prompt):
    """Mock AI responses for demos"""
    if "password" in prompt.lower():
        return "[Mock AI] Your password is medium strength. Consider adding numbers, symbols, and mixed case."
    elif "phishing" in prompt.lower():
        return "[Mock AI] The message looks suspicious. Avoid clicking unknown links and verify the sender."
    elif "email" in prompt.lower():
        return "[Mock AI] This email has low risk of breach. Always enable 2FA and strong passwords."
    else:
        return f"[Mock AI] Response for: {prompt[:50]}..."

# ================= VOICE FUNCTION =================
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate',170)
    engine.say(text)
    engine.runAndWait()

# ================= PAGE CONFIG =================
st.set_page_config(page_title="ZeroDay AI", page_icon="💀", layout="wide")

# ================= DARK UI =================
st.markdown("""
<style>
body {background:#0e1117; color:white;}
h1,h2,h3 {color:#00ff99;}
.stButton>button {
 background:#111; color:#00ff99;
 border-radius:10px; height:3em; width:100%;
}
.stTextInput input,.stTextArea textarea{
 background:#111; color:#00ff99;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("💀 ZeroDay AI – Ultimate Cybersecurity Lab")
st.write("Think like hacker. Defend like pro.")
st.markdown("---")

# ================= TOGGLE: MOCK / REAL =================
use_mock = st.sidebar.checkbox("Use Mock AI (Demo Mode)", value=True)
st.sidebar.info("Toggle off to use real Gemini API with your API key")

# ================= SIDEBAR METRICS =================
st.sidebar.title("⚙ Cyber Command")
st.sidebar.metric("Live Attacks", random.randint(50,200))
st.sidebar.metric("Firewall", "Active 🟢")
st.sidebar.metric("AI Engine", "Online 🤖")

# ================= SESSION STATE INIT =================
for key in ["password_output","phishing_output","email_output","hackerchat_output"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ================= DASHBOARD =================
col1, col2, col3 = st.columns(3)

# ================= PASSWORD =================
with col1:
    st.subheader("🔐 Password Hacker Scan")
    pwd = st.text_input("Enter password", type="password", key="pwd_input")

    if st.button("Scan Password"):
        if pwd:
            with st.spinner("Scanning..."):
                score = random.randint(0,100)
                time.sleep(1)
                st.progress(score)
                if score>80: st.success("Strong Password")
                elif score>50: st.warning("Medium Password")
                else: st.error("Weak Password")

                prompt = f"Analyze password {pwd} strength, crack time, risks, improvement"
                if use_mock:
                    st.session_state.password_output = ask_gemini_mock(prompt)
                else:
                    st.session_state.password_output = ask_gemini_cached(prompt)
        else:
            st.warning("Enter password")

    if st.session_state.password_output:
        st.info(st.session_state.password_output)

# ================= PHISHING =================
with col2:
    st.subheader("📩 Phishing Detector")
    msg = st.text_area("Paste message", key="phishing_input")

    if st.button("Detect Phishing"):
        if msg:
            prob = random.randint(1,100)
            df = pd.DataFrame({
                "Type":["Phishing","Safe"],
                "Value":[prob, 100-prob]
            })
            st.bar_chart(df.set_index("Type"))

            prompt = f"Check phishing and give safety tips: {msg}"
            if use_mock:
                st.session_state.phishing_output = ask_gemini_mock(prompt)
            else:
                st.session_state.phishing_output = ask_gemini_cached(prompt)
        else:
            st.warning("Paste message")

    if st.session_state.phishing_output:
        st.info(st.session_state.phishing_output)

# ================= EMAIL =================
with col3:
    st.subheader("🌐 Email Breach Check")
    email = st.text_input("Enter email", key="email_input")

    if st.button("Check Email"):
        if email:
            risk = random.choice(["Low","Medium","High"])
            if risk=="Low": st.success("Low Risk")
            elif risk=="Medium": st.warning("Medium Risk")
            else: st.error("High Risk")

            prompt = f"Email {email} breach risks and protection"
            if use_mock:
                st.session_state.email_output = ask_gemini_mock(prompt)
            else:
                st.session_state.email_output = ask_gemini_cached(prompt)
        else:
            st.warning("Enter email")

    if st.session_state.email_output:
        st.info(st.session_state.email_output)

# ================= LIVE CYBER MAP =================
st.markdown("---")
st.subheader("🌍 LIVE Global Cyber Threat Map")
st_autorefresh(interval=3000, key="map_refresh")

cities=[
("Delhi",28.61,77.20),
("London",51.50,-0.12),
("Tokyo",35.68,139.69),
("New York",40.71,-74.00),
("Moscow",55.75,37.61),
("Dubai",25.20,55.27),
("Berlin",52.52,13.40),
("Sydney",-33.86,151.21)
]

data=[]
for c in cities:
    data.append([c[0], c[1], c[2], random.randint(30,100)])

df = pd.DataFrame(data, columns=["city","lat","lon","severity"])

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_fill_color='[255,0,0,severity*2]',
    get_radius='severity*1600',
    pickable=True
)

view = pdk.ViewState(latitude=20, longitude=0, zoom=1)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    tooltip={"text":"{city}\nThreat: {severity}%"}
)

st.pydeck_chart(deck)

# ================= HACKER AI (Text Only) =================
st.markdown("---")
st.subheader("🎤 Hacker AI (Text Only)")

voice_q = st.text_input("Ask something", key="hacker_input")

if st.button("Ask Hacker AI"):
    if voice_q:
        with st.spinner("AI thinking..."):
            prompt = f"Answer like ethical hacker with prevention tips: {voice_q}"
            
            # Mock AI for demo
            res = ask_gemini_mock(prompt)
            st.session_state.hackerchat_output = res
    else:
        st.warning("Ask a question")

if st.session_state.hackerchat_output:
    st.info(st.session_state.hackerchat_output)



# ================= FOOTER =================
st.markdown("---")
st.caption("💀 ZeroDay AI | Ultimate Hackathon Winner Build")



