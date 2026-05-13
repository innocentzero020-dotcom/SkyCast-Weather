import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# --- Fixed Video Background Code ---
# Agar ye link na chale toh aap pexels.com se koi bhi mp4 link le sakte hain
video_url = "https://static.videezy.com/system/resources/previews/000/042/301/original/Clouds_6_-_15s_-_4k_res.mp4"

st.markdown(f"""
    <style>
    /* 1. Streamlit ke default background ko khatam karne ke liye */
    .stApp {{
        background: transparent;
    }}

    /* 2. Video ki settings */
    #myVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -2;
        object-fit: cover;
    }}

    /* 3. Darkness Overlay (0.7) */
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
    }}

    /* 4. Glass Cards Styling */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }}

    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    h1, p, span, label, .stMarkdown {{
        color: white !important;
    }}
    </style>

    <video autoplay muted loop playsinline id="myVideo">
        <source src="{video_url}" type="video/mp4">
        Your browser does not support HTML5 video.
    </video>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🌤️ SkyCast Weather</h1>", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("Settings")
unit = st.sidebar.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"])
u_param = "metric" if unit == "Celsius" else "imperial"

# --- Input Area ---
city = st.text_input("Shehar ka naam likhein:", placeholder="e.g. Karachi, London")
api_key = st.secrets["OPENWEATHER_API_KEY"]

if st.button("Mausam Maloom Karein"):
    if not city:
        st.warning("Pehle shehar ka naam toh likhein! 😊")
    else:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': api_key, 'units': u_param}

        try:
            with st.spinner('Data aa raha hai...'):
                response = requests.get(url, params=params)
                data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description'].capitalize()
                icon = data['weather'][0]['icon']
                
                # Result Card
                st.markdown(f"""
                <div class="glass-card">
                    <h2 style='margin:0;'>📍 {data['name']}</h2>
                    <img src="http://openweathermap.org/img/wn/{icon}@4x.png" width="120">
                    <h1 style='font-size: 55px; margin:0;'>{temp}°{'C' if unit=='Celsius' else 'F'}</h1>
                    <p style='font-size: 18px;'>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

                # Small Cards
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div class='glass-card'>💧 Humidity<br>{data['main']['humidity']}%</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='glass-card'>💨 Wind<br>{data['wind']['speed']} m/s</div>", unsafe_allow_html=True)

            else:
                st.error("Shehar nahi mila!")
        except:
            st.error("Connection error!")

st.caption(f"Last updated: {datetime.now().strftime('%I:%M %p')}")
