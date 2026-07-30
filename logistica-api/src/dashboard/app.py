# ==========================================================
# DASHBOARD LOGÍSTICO DE ENVÍOS
# Proyecto ISC6 - Área 5
# ==========================================================

# Librerías necesarias
import json
import os
from datetime import datetime
from pathlib import Path

import psycopg2

import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================================
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Dashboard Logístico de Envíos",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. ESTILOS PERSONALIZADOS
# ==========================================================

st.markdown(
    """
    <style>

        /* Espacio superior de la página */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        /* Tarjetas de indicadores */
        [data-testid="stMetric"] {
            background-color: #172033;
            border: 1px solid #2f3d55;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.20);
        }

        /* Texto del nombre de la métrica */
        [data-testid="stMetricLabel"] {
            font-size: 15px;
            font-weight: 600;
        }

        /* Valor numérico de la métrica */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
        }

        /* Encabezado principal */
        .encabezado {
            background: linear-gradient(90deg, #172033, #253552);
            padding: 22px;
            border-radius: 14px;
            margin-bottom: 20px;
            border-left: 6px solid #4da3ff;
        }

        /* Estado operativo */
        .estado-operativo {
            display: inline-block;
            background-color: #123d2c;
            color: #7ff0ae;
            padding: 7px 14px;
            border-radius: 20px;
            font-weight: bold;
        }

        /* Pie de página */
        .pie-pagina {
            text-align: center;
            color: #9aa4b2;
            font-size: 13px;
            padding-top: 20px;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# 3. CARGAR DATOS REALES DESDE POSTGRESQL
# ==========================================================

# La contraseña NO se escribe dentro del código para evitar subirla a GitHub.
# Antes de ejecutar el dashboard, se configura DB_PASSWORD en PowerShell.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "100.107.111.1"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "sistema_industrial"),
    "user": os.getenv("DB_USER", "dpt_user"),
    "password": os.getenv("DB_PASSWORD", ""),
    "connect_timeout": 6,
}

ruta_json = Path(__file__).parent / "datos" / "envios.json"

CONSULTA_ENVIOS = """
SELECT
    CONCAT('ENV', e.id_envio) AS guia,
    c.nombre AS cliente,
    r.destino AS destino,
    v.placa AS vehiculo,
    co.nombre AS chofer,
    e.estado AS estado,
    COALESCE(SUM(de.cantidad), 0) AS cantidad,
    e.fecha_envio AS fecha
FROM dpt.envios AS e
INNER JOIN dpt.clientes AS c
    ON e.id_cliente = c.id_cliente
INNER JOIN dpt.rutas AS r
    ON e.id_ruta = r.id_ruta
INNER JOIN dpt.conductores AS co
    ON e.id_conductor = co.id_conductor
INNER JOIN dpt.vehiculos AS v
    ON e.id_vehiculo = v.id_vehiculo
LEFT JOIN dpt.detalles_envio AS de
    ON e.id_envio = de.id_envio
GROUP BY
    e.id_envio,
    c.nombre,
    r.destino,
    v.placa,
    co.nombre,
    e.estado,
    e.fecha_envio
ORDER BY e.fecha_envio DESC;
"""


@st.cache_data(ttl=30, show_spinner=False)
def cargar_desde_postgresql():
    """Consulta los registros reales del esquema dpt."""
    if not DB_CONFIG["password"]:
        raise ValueError(
            "No se configuró la variable de entorno DB_PASSWORD."
        )

    conexion = psycopg2.connect(**DB_CONFIG)

    try:
        return pd.read_sql_query(CONSULTA_ENVIOS, conexion)
    finally:
        conexion.close()


def cargar_desde_json():
    """
    Respaldo temporal. Convierte el campo peso del JSON en cantidad
    para conservar el funcionamiento si se pierde la conexión.
    """
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    df_respaldo = pd.DataFrame(datos)

    if "peso" in df_respaldo.columns and "cantidad" not in df_respaldo.columns:
        df_respaldo = df_respaldo.rename(columns={"peso": "cantidad"})

    return df_respaldo


try:
    df_original = cargar_desde_postgresql()
    fuente_datos = "Base de datos PostgreSQL"
    datos_reales = True
    detalle_conexion = (
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']} / "
        f"{DB_CONFIG['dbname']} / esquema dpt"
    )

except (
    psycopg2.Error,
    ValueError,
    KeyError,
    TypeError
) as error_bd:

    try:
        df_original = cargar_desde_json()
        fuente_datos = "Archivo JSON de respaldo"
        datos_reales = False
        detalle_conexion = str(error_bd)

    except FileNotFoundError:
        st.error(
            "No fue posible consultar PostgreSQL y tampoco se encontró "
            "datos/envios.json."
        )
        st.stop()

    except json.JSONDecodeError:
        st.error(
            "No fue posible consultar PostgreSQL y envios.json "
            "tiene un formato incorrecto."
        )
        st.stop()


columnas_requeridas = {
    "guia",
    "cliente",
    "destino",
    "vehiculo",
    "chofer",
    "estado",
    "cantidad",
    "fecha",
}

columnas_faltantes = columnas_requeridas.difference(df_original.columns)

if columnas_faltantes:
    st.error(
        "La fuente de datos no contiene todas las columnas requeridas. "
        f"Faltan: {', '.join(sorted(columnas_faltantes))}"
    )
    st.stop()


# ==========================================================
# 4. PREPARAR Y VALIDAR LOS DATOS
# ==========================================================

# Convertimos la cantidad a número.
# Si un valor es incorrecto, se convierte en 0.
df_original["cantidad"] = pd.to_numeric(
    df_original["cantidad"],
    errors="coerce"
).fillna(0)

# Convertimos la fecha para poder ordenarla correctamente
df_original["fecha"] = pd.to_datetime(
    df_original["fecha"],
    errors="coerce"
)

# Ordenamos los envíos del más reciente al más antiguo
df_original = df_original.sort_values(
    by="fecha",
    ascending=False
)

# Creamos una columna de fecha visible para la tabla
df_original["fecha"] = df_original["fecha"].dt.strftime("%Y-%m-%d")


# ==========================================================
# 5. BARRA LATERAL
# ==========================================================

with st.sidebar:

    st.title("📦 Logística DTP")
    st.markdown("### Dashboard de Envíos")

    st.divider()

    st.write("**Proyecto:** ISC6")
    st.write("**Área:** Área 5")
    st.write("**Módulo:** Logística y Transporte")
    st.write("**Versión:** 1.2")

    st.divider()

    st.info(
        "Este panel permite consultar, filtrar y analizar "
        "la información de los envíos registrados."
    )

    st.markdown("### Funciones disponibles")

    st.write("✅ Indicadores generales")
    st.write("✅ Filtros de búsqueda")
    st.write("✅ Tabla de envíos")
    st.write("✅ Gráficas")
    st.write("✅ Resumen logístico")

    st.divider()

    if datos_reales:
        st.success("🟢 Fuente: PostgreSQL")
    else:
        st.warning("🟡 Fuente: datos de demostración")

    st.caption(
        "El dashboard consulta primero la API y utiliza el archivo JSON "
        "como respaldo cuando el backend no está disponible."
    )

    if st.button("🔄 Actualizar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ==========================================================
# 6. ENCABEZADO PRINCIPAL
# ==========================================================

fecha_actual = datetime.now().strftime("%d/%m/%Y")
hora_actual = datetime.now().strftime("%H:%M")

st.markdown(
    f"""
    <div class="encabezado">
        <h1 style="margin: 0;">📦 Dashboard de Envíos</h1>
        <p style="margin-top: 8px;">
            Panel de control para consultar y analizar el estado de los envíos.
        </p>
        <p>
            <span class="estado-operativo">● ACTIVO</span>
            &nbsp;&nbsp; Fecha: {fecha_actual}
            &nbsp;&nbsp; Hora: {hora_actual}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if datos_reales:
    st.success(
        f"Datos reales cargados correctamente desde PostgreSQL: {detalle_conexion}"
    )
else:
    st.warning(
        "No fue posible conectarse a PostgreSQL. "
        "Se están mostrando datos de respaldo desde envios.json."
    )
    with st.expander("Ver detalle de la conexión"):
        st.code(detalle_conexion)


# ==========================================================
# 7. INDICADORES GENERALES
# ==========================================================

# Número total de envíos
total_envios = len(df_original)

# Cantidad de envíos por estado
total_entregados = len(
    df_original[df_original["estado"] == "Entregado"]
)

total_camino = len(
    df_original[df_original["estado"] == "En camino"]
)

total_pendientes = len(
    df_original[df_original["estado"] == "Pendiente"]
)

total_preparacion = len(
    df_original[df_original["estado"] == "En preparación"]
)

# Creamos cinco columnas para mostrar las métricas
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    label="📦 Total de envíos",
    value=total_envios
)

col2.metric(
    label="✅ Entregados",
    value=total_entregados
)

col3.metric(
    label="🚚 En camino",
    value=total_camino
)

col4.metric(
    label="⏳ Pendientes",
    value=total_pendientes
)

col5.metric(
    label="🛠️ En preparación",
    value=total_preparacion
)

st.divider()


# ==========================================================
# 8. INDICADORES LOGÍSTICOS ADICIONALES
# ==========================================================

# Calculamos la cantidad total
cantidad_total_general = df_original["cantidad"].sum()

# Obtenemos el destino más frecuente
if not df_original.empty:
    destino_principal = df_original["destino"].mode().iloc[0]
    chofer_principal = df_original["chofer"].mode().iloc[0]
    vehiculo_principal = df_original["vehiculo"].mode().iloc[0]
else:
    destino_principal = "Sin datos"
    chofer_principal = "Sin datos"
    vehiculo_principal = "Sin datos"

st.subheader("Resumen logístico")

r1, r2, r3, r4 = st.columns(4)

r1.metric(
    "📦 Unidades totales",
    f"{cantidad_total_general:,.0f} unidades"
)

r2.metric(
    "📍 Destino frecuente",
    destino_principal
)

r3.metric(
    "👤 Chofer frecuente",
    chofer_principal
)

r4.metric(
    "🚛 Vehículo utilizado",
    vehiculo_principal
)

st.divider()


# ==========================================================
# 9. FILTROS DE BÚSQUEDA
# ==========================================================

st.subheader("🔎 Filtros de búsqueda")

filtro1, filtro2, filtro3 = st.columns(3)

# Filtro por estado
with filtro1:
    estado_seleccionado = st.selectbox(
        "Estado del envío",
        ["Todos"] + sorted(
            df_original["estado"].dropna().unique().tolist()
        )
    )

# Filtro por destino
with filtro2:
    destino_seleccionado = st.selectbox(
        "Destino",
        ["Todos"] + sorted(
            df_original["destino"].dropna().unique().tolist()
        )
    )

# Buscador por guía
with filtro3:
    guia_buscada = st.text_input(
        "Buscar por número de guía",
        placeholder="Ejemplo: ENV001"
    )


# Creamos una copia para aplicar los filtros
df_filtrado = df_original.copy()

# Aplicamos filtro por estado
if estado_seleccionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["estado"] == estado_seleccionado
    ]

# Aplicamos filtro por destino
if destino_seleccionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["destino"] == destino_seleccionado
    ]

# Aplicamos búsqueda por guía
if guia_buscada:
    df_filtrado = df_filtrado[
        df_filtrado["guia"].str.contains(
            guia_buscada,
            case=False,
            na=False
        )
    ]


# ==========================================================
# 10. TABLA DE ENVÍOS
# ==========================================================

st.subheader("📋 Listado de envíos")

st.caption(
    f"Registros encontrados: {len(df_filtrado)}"
)

# Renombramos las columnas solo para mostrarlas en pantalla
tabla_mostrar = df_filtrado.rename(
    columns={
        "guia": "Guía",
        "cliente": "Cliente",
        "destino": "Destino",
        "vehiculo": "Vehículo",
        "chofer": "Chofer",
        "estado": "Estado",
        "cantidad": "Cantidad",
        "fecha": "Fecha"
    }
)

st.dataframe(
    tabla_mostrar,
    use_container_width=True,
    hide_index=True
)

st.divider()


# ==========================================================
# 11. GRÁFICAS
# ==========================================================

st.subheader("📊 Indicadores gráficos")

# Solo mostramos gráficas cuando existen registros
if df_filtrado.empty:

    st.warning(
        "NO EXISTEN REGISTROS CON LA COINCIDENCIA DE LA BUSQUEDA."
    )

else:

    # ------------------------------------------------------
    # Gráfica 1: distribución por estado
    # ------------------------------------------------------

    conteo_estados = (
        df_filtrado["estado"]
        .value_counts()
        .reset_index()
    )

    conteo_estados.columns = [
        "Estado",
        "Cantidad"
    ]

    grafica_estado = px.pie(
        conteo_estados,
        names="Estado",
        values="Cantidad",
        title="Distribución de envíos por estado",
        hole=0.40
    )

    grafica_estado.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    # ------------------------------------------------------
    # Gráfica 2: cantidad por destino
    # ------------------------------------------------------

    conteo_destinos = (
        df_filtrado["destino"]
        .value_counts()
        .reset_index()
    )

    conteo_destinos.columns = [
        "Destino",
        "Cantidad"
    ]

    grafica_destinos = px.bar(
        conteo_destinos,
        x="Destino",
        y="Cantidad",
        title="Cantidad de envíos por destino",
        text="Cantidad"
    )

    grafica_destinos.update_traces(
        textposition="outside"
    )

    # Colocamos las primeras dos gráficas en dos columnas
    grafica_col1, grafica_col2 = st.columns(2)

    with grafica_col1:
        st.plotly_chart(
            grafica_estado,
            use_container_width=True
        )

    with grafica_col2:
        st.plotly_chart(
            grafica_destinos,
            use_container_width=True
        )

    # ------------------------------------------------------
    # Gráfica 3: cantidad transportada por destino
    # ------------------------------------------------------

    cantidad_destinos = (
        df_filtrado
        .groupby("destino", as_index=False)["cantidad"]
        .sum()
    )

    cantidad_destinos.columns = [
        "Destino",
        "Cantidad total"
    ]

    grafica_cantidad = px.bar(
        cantidad_destinos,
        x="Destino",
        y="Cantidad total",
        title="Cantidad transportada por destino",
        text="Cantidad total",
        labels={
            "Cantidad total": "Cantidad total"
        }
    )

    grafica_cantidad.update_traces(
        texttemplate="%{text:.0f} unidades",
        textposition="outside"
    )

    st.plotly_chart(
        grafica_cantidad,
        use_container_width=True
    )


st.divider()


# ==========================================================
# 12. RESUMEN DE LOS REGISTROS FILTRADOS
# ==========================================================

st.subheader("Resumen de la consulta")

cantidad_filtrada = df_filtrado["cantidad"].sum()
destinos_filtrados = df_filtrado["destino"].nunique()
clientes_filtrados = df_filtrado["cliente"].nunique()

resumen1, resumen2, resumen3 = st.columns(3)

resumen1.metric(
    "Registros mostrados",
    len(df_filtrado)
)

resumen2.metric(
    "Unidades mostradas",
    f"{cantidad_filtrada:,.0f} unidades"
)

resumen3.metric(
    "Clientes diferentes",
    clientes_filtrados
)

st.success(
    "Dashboard cargado y funcionando correctamente."
)


# ==========================================================
# 13. PIE DE PÁGINA
# ==========================================================

st.markdown(
    """
    <div class="pie-pagina">
        Proyecto ISC6 · Área 5 · Dashboard de Envíos
        <br>
        Versión 1.2 · 2026
    </div>
    """,
    unsafe_allow_html=True
)