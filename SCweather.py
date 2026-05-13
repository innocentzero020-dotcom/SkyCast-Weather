import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# --- Mobile Optimized Video Background ---
video_url = "https://static.videezy.com/system/resources/previews/000/042/301/original/Clouds_6_-_15s_-_4k_res.mp4"

st.markdown(f"""
    <style>
    /* 1. Sab layers ko transparent karein taake video nazar aaye */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"] {{
        background-color: transparent !important;
    }}

    /* 2. Video ki fixed position */
    #myVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -2;
        object-fit: cover;
    }}

    /* 3. Overlay Darkness (0.7) */
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
    }}

    /* 4. Glass Cards (Mobile Responsive) */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 20px;
        color: white;
        margin-bottom: 15px;
        text-align: center;
        width: 100%;
    }}

    /* Input box aur button ko behtar dikhane ke liye */
    .stTextInput input {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }}

    h1, h2, h3, p, span, label {{
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    </style>

    <video autoplay muted loop playsinline id="myVideo">
        <source src="{video_url}" type="video/mp4">
    </video>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- App Content ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🌤️ SkyCast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8;'>Live Weather Updates</p>", unsafe_allow_html=True)

# Input
city = st.text_input("", placeholder="Enter city name (e.g. Karachi)")
api_key = st.secrets["OPENWEATHER_API_KEY"]

if st.button("Mausam Maloom Karein"):
    if city:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description'].capitalize()
                icon = data['weather'][0]['icon']
                
                # Main Result Card
                st.markdown(f"""
                <div class="glass-card">
                    <h2 style='margin:0;'>📍 {data['name']}</h2>
                    <img src="http://openweathermap.org/img/wn/{icon}@4x.png" width="100">
                    <h1 style='font-size: 50px; margin:0;'>{temp}°C</h1>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Secondary Stats
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"<div class='glass-card'>💧 Humidity<br>{data['main']['humidity']}%</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div class='glass-card'>💨 Wind<br>{data['wind']['speed']} m/s</div>", unsafe_allow_html=True)
            else:
                st.error("Shehar nahi mila!")
        except:
            st.error("Connection error!")
