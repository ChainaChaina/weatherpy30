import streamlit as st
import requests

st.set_page_config(page_title="Clima Atual", page_icon="🌤️")

st.title("🌍 Clima Atual na Sua Localização")

# Get location
with st.spinner("Detectando sua localização..."):
    ipinfo_url = "https://ipinfo.io/json"
    response = requests.get(ipinfo_url)
    data = response.json()

    cidade = data.get("city", "Cidade não encontrada")
    regiao = data.get("region", "")
    pais = data.get("country", "")
    loc = data.get("loc", "0,0")  # latitude,longitude

    latitude, longitude = loc.split(",")

st.success(f"Localização detectada: {cidade}, {regiao} ({pais})")

#API call Weather
API_KEY = "d88a30d67489199ad901ceadcb36f9d6" 
weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&lang=pt_br&appid={API_KEY}"

response = requests.get(weather_url)
weather_data = response.json()

if response.status_code == 200:
    clima = weather_data["weather"][0]["description"].capitalize()
    temp = weather_data["main"]["temp"]
    sensacao = weather_data["main"]["feels_like"]
    icone = weather_data["weather"][0]["icon"]
    nome_cidade = weather_data["name"]

    st.image(f"http://openweathermap.org/img/wn/{icone}@2x.png", width=100)
    st.metric(label=f"📍 {nome_cidade}", value=f"{temp}°C", delta=f"Sensação: {sensacao}°C")
    st.write(f"**Condição:** {clima}")
else:
    st.error("Erro ao buscar informações do clima.")



