import streamlit as st
import pymongo
from pymongo import MongoClient
import numpy as np
import ollama
import json

# Подключение к базе данных (MongoDB для векторного поиска)
client = MongoClient("mongodb://localhost:27017/")
db = client["constitution_db"]
collection = db["vectors"]

st.set_page_config(page_title="AI Constitution Chatbot", page_icon="📜", layout="wide")

# Выбор модели Ollama
MODEL_NAME = "llama3.2:1b"

# Функция генерации эмбеддингов через Ollama
def generate_embedding(text):
    response = ollama.embeddings(model=MODEL_NAME, prompt=text)
    return response["embedding"]

# Функция загрузки и обработки файлов
def process_uploaded_file(uploaded_file):
    file_contents = uploaded_file.read().decode("utf-8")
    document_vector = generate_embedding(file_contents)
    doc_id = str(hash(file_contents))
    collection.insert_one({"text": file_contents, "embedding": document_vector, "doc_id": doc_id})
    return "✅ File processed successfully!"

# Multi-Query для RAG Fusion
def generate_multi_queries(query):
    variations = [query, f"Explain {query} in detail", f"Summarize {query}"]
    return variations

# Поиск релевантных статей (RAG Fusion + Multi Query)
def search_articles_rag_fusion(query):
    queries = generate_multi_queries(query)
    aggregated_results = []
    for q in queries:
        query_embedding = np.array(generate_embedding(q))
        articles = list(collection.find())
        results = []
        for article in articles:
            article_embedding = np.array(article.get("embedding", []))
            if len(article_embedding) > 0:
                similarity = np.dot(query_embedding, article_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(article_embedding)
                )
                results.append((similarity, article))
        results.sort(reverse=True, key=lambda x: x[0])
        aggregated_results.extend([result[1] for result in results[:3]])
    return aggregated_results[:3]

# Функция обработки вопросов пользователя
def ask_ollama(query, context):
    combined_context = "\n\n".join([f"{doc['text']}" for doc in context])
    prompt = (
        "You are an AI assistant specializing in the Constitution of Kazakhstan. "
        "Your task is to provide factual, informative, and structured answers based on the provided context. "
        "Use only the given context and avoid making assumptions.\n\n"
        f"### Context ###\n{combined_context}\n\n"
        f"### Question ###\n{query}\n\n"
        "### Answer ###"
    )
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        if isinstance(response, str):
            response = json.loads(response)
        answer = response.get("message") or response.get("content") or "⚠️ Ошибка: Model refused to answer."
        return answer
    except json.JSONDecodeError:
        return "⚠️ Ошибка: Unable to parse JSON response."
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)}"

# Интерфейс Streamlit
st.sidebar.title("Search Constitution")
search_query = st.sidebar.text_input("Search in Constitution")
if st.sidebar.button("Search"):
    if search_query.strip():
        results = search_articles_rag_fusion(search_query)
        st.sidebar.write("Search Results:")
        for article in results:
            st.sidebar.markdown(f"- {article['text'][:200]}...")

st.sidebar.title("Upload Documents")
uploaded_files = st.sidebar.file_uploader("Upload files", accept_multiple_files=True, type=["txt", "pdf"], help="Upload text or PDF files.")
if uploaded_files:
    for uploaded_file in uploaded_files:
        message = process_uploaded_file(uploaded_file)
        st.sidebar.success(message)

st.title("Constitution AI Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask a question about the Constitution:")
if st.button("Send"):
    if user_input.strip():
        st.session_state["messages"].append({"user": "You", "content": user_input})
        results = search_articles_rag_fusion(user_input)
        bot_response = ask_ollama(user_input, results)
        st.session_state["messages"].append({"user": "Bot", "content": bot_response})

for message in st.session_state["messages"]:
    st.chat_message("user" if message["user"] == "You" else "assistant").markdown(message["content"])

st.sidebar.subheader("Database Content")
total_documents = collection.count_documents({})
st.sidebar.write(f"Total documents in database: {total_documents}")
