import streamlit as st
import requests
import pycountry
from datetime import datetime
from pathlib import Path

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="SkyCast Weather",
    page_icon="🌤️",
    layout="centered"
)

# -------------------- CITY BACKGROUND SYSTEM --------------------
ASSETS_DIR = Path("assets")

CITY_BACKGROUNDS = {
    "karachi": str(ASSETS_DIR / "karachi.jpg"),
    "lahore": str(ASSETS_DIR / "lahore.jpg"),
    "islamabad": str(ASSETS_DIR / "islamabad.jpg"),
    "peshawar": str(ASSETS_DIR / "peshawar.jpg"),
    "quetta": str(ASSETS_DIR / "quetta.jpg"),
    "multan": str(ASSETS_DIR / "multan.jpg"),
}

DEFAULT_BACKGROUND = str(ASSETS_DIR / "default.jpg")


def get_background_for_city(city_name: str) -> str:
    if not city_name:
        return DEFAULT_BACKGROUND

    city_lower = city_name.strip().lower()

    for key, image_path in CITY_BACKGROUNDS.items():
        if key in city_lower:
            return image_path

    return DEFAULT_BACKGROUND


# -------------------- INPUT --------------------
city = st.text_input(
    "Enter city name",
    placeholder="e.g. Karachi or Karachi, PK"
)

# -------------------- DYNAMIC BACKGROUND --------------------
bg_image_url = get_background_for_city(city)

# -------------------- CUSTOM CSS --------------------
st.markdown(
    f"""
    <style>

    [data-testid="stAppViewContainer"] {{
        background-image:
            linear-gradient(rgba(0, 0, 0, 0.72), rgba(0, 0, 0, 0.72)),
            url("{bg_image_url}");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"],
    [data-testid="stMainViewContainer"] {{
        background-color: transparent !important;
    }}

    .hero-card {{
        background: rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);

        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.20);

        padding: 28px;
        margin-bottom: 20px;

        text-align: center;
        color: white;

        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    }}

    .info-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);

        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.16);

        padding: 20px;
        margin-bottom: 15px;

        text-align: center;
        color: white;

        box-shadow: 0 8px 28px rgba(0,0,0,0.25);
    }}

    .metric-label {{
        font-size: 14px;
        opacity: 0.85;
        margin-bottom: 6px;
    }}

    .metric-value {{
        font-size: 26px;
        font-weight: bold;
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
        color: white !important;

        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.25) !important;
    }}

    .stButton > button {{
        width: 100%;

        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.25);

        background: rgba(255,255,255,0.18);
        color: white;

        font-weight: bold;
        padding: 0.7rem 1rem;
    }}

    h1, h2, h3, p, span {{
        color: white !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- HELPERS --------------------
def get_country_name(country_code: str) -> str:
    if not country_code:
        return "Unknown"

    country = pycountry.countries.get(alpha_2=country_code.upper())

    if country:
        return country.name

    return country_code


def format_local_time(unix_ts: int, timezone_offset: int) -> str:
    local_dt = datetime.utcfromtimestamp(unix_ts + timezone_offset)
    return local_dt.strftime("%I:%M %p")


def get_wind_direction(deg):
    if deg is None:
        return "N/A"

    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(deg / 45) % 8

    return directions[index]


# -------------------- HEADER --------------------
st.markdown(
    "<h1 style='text-align:center;'>🌤️ SkyCast Weather</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Professional live weather insights from around the world</p>",
    unsafe_allow_html=True
)

# -------------------- API KEY --------------------
api_key = st.secrets["OPENWEATHER_API_KEY"]

# -------------------- BUTTON --------------------
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

                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                data = response.json()

            if response.status_code == 200:

                # -------------------- WEATHER DATA --------------------
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]

                temp_min = data["main"]["temp_min"]
                temp_max = data["main"]["temp_max"]

                humidity = data["main"]["humidity"]

                pressure = data["main"]["pressure"]

                visibility = data.get("visibility", 0) / 1000

                clouds = data.get("clouds", {}).get("all", 0)

                wind_speed = data.get("wind", {}).get("speed", 0)

                wind_deg = data.get("wind", {}).get("deg")

                description = data["weather"][0]["description"].capitalize()

                icon = data["weather"][0]["icon"]

                # -------------------- LOCATION --------------------
                city_name = data.get("name", "Unknown City")

                country_code = data.get("sys", {}).get("country", "")

                country_name = get_country_name(country_code)

                # -------------------- TIME DATA --------------------
                timezone_offset = data.get("timezone", 0)

                sunrise = format_local_time(
                    data["sys"]["sunrise"],
                    timezone_offset
                )

                sunset = format_local_time(
                    data["sys"]["sunset"],
                    timezone_offset
                )

                local_time = datetime.utcfromtimestamp(
                    datetime.utcnow().timestamp() + timezone_offset
                ).strftime("%I:%M %p")

                # -------------------- COORDINATES --------------------
                lat = data.get("coord", {}).get("lat", "N/A")

                lon = data.get("coord", {}).get("lon", "N/A")

                # -------------------- MAIN HERO CARD --------------------
                st.markdown(f"""
                <div class="hero-card">

                    <h2 style="margin:0;">
                        📍 {city_name}, {country_name}
                    </h2>

                    <p class="subtle">
                        {description}
                    </p>

                    <img src="https://openweathermap.org/img/wn/{icon}@4x.png" width="150">

                    <h1 style="font-size:64px; margin:0;">
                        {temp}°C
                    </h1>

                    <p style="font-size:18px;">
                        Feels like <b>{feels_like}°C</b>
                    </p>

                    <p class="subtle">
                        High: {temp_max}°C • Low: {temp_min}°C
                    </p>

                </div>
                """, unsafe_allow_html=True)

                # -------------------- WEATHER DETAILS --------------------
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            💧 Humidity
                        </div>

                        <div class="metric-value">
                            {humidity}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            💨 Wind
                        </div>

                        <div class="metric-value">
                            {wind_speed} m/s
                        </div>

                        <div class="subtle">
                            {get_wind_direction(wind_deg)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # -------------------- SECOND ROW --------------------
                col3, col4 = st.columns(2)

                with col3:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            🌡️ Pressure
                        </div>

                        <div class="metric-value">
                            {pressure} hPa
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            👀 Visibility
                        </div>

                        <div class="metric-value">
                            {visibility:.1f} km
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # -------------------- THIRD ROW --------------------
                col5, col6 = st.columns(2)

                with col5:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            ☁️ Cloudiness
                        </div>

                        <div class="metric-value">
                            {clouds}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col6:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            🕒 Local Time
                        </div>

                        <div class="metric-value">
                            {local_time}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # -------------------- EXTRA SECTION --------------------
                st.markdown("### Additional Information")

                extra1, extra2, extra3 = st.columns(3)

                with extra1:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            🌅 Sunrise
                        </div>

                        <div class="metric-value">
                            {sunrise}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with extra2:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            🌇 Sunset
                        </div>

                        <div class="metric-value">
                            {sunset}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with extra3:
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="metric-label">
                            📌 Coordinates
                        </div>

                        <div class="metric-value">
                            {lat}, {lon}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                message = data.get("message", "City not found")
                st.error(f"City not found. {message.capitalize()}")

        except requests.exceptions.RequestException:
            st.error("Network error. Please check your internet connection.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# -------------------- FOOTER --------------------
st.markdown("<br><hr>", unsafe_allow_html=True)

st.caption(
    f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}"
)
