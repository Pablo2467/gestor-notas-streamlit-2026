import streamlit as st
st.set_page_config(page_title="Calculadora IMC", page_icon="궬궨궭궮궯")
st.title("Calculadora de IMC")

sexo = st.selectbox("Sexo", ["Hombre", "Mujer"])
peso = st.number_input("Peso (kg)", min_value=1.0, value=70.0)
estatura = st.number_input("Estatura (m)", min_value=0.5, value=1.70)

if st.button("Calcular IMC"):
    imc = peso / (estatura ** 2)
    if imc < 18.5:
        estado = "Bajo peso"
    elif imc < 25:
        estado = "Peso normal"
    elif imc < 30:
        estado = "Sobrepeso"
    else:
        estado = "Obesidad"
    st.metric("IMC", f"{imc:.2f}")
    st.success(f"Clasificación: {estado}")
    st.caption(f"Sexo registrado: {sexo}") 