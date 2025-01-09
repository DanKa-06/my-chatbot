# Ollama Chatbot

This project is a chatbot powered by Ollama and Streamlit. It allows users to upload multiple text files (.txt) and ask questions about their content.

## Project Files:

*   `app.py`: The main Streamlit application file. Contains the logic for handling user input, generating responses using Ollama, and interacting with the Chroma vector database.
*   `requirements.txt`: A list of Python package dependencies.
*   `README.md`: This file (project description).

## Dependencies:

*   `streamlit`
*   `langchain`
*   `langchain_community`
*   `chromadb`
*   `ollama`

## Installation:

1.  Make sure you have Python 3.8 or higher installed.
2.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  Install and run Ollama. Download the `llama2` model:

    ```bash
    ollama pull llama2
    ```

## Running the application:

1.  Navigate to the project directory in your terminal.
2.  Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## How to use:

1.  Upload one or more `.txt` files using the file uploader.
2.  Wait for the files to be processed and added to the knowledge base. A success message will be displayed.
3.  Enter your question in the text input field.
4.  Click the "Send" button or press Enter to submit your question.
5.  The bot's response will be displayed below.



## Error Handling:

The application includes basic error handling for Ollama initialization, file processing, and response generation. Error messages will be displayed in the Streamlit interface.

## Contributing:

Contributions are welcome! Please open an issue or submit a pull request.

## License:

(LICENSE.txt)

## Author:

Dana Otepova
