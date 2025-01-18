# Ollama Chatbot

This Streamlit application provides a chatbot interface for querying information related to the Constitution of the Republic of Kazakhstan. It leverages the power of Ollama as the large language model (LLM), Sentence Transformers for generating text embeddings, and Chroma as a persistent vector database for efficient semantic search.

## Features

*   **Constitution-Aware Answering:** Answers questions specifically about the Constitution of Kazakhstan by retrieving relevant information from a vector database built from the Constitution's text.
*   **General Knowledge Answering:** Handles general knowledge questions using the LLM's built-in knowledge, even if the Constitution database hasn't been initialized or the question isn't directly related to the Constitution.
*   **Custom Document Upload (Optional):** Allows users to upload their own `.txt` files to extend the chatbot's knowledge base. Uploaded documents are processed and added to the vector database, enabling the chatbot to answer questions based on their content. (**Note:** Implement this feature if applicable to your code.)
*   **Persistent Database:** Uses a persistent Chroma database, meaning the processed Constitution text and uploaded documents (if enabled) are stored on disk. This avoids re-processing the data on every app restart, improving performance.
*   **Error Handling:** Includes robust error handling to gracefully manage issues like network problems during Constitution text retrieval, Ollama initialization failures, incorrect file uploads, and database loading errors.

## Installation

1.  **Clone the repository (if applicable):**

    ```bash
    git clone [repository_url] 
    ```

2.  **Create a virtual environment (highly recommended):** This isolates project dependencies.

    ```bash
    python -m venv venv       
    venv\Scripts\activate       
    ```

3.  **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```


4.  **Install and run Ollama:** Follow the instructions on the [Ollama website](https://ollama.ai/) to install Ollama. Download a suitable model (e.g., `llama2`) using the Ollama CLI:

    ```bash
    ollama pull llama2
    ```

    **Important:** Ensure Ollama is running before launching the application. You can check if it's running by trying `ollama list` in your terminal.

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2.  **Interact with the chatbot:** Once the application is running in your web browser, you can type your questions in the text input field and press "Send" to get responses.

## Examples

Here are some examples of how you can interact with the chatbot:

*   **Constitution-specific questions:**
    *   What are the fundamental rights enshrined in the Constitution of Kazakhstan?
    *   What does the Constitution say about the role of the President?
    *   What are the procedures for amending the Constitution?
*   **General knowledge questions (if no Constitution database is present or the question is unrelated):**
    *   What is the capital of France?
    *   Who painted the Mona Lisa?
    *   How many planets are in our solar system?
*   **Custom document upload (if implemented):**
    *   Upload a text file containing a company policy document and ask: "What are the conditions for taking a leave of absence?"
    *   Upload a product description file and ask: "What are the key features of this product?"

The chatbot will use its knowledge and the available databases (Constitution and uploaded documents, if enabled) to provide informative answers. If the database hasn't been created yet, the bot will attempt to answer using only the Ollama LLM's built-in knowledge.

## Project Structure (for Developers)

*   `app.py`: The main Streamlit application file. Contains the logic for handling user input, generating responses using Ollama, and interacting with the Chroma vector database.
*   `requirements.txt`: A list of Python package dependencies.
*   `README.md`: This file (project description).
*   `LICENSE`: The file containing the project's license (e.g., MIT License).
*   `test.py` (optional): A file containing unit tests for the application.
*   `db` (created automatically): The directory where the Chroma database is stored.

## Error Handling

The application includes error handling for the following scenarios:

*   **Failed Constitution Retrieval:** If the application cannot fetch the Constitution text from the URL, an error message will be displayed in the Streamlit interface.
*   **Ollama/Embeddings Initialization Errors:** If there is an issue initializing Ollama or the Sentence Transformer embeddings (e.g., Ollama is not running, incorrect model name), an error message will be displayed.
*   **File Processing Errors:** If there is a problem processing a user-uploaded file (e.g., incorrect file format, encoding issues), an error message indicating the specific file and the error will be shown.
*   **Database Loading Errors:** If there is an error while trying to load an existing Chroma database (e.g., corrupted database files), an error message will be shown.

## License

This project is licensed under the MIT License (see the `LICENSE` file for details). Replace `(see the LICENSE file for details)` with a direct link to your license if hosted online.

## Author

[Dana Otepova]
