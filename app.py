import streamlit as st
import requests as req
from google import genai

def api_calling(cityname):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=3f6266bfdd380ce3d2f22e537db5b435"
    data= req.get(url)
    data=data.json()
    if data:
        return data['main']
    else:
        return "Data not found"
    
st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="centered")

st.title("🌦️ My Weather App ")
st.caption("Live weather + AI suggestions for your day 🌞☔❄️")

with st.sidebar:
    st.header("📍 Select Location")
    city= st.text_input(" Enter city name")
    st.write("Tip: Try Hyderabad, Delhi, Chennai 🌆")

    btn = st.button("Submit")
    if btn:
        st.session_state.weather =api_calling(city)
        # st.write(dataa)/


    if "weather" in st.session_state:
        dataa= st.session_state.weather

        temp = dataa["temp"] - 273.15
        
        col1,col2,col3 = st.columns(3)

        with col1:
            st.metric('🌡️ Temp', f"{dataa["temp"]-273.15} °C")
            st.metric('🌡️ Temp_min',f"{dataa['temp_min']-273.15} °C")

        with col2:
            st.metric('🌊 Sea_level', dataa["sea_level"])
            st.metric('💧 Humidity',f"{dataa['humidity']}%")

        if temp > 30:
            st.success("♨️ It's host outside! Stay hydrated 💧")
        elif temp < 15:
            st.warning("❄️ Cold weather! Wear warm clothes ")
        else:
            st.info("🌤️ Pleasant weather today!")

    



def gemini_calling(city, dataa):
        
        h= api_calling(city)
        prompt=f"""
             You are a weather assistant.

             Here is the weather data:
             Temperature: {dataa['temp'] - 273.15}°C
             Min Temp: {dataa['temp_min'] - 273.15}°C
             Humidity: {dataa['humidity']}%
             Sea level: {dataa['sea_level']}
            
            Give clothing adivice, food suggestions, medicine to carry, skincare tips.
             {h}
            """
           
        # api_calling(city)
        # print(data)

        client = genai.Client(api_key="AIzaSyDdZZTvkAXcXgV8dXNpnNCn212ol27ZikM")
        with st.spinner("Loading AI suggestions 🤖..."):

          response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        return response.text

ai_sugg= st.button("🤖 Generate suggestions with AI")

if ai_sugg:
    if "weather" in st.session_state:
         dataa = st.session_state.weather
         st.write(gemini_calling(city, dataa))
    else:
        st.warning("Please submit city first..")