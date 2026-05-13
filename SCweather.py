import base64
from datetime import datetime
from pathlib import Path

import pycountry
import requests
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SkyCast Weather",
    page_icon="🌤️",
    layout="centered"
)

# =========================================================
# PATHS / CITY BACKGROUNDS
# =========================================================
ASSETS_DIR = Path("assets")

CITY_BACKGROUNDS = {
    "karachi": ASSETS_DIR / "karachi.jpg",
    "lahore": ASSETS_DIR / "lahore.jpg",
    "islamabad": ASSETS_DIR / "islamabad.jpg",
    "peshawar": ASSETS_DIR / "peshawar.jpg",
    "quetta": ASSETS_DIR / "quetta.jpg",
    "multan": ASSETS_DIR / "multan.jpg",
}

DEFAULT_BACKGROUND = ASSETS_DIR / "default.jpg"


def image_to_data_uri(image_path: Path) -> str | None:
    """Convert local image to base64 data URI for CSS background."""
    if not image_path.exists():
        return None

    ext = image_path.suffix.lower()
    mime = "image/jpeg"
    if ext == ".png":
        mime = "image/png"
    elif ext == ".webp":
        mime = "image/webp"

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def get_background_for_city(city_name: str) -> str | None:
    if not city_name:
        return image_to_data_uri(DEFAULT_BACKGROUND)

    city_lower = city_name.strip().lower()

    for key, path in CITY_BACKGROUNDS.items():
        if key in city_lower:
            return image_to_data_uri(path)

    return image_to_data_uri(DEFAULT_BACKGROUND)


def get_country_name(country_code: str) -> str:
    if not country_code:
        return "Unknown"

    country = pycountry.countries.get(alpha_2=country_code.upper())
    return country.name if country else country_code.upper()


def format_local_time(unix_ts: int, timezone_offset: int) -> str:
    if not unix_ts:
        return "N/A"
    local_time = datetime.utcfromtimestamp(unix_ts + timezone_offset)
    return local_time.strftime("%I:%M %p")


def get_wind_direction(deg):
    if deg is None:
        return "N/A"
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(deg / 45) % 8
    return directions[index]


# =========================================================
# INPUT
# =========================================================
city = st.text_input(
    "Enter city name",
    placeholder="e.g. Karachi or Karachi, PK"
)

bg_image = get_background_for_city(city)

# =========================================================
# CUSTOM CSS
# =========================================================
bg_css = ""
if bg_image:
    bg_css = f'url("{bg_image}")'
else:
    bg_css = 'none'

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image:
            linear-gradient(rgba(0, 0, 0, 0.72), rgba(0, 0, 0, 0.72)),
            {bg_css};
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"],
    [data-testid="stMainViewContainer"] {{
        background-color: transparent !important;
    }}

    .stTextInput label {{
        color: white !important;
        font-weight: 600;
    }}

    .stTextInput input {{
        background: rgba(255,255,255,0.12) !important;
        color: white !important;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.25) !important;
    }}

    .stButton > button {{
        width: 100%;
        background: rgba(255,255,255,0.18);
        color: white;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.25);
        padding: 0.75rem 1rem;
        font-weight: bold;
        font-size: 16px;
    }}

    h1, h2, h3, p, span, label {{
        color: white !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
st.markdown("# 🌤️ SkyCast Weather")
st.markdown("Professional live weather insights from around the world")

# =========================================================
# API KEY
# =========================================================
api_key = st.secrets["OPENWEATHER_API_KEY"]

# =========================================================
# MAIN ACTION
# =========================================================
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
                # Weather
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
                description = data["weather"][0]["description"].capitalize()
                icon = data["weather"][0]["icon"]

                # Location
                city_name = data.get("name", "Unknown City")
                country_code = data.get("sys", {}).get("country", "")
                country_name = get_country_name(country_code)

                # Time
                timezone_offset = data.get("timezone", 0)
                sunrise = format_local_time(data["sys"]["sunrise"], timezone_offset)
                sunset = format_local_time(data["sys"]["sunset"], timezone_offset)
                local_time = datetime.utcfromtimestamp(
                    datetime.utcnow().timestamp() + timezone_offset
                ).strftime("%I:%M %p")

                # Coordinates
                lat = data.get("coord", {}).get("lat", "N/A")
                lon = data.get("coord", {}).get("lon", "N/A")

                # =====================================================
                # HERO SECTION
                # =====================================================
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.image(
                        f"https://openweathermap.org/img/wn/{icon}@4x.png",
                        width=160
                    )

                with col2:
                    st.subheader(f"📍 {city_name}, {country_name}")
                    st.markdown(f"**{description}**")
                    st.markdown(f"## {temp}°C")
                    st.markdown(f"Feels like **{feels_like}°C**")
                    st.caption(f"High: {temp_max}°C • Low: {temp_min}°C")

                st.markdown("---")

                # =====================================================
                # STATS
                # =====================================================
                row1 = st.columns(2)
                row1[0].metric("Humidity", f"{humidity}%")
                row1[1].metric("Wind Speed", f"{wind_speed} m/s", help=f"Direction: {get_wind_direction(wind_deg)}")

                row2 = st.columns(2)
                row2[0].metric("Pressure", f"{pressure} hPa")
                row2[1].metric("Visibility", f"{visibility_km:.1f} km")

                row3 = st.columns(2)
                row3[0].metric("Cloudiness", f"{clouds}%")
                row3[1].metric("Local Time", local_time)

                st.markdown("### Additional Information")

                row4 = st.columns(3)
                row4[0].metric("Sunrise", sunrise)
                row4[1].metric("Sunset", sunset)
                row4[2].metric("Coordinates", f"{lat}, {lon}")

            else:
                message = data.get("message", "City not found")
                st.error(f"City not found. {message.capitalize()}")

        except requests.exceptions.RequestException:
            st.error("Network error. Please check your internet connection.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}")
