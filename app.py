import requests

# Reemplaza con la URL generada por Cloudflared en Colab
API_URL = " https://archives-rf-yo-bacteria.trycloudflare.com"

def assistant_app():
    st.title("🤖 Asistente Virtual con RAG")
    st.write(f"¡Bienvenido, {st.session_state.username}! Escribe tu pregunta y el modelo te responderá.")

    query = st.text_input("Escribe tu pregunta aquí:")

    if st.button("Consultar"):
        response = requests.post(API_URL, json={"text": query})
        respuesta = response.json().get("response", "Error en la respuesta")
        st.write(respuesta)

