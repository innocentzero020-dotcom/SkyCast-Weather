import streamlit as st
import requests
import pycountry
from datetime import datetime

# Page config
st.set_page_config(page_title="SkyCast Weather", page_icon="🌤️", layout="centered")

# Custom CSS (same as before) ...
# Header
st.markdown("<h1 style='text-align: center;'>🌤️ SkyCast Weather</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Live weather updates from around the world</p>", unsafe_allow_html=True)

# Input
city = st.text_input("Enter city name:", placeholder="e.g. Karachi, Pakistan")

if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name first! 😊")
    else:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': st.secrets["OPENWEATHER_API_KEY"], 'units': 'metric'}
        try:
            with st.spinner('Fetching data...'):
                response = requests.get(url, params=params)
                data = response.json()
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description'].capitalize()
                icon = data['weather'][0]['icon']
                country_code = data['sys']['country']           # e.g. "PK"
                country = pycountry.countries.get(alpha_2=country_code).name
                st.markdown(f"""
                <div class="glass-card">
                    <h2 style='margin:0;'>📍 {data['name']}, {country}</h2>
                    <img src="http://openweathermap.org/img/wn/{icon}@4x.png" width="150">
                    <h1 style='font-size:60px; margin:0;'>{temp}°C</h1>
                    <p style='font-size:20px;'><b>{desc}</b></p>
                </div>
                """, unsafe_allow_html=True)
                # (humidity and wind as before)
            else:
                st.error("City not found. Please check the spelling!")
        except Exception:
            st.error("There seems to be a problem with the internet connection.")
# Footer (unchanged) ...
