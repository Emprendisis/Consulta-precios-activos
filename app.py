import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Consulta de Precios", layout="centered")
st.title("📊 Consulta de precios históricos de activos")
st.markdown("Consulta el precio de cierre histórico de cualquier acción, fondo o ETF.")

# Ticker
ticker = st.text_input("🔍 Ingresa el ticker (clave de pizarra):", "AAPL")

# Frecuencia
frecuencia = st.selectbox("🕒 Frecuencia:", ["Diaria", "Semanal", "Mensual"])
intervalos = {"Diaria": "1d", "Semanal": "1wk", "Mensual": "1mo"}

# Plazo
plazo = st.selectbox("📅 Plazo:", ["1 día", "1 mes", "3 meses", "6 meses", "12 meses", "5 años"])
plazos = {"1 día": "1d", "1 mes": "1mo", "3 meses": "3mo", "6 meses": "6mo", "12 meses": "1y", "5 años": "5y"}

# Botón
if st.button("🔽 Obtener precios"):
    try:
        data = yf.Ticker(ticker).history(period=plazos[plazo], interval=intervalos[frecuencia])
        if data.empty:
            st.warning("⚠️ No se encontraron datos para los criterios seleccionados.")
        else:
            precios = data[['Close']].rename(columns={'Close': 'Precio de Cierre'})
st.success(f"✅ Datos obtenidos para {ticker}")
st.line_chart(precios)

excel_file = f"{ticker}_{intervalos[frecuencia]}_{plazos[plazo]}.xlsx"
precios.index = precios.index.tz_localize(None)  # ← Esta línea soluciona el error
precios.to_excel(excel_file)

with open(excel_file, "rb") as f:
    st.download_button("📥 Descargar en Excel", f, file_name=excel_file)
    except Exception as e:
        st.error(f"❌ Ocurrió un error: {e}")
