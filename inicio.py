import os
import requests
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="Fortnite Hub", page_icon="🎮", layout="wide")

load_dotenv()

# 1. Estilos CSS
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background-color: #0e1117;
}

.hero {
    background: linear-gradient(135deg, #1c1f2b 0%, #0e1117 100%);
    border: 1px solid #2e3245;
    border-radius: 16px;
    padding: 48px 32px;
    margin-bottom: 24px;
    text-align: center;
}

.hero .hero-titulo {
    color: white;
    font-size: 56px;
    font-weight: bold;
}

.hero .hero-sub {
    color: #4da6ff;
    font-size: 20px;
    margin-top: 10px;
}

.seccion {
    color: white;
    font-size: 26px;
    font-weight: bold;
    margin: 28px 0 12px 0;
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

.tarjeta .icono {
    font-size: 44px;
}

.tarjeta .descripcion {
    color: #b8bdd0;
    font-size: 16px;
    margin-top: 8px;
    min-height: 72px;
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

[data-testid="stPageLink"] a {
    justify-content: center;
    background-color: #1c1f2b;
    border: 1px solid #2e3245;
    border-radius: 10px;
}

[data-testid="stPageLink"] a:hover {
    border-color: #4da6ff;
}
</style>
""", unsafe_allow_html=True)

# 2. Datos fijos
api_key = os.getenv("API_KEY")

URL_JUGADOR = "https://fortnite-api.com/v2/stats/br/v2"
URL_COSMETICOS = "https://fortnite-api.com/v2/cosmetics/br/search"
URL_TIENDA = "https://fortnite-api.com/v2/shop"
URL_MAPA = "https://fortnite-api.com/v1/map"

NOMBRE_CREADOR = "NUKESV"
SKIN_CREADOR = "The Visitor"


# 3. Funciones
@st.cache_data(ttl=3600)
def pedir(url, params=None, con_llave=False):
    headers = {"Authorization": api_key} if con_llave else {}
    respuesta = requests.get(url, headers=headers, params=params)
    if respuesta.status_code == 200:
        return respuesta.json()
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
        texto = f"{valor:,}" if valor is not None else "—"
        with columnas[i]:
            st.markdown(f"""
            <div class="tarjeta">
                <div class="etiqueta">{etiqueta}</div>
                <div class="valor">{texto}</div>
            </div>
            """, unsafe_allow_html=True)


# 4. Datos dinámicos (si una petición falla, el valor queda en None)
datos_tienda = pedir(URL_TIENDA)
articulos_hoy = None
if datos_tienda:
    entradas = datos_tienda["data"]["entries"]
    articulos_hoy = len([e for e in entradas if "brItems" in e])

datos_mapa = pedir(URL_MAPA)
lugares_mapa = None
if datos_mapa:
    lugares_mapa = len(datos_mapa["data"]["pois"])

datos_creador = pedir(URL_JUGADOR, {"name": NOMBRE_CREADOR}, con_llave=True)
victorias_creador = None
horas_creador = None
if datos_creador:
    general = datos_creador["data"]["stats"]["all"]["overall"]
    victorias_creador = general["wins"]
    horas_creador = general["minutesPlayed"] // 60

datos_skin = pedir(URL_COSMETICOS, {"name": SKIN_CREADOR, "matchMethod": "starts"})
imagen_creador = None
if datos_skin:
    imagen_creador = datos_skin["data"]["images"]["icon"]

# 5. Página
st.markdown("""
<div class="hero">
    <div class="hero-titulo">Fortnite Hub</div>
    <div class="hero-sub">Mira la tienda de hoy, explora el mapa y consulta las estadísticas de cualquier jugador.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="seccion">Qué puedes hacer aquí</div>', unsafe_allow_html=True)

paginas = [
    ("🛒", "Tienda",
     "Mira los artículos que están a la venta hoy, con su imagen y su precio en V-Bucks.",
     "pages/1_tienda.py", "Abrir la tienda"),
    ("🗺️", "Mapa",
     "Explora el mapa actual del juego y cambia entre la versión con nombres y la versión sin nombres.",
     "pages/2_mapa.py", "Abrir el mapa"),
    ("📊", "Estadísticas",
     "Escribe el nombre de un jugador de Epic Games y mira sus victorias, partidas y horas jugadas.",
     "pages/3_estadisticas.py", "Ver estadísticas"),
]

columnas = st.columns(3)

for i, (icono, titulo, descripcion, ruta, boton) in enumerate(paginas):
    with columnas[i]:
        st.markdown(f"""
        <div class="tarjeta">
            <div class="icono">{icono}</div>
            <div class="etiqueta">{titulo}</div>
            <div class="descripcion">{descripcion}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(ruta, label=boton)

st.markdown('<div class="seccion">Fortnite hoy</div>', unsafe_allow_html=True)

mostrar_tarjetas([
    ("Artículos en la tienda", articulos_hoy),
    ("Lugares en el mapa", lugares_mapa),
    ("Victorias del creador", victorias_creador),
])

st.markdown('<div class="seccion">Quién hizo esta página</div>', unsafe_allow_html=True)

mostrar_encabezado(f"{NOMBRE_CREADOR} 👑", imagen_creador, "Creador de Fortnite Hub", "creador")

if horas_creador is not None:
    st.caption(f"{NOMBRE_CREADOR} lleva {horas_creador:,} horas jugadas en Battle Royale, en esta temporada.")