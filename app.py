import streamlit as st
import json
import plotly.express as px
import pandas as pd

# -----------------------
# CONFIGURACIÓN Y ESTILO
# -----------------------

st.set_page_config(
    page_title="SalesOS IA",
    page_icon="📊",
    layout="wide"
)

COLOR_BG = "#f4f6f8"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#0f172a"
COLOR_TEXT_SEC = "#475569"
COLOR_ACCENT = "#2563eb"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {COLOR_BG};
        color: {COLOR_TEXT};
        font-family: "Inter", system-ui, -apple-system, sans-serif;
    }}
    .stMetric {{
        background-color: {COLOR_CARD};
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .stMetricLabel {{
        color: {COLOR_TEXT_SEC};
        font-size: 14px;
    }}
    .stMetricValue {{
        color: {COLOR_ACCENT};
        font-size: 24px;
        font-weight: 700;
    }}
    h1 {{
        font-size: 28px;
        font-weight: 700;
        color: {COLOR_TEXT};
        margin-bottom: 10px;
    }}
    h2, h3, h4 {{
        font-size: 20px;
        font-weight: 600;
        color: {COLOR_TEXT};
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 8px 16px;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------
# CARGA DE DATOS
# -----------------------

@st.cache_data
def load_sectores():
    with open("sectores.json", "r", encoding="utf-8") as f:
        return json.load(f)

sectores = load_sectores()

# Crear lista de sectores para el DataFrame
lista_sectores = []
for nombre_sector, datos in sectores.items():
    lista_sectores.append({
        "nombre": nombre_sector,
        "descripcion": datos.get("1. Descripción", ""),
        "problemas": datos.get("2. Principales problemas", []),
        "procesos_manuales": datos.get("3. Procesos manuales", ""),
        "oportunidades": datos.get("4. Oportunidades de automatización", []),
        "aplicaciones_ia": datos.get("5. Aplicaciones de IA", []),
        "problemas_legales": datos.get("6. Problemas legales", ""),
        "señales_problema": datos.get("7. Señales de problema", []),
        "preguntas": datos.get("8. 15 preguntas de descubrimiento", []),
        "objeciones": datos.get("9. 15 objeciones", []),
        "respuestas_objeciones": datos.get("10. Respuestas a objeciones", ""),
        "indicadores_prioridad": datos.get("11. Indicadores de prioridad", []),
        "señales_alarma": datos.get("12. Señales de alarma", []),
    })

df = pd.DataFrame(lista_sectores)

# -----------------------
# ESTADO (favoritos, notas, modo reunión)
# -----------------------

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []
if "notas" not in st.session_state:
    st.session_state.notas = {s: "" for s in sectores}
if "modo_reunion" not in st.session_state:
    st.session_state.modo_reunion = False

# -----------------------
# SIDEBAR – MENÚ
# -----------------------

st.sidebar.title("SalesOS IA")
st.sidebar.markdown("Menú")

opcion = st.sidebar.radio(
    "Navegación",
    [
        "Inicio / Resumen",
        "Explorador de sectores",
        "Comparador",
        "Export / API",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Herramientas")

buscar = st.sidebar.text_input("🔍 Buscar por palabra clave", "")

st.sidebar.markdown("---")
st.sidebar.markdown("### Opciones")

modo_reunion = st.sidebar.checkbox("Modo reunión", value=st.session_state.modo_reunion)
st.session_state.modo_reunion = modo_reunion

st.sidebar.markdown("---")
if st.sidebar.button("📋 Limpiar favoritos"):
    st.session_state.favoritos = []

# -----------------------
# UTILS
# -----------------------

def safe_list(lst):
    return lst if isinstance(lst, list) else []

def safe_str(s):
    return s if isinstance(s, str) else str(s) if s else ""

# -----------------------
# PÁGINAS
# -----------------------

if opcion == "Inicio / Resumen":
    st.title("SalesOS IA")
    st.markdown("Dashboard de inteligencia comercial por sectores.")

    # KPIs globales
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Sectores", len(sectores))
    with c2:
        total_problemas = sum(len(safe_list(s.get("2. Principales problemas", []))) for s in sectores.values())
        st.metric("Problemas identificados", total_problemas)
    with c3:
        total_preguntas = sum(len(safe_list(s.get("8. 15 preguntas de descubrimiento", []))) for s in sectores.values())
        st.metric("Preguntas de descubrimiento", total_preguntas)

    st.markdown("---")

    # Filtro por búsqueda
    if buscar:
        q = buscar.lower()
        df_fil = df[
            df["nombre"].str.lower().str.contains(q) |
            df["descripcion"].str.lower().str.contains(q) |
            df["procesos_manuales"].str.lower().str.contains(q) |
            df["problemas_legales"].str.lower().str.contains(q) |
            df["respuestas_objeciones"].str.lower().str.contains(q)
        ]
    else:
        df_fil = df

    if df_fil.empty:
        st.warning("No se encontraron sectores con ese filtro.")
    else:
        # Lista de sectores con tarjetas
        st.subheader("Sectores disponibles")
        
        for idx, row in df_fil.iterrows():
            with st.expander(f"**{row['nombre']}**"):
                st.write("**Descripción:**")
                st.write(row["descripcion"])
                
                st.write("**Problemas principales:**")
                problemas = safe_list(row["problemas"])
                if problemas:
                    for p in problemas:
                        st.write(f"- {p}")
                else:
                    st.write("Sin problemas registrados.")
                
                st.write("**Aplicaciones de IA:**")
                aplicaciones = safe_list(row["aplicaciones_ia"])
                if aplicaciones:
                    for a in aplicaciones:
                        st.write(f"- {a}")
                else:
                    st.write("Sin aplicaciones registradas.")

elif opcion == "Explorador de sectores":
    st.title("Explorador de sectores")
    st.markdown("Navega sector a sector con toda la información estructurada.")

    sector_sel = st.selectbox(
        "Selecciona un sector",
        options=list(sectores.keys()),
    )

    sec_data = sectores[sector_sel]

    st.markdown("---")

    # Mostrar las 10 fichas en pestañas
    tabs = st.tabs([
        "1. Descripción",
        "2. Problemas",
        "3. Procesos",
        "4. Oportunidades",
        "5. IA",
        "6. Legal",
        "7. Señales",
        "8. Preguntas",
        "9. Objeciones",
        "10. Respuestas",
    ])

    with tabs[0]:
        st.markdown("### 1. Descripción")
        st.write(sec_data.get("1. Descripción", "Sin descripción disponible."))

    with tabs[1]:
        st.markdown("### 2. Principales problemas")
        problemas = safe_list(sec_data.get("2. Principales problemas", []))
        if problemas:
            for p in problemas:
                st.write(f"- {p}")
        else:
            st.write("Sin problemas registrados.")

    with tabs[2]:
        st.markdown("### 3. Procesos manuales habituales")
        procesos = safe_str(sec_data.get("3. Procesos manuales", ""))
        if procesos:
            st.write(procesos)
        else:
            st.write("Sin procesos registrados.")

    with tabs[3]:
        st.markdown("### 4. Oportunidades de automatización")
        oportunidades = safe_list(sec_data.get("4. Oportunidades de automatización", []))
        if oportunidades:
            for o in oportunidades:
                st.write(f"- {o}")
        else:
            st.write("Sin oportunidades registradas.")

    with tabs[4]:
        st.markdown("### 5. Aplicaciones de IA")
        aplicaciones = safe_list(sec_data.get("5. Aplicaciones de IA", []))
        if aplicaciones:
            for a in aplicaciones:
                st.write(f"- {a}")
        else:
            st.write("Sin aplicaciones registradas.")

    with tabs[5]:
        st.markdown("### 6. Problemas legales / normativos")
        legales = safe_str(sec_data.get("6. Problemas legales", ""))
        if legales:
            st.write(legales)
        else:
            st.write("Sin problemas legales registrados.")

    with tabs[6]:
        st.markdown("### 7. Señales de problema")
        senales = safe_list(sec_data.get("7. Señales de problema", []))
        if senales:
            for s in senales:
                st.write(f"- {s}")
        else:
            st.write("Sin señales registradas.")

    with tabs[7]:
        st.markdown("### 8. 15 preguntas de descubrimiento")
        preguntas = safe_list(sec_data.get("8. 15 preguntas de descubrimiento", []))
        if preguntas:
            for i, p in enumerate(preguntas, 1):
                st.write(f"{i}. {p}")
        else:
            st.write("Sin preguntas registradas.")

    with tabs[8]:
        st.markdown("### 9. 15 objeciones típicas")
        objeciones = safe_list(sec_data.get("9. 15 objeciones", []))
        if objeciones:
            for i, o in enumerate(objeciones, 1):
                st.write(f"{i}. {o}")
        else:
            st.write("Sin objeciones registradas.")

    with tabs[9]:
        st.markdown("### 10. Respuestas a objeciones")
        respuestas = safe_str(sec_data.get("10. Respuestas a objeciones", ""))
        if respuestas:
            st.write(respuestas)
        else:
            st.write("Sin respuestas registradas.")

    # Fichas adicionales (11 y 12)
    st.markdown("---")
    st.markdown("### Fichas adicionales")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 11. Indicadores de prioridad")
        indicadores = safe_list(sec_data.get("11. Indicadores de prioridad", []))
        if indicadores:
            for i in indicadores:
                st.write(f"- {i}")
        else:
            st.write("Sin indicadores registrados.")

    with c2:
        st.markdown("#### 12. Señales de alarma")
        alarmas = safe_list(sec_data.get("12. Señales de alarma", []))
        if alarmas:
            for a in alarmas:
                st.write(f"- {a}")
        else:
            st.write("Sin señales de alarma registradas.")

    # Notas por sector
    st.markdown("---")
    st.markdown("### Notas")
    notas_val = st.text_area(
        "Añade notas personales sobre este sector",
        value=st.session_state.notas.get(sector_sel, ""),
        key=f"notas_{sector_sel}",
        height=150,
    )
    st.session_state.notas[sector_sel] = notas_val

    # Favoritos
    st.markdown("---")
    if sector_sel in st.session_state.favoritos:
        if st.button("⭐ Quitar de favoritos"):
            st.session_state.favoritos.remove(sector_sel)
    else:
        if st.button("⭐ Añadir a favoritos"):
            st.session_state.favoritos.append(sector_sel)

elif opcion == "Comparador":
    st.title("Comparador de sectores")
    st.markdown("Compara hasta 3 sectores lado a lado.")

    sectores_sel = st.multiselect(
        "Selecciona sectores para comparar",
        options=list(sectores.keys()),
        max_selections=3,
    )

    if len(sectores_sel) >= 2:
        cols = st.columns(len(sectores_sel))
        
        for idx, sector in enumerate(sectores_sel):
            with cols[idx]:
                st.markdown(f"#### {sector}")
                sec_data = sectores[sector]
                
                st.markdown("**Descripción:**")
                st.write(sec_data.get("1. Descripción", "N/A")[:300] + "...")
                
                st.markdown("**Problemas:**")
                problemas = safe_list(sec_data.get("2. Principales problemas", []))[:5]
                for p in problemas:
                    st.write(f"- {p}")
                
                st.markdown("**IA:**")
                ia = safe_list(sec_data.get("5. Aplicaciones de IA", []))[:5]
                for i in ia:
                    st.write(f"- {i}")

    elif len(sectores_sel) == 1:
        st.info("Selecciona al menos 2 sectores para comparar.")
    else:
        st.info("Selecciona sectores arriba para comparar.")

elif opcion == "Export / API":
    st.title("Export / API")
    st.markdown("Exporta los datos en diferentes formatos.")

    st.markdown("### Descargar JSON completo")
    st.json(sectores)

    st.markdown("---")
    st.markdown("### Descargar CSV")
    
    # Preparar DataFrame para exportar
    df_export = pd.DataFrame(lista_sectores)
    csv = df_export.to_csv(index=False, encoding="utf-8").encode("utf-8")
    
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="sectores_salesos.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.markdown("### Favoritos")
    if st.session_state.favoritos:
        st.write("Tus sectores favoritos:")
        for fav in st.session_state.favoritos:
            st.write(f"- {fav}")
    else:
        st.write("No tienes sectores favoritos aún.")

# -----------------------
# FOOTER
# -----------------------

st.markdown("---")
st.markdown("SalesOS IA © 2026")
