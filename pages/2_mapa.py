import requests
import streamlit as st

st.set_page_config(page_title="Mapa Fortnite", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background-color: #0e1117;
}

[data-testid="stImage"] img {
    background-color: #1c1f2b;
    border: 1px solid #2e3245;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stImage"] img:hover {
    border-color: #4da6ff;
}

[data-testid="stImageCaption"] {
    color: #4da6ff;
    font-size: 16px;
    text-align: center;
}

[data-testid="stRadio"] {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

[data-testid="stRadio"] [role="radiogroup"] {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: center;
    gap: 40px;
    width: 100%;
}

[data-testid="stRadio"] label {
    white-space: nowrap;
}

[data-testid="stRadio"] label p {
    font-size: 24px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

url_api = "https://fortnite-api.com/v1/map"

respuesta = requests.get(url_api)

if respuesta.status_code == 200:
    mapa_json = respuesta.json()
    imagenes = mapa_json["data"]["images"]
    lugares = mapa_json["data"]["pois"]

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    tipo = st.radio("Tipo de mapa", ["Con nombres", "Sin nombres"], horizontal=True)

if tipo == "Con nombres":
    st.image(imagenes["pois"], caption="Mapa de Fortnite")
else:
     st.image(imagenes["blank"], caption="Mapa de Fortnite")

st.metric("Lugares en el mapa", len(lugares))