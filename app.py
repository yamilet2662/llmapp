import streamlit as st
import pyrebase4

# Configuración de Firebase
firebaseConfig = {
  "apiKey": "AIzaSyAICAjsaozpQzeqOpe_GcpChgU7f-_dcGc",
  "authDomain": "webapp-44ab7.firebaseapp.com",
  "projectId": "webapp-44ab7",
  "storageBucket": "webapp-44ab7.firebasestorage.app",
  "messagingSenderId": "425509769824",
  "appId": "1:425509769824:web:daee573e6e332b150f2905",
  "measurementId": "G-BRVS90CX5L"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Manejo de sesión en Streamlit
if "user" not in st.session_state:
    st.session_state["user"] = None

st.title("🤖 Asistente Virtual con LLM")

# Sección de Login / Registro
tab = st.radio("Selecciona una opción:", ["Iniciar Sesión", "Registrarse"])

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state["user"] = user
        st.success("Inicio de sesión exitoso ✅")
        st.rerun()
    except Exception as e:
        st.error("Error al iniciar sesión: " + str(e))

def register(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        st.success("Cuenta creada exitosamente 🎉. Ahora inicia sesión.")
    except Exception as e:
        st.error("Error al registrarse: " + str(e))

if st.session_state["user"] is None:
    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")
    
    if tab == "Iniciar Sesión":
        if st.button("Ingresar"):
            login(email, password)
    else:
        confirm_password = st.text_input("Confirmar Contraseña", type="password")
        if st.button("Registrarse"):
            if password == confirm_password:
                register(email, password)
            else:
                st.error("Las contraseñas no coinciden.")
else:
    st.success(f"Bienvenido {st.session_state['user']['email']} 👋")
    if st.button("Cerrar Sesión"):
        st.session_state["user"] = None
        st.rerun()

# Sección de Chat (solo visible si el usuario está autenticado)
if st.session_state["user"]:
    st.subheader("💬 Chat con el Asistente Virtual")
    user_input = st.text_input("Escribe tu mensaje:")
    if st.button("Enviar"):
        if user_input:
            st.write(f"🤖 Respuesta del asistente: {user_input[::-1]}")  # Simulación de respuesta
        else:
            st.error("Por favor, ingresa un mensaje.")
