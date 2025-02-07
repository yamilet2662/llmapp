import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Configurar Firebase
cred = credentials.Certificate("path/to/serviceAccountKey.json")  # 🔹 Asegúrate de subir tu JSON de credenciales
firebase_admin.initialize_app(cred)

# Función para autenticar usuarios
def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        st.success(f"Bienvenido {user.email} ✅")
    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")
