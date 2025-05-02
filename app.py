import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests

# Configurar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Función para autenticar usuarios
def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        st.session_state["user"] = user.uid  # Guardar sesión con UID en lugar de email
        st.success("Inicio de sesión exitoso ✅")
    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")

# Función para cerrar sesión
def logout():
    st.session_state["user"] = None
    st.session_state["chat_history"] = []  # Limpiar historial al cerrar sesión
    st.rerun()

# ✅ Función corregida para enviar pregunta al modelo en Hugging Face Spaces
def ask_model(question):
    API_URL = "https://yamilet26-BioMet.hf.space/chat"
    
    try:
        response = requests.post(API_URL, json={"query": question})
        
        if response.status_code != 200:
            return f"⚠️ Error en la API: {response.status_code} - {response.reason}"
        
        data = response.json()
        return data.get("response", "⚠️ Error en la respuesta del modelo.")
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error de conexión con la API: {e}"


# Diseño mejorado
st.title("BIENVENID@ A BIOMET")

# Verificar si el usuario ha iniciado sesión
if "user" not in st.session_state or not st.session_state["user"]:
    st.subheader("🔐 Inicio de Sesión")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        login(email, password)
else:
    st.subheader("👋 Conversemos:")
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    for chat in st.session_state["chat_history"]:
        with st.chat_message("user"):
            st.markdown(chat["user"])
        with st.chat_message("bot"):
            st.markdown(chat["bot"])
    
    # ✅ Procesar solo una vez la pregunta
    question = st.chat_input("Escribe tu mensaje...")
    if question:
        with st.chat_message("user"):
            st.markdown(question)
        
        with st.spinner("Pensando..."):
            answer = ask_model(question)  # Se obtiene la respuesta
            
        with st.chat_message("bot"):
            st.markdown(answer)  # Asegura que se muestre la respuesta en el chat
        
        # ✅ Evitar duplicados en el historial
        if not any(chat["user"] == question and chat["bot"] == answer for chat in st.session_state["chat_history"]):
            st.session_state["chat_history"].append({"user": question, "bot": answer})
    
    # Botón para cerrar sesión
    if st.button("Cerrar sesión"):
        logout()

