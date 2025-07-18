import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO

st.set_page_config(page_title="Clima Histórico", page_icon="🌦️")
st.title("📈 Clima - Últimos 30 dias")

# Detectar localização do usuário
with st.spinner("Detectando sua localização..."):
    ipinfo_url = "https://ipinfo.io/json"
    loc_data = requests.get(ipinfo_url).json()
    cidade = loc_data.get("city", "Desconhecida")
    latitude, longitude = loc_data["loc"].split(",")

st.success(f"Local detectado: {cidade} (Lat: {latitude}, Lon: {longitude})")

# Datas
data_fim = datetime.today()
data_inicio = data_fim - timedelta(days=30)
start_date = data_inicio.strftime("%Y-%m-%d")
end_date = data_fim.strftime("%Y-%m-%d")

# Chamada à Open-Meteo
with st.spinner("Buscando dados meteorológicos..."):
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,"
        f"precipitation_sum,windspeed_10m_max,"
        f"relative_humidity_2m_mean,shortwave_radiation_sum"
        f"&timezone=America/Sao_Paulo"
    )
    resposta = requests.get(url)
    dados = resposta.json()
    print(dados)  # Para depuração, remova em produção

# Processar dados
if "daily" in dados:
    df = pd.DataFrame(dados["daily"])
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df.columns = [
        "Temp. Máx (°C)", "Temp. Mín (°C)", "Precipitação (mm)",
        "Vento Máx (km/h)", "Umidade Média (%)", "Radiação Solar (kWh/m²)"
    ]

    # Exibir gráficos
    st.subheader("🌡️ Temperatura")
    st.line_chart(df[["Temp. Máx (°C)", "Temp. Mín (°C)"]])

    st.subheader("🌧️ Precipitação")
    st.bar_chart(df["Precipitação (mm)"])

    st.subheader("💨 Vento Máximo")
    st.line_chart(df["Vento Máx (km/h)"])

    st.subheader("🌞 Radiação Solar")
    st.line_chart(df["Radiação Solar (kWh/m²)"])

    st.subheader("📅 Tabela dos últimos 30 dias")
    st.dataframe(df)

    # Gerar botão para download em Excel
    # usando BytesIO para criar um arquivo Excel em memória
    def to_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            dataframe.to_excel(writer, sheet_name="Clima", index=True)
        output.seek(0)
        return output

    st.download_button(
        label="📥 Baixar dados em Excel",
        data=to_excel(df),
        file_name="clima_30_dias.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.error("Não foi possível obter os dados climáticos 😒")
