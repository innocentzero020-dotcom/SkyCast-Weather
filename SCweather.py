import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# --- Custom CSS for Image Background ---
# Maine ek behtareen clouds wali image select ki hai (Unsplash se)
bg_image_url = "https://images.unsplash.com/photo-1592210454359-9043f067919b?q=80&w=1920&auto=format&fit=crop"

st.markdown(f"""
    <style>
    /* 1. Pure app structure par background image aur darkness overlay set karein */
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                          url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed; /* Background ko stick rakhta hai */
    }}

    /* 2. Streamlit ke internal containers ko transparent karein mobile ke liye */
    [data-testid="stHeader"], [data-testid="stMainViewContainer"] {{
        background-color: transparent !important;
    }}

    /* 3. Glass Cards Styling (Same as before) */
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

    /* Input elements style update for image background */
    .stTextInput input {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    ```
    ```
    }}
    .stTextInput label {{
        color: white !important;
    }}

    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-weight: bold;
    }}

    /* Text color fixes */
    h1, h2, h3, p, span, .stMarkdown {{
        color: white !important;
    }}
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
