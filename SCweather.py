import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# --- Custom CSS for Image Background ---
# Maine ek behtareen clouds wali image select ki hai (Unsplash se)
bg_image_url = "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920"

# --- CSS Update for Input Visibility ---
st.markdown("""
    <style>
    /* Input box ke andar ka text (Jo user type karega) */
    .stTextInput input {
        color: #FFFFFF !important; /* Likhaai ka rang bilkul safaid */
        background: rgba(255, 255, 255, 0.2) !important; /* Box thoda sa transparent white */
        caret-color: white !important; /* Cursor ka rang */
    }

    /* Placeholder text ka rang (e.g. "Enter city name") */
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important; /* Halka safaid taake farq nazar aaye */
    }

    /* Input box ke upar ka label (Shehar ka naam likhein) */
    .stTextInput label {
        color: white !important;
        font-weight: bold;
        text-shadow: 1px 1px 2px black; /* Label ke piche halka sa saya taake saaf dikhe */
    }
    
    /* Input box focus hone par border ka rang */
    .stTextInput input:focus {
        border: 1px solid #007bff !important;
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🌤️ SkyCast Weather</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Duniya bhar ke mausam ki live updates</p>", unsafe_allow_html=True)

# --- Input Area ---
city = st.text_input("Shehar ka naam likhein:", placeholder="e.g. Karachi, London")
api_key = st.secrets["OPENWEATHER_API_KEY"]

if st.button("Mausam Maloom Karein"):
    if not city:
        st.warning("Pehle shehar ka naam toh likhein! 😊")
    else:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': api_key, 'units': 'metric'}

        try:
            with st.spinner('Data aa raha hai...'):
                response = requests.get(url, params=params)
                data = response.json()

            if response.status_code == 200:
                # Data Extraction
                temp = data['main']['temp']
                desc = data['weather'][0]['description'].capitalize()
                icon = data['weather'][0]['icon']
                
                # --- Results (Glass Card) ---
                st.markdown(f"""
                <div class="glass-card">
                    <h2 style='margin:0;'>📍 {data['name']}</h2>
                    <img src="http://openweathermap.org/img/wn/{icon}@4x.png" width="150">
                    <h1 style='font-size: 60px; margin:0;'>{temp}°C</h1>
                    <p style='font-size: 20px;'><b>{desc}</b></p>
                </div>
                """, unsafe_allow_html=True)

                # Small Stats Cards
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div class='glass-card'>💧 Humidity<br>{data['main']['humidity']}%</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='glass-card'>💨 Wind<br>{data['wind']['speed']} m/s</div>", unsafe_allow_html=True)

            else:
                st.error("Shehar nahi mila. Spelling check karein!")

        except:
            st.error("Internet connection ka masla hai.")

# --- Footer ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}")
