import streamlit as st
import pandas as pd
import plotly.express as px

import database as db

st.set_page_config(page_title="Gestor Académico de Notas", page_icon="📚", layout="wide")
db.crear_tablas()


def calcular_nota_corte(actividades):
    """Nota del corte = Σ (nota de actividad × porcentaje de actividad / 100)."""
    return sum(nota * porcentaje / 100 for (_, _, porcentaje, nota) in actividades)


def calcular_porcentaje_evaluado_corte(actividades):
    """Qué tanto del 100% del corte ya tiene actividades registradas (tope 100)."""
    suma = sum(porcentaje for (_, _, porcentaje, _) in actividades)
    return min(suma, 100)


def calcular_resumen_asignatura(asignatura_id):
    """
    Devuelve: nota_acumulada, porcentaje_evaluado_total (0-100), es_final (bool)
    """
    cortes = db.obtener_cortes(asignatura_id)
    nota_acumulada = 0.0
    porcentaje_evaluado_total = 0.0

    for (corte_id, numero, porcentaje_corte) in cortes:
        actividades = db.obtener_actividades(corte_id)
        nota_corte = calcular_nota_corte(actividades)
        aporte_corte = nota_corte * porcentaje_corte / 100
        nota_acumulada += aporte_corte

        pct_evaluado_corte = calcular_porcentaje_evaluado_corte(actividades)
        porcentaje_evaluado_total += porcentaje_corte * (pct_evaluado_corte / 100)

    es_final = porcentaje_evaluado_total >= 99.99
    return round(nota_acumulada, 2), round(porcentaje_evaluado_total, 1), es_final


st.sidebar.title("📚 Gestor Académico")
seccion = st.sidebar.radio(
    "Navegación",
    ["Dashboard", "Asignaturas", "Configuración de cortes", "Actividades y notas"]
)

if seccion == "Dashboard":
    st.title("Dashboard")

    asignaturas = db.obtener_asignaturas()

    if not asignaturas:
        st.info("Todavía no hay asignaturas registradas. Ve a la sección 'Asignaturas' para crear la primera.")
    else:
        filas_resumen = []
        for (asignatura_id, nombre) in asignaturas:
            nota, pct_evaluado, es_final = calcular_resumen_asignatura(asignatura_id)
            filas_resumen.append({
                "Asignatura": nombre,
                "Nota": nota,
                "% Evaluado": pct_evaluado,
                "Estado": "Final" if es_final else "Parcial"
            })

        df_resumen = pd.DataFrame(filas_resumen)
        promedio_general = round(df_resumen["Nota"].mean(), 2)

        columnas = st.columns(3)
        columnas[0].metric("Promedio general", promedio_general)
        columnas[1].metric("Asignaturas registradas", len(asignaturas))
        columnas[2].metric(
            "Asignaturas finalizadas",
            int((df_resumen["Estado"] == "Final").sum())
        )

        st.subheader("Detalle por asignatura")
        st.dataframe(df_resumen, use_container_width=True)

        fig = px.bar(
            df_resumen,
            x="Asignatura",
            y="Nota",
            color="Estado",
            title="Nota acumulada / final por asignatura",
            range_y=[0, 5],
            color_discrete_map={"Final": "#1B4D3E", "Parcial": "#C0392B"}
        )
        st.plotly_chart(fig, use_container_width=True)



elif seccion == "Asignaturas":
    st.title("Asignaturas")

    with st.form("form_nueva_asignatura", clear_on_submit=True):
        nombre_nueva = st.text_input("Nombre de la asignatura")
        enviado = st.form_submit_button("Crear asignatura")

        if enviado:
            if not nombre_nueva.strip():
                st.error("El nombre de la asignatura no puede estar vacío.")
            else:
                db.crear_asignatura(nombre_nueva.strip())
                st.success(f"Asignatura '{nombre_nueva}' creada con sus 3 cortes iniciales.")
                st.rerun()

    st.subheader("Asignaturas registradas")
    asignaturas = db.obtener_asignaturas()
    if asignaturas:
        st.dataframe(
            pd.DataFrame(asignaturas, columns=["ID", "Nombre"]),
            use_container_width=True
        )
    else:
        st.info("Aún no has creado ninguna asignatura.")


elif seccion == "Configuración de cortes":
    st.title("Configuración de cortes")

    asignaturas = db.obtener_asignaturas()
    if not asignaturas:
        st.info("Primero crea una asignatura en la sección 'Asignaturas'.")
    else:
        nombres_asignaturas = {nombre: aid for (aid, nombre) in asignaturas}
        nombre_seleccionado = st.selectbox("Selecciona una asignatura", list(nombres_asignaturas.keys()))
        asignatura_id = nombres_asignaturas[nombre_seleccionado]

        cortes = db.obtener_cortes(asignatura_id)

        st.write("Define el porcentaje de cada corte. La suma de los tres debe ser 100%.")

        valores_porcentaje = {}
        for (corte_id, numero, porcentaje_actual) in cortes:
            valores_porcentaje[corte_id] = st.number_input(
                f"Corte {numero} (%)",
                min_value=0.0, max_value=100.0,
                value=float(porcentaje_actual),
                step=1.0,
                key=f"corte_{corte_id}"
            )

        suma_total = sum(valores_porcentaje.values())
        st.caption(f"Suma actual: {suma_total:.1f}%")

        if st.button("Guardar porcentajes"):
            if abs(suma_total - 100) > 0.01:
                st.error(f"La suma de los tres cortes debe ser exactamente 100%. Suma actual: {suma_total:.1f}%")
            else:
                for corte_id, porcentaje in valores_porcentaje.items():
                    db.actualizar_porcentaje_corte(corte_id, porcentaje)
                st.success("Porcentajes guardados correctamente.")
                st.rerun()


elif seccion == "Actividades y notas":
    st.title("Actividades y notas")

    asignaturas = db.obtener_asignaturas()
    if not asignaturas:
        st.info("Primero crea una asignatura en la sección 'Asignaturas'.")
    else:
        nombres_asignaturas = {nombre: aid for (aid, nombre) in asignaturas}
        nombre_seleccionado = st.selectbox("Asignatura", list(nombres_asignaturas.keys()))
        asignatura_id = nombres_asignaturas[nombre_seleccionado]

        cortes = db.obtener_cortes(asignatura_id)
        opciones_corte = {f"Corte {numero} ({porcentaje}%)": corte_id for (corte_id, numero, porcentaje) in cortes}
        etiqueta_corte = st.selectbox("Corte", list(opciones_corte.keys()))
        corte_id = opciones_corte[etiqueta_corte]

        actividades = db.obtener_actividades(corte_id)
        suma_porcentaje_actual = sum(p for (_, _, p, _) in actividades)

        st.subheader("Actividades registradas en este corte")
        if actividades:
            df_actividades = pd.DataFrame(
                actividades, columns=["ID", "Nombre", "% Actividad", "Nota"]
            )
            st.dataframe(df_actividades, use_container_width=True)
        else:
            st.info("Este corte todavía no tiene actividades.")

        st.caption(f"Porcentaje ya asignado en este corte: {suma_porcentaje_actual:.1f}% de 100%")

        st.subheader("Agregar nueva actividad")
        with st.form("form_nueva_actividad", clear_on_submit=True):
            nombre_actividad = st.text_input("Nombre de la actividad")
            porcentaje_actividad = st.number_input(
                "Porcentaje dentro del corte (%)",
                min_value=0.0, max_value=100.0, value=0.0, step=1.0
            )
            nota_actividad = st.number_input(
                "Nota (0.0 a 5.0)",
                min_value=0.0, max_value=5.0, value=0.0, step=0.1
            )
            enviado = st.form_submit_button("Guardar actividad")

            if enviado:
                if not nombre_actividad.strip():
                    st.error("El nombre de la actividad no puede estar vacío.")
                elif porcentaje_actividad <= 0:
                    st.error("El porcentaje debe ser mayor a 0.")
                elif suma_porcentaje_actual + porcentaje_actividad > 100:
                    st.error(
                        f"No puedes agregar esta actividad: el corte ya tiene {suma_porcentaje_actual:.1f}% "
                        f"asignado y esta actividad sumaría {suma_porcentaje_actual + porcentaje_actividad:.1f}%."
                    )
                else:
                    db.crear_actividad(corte_id, nombre_actividad.strip(), porcentaje_actividad, nota_actividad)
                    st.success(f"Actividad '{nombre_actividad}' guardada.")
                    st.rerun()