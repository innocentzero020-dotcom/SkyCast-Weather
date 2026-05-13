import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #007bff;
        color: white;
        height: 3em;
        font-weight: bold;
    }
    .weather-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("🌤️ SkyCast Weather")
st.write("Duniya bhar ke mausam ki live updates")

# --- Sidebar (Settings) ---
st.sidebar.header("Settings")
unit = st.sidebar.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"])
u_param = "metric" if unit == "Celsius" else "imperial"

# --- Input Area ---
city = st.text_input("Shehar ka naam likhein:", placeholder="e.g. Karachi, Baldia Town, London")
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
                
                # Convert Sunrise/Sunset
                sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
                sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')

                # --- Display Results ---
                st.markdown(f"### 📍 {data['name']}, {data['sys']['country']}")
                
                # Main Card
                col_main1, col_main2 = st.columns(2)
                with col_main1:
                    st.image(f"http://openweathermap.org/img/wn/{icon}@4x.png")
                with col_main2:
                    st.header(f"{temp}°{'C' if unit=='Celsius' else 'F'}")
                    st.write(f"**{desc}**")
                    st.write(f"Feels like: {feels_like}°")

                st.divider()

                # Stats Columns
                col1, col2, col3 = st.columns(3)
                col1.metric("Nami (Humidity)", f"{humidity}%")
                col2.metric("Hawa (Wind)", f"{wind} m/s")
                col3.metric("Pressure", f"{data['main']['pressure']} hPa")

                # Sun Info
                st.info(f"🌅 **Sunrise:** {sunrise} | 🌇 **Sunset:** {sunset}")

                # Success Message
                st.balloons()

            else:
                st.error("Shehar nahi mila. Spelling check karein!")

        except Exception as e:
            st.error("Internet connection ka masla hai.")

# --- Footer ---
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%d %b, %Y | %I:%M %p')}")