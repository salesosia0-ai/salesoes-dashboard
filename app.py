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

# Colores base (estilo dashboard limpio tipo Power BI)
COLOR_BG = "#f4f6f8"        # fondo general (gris muy suave)
COLOR_CARD = "#ffffff"      # fondo de tarjetas (blanco)
COLOR_TEXT = "#0f172a"      # texto principal (azul muy oscuro)
COLOR_TEXT_SEC = "#475569"  # texto secundario (gris azulado)
COLOR_ACCENT = "#2563eb"    # acento principal (azul)
COLOR_PALETTE = [
    "#2563eb",  # azul
    "#10b981",  # verde
    "#f59e0b",  # ámbar
    "#ef4444",  # rojo
    "#8b5cf6",  # violeta
    "#06b6d4",  # cyan
    "#f97316",  # naranja
]

# CSS para look tipo Power BI
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {COLOR_BG};
        color: {COLOR_TEXT};
        font-family: "Inter", system-ui, -apple-system, sans-serif;
    }}
    .stMarkdown, .stMarkdown p, .stSidebar .stMarkdown {{
        color: {COLOR_TEXT};
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

# Acortar nombres para gráficas
df["nombre_corto"] = df["nombre"].str.replace(" y ", " & ").str.replace("Centros Deportivos", "C. Deportivos")

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
        st.metric("Fit muy alto", sum(1 for s in sectores if s["fit"] == "Muy alto"))
    with c3:
        st.metric("Fit alto", sum(1 for s in sectores if s["fit"] == "Alto"))
    with c4:
        total_fact = sum(s.get("facturacion_agregada_num", 0) for s in sectores)
        st.metric("Facturación agregada (aprox)", f"~{total_fact:,} M€")

    st.markdown("---")

    # Filtro por búsqueda
    if buscar:
        df_fil = df[
            df["nombre"].str.lower().str.contains(buscar.lower()) |
            df["subsector"].str.lower().str.contains(buscar.lower()) |
            df["problemas"].apply(lambda x: any(buscar.lower() in p.lower() for p in x))
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
            # Ajustar tamaño máximo y opacidad para evitar solapamiento excesivo
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
    st.markdown("Navega sector a
