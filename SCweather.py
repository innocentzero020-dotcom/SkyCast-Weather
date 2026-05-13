import streamlit as st
import requests
import pycountry
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="SkyCast Weather",
    page_icon="🌤️",
    layout="centered"
)

# --- Custom CSS for Image Background ---
bg_image_url = "https://images.unsplash.com/photo-1592210454359-9043f067919b?q=80&w=1920&auto=format&fit=crop"

st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.70), rgba(0, 0, 0, 0.70)),
                          url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"], [data-testid="stMainViewContainer"] {{
        background-color: transparent !important;
    }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.20);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 25px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }}

    .stTextInput input {{
        background: rgba(255, 255, 255, 0.12) !important;
        color: black !important;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.30) !important;
    }}

    .stTextInput label {{
        color: white !important;
        font-weight: 600;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.20);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.30);
        font-weight: bold;
        padding: 0.6rem 1rem;
    }}

    h1, h2, h3, p, span, .stMarkdown {{
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

def get_country_name(country_code: str) -> str:
    """Convert 2-letter country code to full country name."""
    if not country_code:
        return "Unknown"
    country = pycountry.countries.get(alpha_2=country_code.upper())
    if country:
        return country.name
    return country_code.upper()

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🌤️ SkyCast Weather</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Live weather updates from around the world</p>",
    unsafe_allow_html=True
)

# --- Input Area ---
city = st.text_input(
    "Enter city name:",
    placeholder="e.g. Karachi or Karachi, PK"
)

api_key = st.secrets["OPENWEATHER_API_KEY"]

if st.button("Get Weather"):
    if not city.strip():
        st.warning("Please enter a city name first! 😊")
    else:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city.strip(),
            "appid": api_key,
            "units": "metric"
        }

        try:
            with st.spinner("Fetching weather data..."):
                response = requests.get(url, params=params, timeout=10)
                data = response.json()

            if response.status_code == 200:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"].capitalize()
                icon = data["weather"][0]["icon"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                city_name = data.get("name", "Unknown City")
                country_code = data.get("sys", {}).get("country", "")
                country_name = get_country_name(country_code)

                st.markdown(f"""
                <div class="glass-card">
                    <h2 style="margin: 0;">📍 {city_name}, {country_name}</h2>
                    <img src="https://openweathermap.org/img/wn/{icon}@4x.png" width="150">
                    <h1 style="font-size: 60px; margin: 0;">{temp}°C</h1>
                    <p style="font-size: 20px;"><b>{desc}</b></p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        f"<div class='glass-card'>💧 Humidity<br>{humidity}%</div>",
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f"<div class='glass-card'>💨 Wind<br>{wind_speed} m/s</div>",
                        unsafe_allow_html=True
                    )

            else:
                message = data.get("message", "City not found.")
                st.error(f"City not found. {message.capitalize()}")

        except requests.exceptions.RequestException:
            st.error("Network error. Please check your internet connection.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# --- Footer ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}")
