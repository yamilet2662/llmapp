import streamlit as st  
from sentence_transformers import SentenceTransformer  
from llama_cpp import Llama  
import faiss  
import numpy as np  
import json  

# Título de la aplicación  
st.title("Asistente Virtual Basado en RAG")  
st.write("Interactúa con un modelo optimizado para responder preguntas en un dominio específico.")  

# Cargar el índice FAISS  
@st.cache_resource  
def load_faiss_index():  
    return faiss.read_index("base_mb.index")  

# Cargar la base de datos con textos indexados  
@st.cache_resource  
def load_database():  
    with open("base_datos_t.json", "r", encoding="utf-8") as f:  
        return json.load(f)  

# Cargar el modelo de embeddings  
@st.cache_resource  
def load_embed_model():  
    return SentenceTransformer('all-MiniLM-L6-v2')  

# Cargar el modelo Llama  
@st.cache_resource  
def load_llama_model():  
    return Llama(model_path="./Llama-3.2-3B-Promptist-Mini.Q4_K_M.gguf", n_ctx=2048)  

# Función para buscar en FAISS  
def search_faiss(query, index, data, embed_model, k=5):  
    query_embedding = embed_model.encode([query], convert_to_tensor=False)  
    query_embedding = np.array(query_embedding).astype('float32')  
    distances, indices = index.search(query_embedding, k)  
    results = [data[i] for i in indices[0] if i < len(data)]  
    return results  

# Generar respuesta con RAG  
def generate_response(query, index, data, embed_model, llm, top_k=5):  
    # Recuperar documentos relevantes  
    retrieved_docs = search_faiss(query, index, data, embed_model, k=top_k)  
    if not retrieved_docs:  
        return "No se encontraron documentos relevantes."  

    # Construir contexto con fragmentos relevantes  
    context = " ".join([doc['content'][:5000] for doc in retrieved_docs])  # Máx 500 caracteres por doc  

    # Crear prompt con contexto recuperado  
    input_text = f"""Contexto relevante: {context}  
    Pregunta: {query}  
    Responde de manera clara y precisa en un párrafo.  
    """  

    # Generar respuesta con el modelo Llama  
    response = llm.create_chat_completion(  
        messages=[{"role": "user", "content": input_text}]  
    )  

    return response["choices"][0]["message"]["content"]  

# Cargar recursos  
st.write("Cargando modelos y datos...")  
index = load_faiss_index()  
data = load_database()  
embed_model = load_embed_model()  
llm = load_llama_model()  
st.success("Modelos y datos cargados correctamente.")  

# Entrada del usuario  
user_query = st.text_input("Haz tu pregunta:", placeholder="Escribe tu consulta aquí...")  

# Botón para generar respuesta  
if st.button("Enviar"):  
    if user_query:  
        with st.spinner("Generando respuesta..."):  
            response = generate_response(user_query, index, data, embed_model, llm)  
        st.success("Respuesta generada:")  
        st.write(response)  
    else:  
        st.warning("Por favor, escribe una pregunta antes de enviar.")
