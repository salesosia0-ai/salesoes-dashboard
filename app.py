import streamlit as st
import plotly.express as px
import pandas as pd

# -----------------------
# CONFIGURACIÓN Y ESTILO
# -----------------------

st.set_page_config(
    page_title="Salesoes IA",
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
# DATOS DE LOS SECTORES
# -----------------------

sectores = [
    {
        "sector_id": "01",
        "nombre": "Asesorías y Gestorías",
        "subsector": "Servicios Profesionales",
        "fit": "Muy alto",
        "tamano_mercado": "~27.000 asesorías",
        "tamano_mercado_num": 27000,
        "facturacion_agregada": "~8.500M€/año",
        "facturacion_agregada_num": 8500,
        "adopcion_ia": "~35%",
        "adopcion_ia_num": 35,
        "problemas": [
            "Introducción manual de datos de clientes",
            "Conciliación bancaria y categorización de gastos manual",
            "Informes trimestrales/IVA repetitivos y poco personalizados",
            "Dificultad para escalar sin aumentar personal administrativo",
        ],
        "herramientas_ia": [
            "Fintonic Business",
            "Anytype",
            "Zapier + ChatGPT para flujos de informes",
        ],
        "preguntas_descubrimiento": [
            "¿Cuánto tiempo pasáis introduciendo datos de clientes manualmente?",
            "¿Cómo gestionáis hoy la conciliación y clasificación de gastos?",
            "¿Qué tipo de informes estáis entregando a clientes hoy?",
            "¿Os gustaría automatizar parte de la preparación de IVA y trimestrales?",
        ],
        "objeciones": [
            {
                "objecion": "No tenemos presupuesto",
                "respuesta": "Empezamos con un piloto pequeño que se paga con el ahorro de tiempo en 1–2 meses.",
            },
            {
                "objecion": "Nuestros clientes no valoran la tecnología",
                "respuesta": "No se trata de venderles tecnología, sino de darles más tiempo y claridad en sus números.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con portal del cliente",
            "Ofrecen productos digitales (nóminas, high-ticket, etc.)",
        ],
    },
    {
        "sector_id": "02",
        "nombre": "Despachos de Abogados",
        "subsector": "Servicios Profesionales - Legal",
        "fit": "Muy alto",
        "tamano_mercado": "~140.000 abogados",
        "tamano_mercado_num": 140000,
        "facturacion_agregada": "~12.000M€/año",
        "facturacion_agregada_num": 12000,
        "adopcion_ia": "~28%",
        "adopcion_ia_num": 28,
        "problemas": [
            "Búsqueda de jurisprudencia y doctrina manual",
            "Redacción de escritos y contratos muy repetitiva",
            "Gestión del tiempo por abogado poco eficiente",
        ],
        "herramientas_ia": [
            "LegesAI",
            "ChatGPT avanzado para esbozos y resúmenes",
            "Notion AI para gestión de conocimiento interno",
        ],
        "preguntas_descubrimiento": [
            "¿Cuánto tiempo pasáis buscando jurisprudencia y doctrina?",
            "¿Tenéis plantillas estandarizadas para escritos y contratos?",
            "¿Cómo medís la productividad de cada abogado?",
        ],
        "objeciones": [
            {
                "objecion": "No tenemos presupuesto",
                "respuesta": "Empezamos con un piloto en un área (ej. laboral) donde el ROI es muy rápido.",
            },
            {
                "objecion": "La abogacía es muy artesanal",
                "respuesta": "La IA no reemplaza el criterio, solo automatiza la parte repetitiva de la búsqueda y redacción.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con portal del cliente",
            "Especialización en áreas con alto volumen de escritos",
        ],
    },
    {
        "sector_id": "03",
        "nombre": "Clínicas Dentales",
        "subsector": "Salud - Odontología",
        "fit": "Muy alto",
        "tamano_mercado": "~24.000 clínicas",
        "tamano_mercado_num": 24000,
        "facturacion_agregada": "~1.305M€",
        "facturacion_agregada_num": 1305,
        "adopcion_ia": "~25%",
        "adopcion_ia_num": 25,
        "problemas": [
            "Agenda con huecos improductivos",
            "Seguimiento de pacientes post-tratamiento manual",
            "Falta de upselling sistemático de tratamientos",
        ],
        "herramientas_ia": [
            "Overjet",
            "Chatbots para recordatorios de citas",
            "CRM con automatizaciones (HubSpot, Pipedrive)",
        ],
        "preguntas_descubrimiento": [
            "¿Cuántos huecos improductivos tenéis en agenda por semana?",
            "¿Cómo seguís a los pacientes tras un tratamiento?",
            "¿Tenéis algún proceso sistemático para proponer tratamientos adicionales?",
        ],
        "objeciones": [
            {
                "objecion": "La odontología es muy manual",
                "respuesta": "La IA no toca el sillón, pero sí llena la agenda y mejora el seguimiento.",
            },
            {
                "objecion": "Ya usamos un software de clínica",
                "respuesta": "Lo integraremos o partiremos de ahí para añadir automatizaciones, no para sustituirlo.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con cita online",
            "Clínicas con varios doctores y varios tratamientos",
        ],
    },
    {
        "sector_id": "04",
        "nombre": "Clínicas Veterinarias",
        "subsector": "Salud - Veterinaria",
        "fit": "Alto",
        "tamano_mercado": "~7.032 clínicas",
        "tamano_mercado_num": 7032,
        "facturacion_agregada": "~3.069M€/año",
        "facturacion_agregada_num": 3069,
        "adopcion_ia": "~15%",
        "adopcion_ia_num": 15,
        "problemas": [
            "Agenda con huecos improductivos",
            "Falta de seguimiento de campañas de vacunación y desparasitación",
            "Poca fidelización sistemática de clientes",
        ],
        "herramientas_ia": [
            "SignalPET",
            "Chatbots para recordatorios de vacunas",
            "CRM con automatizaciones",
        ],
        "preguntas_descubrimiento": [
            "¿Cuántos huecos improductivos tenéis en agenda por semana?",
            "¿Cómo gestionáis hoy los recordatorios de vacunas y desparasitaciones?",
            "¿Tenéis algún programa de fidelización activo?",
        ],
        "objeciones": [
            {
                "objecion": "La veterinaria es muy manual",
                "respuesta": "La IA no toca al paciente, pero ayuda a llenar agenda y fidelizar dueños.",
            },
            {
                "objecion": "Ya usamos un software veterinario",
                "respuesta": "Partimos de vuestro software y añadimos capas de automatización encima.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con cita online",
            "Clínicas con varios veterinarios y servicios avanzados",
        ],
    },
    {
        "sector_id": "05",
        "nombre": "Inmobiliarias",
        "subsector": "Servicios - Inmobiliario",
        "fit": "Muy alto",
        "tamano_mercado": "~60.683 agencias",
        "tamano_mercado_num": 60683,
        "facturacion_agregada": "~9.400M€/año",
        "facturacion_agregada_num": 9400,
        "adopcion_ia": "~20%",
        "adopcion_ia_num": 20,
        "problemas": [
            "Captación manual de propiedades",
            "Descripciones de inmuebles repetitivas y poco persuasivas",
            "Filtrado de leads poco eficiente",
        ],
        "herramientas_ia": [
            "Idealista AVM",
            "ChatGPT para descripciones de inmuebles",
            "CRM con scoring de leads",
        ],
        "preguntas_descubrimiento": [
            "¿Cuánto tiempo pasáis captando y describiendo propiedades?",
            "¿Cómo filtráis hoy los leads que llegan de portales?",
            "¿Tenéis algún proceso de seguimiento tras la primera visita?",
        ],
        "objeciones": [
            {
                "objecion": "El sector es muy relacional",
                "respuesta": "La IA no reemplaza la relación, sino que libera tiempo para que la cuidéis más.",
            },
            {
                "objecion": "Ya usamos Idealista y portales",
                "respuesta": "Exacto, ahí es donde metemos IA para mejorar descripciones, pricing y seguimiento.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con buscador avanzado",
            "Agencias con varios agentes y carteras altas",
        ],
    },
    {
        "sector_id": "06",
        "nombre": "Hoteles",
        "subsector": "Hostelería - Alojamiento",
        "fit": "Muy alto",
        "tamano_mercado": "~14.613 hoteles",
        "tamano_mercado_num": 14613,
        "facturacion_agregada": "~125.340M€",
        "facturacion_agregada_num": 125340,
        "adopcion_ia": "~25%",
        "adopcion_ia_num": 25,
        "problemas": [
            "Pricing estático o reactivo",
            "Falta de personalización en la experiencia del huésped",
            "Reservas directas bajas frente a OTAs",
        ],
        "herramientas_ia": [
            "Duetto",
            "Chatbots para pre-check-in y preguntas frecuentes",
            "CRM hotelero con automatizaciones",
        ],
        "preguntas_descubrimiento": [
            "¿Cómo fijáis hoy los precios de habitación?",
            "¿Qué porcentaje de reservas son directas vs OTAs?",
            "¿Tenéis algún proceso de personalización antes/durante la estancia?",
        ],
        "objeciones": [
            {
                "objecion": "El sector es muy tradicional",
                "respuesta": "La IA se usa ya en cadenas grandes; la clave es empezar con un caso claro (pricing o reservas).",
            },
            {
                "objecion": "Ya usamos un PMS",
                "respuesta": "Partimos de vuestro PMS y añadimos capas de IA para pricing y comunicación.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con motor de reservas",
            "Hoteles con varios tipos de habitación y temporadas",
        ],
    },
    {
        "sector_id": "07",
        "nombre": "Apartamentos Turísticos",
        "subsector": "Hostelería - Alojamiento Vacacional",
        "fit": "Alto",
        "tamano_mercado": "~400k-500k viviendas",
        "tamano_mercado_num": 450000,
        "facturacion_agregada": "~25.000-35.000M€",
        "facturacion_agregada_num": 30000,
        "adopcion_ia": "~15%",
        "adopcion_ia_num": 15,
        "problemas": [
            "Pricing estático o intuitivo",
            "Gestión de mensajes repetitivos con huéspedes",
            "Falta de centralización de reservas directas",
        ],
        "herramientas_ia": [
            "PriceLabs",
            "Chatbots para WhatsApp y email",
            "Herramientas de canal + automatizaciones",
        ],
        "preguntas_descubrimiento": [
            "¿Cómo fijáis hoy los precios por temporada?",
            "¿Cuánto tiempo pasáis respondiendo mensajes repetitivos?",
            "¿Qué porcentaje de reservas os llegan directas vs plataformas?",
        ],
        "objeciones": [
            {
                "objecion": "Los apartamentos se gestionan manualmente",
                "respuesta": "La IA automatiza pricing y mensajes, no la limpieza ni el check-in físico.",
            },
            {
                "objecion": "Ya usamos Airbnb/Booking",
                "respuesta": "Empezamos optimizando precios y mensajes ahí, y luego impulsamos reservas directas.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con motor de reservas",
            "Gestores con varias viviendas (10+)",
        ],
    },
    {
        "sector_id": "08",
        "nombre": "Restaurantes",
        "subsector": "Hostelería - Restauración",
        "fit": "Alto",
        "tamano_mercado": "~160.000 restaurantes",
        "tamano_mercado_num": 160000,
        "facturacion_agregada": "~85.000-95.000M€",
        "facturacion_agregada_num": 90000,
        "adopcion_ia": "~18%",
        "adopcion_ia_num": 18,
        "problemas": [
            "Predicción de demanda inexacta",
            "Desperdicio de comida por sobre-compra",
            "Falta de fidelización sistemática de clientes",
        ],
        "herramientas_ia": [
            "Tenzo",
            "Chatbots para reservas y preguntas frecuentes",
            "CRM con campañas de fidelización",
        ],
        "preguntas_descubrimiento": [
            "¿Cómo decidís cuánta comida comprar cada semana?",
            "¿Cuánto estimáis que tiráis de comida por semana?",
            "¿Tenéis algún programa de fidelización o base de datos de clientes?",
        ],
        "objeciones": [
            {
                "objecion": "El sector es muy tradicional",
                "respuesta": "La IA no cocina, pero ayuda a comprar mejor y llenar mesas en horas bajas.",
            },
            {
                "objecion": "Ya usamos reservas online",
                "respuesta": "Perfecto, ahí es donde metemos IA para forecasting y fidelización.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con reservas online",
            "Restaurantes con varios turnos y carta extensa",
        ],
    },
    {
        "sector_id": "09",
        "nombre": "Gimnasios y Centros Deportivos",
        "subsector": "Deporte y Bienestar",
        "fit": "Alto",
        "tamano_mercado": "~5.800 centros",
        "tamano_mercado_num": 5800,
        "facturacion_agregada": "~3.200M€/año",
        "facturacion_agregada_num": 3200,
        "adopcion_ia": "Media-alta",
        "adopcion_ia_num": 22,
        "problemas": [
            "Baja retención de abonados",
            "Falta de personalización en rutinas y seguimiento",
            "Comunicación genérica y poco segmentada",
        ],
        "herramientas_ia": [
            "Virtuagym",
            "Chatbots para dudas y recordatorios",
            "CRM con segmentación y automatizaciones",
        ],
        "preguntas_descubrimiento": [
            "¿Cuál es vuestra tasa de bajas mensual/anual?",
            "¿Cómo seguís a los abonados que dejan de venir?",
            "¿Ofrecéis planes personalizados o solo acceso general?",
        ],
        "objeciones": [
            {
                "objecion": "No tenemos presupuesto",
                "respuesta": "Empezamos con un piloto en retención que se paga con menos bajas.",
            },
            {
                "objecion": "Nuestros clientes no usarían una app",
                "respuesta": "No hace falta que la usen; la IA trabaja desde el lado del gimnasio (mensajes, análisis).",
            },
        ],
        "señal_prioridad": [
            "Web moderna con app o reservas online",
            "Centros con varias salas y actividades",
        ],
    },
    {
        "sector_id": "10",
        "nombre": "Clínicas de Estética y Centros de Belleza",
        "subsector": "Salud y Bienestar - Estética",
        "fit": "Alto",
        "tamano_mercado": "Cientos de centros",
        "tamano_mercado_num": 3000,
        "facturacion_agregada": "Cientos de M€",
        "facturacion_agregada_num": 5000,
        "adopcion_ia": "Media-alta",
        "adopcion_ia_num": 20,
        "problemas": [
            "Agenda con huecos improductivos",
            "Falta de seguimiento post-tratamiento",
            "Poco upselling sistemático de tratamientos",
        ],
        "herramientas_ia": [
            "HubSpot",
            "Chatbots para recordatorios y citas",
            "CRM con automatizaciones de marketing",
        ],
        "preguntas_descubrimiento": [
            "¿Cuántos huecos improductivos tenéis en agenda por semana?",
            "¿Cómo seguís a las clientas tras un tratamiento?",
            "¿Tenéis algún proceso para proponer tratamientos complementarios?",
        ],
        "objeciones": [
            {
                "objecion": "Nuestras clientes no usarían una app",
                "respuesta": "La IA no necesita que usen app; automatiza mensajes y seguimiento desde vuestro lado.",
            },
            {
                "objecion": "Ya usamos un software de gestión",
                "respuesta": "Partimos de él y añadimos capas de automatización y mensajes inteligentes.",
            },
        ],
        "señal_prioridad": [
            "Web moderna con reservas online",
            "Centros con varios tratamientos de alto ticket",
        ],
    },
]

df = pd.DataFrame(sectores)

# Acortar nombres para gráficas
df["nombre_corto"] = df["nombre"].str.replace(" y ", " & ").str.replace("Centros Deportivos", "C. Deportivos")

# -----------------------
# PESTAÑAS
# -----------------------

tab1, tab2 = st.tabs(["🏠 Inicio / Resumen", "🔍 Explorador de sectores"])

# -----------------------
# PESTAÑA 1: INICIO
# -----------------------

with tab1:
    st.title("Dashboard Salesoes IA")
    st.markdown("10 sectores priorizados para prospección, diagnóstico y automatización.")

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

    # Gráficas en rejilla 2x2
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # 1. Tamaño de mercado
    with row1_col1:
        st.subheader("Tamaño de mercado por sector")
        fig_tamano = px.bar(
            df,
            x="nombre_corto",
            y="tamano_mercado_num",
            title="Tamaño de mercado (nº de empresas / centros)",
            labels={"nombre_corto": "Sector", "tamano_mercado_num": "Tamaño"},
            color="tamano_mercado_num",
            color_continuous_scale="Blues",
        )
        fig_tamano.update_traces(marker_line_color="white", marker_line_width=1)
        fig_tamano.update_layout(
            margin=dict(l=40, r=40, t=60, b=80),
            showlegend=False,
            xaxis_tickangle=-30,
            title_font_size=16,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=12,
            yaxis_tickfont_size=12,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=COLOR_TEXT,
        )
        st.plotly_chart(fig_tamano, use_container_width=True)

    # 2. Facturación agregada
    with row1_col2:
        st.subheader("Facturación agregada por sector")
        fig_fact = px.bar(
            df,
            x="nombre_corto",
            y="facturacion_agregada_num",
            title="Facturación agregada (M€)",
            labels={"nombre_corto": "Sector", "facturacion_agregada_num": "Facturación (M€)"},
            color="facturacion_agregada_num",
            color_continuous_scale="Greens",
        )
        fig_fact.update_traces(marker_line_color="white", marker_line_width=1)
        fig_fact.update_layout(
            margin=dict(l=40, r=40, t=60, b=80),
            showlegend=False,
            xaxis_tickangle=-30,
            title_font_size=16,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=12,
            yaxis_tickfont_size=12,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=COLOR_TEXT,
        )
        st.plotly_chart(fig_fact, use_container_width=True)

    # 3. Adopción de IA
    with row2_col1:
        st.subheader("Adopción de IA por sector")
        fig_ia = px.bar(
            df,
            x="nombre_corto",
            y="adopcion_ia_num",
            title="Adopción estimada de IA (%)",
            labels={"nombre_corto": "Sector", "adopcion_ia_num": "Adopción IA (%)"},
            color="adopcion_ia_num",
            color_continuous_scale="Purples",
        )
        fig_ia.update_traces(marker_line_color="white", marker_line_width=1)
        fig_ia.update_layout(
            margin=dict(l=40, r=40, t=60, b=80),
            showlegend=False,
            xaxis_tickangle=-30,
            title_font_size=16,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=12,
            yaxis_tickfont_size=12,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=COLOR_TEXT,
        )
        st.plotly_chart(fig_ia, use_container_width=True)

    # 4. Matriz Fit vs Adopción
    with row2_col2:
        st.subheader("Matriz Fit vs Adopción de IA")
        df_scatter = df.copy()
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
            size_max=25,
        )
        fig_scatter.update_traces(textposition="top center", marker_line_width=1, marker_line_color="white")
        fig_scatter.update_layout(
            margin=dict(l=40, r=40, t=60, b=40),
            title_font_size=16,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=12,
            yaxis_tickfont_size=12,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=COLOR_TEXT,
            legend_title_font_size=13,
            legend_font_size=12,
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------
# PESTAÑA 2: EXPLORADOR
# -----------------------

with tab2:
    st.title("Explorador de sectores")
    st.markdown("Navega sector a sector con toda la información estructurada.")

    fit_sel = st.multiselect(
        "Filtrar por Fit",
        options=["Muy alto", "Alto"],
        default=["Muy alto", "Alto"],
    )

    sectores_filt = [s for s in sectores if s["fit"] in fit_sel]

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
        st.info(f"Tamaño: {sec_row['tamano_mercado']}")
    with c2:
        st.info(f"Facturación: {sec_row['facturacion_agregada']}")
    with c3:
        st.info(f"Adopción IA: {sec_row['adopcion_ia']}")
    with c4:
        st.info(f"Fit: {sec_row['fit']}")

    st.markdown("---")

    st.markdown("### Ficha rápida")
    st.write(f"**Subsector:** {sec_row['subsector']}")

    st.markdown("### Problemas principales")
    for p in sec_row["problemas"]:
        st.write(f"- {p}")

    st.markdown("### Herramientas IA de referencia")
    for h in sec_row["herramientas_ia"]:
        st.write(f"- {h}")

    st.markdown("### Preguntas de descubrimiento")
    for q in sec_row["preguntas_descubrimiento"]:
        st.write(f"- {q}")

    st.markdown("### Objeciones típicas y respuestas")
    for o in sec_row["objeciones"]:
        st.write(f"**Objeción:** {o['objecion']}")
        st.write(f"*Respuesta:* {o['respuesta']}")
        st.write("")

    st.markdown("### Señales de prioridad")
    for s in sec_row["señal_prioridad"]:
        st.write(f"- {s}")
