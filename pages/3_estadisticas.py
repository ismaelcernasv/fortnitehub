import os
import requests
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="Jugador Fortnite", layout="wide")

load_dotenv()

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
    padding: 20px;
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid #2e3245;
}

.tarjeta:hover {
    border-color: #4da6ff;
}

.tarjeta .etiqueta {
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.tarjeta .valor {
    color: #4da6ff;
    font-size: 36px;
    font-weight: bold;
    margin-top: 8px;
}

.perfil {
    display: flex;
    align-items: center;
    gap: 20px;
    background-color: #1c1f2b;
    border: 1px solid #2e3245;
    border-radius: 16px;
    padding: 16px 24px;
    margin: 10px 0 20px 0;
}

.perfil:hover {
    border-color: #4da6ff;
}

.perfil img {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    object-fit: cover;
    background-color: #0e1117;
    border: 3px solid #4da6ff;
    box-shadow: 0 0 18px rgba(77, 166, 255, 0.45);
}

.perfil .sin-imagen {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background-color: #0e1117;
    border: 3px solid #4da6ff;
    color: #4da6ff;
    font-size: 36px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
}

.perfil .perfil-nombre {
    color: white;
    font-size: 32px;
    font-weight: bold;
}

.perfil .perfil-etiqueta {
    color: #4da6ff;
    font-size: 16px;
    margin-top: 2px;
}

.perfil.creador {
    border-color: #f5c542;
}

.perfil.creador img {
    border-color: #f5c542;
    box-shadow: 0 0 18px rgba(245, 197, 66, 0.5);
}

.perfil.creador .perfil-etiqueta {
    color: #f5c542;
}
</style>
""", unsafe_allow_html=True)

# 2. Datos fijos
url_jugador = "https://fortnite-api.com/v2/stats/br/v2"
url_cosmeticos = "https://fortnite-api.com/v2/cosmetics/br/search"
api_key = os.getenv("API_KEY")
headers = {"Authorization": api_key}

SKIN_DEFAULT = "Jonesy"
SKIN_CREADOR = "The Visitor"


# 3. Funciones
@st.cache_data
def obtener_skin(nombre_skin):
    parametros = {"name": nombre_skin, "matchMethod": "starts"}
    respuesta = requests.get(url_cosmeticos, params=parametros)
    if respuesta.status_code == 200:
        return respuesta.json()["data"]["images"]["icon"]
    return None


def mostrar_encabezado(nombre, imagen_url, etiqueta, clase=""):
    if imagen_url:
        imagen = f'<img src="{imagen_url}">'
    else:
        imagen = '<div class="sin-imagen">?</div>'

    st.markdown(f"""
    <div class="perfil {clase}">
        {imagen}
        <div>
            <div class="perfil-nombre">{nombre}</div>
            <div class="perfil-etiqueta">{etiqueta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def mostrar_tarjetas(datos):
    columnas = st.columns(len(datos))
    for i, (etiqueta, valor) in enumerate(datos):
        with columnas[i]:
            st.markdown(f"""
            <div class="tarjeta">
                <div class="etiqueta">{etiqueta}</div>
                <div class="valor">{valor:,}</div>
            </div>
            """, unsafe_allow_html=True)


# 4. Página
st.title("Estadísticas de jugador: temporada actual")

jugador = st.text_input("Ingresa tu nombre de EpicGames")

if jugador:
    parametros = {"name": jugador}
    respuesta = requests.get(url_jugador, headers=headers, params=parametros)

    if respuesta.status_code == 200:
        datos_jugador = respuesta.json()
        general = datos_jugador["data"]["stats"]["all"]["overall"]

        mostrar_encabezado(jugador, obtener_skin(SKIN_DEFAULT), "Jugador")

        mostrar_tarjetas([
            ("Victorias", general["wins"]),
            ("Partidas", general["matches"]),
            ("Horas jugadas", general["minutesPlayed"] // 60),
        ])
    else:
        st.error("Jugador no encontrado o cuenta privada")

# --- BANNER DEL CREADOR (SIEMPRE VISIBLE) ---
st.divider()

respuesta_creador = requests.get(url_jugador, headers=headers, params={"name": "NUKESV"})

if respuesta_creador.status_code == 200:
    datos_creador = respuesta_creador.json()
    general_creador = datos_creador["data"]["stats"]["all"]["overall"]

    mostrar_encabezado("NUKESV 👑", obtener_skin(SKIN_CREADOR), "Creador", "creador")

    mostrar_tarjetas([
        ("Nivel del pase", datos_creador["data"]["battlePass"]["level"]),
        ("Victorias totales", general_creador["wins"]),
        ("Horas jugadas", general_creador["minutesPlayed"] // 60),
    ])
else:
    st.warning("Las estadísticas del creador no están disponibles en este momento.")