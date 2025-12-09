import streamlit as st
import google.generativeai as genai
import os

# Título de la App
st.title("Mi App con Gemini 🚀")

# 1. Configuración de la API Key (OJO: Esto se conecta a los "Secretos" de Streamlit)
# No pongas tu clave real aquí directamente en el código.
api_key = st.secrets["GEMINI_API_KEY"] 

# 2. Configurar el modelo
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # Puedes usar 'gemini-pro' también

# 3. Interfaz de usuario (Input)
user_input = st.text_input("Pregúntale algo a tu IA:", placeholder="Escribe aquí...")

# 4. Lógica de respuesta
if st.button("Enviar"):
    if user_input:
        try:
            response = model.generate_content(user_input)
            st.write("### Respuesta de Gemini:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor escribe algo.")
