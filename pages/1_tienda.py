import requests
import streamlit as st

st.set_page_config(page_title="Tienda Fortnite", layout="wide")

# 1. Estilos CSS
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background-color: #0e1117;
}

.tarjeta {
    background-color: #1c1f2b;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid #2e3245;
}

.tarjeta:hover {
    border-color: #4da6ff;
}

.tarjeta img {
    width: 100%;
    border-radius: 8px;
}

.tarjeta .nombre {
    color: white;
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
}

.tarjeta .precio {
    color: #4da6ff;
    font-size: 16px;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("Tienda de Fortnite")

# 2. Datos de la API
url = "https://fortnite-api.com/v2/shop"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()
    articulos = datos["data"]["entries"]

    # Guardamos solo los artículos que sí se van a mostrar
    tarjetas = []

    for item in articulos:
        if "brItems" in item:
            nombre = item["brItems"][0]["name"]
            precio = item["finalPrice"]
            imagen_url = item.get("newDisplayAsset", {}).get("renderImages", [{}])[0].get("image")

            if imagen_url:
                tarjetas.append((nombre, precio, imagen_url))

    # Dibujamos las tarjetas de 3 en 3, una fila a la vez
    for inicio in range(0, len(tarjetas), 3):
        fila = tarjetas[inicio:inicio + 3]
        columnas = st.columns(3)

        for columna, (nombre, precio, imagen_url) in zip(columnas, fila):
            with columna:
                st.markdown(f"""
                <div class="tarjeta">
                    <img src="{imagen_url}">
                    <div class="nombre">{nombre}</div>
                    <div class="precio">{precio} V-Bucks</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.error("ERROR AL CONECTARSE")