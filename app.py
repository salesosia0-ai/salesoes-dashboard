import streamlit as st
import plotly.express as px
import pandas as pd
import json

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
    h2, h3 {{
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

sectores_raw = load_sectores()

# Transformar el JSON nuevo a la estructura que el app.py original esperaba
sectores = []
for nombre, datos in sectores_raw.items():
    descripcion = datos.get("1. Descripción", "")
    
    # Extraer datos numéricos estimados de la descripción (o defaults)
    tamano_map = {
        "1. Asesorías y Gestorías": 100000,
        "2. Clínicas Dentales": 15000,
        "3. Inmobiliarias": 30000,
        "4. Hoteles": 15000,
        "5. Restaurantes": 200000,
        "6. Apartamentos Turísticos": 400000,
        "7. Talleres Mecánicos": 30000,
        "8. Constructoras": 100000,
        "9. Empresas de Transporte": 50000,
        "10. Academias y Centros de Formación": 20000,
    }
    
    fact_map = {
        "1. Asesorías y Gestorías": 15000,
        "2. Clínicas Dentales": 3000,
        "3. Inmobiliarias": 10000,
        "4. Hoteles": 25000,
        "5. Restaurantes": 50000,
        "6. Apartamentos Turísticos": 30000,
        "7. Talleres Mecánicos": 15000,
        "8. Constructoras": 50000,
        "9. Empresas de Transporte": 25000,
        "10. Academias y Centros de Formación": 5000,
    }
    
    ia_map = {
        "1. Asesorías y Gestorías": 15,
        "2. Clínicas Dentales": 25,
        "3. Inmobiliarias": 30,
        "4. Hoteles": 35,
        "5. Restaurantes": 20,
        "6. Apartamentos Turísticos": 40,
        "7. Talleres Mecánicos": 15,
        "8. Constructoras": 20,
        "9. Empresas de Transporte": 25,
        "10. Academias y Centros de Formación": 20,
    }
    
    fit_map = {
        "1. Asesorías y Gestorías": "Muy alto",
        "2. Clínicas Dentales": "Muy alto",
        "3. Inmobiliarias": "Muy alto",
        "4. Hoteles": "Muy alto",
        "5. Restaurantes": "Muy alto",
        "6. Apartamentos Turísticos": "Alto",
        "7. Talleres Mecánicos": "Alto",
        "8. Constructoras": "Alto",
        "9. Empresas de Transporte": "Alto",
        "10. Academias y Centros de Formación": "Alto",
    }
    
    sectores.append({
        "nombre": nombre,
        "subsector": "Pymes y autónomos",
        "descripcion": descripcion,
        "problemas": datos.get("2. Principales problemas", []),
        "procesos_manuales": datos.get("3. Procesos manuales", []),
        "oportunidades_automatizacion": datos.get("4. Oportunidades de automatización", []),
        "aplicaciones_ia": datos.get("5. Aplicaciones de IA", []),
        "problemas_legales": datos.get("6. Problemas legales", []),
        "senales_problema": datos.get("7. Señales de problema", []),
        "indicadores_prioridad": datos.get("11. Indicadores de prioridad", []),
        "senales_alarma": datos.get("12. Señales de alarma", []),
        "preguntas_descubrimiento": datos.get("8. 15 preguntas de descubrimiento", []),
        "objeciones": datos.get("9. 15 objeciones", []),
        "respuestas_objeciones": datos.get("10. Respuestas a objeciones", []),
        "guion_path": datos.get("guion_path", ""),
        "email_path": datos.get("email_path", ""),
        "deck_path": datos.get("deck_path", ""),
        "tamano_mercado": descripcion,
        "facturacion_agregada": descripcion,
        "adopcion_ia": descripcion,
        "fit": fit_map.get(nombre, "Alto"),
        "tamano_mercado_num": tamano_map.get(nombre, 50000),
        "facturacion_agregada_num": fact_map.get(nombre, 10000),
        "adopcion_ia_num": ia_map.get(nombre, 25),
    })

df = pd.DataFrame(sectores)
df["nombre_corto"] = df["nombre"].str.replace(" y ", " & ")

# -----------------------
# ESTADO (favoritos, notas, modo reunión)
# -----------------------

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []
if "notas" not in st.session_state:
    st.session_state.notas = {s["nombre"]: "" for s in sectores}
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
        "Estrategia comercial",
        "Comparador",
        "Priorización",
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

def to_csv(df_local):
    return df_local.to_csv(index=False).encode("utf-8")

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
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Sectores", len(sectores))
    with c2:
        st.metric("Fit muy alto", sum(1 for s in sectores if s.get("fit") == "Muy alto"))
    with c3:
        st.metric("Fit alto", sum(1 for s in sectores if s.get("fit") == "Alto"))
    with c4:
        total_fact = sum(s.get("facturacion_agregada_num", 0) for s in sectores)
        st.metric("Facturación agregada (aprox)", f"~{total_fact:,} M€")

    st.markdown("---")

    # Filtro por búsqueda
    if buscar:
        q = buscar.lower()
        df_fil = df[
            df["nombre"].str.lower().str.contains(q) |
            df["subsector"].str.lower().str.contains(q) |
            df["problemas"].apply(lambda x: any(q in str(p).lower() for p in safe_list(x))) |
            df["aplicaciones_ia"].apply(lambda x: any(q in str(p).lower() for p in safe_list(x))) |
            df["preguntas_descubrimiento"].apply(lambda x: any(q in str(p).lower() for p in safe_list(x)))
        ]
    else:
        df_fil = df

    if df_fil.empty:
        st.warning("No se encontraron sectores con ese filtro.")
    else:
        # Gráficas en rejilla 2x2
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        # 1. Tamaño de mercado
        with row1_col1:
            st.subheader("Tamaño de mercado por sector")
            fig_tamano = px.bar(
                df_fil,
                x="nombre_corto",
                y="tamano_mercado_num",
                title="Tamaño de mercado (nº de empresas / centros)",
                labels={"nombre_corto": "Sector", "tamano_mercado_num": "Tamaño"},
                color="tamano_mercado_num",
                color_continuous_scale="Blues",
            )
            fig_tamano.update_traces(marker_line_color="white", marker_line_width=1)
            fig_tamano.update_layout(
                margin=dict(l=40, r=40, t=60, b=100),
                showlegend=False,
                xaxis_tickangle=-45,
                title_font_size=16,
                xaxis_title_font_size=13,
                yaxis_title_font_size=13,
                xaxis_tickfont_size=11,
                yaxis_tickfont_size=11,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color=COLOR_TEXT,
            )
            st.plotly_chart(fig_tamano, use_container_width=True)
            st.download_button(
                label="📥 Descargar datos (CSV)",
                data=to_csv(df_fil[["nombre", "tamano_mercado_num"]]),
                file_name="tamano_mercado.csv",
                mime="text/csv",
            )

        # 2. Facturación agregada
        with row1_col2:
            st.subheader("Facturación agregada por sector")
            fig_fact = px.bar(
                df_fil,
                x="nombre_corto",
                y="facturacion_agregada_num",
                title="Facturación agregada (M€)",
                labels={"nombre_corto": "Sector", "facturacion_agregada_num": "Facturación (M€)"},
                color="facturacion_agregada_num",
                color_continuous_scale="Greens",
            )
            fig_fact.update_traces(marker_line_color="white", marker_line_width=1)
            fig_fact.update_layout(
                margin=dict(l=40, r=40, t=60, b=100),
                showlegend=False,
                xaxis_tickangle=-45,
                title_font_size=16,
                xaxis_title_font_size=13,
                yaxis_title_font_size=13,
                xaxis_tickfont_size=11,
                yaxis_tickfont_size=11,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color=COLOR_TEXT,
            )
            st.plotly_chart(fig_fact, use_container_width=True)
            st.download_button(
                label="📥 Descargar datos (CSV)",
                data=to_csv(df_fil[["nombre", "facturacion_agregada_num"]]),
                file_name="facturacion_agregada.csv",
                mime="text/csv",
            )

        # 3. Adopción de IA
        with row2_col1:
            st.subheader("Adopción de IA por sector")
            fig_ia = px.bar(
                df_fil,
                x="nombre_corto",
                y="adopcion_ia_num",
                title="Adopción estimada de IA (%)",
                labels={"nombre_corto": "Sector", "adopcion_ia_num": "Adopción IA (%)"},
                color="adopcion_ia_num",
                color_continuous_scale="Purples",
            )
            fig_ia.update_traces(marker_line_color="white", marker_line_width=1)
            fig_ia.update_layout(
                margin=dict(l=40, r=40, t=60, b=100),
                showlegend=False,
                xaxis_tickangle=-45,
                title_font_size=16,
                xaxis_title_font_size=13,
                yaxis_title_font_size=13,
                xaxis_tickfont_size=11,
                yaxis_tickfont_size=11,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color=COLOR_TEXT,
            )
            st.plotly_chart(fig_ia, use_container_width=True)
            st.download_button(
                label="📥 Descargar datos (CSV)",
                data=to_csv(df_fil[["nombre", "adopcion_ia_num"]]),
                file_name="adopcion_ia.csv",
                mime="text/csv",
            )

        # 4. Matriz Fit vs Adopción
        with row2_col2:
            st.subheader("Matriz Fit vs Adopción de IA")
            df_scatter = df_fil.copy()
            df_scatter["fit_num"] = df_scatter["fit"].map({"Muy alto": 2, "Alto": 1})
            fig_scatter = px.scatter(
                df_scatter,
                x="adopcion_ia_num",
                y="fit_num",
                text="nombre",
                title="Fit vs Adopción de IA (cada punto es un sector)",
                labels={
                    "adopcion_ia_num": "Adopción IA (%)",
                    "fit_num": "Fit (1=Alto, 2=Muy alto)",
                },
                size="facturacion_agregada_num",
                color="fit",
                color_discrete_map={"Muy alto": COLOR_ACCENT, "Alto": "#94a3b8"},
                size_max=20,
                opacity=0.8,
            )
            fig_scatter.update_traces(
                textposition="top center",
                marker_line_width=1,
                marker_line_color="white",
            )
            fig_scatter.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                title_font_size=16,
                xaxis_title_font_size=13,
                yaxis_title_font_size=13,
                xaxis_tickfont_size=11,
                yaxis_tickfont_size=11,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color=COLOR_TEXT,
                legend_title_font_size=13,
                legend_font_size=12,
                xaxis_range=[0, max(df_scatter["adopcion_ia_num"]) * 1.2],
                yaxis_range=[0.5, 2.5],
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.download_button(
                label="📥 Descargar datos (CSV)",
                data=to_csv(df_scatter[["nombre", "fit", "adopcion_ia_num", "facturacion_agregada_num"]]),
                file_name="matriz_fit_ia.csv",
                mime="text/csv",
            )

elif opcion == "Explorador de sectores":
    st.title("Explorador de sectores")
    st.markdown("Navega sector a sector con toda la información estructurada.")

    fit_sel = st.multiselect(
        "Filtrar por Fit",
        options=["Muy alto", "Alto"],
        default=["Muy alto", "Alto"],
    )

    sectores_filt = [s for s in sectores if s.get("fit") in fit_sel]

    if not sectores_filt:
        st.warning("No hay sectores con ese filtro. Selecciona otro fit.")
        st.stop()

    sector_sel = st.selectbox(
        "Selecciona un sector",
        options=[s["nombre"] for s in sectores_filt],
    )

    sec_row = next(s for s in sectores_filt if s["nombre"] == sector_sel)

    st.subheader(f"Sector: {sec_row['nombre']}")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info(f"Tamaño: {sec_row.get('tamano_mercado_num', 'N/A'):,}")
    with c2:
        st.info(f"Facturación: {sec_row.get('facturacion_agregada_num', 'N/A'):,} M€")
    with c3:
        st.info(f"Adopción IA: {sec_row.get('adopcion_ia_num', 'N/A')}%")
    with c4:
        st.info(f"Fit: {sec_row.get('fit', 'N/A')}")

    st.markdown("---")

    st.markdown("### Descripción")
    st.write(sec_row.get("descripcion", "Sin descripción disponible."))

    st.markdown("### Ficha rápida")
    st.write(f"**Subsector:** {sec_row.get('subsector', 'N/A')}")

    st.markdown("### Problemas principales")
    problemas = sec_row.get("problemas", [])
    if isinstance(problemas, str):
        st.write(problemas)
    elif problemas:
        for p in problemas:
            st.write(f"- {p}")
    else:
        st.write("Sin problemas registrados.")

    st.markdown("### Procesos manuales habituales")
    procesos = sec_row.get("procesos_manuales", [])
    if isinstance(procesos, str):
        st.write(procesos)
    elif procesos:
        for p in procesos:
            st.write(f"- {p}")
    else:
        st.write("Sin procesos registrados.")

        st.markdown("### Oportunidades de automatización")
    oportunidades = sec_row.get("oportunidades_automatizacion", [])
    if isinstance(oportunidades, str):
        st.write(oportunidades)
    elif oportunidades:
        for o in oportunidades:
            st.write(f"- {o}")
    else:
        st.write("Sin oportunidades registradas.")

    st.markdown("### Aplicaciones de IA")
    aplicaciones = sec_row.get("aplicaciones_ia", [])
    if isinstance(aplicaciones, str):
        st.write(aplicaciones)
    elif aplicaciones:
        for a in aplicaciones:
            st.write(f"- {a}")
    else:
        st.write("Sin aplicaciones registradas.")

    st.markdown("### Material comercial")
    c1, c2, c3 = st.columns(3)

    with c1:
        if sec_row.get("guion_path"):
            st.markdown(f"[📄 Abrir guion]({sec_row['guion_path']})")

    with c2:
        if sec_row.get("email_path"):
            st.markdown(f"[📧 Abrir email]({sec_row['email_path']})")

    with c3:
        if sec_row.get("deck_path"):
            st.markdown(f"[📊 Abrir deck]({sec_row['deck_path']})")

    st.markdown("---")

    st.markdown("### Problemas legales / normativos")
    legales = sec_row.get("problemas_legales", [])
    if isinstance(legales, str):
        st.write(legales)
    elif legales:
        for l in legales:
            st.write(f"- {l}")
    else:
        st.write("Sin problemas legales registrados.")

    st.markdown("### Señales de problema")
    senales_prob = sec_row.get("senales_problema", [])
    if isinstance(senales_prob, str):
        st.write(senales_prob)
    elif senales_prob:
        for s in senales_prob:
            st.write(f"- {s}")
    else:
        st.write("Sin señales registradas.")

    # CORRECCIÓN OBLIGATORIA: Apartado 11
    st.markdown("### Indicadores de prioridad")
    # Extraer directamente del JSON raw
    sec_raw = sectores_raw.get(sec_row["nombre"], {})
    indicadores_raw = sec_raw.get("11. Indicadores de prioridad", [])
    if isinstance(indicadores_raw, str):
        st.write(indicadores_raw)
    elif indicadores_raw:
        for i in indicadores_raw:
            st.write(f"- {i}")
    else:
        st.write("Sin indicadores registrados.")

    # CORRECCIÓN OBLIGATORIA: Apartado 12
    st.markdown("### Señales de alarma")
    # Extraer directamente del JSON raw
    alarmas_raw = sec_raw.get("12. Señales de alarma", [])
    if isinstance(alarmas_raw, str):
        st.write(alarmas_raw)
    elif alarmas_raw:
        for a in alarmas_raw:
            st.write(f"- {a}")
    else:
        st.write("Sin señales de alarma registradas.")

    st.markdown("### Preguntas de descubrimiento")
    preguntas = sec_row.get("preguntas_descubrimiento", [])
    if isinstance(preguntas, str):
        st.write(preguntas)
    elif preguntas:
        for q in preguntas:
            st.write(f"- {q}")
    else:
        st.write("Sin preguntas registradas.")

    st.markdown("### Objeciones típicas y respuestas")
    objeciones = sec_row.get("objeciones", [])
    if isinstance(objeciones, str):
        st.write(objeciones)
    elif objeciones:
        for o in objeciones:
            st.write(f"- {o}")
        st.write("")
    else:
        st.write("Sin objeciones registradas.")

    st.markdown("### Respuestas a objeciones")
    respuestas = sec_row.get("respuestas_objeciones", [])
    if isinstance(respuestas, str):
        st.write(respuestas)
    elif respuestas:
        for r in respuestas:
            st.write(f"{r}")
    else:
        st.write("Sin respuestas registradas.")

    # Notas por sector
    st.markdown("---")
    st.markdown("### Notas")
    notas_val = st.text_area(
        "Añade notas personales sobre este sector",
        value=st.session_state.notas.get(sec_row["nombre"], ""),
        key=f"notas_{sec_row['nombre']}",
    )
    st.session_state.notas[sec_row["nombre"]] = notas_val

    # Favoritos
    st.markdown("---")
    if sec_row["nombre"] in st.session_state.favoritos:
        if st.button("⭐ Quitar de favoritos"):
            st.session_state.favoritos.remove(sec_row["nombre"])
    else:
        if st.button("⭐ Añadir a favoritos"):
            st.session_state.favoritos.append(sec_row["nombre"])

elif opcion == "Estrategia comercial":
    st.title("Estrategia comercial")
    st.markdown("Define tu estrategia de venta por sector.")

    st.markdown("### Sectores por prioridad")
    
    # Agrupar por fit
    muy_alto = [s for s in sectores if s.get("fit") == "Muy alto"]
    alto = [s for s in sectores if s.get("fit") == "Alto"]
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🔴 Fit Muy Alto")
        for s in muy_alto:
            st.write(f"- **{s['nombre']}**: {s['tamano_mercado_num']:,} empresas, {s['facturacion_agregada_num']:,} M€")
    
    with c2:
        st.subheader("🟠 Fit Alto")
        for s in alto:
            st.write(f"- **{s['nombre']}**: {s['tamano_mercado_num']:,} empresas, {s['facturacion_agregada_num']:,} M€")

    st.markdown("---")
    st.markdown("### Recomendaciones por sector")
    
    sector_estrategia = st.selectbox(
        "Selecciona un sector para ver recomendaciones",
        options=[s["nombre"] for s in sectores],
    )
    
    sec_estrategia = next(s for s in sectores if s["nombre"] == sector_estrategia)
    
    st.markdown(f"**{sec_estrategia['nombre']}**")
    st.write(f"**Tamaño:** {sec_estrategia['tamano_mercado_num']:,} empresas")
    st.write(f"**Facturación:** {sec_estrategia['facturacion_agregada_num']:,} M€")
    st.write(f"**Adopción IA:** {sec_estrategia['adopcion_ia_num']}%")
    st.write(f"**Fit:** {sec_estrategia['fit']}")
    
    st.markdown("**Problemas principales:**")
    problemas = sec_estrategia.get("problemas", [])
    if isinstance(problemas, str):
        st.write(problemas)
    elif problemas:
        for p in problemas[:5]:
            st.write(f"- {p}")
    
    st.markdown("**Aplicaciones de IA:**")
    ia = sec_estrategia.get("aplicaciones_ia", [])
    if isinstance(ia, str):
        st.write(ia)
    elif ia:
        for i in ia[:5]:
            st.write(f"- {i}")

elif opcion == "Comparador":
    st.title("Comparador de sectores")
    st.markdown("Compara hasta 3 sectores lado a lado.")

    sectores_sel = st.multiselect(
        "Selecciona sectores para comparar",
        options=[s["nombre"] for s in sectores],
        max_selections=3,
    )

    if len(sectores_sel) >= 2:
        cols = st.columns(len(sectores_sel))
        
        for idx, nombre_sector in enumerate(sectores_sel):
            with cols[idx]:
                sec = next(s for s in sectores if s["nombre"] == nombre_sector)
                st.markdown(f"#### {sec['nombre']}")
                
                st.write(f"**Tamaño:** {sec['tamano_mercado_num']:,}")
                st.write(f"**Facturación:** {sec['facturacion_agregada_num']:,} M€")
                st.write(f"**Adopción IA:** {sec['adopcion_ia_num']}%")
                st.write(f"**Fit:** {sec['fit']}")
                
                st.markdown("**Problemas:**")
                problemas = sec.get("problemas", [])
                if isinstance(problemas, str):
                    st.write(problemas[:200] + "...")
                elif problemas:
                    for p in problemas[:3]:
                        st.write(f"- {p}")
                
                st.markdown("**IA:**")
                ia = sec.get("aplicaciones_ia", [])
                if isinstance(ia, str):
                    st.write(ia[:200] + "...")
                elif ia:
                    for i in ia[:3]:
                        st.write(f"- {i}")

    elif len(sectores_sel) == 1:
        st.info("Selecciona al menos 2 sectores para comparar.")
    else:
        st.info("Selecciona sectores arriba para comparar.")

elif opcion == "Priorización":
    st.title("Priorización")
    st.markdown("Filtra por prioridad y sector.")

    # Filtros
    fit_filter = st.multiselect(
        "Filtrar por Fit",
        options=["Muy alto", "Alto"],
        default=["Muy alto", "Alto"],
    )
    
    tamano_min = st.slider(
        "Tamaño mínimo de mercado",
        min_value=0,
        max_value=500000,
        value=0,
        step=10000,
    )
    
    df_prior = df[
        (df["fit"].isin(fit_filter)) &
        (df["tamano_mercado_num"] >= tamano_min)
    ]
    
    st.markdown(f"**{len(df_prior)} sectores** encontrados")
    
    if not df_prior.empty:
        # Ordenar por facturación
        df_prior_sorted = df_prior.sort_values("facturacion_agregada_num", ascending=False)
        
        st.markdown("### Sectores priorizados (por facturación)")
        
        for idx, row in df_prior_sorted.iterrows():
            with st.expander(f"**{row['nombre']}** - {row['facturacion_agregada_num']:,} M€ ({row['fit']})"):
                st.write(f"**Tamaño:** {row['tamano_mercado_num']:,}")
                st.write(f"**Adopción IA:** {row['adopcion_ia_num']}%")
                
                st.markdown("**Problemas:**")
                problemas = row.get("problemas", [])
                if isinstance(problemas, str):
                    st.write(problemas)
                elif problemas:
                    for p in problemas:
                        st.write(f"- {p}")

elif opcion == "Export / API":
    st.title("Export / API")
    st.markdown("Exporta los datos en diferentes formatos.")

    st.markdown("### Descargar JSON completo")
    st.json(sectores_raw)

    st.markdown("---")
    st.markdown("### Descargar CSV")
    
    csv = df.to_csv(index=False).encode("utf-8")
    
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
        
        # Exportar favoritos
        fav_data = [s for s in sectores if s["nombre"] in st.session_state.favoritos]
        fav_df = pd.DataFrame(fav_data)
        fav_csv = fav_df.to_csv(index=False).encode("utf-8")
        
        st.download_button(
            label="📥 Descargar favoritos (CSV)",
            data=fav_csv,
            file_name="favoritos_salesos.csv",
            mime="text/csv",
        )
    else:
        st.write("No tienes sectores favoritos aún.")

# -----------------------
# FOOTER
# -----------------------

st.markdown("---")
st.markdown("SalesOS IA © 2026")
