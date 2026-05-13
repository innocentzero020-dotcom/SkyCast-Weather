import streamlit as st
import requests
import pycountry
from datetime import datetime, timedelta

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="SkyCast Weather",
    page_icon="🌤️",
    layout="centered"
)

# -------------------- Custom CSS --------------------
bg_image_url = "https://images.unsplash.com/photo-1592210454359-9043f067919b?q=80&w=1920&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image:
            linear-gradient(rgba(0, 0, 0, 0.72), rgba(0, 0, 0, 0.72)),
            url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"], [data-testid="stMainViewContainer"] {{
        background-color: transparent !important;
    }}

    .hero-card {{
        background: rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.35);
        color: white;
        text-align: center;
        margin-bottom: 18px;
    }}

    .info-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.25);
        color: white;
        text-align: center;
        height: 100%;
    }}

    .metric-label {{
        font-size: 14px;
        opacity: 0.85;
        margin-bottom: 6px;
    }}

    .metric-value {{
        font-size: 24px;
        font-weight: 700;
        line-height: 1.2;
    }}

    .subtle {{
        opacity: 0.8;
        font-size: 14px;
    }}

    .stTextInput label {{
        color: white !important;
        font-weight: 600;
    }}

    .stTextInput input {{
        background: rgba(255, 255, 255, 0.12) !important;
        color: black !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.28) !important;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.18);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.28);
        font-weight: 700;
        padding: 0.65rem 1rem;
    }}

    h1, h2, h3, p, span, .stMarkdown {{
        color: white !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Helpers --------------------
def get_country_name(country_code: str) -> str:
    if not country_code:
        return "Unknown"
    country = pycountry.countries.get(alpha_2=country_code.upper())
    return country.name if country else country_code.upper()

def format_local_time(unix_ts: int, timezone_offset: int) -> str:
    if not unix_ts:
        return "N/A"
    local_dt = datetime.utcfromtimestamp(unix_ts + timezone_offset)
    return local_dt.strftime("%I:%M %p")

def wind_direction(deg):
    if deg is None:
        return "N/A"
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    index = round(deg / 45) % 8
    return directions[index]

# -------------------- Header --------------------
st.markdown("<h1 style='text-align:center;'>🌤️ SkyCast Weather</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Live weather updates with detailed insights from around the world</p>",
    unsafe_allow_html=True
)

# -------------------- Input --------------------
with st.form("weather_form"):
    city = st.text_input(
        "Enter city name",
        placeholder="e.g. Karachi or Karachi, PK"
    )
    submitted = st.form_submit_button("Get Weather")

# -------------------- API Key --------------------
api_key = st.secrets["OPENWEATHER_API_KEY"]

# -------------------- Main Logic --------------------
if submitted:
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
                # Core data
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                temp_min = data["main"]["temp_min"]
                temp_max = data["main"]["temp_max"]
                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                visibility_km = data.get("visibility", 0) / 1000
                clouds = data.get("clouds", {}).get("all", 0)
                wind_speed = data.get("wind", {}).get("speed", 0)
                wind_deg = data.get("wind", {}).get("deg")
                desc = data["weather"][0]["description"].capitalize()
                icon = data["weather"][0]["icon"]

                # Location data
                city_name = data.get("name", "Unknown City")
                country_code = data.get("sys", {}).get("country", "")
                country_name = get_country_name(country_code)

                # Time data
                timezone_offset = data.get("timezone", 0)
                sunrise = format_local_time(data.get("sys", {}).get("sunrise"), timezone_offset)
                sunset = format_local_time(data.get("sys", {}).get("sunset"), timezone_offset)
                local_time = datetime.utcfromtimestamp(datetime.utcnow().timestamp() + timezone_offset).strftime("%I:%M %p")

                # Coordinates
                lat = data.get("coord", {}).get("lat", "N/A")
                lon = data.get("coord", {}).get("lon", "N/A")

                # -------------------- Hero Card --------------------
                st.markdown(f"""
                <div class="hero-card">
                    <h2 style="margin:0; font-size: 32px;">📍 {city_name}, {country_name}</h2>
                    <p class="subtle" style="margin-top: 8px;">{desc}</p>
                    <img src="https://openweathermap.org/img/wn/{icon}@4x.png" width="150">
                    <h1 style="font-size: 64px; margin: 0;">{temp}°C</h1>
                    <p style="font-size: 18px; margin-top: 8px;">
                        Feels like <b>{feels_like}°C</b> · High <b>{temp_max}°C</b> · Low <b>{temp_min}°C</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # -------------------- Main Details --------------------
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Humidity</div>
                        <div class="metric-value">{humidity}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Wind</div>
                        <div class="metric-value">{wind_speed} m/s</div>
                        <div class="subtle">Direction: {wind_direction(wind_deg)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col3, col4 = st.columns(2)

                with col3:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Pressure</div>
                        <div class="metric-value">{pressure} hPa</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Visibility</div>
                        <div class="metric-value">{visibility_km:.1f} km</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col5, col6 = st.columns(2)

                with col5:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Cloudiness</div>
                        <div class="metric-value">{clouds}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col6:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Local Time</div>
                        <div class="metric-value">{local_time}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # -------------------- Extra Info --------------------
                st.markdown("### Additional Information")
                extra_col1, extra_col2, extra_col3 = st.columns(3)

                with extra_col1:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Sunrise</div>
                        <div class="metric-value">{sunrise}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with extra_col2:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Sunset</div>
                        <div class="metric-value">{sunset}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with extra_col3:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">Coordinates</div>
                        <div class="metric-value">{lat}, {lon}</div>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                message = data.get("message", "City not found")
                st.error(f"City not found. {message.capitalize()}")

        except requests.exceptions.RequestException:
            st.error("Network error. Please check your internet connection.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# -------------------- Footer --------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}")
