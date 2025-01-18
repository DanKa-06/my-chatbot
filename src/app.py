import streamlit as st
from langchain.llms import Ollama
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
import requests
from bs4 import BeautifulSoup
import os

def get_constitution_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        constitution_text = ""
        for p in soup.find_all('p'):
            constitution_text += p.text + "\n"
        return constitution_text.strip()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching constitution text: {e}")
        return None

try:
    llm = Ollama(model="llama2")
    embeddings = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")
except Exception as e:
    st.error(f"Error initializing Ollama or embeddings: {e}. Ensure Ollama is running and model is available.")
    llm = None
    embeddings = None

persist_directory = "db"
vectordb = None
qa = None

def initialize_qa(vectordb_to_use):
    global qa
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectordb_to_use.as_retriever())

def generate_response(prompt):
    if prompt.lower() == "hi":
        return "Hi. How can I help you?"
    try:
        if qa:
            response = qa.run(prompt)
            return response
        elif llm:
            return llm(prompt)
        else:
            return "Ollama model is not initialized. Please ensure Ollama is running."
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "An error occurred. Please try again."

def main():
    global vectordb
    st.title("Ollama Chatbot")

    constitution_url = "https://www.akorda.kz/en/constitution-of-the-republic-of-kazakhstan-50912"

    if embeddings is None or llm is None:
        st.error("Embeddings or LLM initialization failed. The application cannot run.")
        return

    if not os.path.exists(persist_directory):
        with st.spinner("Initializing with Constitution Text..."):
            constitution_text = get_constitution_text(constitution_url)
            if constitution_text:
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                docs = text_splitter.create_documents([constitution_text])
                vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)
                vectordb.persist()
                initialize_qa(vectordb)
                st.success("Database created using the Constitution text!")
            else:
                st.error("Failed to fetch constitution text.")
    elif vectordb is None:
        try:
            vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
            initialize_qa(vectordb)
        except Exception as e:
            st.error(f"Error loading existing database: {e}")

    uploaded_files = st.file_uploader("Upload text files", accept_multiple_files=True, type=["txt"])

    if uploaded_files:
        with st.spinner("Processing files..."):
            all_docs = []
            for uploaded_file in uploaded_files:
                try:
                    file_contents = uploaded_file.read().decode("utf-8")
                    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                    docs = text_splitter.create_documents([file_contents])
                    all_docs.extend(docs)
                    st.write(f"File '{uploaded_file.name}' successfully processed.")
                except Exception as e:
                    st.error(f"File processing error '{uploaded_file.name}': {e}")
            if all_docs:
                if vectordb is None:
                    vectordb = Chroma.from_documents(documents=all_docs, embedding=embeddings, persist_directory=persist_directory)
                    vectordb.persist()
                    st.info("New database created from uploaded files.")
                else:
                    vectordb.add_documents(all_docs)
                    vectordb.persist()
                    st.info("Files added to existing database.")
                initialize_qa(vectordb)

    user_input = st.text_input("Enter your question:", key="user_input")
    send_button_pressed = st.button("Send")

    if user_input and (send_button_pressed or st.session_state.get('user_input_submitted')):
        st.session_state['user_input_submitted'] = False
        with st.spinner('Generating response...'):
            response = generate_response(user_input)
        st.text_area("Answer:", value=response, height=200)

    if user_input and st.session_state.get('user_input_submitted') is None:
        st.session_state['user_input_submitted'] = False

    if user_input and st.session_state.get('user_input_submitted') is False:
        if st.session_state.get('user_input') != user_input:
            st.session_state['user_input'] = user_input
            st.session_state['user_input_submitted'] = True

if __name__ == "__main__":
    main()
