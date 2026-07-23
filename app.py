import streamlit as st
import pandas as pd

st.set_page_config(page_title="Salesoes IA", layout="wide")

st.title("Dashboard Salesoes IA")
st.markdown("10 sectores priorizados para prospección, diagnóstico y automatización.")

# Datos de los 10 sectores
sectores = [
    {
        "sector_id": "01",
        "nombre": "Asesorías y Gestorías",
        "subsector": "Servicios Profesionales",
        "fit": "Muy alto",
        "tamano_mercado": "~27.000 asesorías",
        "facturacion_agregada": "~8.500M€/año",
        "adopcion_ia": "~35%",
        "top_problema": "Introducción manual de datos de clientes",
        "top_herramienta": "Fintonic Business",
        "top_objecion": "No tenemos presupuesto",
        "señal_prioridad": "Web moderna con portal del cliente",
    },
    {
        "sector_id": "02",
        "nombre": "Despachos de Abogados",
        "subsector": "Servicios Profesionales - Legal",
        "fit": "Muy alto",
        "tamano_mercado": "~140.000 abogados",
        "facturacion_agregada": "~12.000M€/año",
        "adopcion_ia": "~28%",
        "top_problema": "Búsqueda de jurisprudencia manual",
        "top_herramienta": "LegesAI",
        "top_objecion": "No tenemos presupuesto",
        "señal_prioridad": "Web moderna con portal del cliente",
    },
    {
        "sector_id": "03",
        "nombre": "Clínicas Dentales",
        "subsector": "Salud - Odontología",
        "fit": "Muy alto",
        "tamano_mercado": "~24.000 clínicas",
        "facturacion_agregada": "~1.305M€",
        "adopcion_ia": "~25%",
        "top_problema": "Agenda con huecos improductivos",
        "top_herramienta": "Overjet",
        "top_objecion": "La odontología es muy manual",
        "señal_prioridad": "Web moderna con cita online",
    },
    {
        "sector_id": "04",
        "nombre": "Clínicas Veterinarias",
        "subsector": "Salud - Veterinaria",
        "fit": "Alto",
        "tamano_mercado": "~7.032 clínicas",
        "facturacion_agregada": "~3.069M€/año",
        "adopcion_ia": "~15%",
        "top_problema": "Agenda con huecos improductivos",
        "top_herramienta": "SignalPET",
        "top_objecion": "La veterinaria es muy manual",
        "señal_prioridad": "Web moderna con cita online",
    },
    {
        "sector_id": "05",
        "nombre": "Inmobiliarias",
        "subsector": "Servicios - Inmobiliario",
        "fit": "Muy alto",
        "tamano_mercado": "~60.683 agencias",
        "facturacion_agregada": "~9.400M€/año",
        "adopcion_ia": "~20%",
        "top_problema": "Captación manual de propiedades",
        "top_herramienta": "Idealista AVM",
        "top_objecion": "El sector es muy relacional",
        "señal_prioridad": "Web moderna con buscador avanzado",
    },
    {
        "sector_id": "06",
        "nombre": "Hoteles",
        "subsector": "Hostelería - Alojamiento",
        "fit": "Muy alto",
        "tamano_mercado": "~14.613 hoteles",
        "facturacion_agregada": "~125.340M€",
        "adopcion_ia": "~25%",
        "top_problema": "Pricing estático o reactivo",
        "top_herramienta": "Duetto",
        "top_objecion": "El sector es muy tradicional",
        "señal_prioridad": "Web moderna con motor de reservas",
    },
    {
        "sector_id": "07",
        "nombre": "Apartamentos Turísticos",
        "subsector": "Hostelería - Alojamiento Vacacional",
        "fit": "Alto",
        "tamano_mercado": "~400k-500k viviendas",
        "facturacion_agregada": "~25.000-35.000M€",
        "adopcion_ia": "~15%",
        "top_problema": "Pricing estático o intuitivo",
        "top_herramienta": "PriceLabs",
        "top_objecion": "Los apartamentos se gestionan manualmente",
        "señal_prioridad": "Web moderna con motor de reservas",
    },
    {
        "sector_id": "08",
        "nombre": "Restaurantes",
        "subsector": "Hostelería - Restauración",
        "fit": "Alto",
        "tamano_mercado": "~160.000 restaurantes",
        "facturacion_agregada": "~85.000-95.000M€",
        "adopcion_ia": "~18%",
        "top_problema": "Predicción de demanda inexacta",
        "top_herramienta": "Tenzo",
        "top_objecion": "El sector es muy tradicional",
        "señal_prioridad": "Web moderna con reservas online",
    },
    {
        "sector_id": "09",
        "nombre": "Gimnasios y Centros Deportivos",
        "subsector": "Deporte y Bienestar",
        "fit": "Alto",
        "tamano_mercado": "~5.800 centros",
        "facturacion_agregada": "~3.200M€/año",
        "adopcion_ia": "Media-alta",
        "top_problema": "Baja retención",
        "top_herramienta": "Virtuagym",
        "top_objecion": "No tenemos presupuesto",
        "señal_prioridad": "Web moderna con app o reservas online",
    },
    {
        "sector_id": "10",
        "nombre": "Clínicas de Estética y Centros de Belleza",
        "subsector": "Salud y Bienestar - Estética",
        "fit": "Alto",
        "tamano_mercado": "Cientos de centros",
        "facturacion_agregada": "Cientos de M€",
        "adopcion_ia": "Media-alta",
        "top_problema": "Agenda con huecos improductivos",
        "top_herramienta": "HubSpot",
        "top_objecion": "Nuestras clientes no usarían una app",
        "señal_prioridad": "Web moderna con reservas online",
    },
]

# KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Sectores", len(sectores))
with c2:
    st.metric("Fit muy alto", sum(1 for s in sectores if s["fit"] == "Muy alto"))
with c3:
    st.metric("Fit alto", sum(1 for s in sectores if s["fit"] == "Alto"))
with c4:
    st.metric("Campos por sector", len(sectores[0].keys()))

st.subheader("Filtros")
fit_sel = st.multiselect(
    "Fit",
    options=[s["fit"] for s in sectores],
    default=list(set([s["fit"] for s in sectores]))
)

sectores_filt = [s for s in sectores if s["fit"] in fit_sel]

sector_sel = st.selectbox(
    "Selecciona un sector",
    options=[s["nombre"] for s in sectores_filt]
)

sec_row = next(s for s in sectores_filt if s["nombre"] == sector_sel)

st.subheader(f"Sector: {sec_row['nombre']}")
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"Tamaño: {sec_row['tamano_mercado']}")
with c2:
    st.info(f"Facturación: {sec_row['facturacion_agregada']}")
with c3:
    st.info(f"Adopción IA: {sec_row['adopcion_ia']}")

st.markdown("### Ficha rápida")
st.write(f"**Subsector:** {sec_row['subsector']}")
st.write(f"**Problema principal:** {sec_row['top_problema']}")
st.write(f"**Herramienta IA:** {sec_row['top_herramienta']}")
st.write(f"**Objeción típica:** {sec_row['top_objecion']}")
st.write(f"**Señal de prioridad:** {sec_row['señal_prioridad']}")
