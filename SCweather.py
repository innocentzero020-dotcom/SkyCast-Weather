import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# --- Custom CSS & Video Background ---
# Maine ek cloud video ka link dala hai, aap isay badal bhi sakte hain
video_url = "https://assets.mixkit.co/videos/preview/mixkit-clouds-moving-fast-in-the-sky-31215-large.mp4"

st.markdown(f"""
    <style>
    /* Video ko poori screen par set karne ke liye */
    #myVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
    }}

    /* Darkness Overlay (Aapki pasand ke mutabiq 0.7 set kiya hai) */
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
    }}

    .glass-card {{
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
    }}

    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        font-weight: bold;
    }}

    h1, p, span, label {{
        color: white !important;
    }}
    </style>

    <video autoplay muted loop id="myVideo">
        <source src="{video_url}" type="video/mp4">
    </video>
    <div class="overlay"></div>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🌤️ SkyCast Weather</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Duniya bhar ke mausam ki live updates</p>", unsafe_allow_html=True)

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
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind = data['wind']['speed']
                desc = data['weather'][0]['description'].capitalize()
                icon = data['weather'][0]['icon']
                
                sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
                sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')

                # --- Results ---
                st.markdown(f"""
                <div class="glass-card">
                    <h2 style='margin:0;'>📍 {data['name']}, {data['sys']['country']}</h2>
                    <img src="http://openweathermap.org/img/wn/{icon}@4x.png" width="150">
                    <h1 style='font-size: 60px; margin:0;'>{temp}°{'C' if unit=='Celsius' else 'F'}</h1>
                    <p style='font-size: 20px;'><b>{desc}</b></p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div class='glass-card'>💧<br>{humidity}%</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='glass-card'>💨<br>{wind} m/s</div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='glass-card'>🌅<br>{sunrise}</div>", unsafe_allow_html=True)

            else:
                st.error("Shehar nahi mila!")
        except:
            st.error("Internet ka masla hai.")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}")
