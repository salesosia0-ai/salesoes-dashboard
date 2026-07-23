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

sectores = load_sectores()
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

# -----------------------
# UTILS
# -----------------------

def to_csv(df_local):
    return df_local.to_csv(index=False).encode("utf-8")

def safe_list(lst):
    return lst if isinstance(lst, list) else []

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
            df["problemas"].apply(lambda x: any(q in p.lower() for p in safe_list(x))) |
            df["aplicaciones_ia"].apply(lambda x: any(q in p.lower() for p in safe_list(x))) |
            df["preguntas_descubrimiento"].apply(lambda x: any(q in p.lower() for p in safe_list(x)))
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

        # 4. Matriz Fit vs Adopción (corregida)
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
        st.info(f"Tamaño: {sec_row.get('tamano_mercado', 'N/A')}")
    with c2:
        st.info(f"Facturación: {sec_row.get('facturacion_agregada', 'N/A')}")
    with c3:
        st.info(f"Adopción IA: {sec_row.get('adopcion_ia', 'N/A')}")
    with c4:
        st.info(f"Fit: {sec_row.get('fit', 'N/A')}")

    st.markdown("---")

    st.markdown("### Descripción")
    st.write(sec_row.get("descripcion", "Sin descripción disponible."))

    st.markdown("### Ficha rápida")
    st.write(f"**Subsector:** {sec_row.get('subsector', 'N/A')}")

    st.markdown("### Problemas principales")
    problemas = safe_list(sec_row.get("problemas", []))
    if problemas:
        for p in problemas:
            st.write(f"- {p}")
    else:
        st.write("Sin problemas registrados.")

    st.markdown("### Procesos manuales habituales")
    procesos = safe_list(sec_row.get("procesos_manuales", []))
    if procesos:
        for p in procesos:
            st.write(f"- {p}")
    else:
        st.write("Sin procesos registrados.")

    st.markdown("### Oportunidades de automatización")
    oportunidades = safe_list(sec_row.get("oportunidades_automatizacion", []))
    if oportunidades:
        for p in oportunidades:
            st.write(f"- {p}")
    else:
        st.write("Sin oportunidades registradas.")

    st.markdown("### Aplicaciones de IA")
    aplicaciones = safe_list(sec_row.get("aplicaciones_ia", []))
    if aplicaciones:
        for p in aplicaciones:
            st.write(f"- {p}")
    else:
        st.write("Sin aplicaciones registradas.")

    st.markdown("### Problemas legales / normativos")
    legales = safe_list(sec_row.get("problemas_legales", []))
    if legales:
        for p in legales:
            st.write(f"- {p}")
    else:
        st.write("Sin problemas legales registrados.")

    st.markdown("### Señales de problema")
    senales_prob = safe_list(sec_row.get("senales_problema", []))
    if senales_prob:
        for p in senales_prob:
            st.write(f"- {p}")
    else:
        st.write("Sin señales registradas.")

    st.markdown("### Indicadores de prioridad")
    indicadores = safe_list(sec_row.get("indicadores_prioridad", []))
    if indicadores:
        for p in indicadores:
            st.write(f"- {p}")
    else:
        st.write("Sin indicadores registrados.")

    st.markdown("### Señales de alarma")
    senales_alarma = safe_list(sec_row.get("senales_alarma", []))
    if senales_alarma:
        for p in senales_alarma:
            st.write(f"- {p}")
    else:
        st.write("Sin señales de alarma registradas.")

    st.markdown("### Herramientas IA de referencia")
    herramientas = safe_list(sec_row.get("herramientas_ia", []))
    if herramientas:
        for h in herramientas:
            st.write(f"- {h}")
    else:
        st.write("Sin herramientas registradas.")

    st.markdown("### Preguntas de descubrimiento")
    preguntas = safe_list(sec_row.get("preguntas_descubrimiento", []))
    if preguntas:
        for q in preguntas:
            st.write(f"- {q}")
    else:
        st.write("Sin preguntas registradas.")

    st.markdown("### Objeciones típicas y respuestas")
    objeciones = safe_list(sec_row.get("objeciones", []))
    if objeciones:
        for o in objeciones:
            if isinstance(o, dict):
                st.write(f"**Objeción:** {o.get('objecion', '')}")
                st.write(f"*Respuesta:* {o.get('respuesta', '')}")
            else:
                st.write(f"- {o}")
            st.write("")
    else:
        st.write("Sin objeciones registradas.")

    st.markdown("### Señales de prioridad")
    senales_pri = safe_list(sec_row.get("señal_prioridad", []))
    if senales_pri:
        for p in senales_pri:
            st.write(f"- {p}")
    else:
        st.write("Sin señales de prioridad registradas.")

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

else:
    st.title(opcion)
    st.markdown("Esta sección está en construcción. Pronto disponible.")
