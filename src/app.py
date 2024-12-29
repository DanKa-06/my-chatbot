import streamlit as st
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

try:
  llm = Ollama(model="llama2")
  embeddings = OllamaEmbeddings()
except Exception as e:
  st.error(f"Error initializing Ollama: {e}. Make sure Ollama is running and the model is available.")
  st.stop()

persist_directory = "db"

try:
  vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
except ValueError:
  vectordb = Chroma.from_documents(documents=[], embedding=embeddings, persist_directory=persist_directory)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectordb.as_retriever())

def generate_response(prompt):
  try:
    response = qa.run(prompt)
    return response
  except Exception as e:
    st.error(f"Error generating response: {e}")
    return "An error occurred. Please try again."

def main():
  st.title("Ollama Chatbot")

  user_input = st.text_input("Введите ваше сообщение:")

  if user_input:
    with st.spinner('Generating response...'):
      response = generate_response(user_input)
    st.text_area("Бот:", value=response, height=200)

if __name__ == "__main__":
  main()