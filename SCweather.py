import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# --- Custom CSS for "Liquid Glass" Look ---
# Yeh CSS wahi glassmorphism effect degi jo React component mein tha
st.markdown("""
    <style>
    .main {
        background: url("https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    .stApp {
        background: rgba(0, 0, 0, ;0.9 /* Background ko thoda dark karne ke liye */
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 25px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid white;
    }
    h1, p, span, label {
        color: white !important;
    }
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🌤️ SkyCast Weather</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Duniya bhar ke mausam ki live updates</p>", unsafe_allow_html=True)

# --- Sidebar (Settings) ---
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
                # Data Extraction
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind = data['wind']['speed']
                desc = data['weather'][0]['description'].capitalize()
                icon = data['weather'][0]['icon']
                
                sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
                sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')

                # --- Display Results in Glass Cards ---
                st.markdown(f"""
                <div class="glass-card">
                    <h2 style='margin:0;'>📍 {data['name']}, {data['sys']['country']}</h2>
                    <img src="http://openweathermap.org/img/wn/{icon}@4x.png" width="150">
                    <h1 style='font-size: 60px; margin:0;'>{temp}°{'C' if unit=='Celsius' else 'F'}</h1>
                    <p style='font-size: 20px;'><b>{desc}</b></p>
                    <p>Feels like: {feels_like}°</p>
                </div>
                """, unsafe_allow_html=True)

                # Stats Row
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div class='glass-card'>💧<br><b>Nami</b><br>{humidity}%</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='glass-card'>💨<br><b>Hawa</b><br>{wind} m/s</div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='glass-card'>🌡️<br><b>Pressure</b><br>{data['main']['pressure']}</div>", unsafe_allow_html=True)

                st.markdown(f"<div class='glass-card'>🌅 Sunrise: {sunrise} | 🌇 Sunset: {sunset}</div>", unsafe_allow_html=True)
                st.balloons()

            else:
                st.error("Shehar nahi mila. Spelling check karein!")

        except Exception as e:
            st.error("Internet connection ka masla hai.")

# --- Footer ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}")
