import streamlit as st
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
import os

try:
    llm = Ollama(model="llama2")
    embeddings = OllamaEmbeddings()
except Exception as e:
    st.error(f"Error initializing Ollama: {e}. Make sure Ollama is running and the model is available.")
    st.stop()

persist_directory = "db"
vectordb = None 

if os.path.exists(persist_directory): 
    try:
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    except Exception as e: 
        st.error(f"Database loading error: {e}")
        st.stop()
else:
    vectordb = Chroma.from_documents(documents=[], embedding=embeddings, persist_directory=persist_directory)
    st.info("New database created.")
    vectordb.persist() 


if vectordb is None: 
    st.error("Failed to initialise database.")
    st.stop()

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectordb.as_retriever())

def generate_response(prompt):
    if prompt.lower() == "hi":
        prompt = "To the greeting 'hi' answer: 'Hi. How can I help you?'"
    try:
        response = qa.run(prompt)
        return response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "An error occurred. Please try again."

def main():
    st.title("Ollama Chatbot")

    uploaded_files = st.file_uploader("Upload text files", accept_multiple_files=True, type=["txt"])

    if uploaded_files:
        with st.spinner("File Processing..."):
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
                vectordb.add_documents(all_docs)
                vectordb.persist()
                st.success("Files added to knowledge base!")

    user_input = st.text_input("Enter your question:", key="user_input")
    send_button_pressed = st.button("Send")

    if user_input and (send_button_pressed or st.session_state.get('user_input_submitted')):
        st.session_state['user_input_submitted'] = False
        with st.spinner('Generating a response...'):
            response = generate_response(user_input)
        st.text_area("Bot:", value=response, height=200)

    if user_input and st.session_state.get('user_input_submitted') is None:
        st.session_state['user_input_submitted'] = False

    if user_input and st.session_state.get('user_input_submitted') is False:
        if st.session_state.get('user_input') != user_input:
            st.session_state['user_input'] = user_input
            st.session_state['user_input_submitted'] = True


if __name__ == "__main__":
    main()
