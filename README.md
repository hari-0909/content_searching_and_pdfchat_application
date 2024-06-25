# content_searching_and_pdfchat_application
This project provides a web-based interface for searching text within PDF files. The solution integrates a PHP front-end for user interaction and a backend powered by Python scripts for searching text in PDFs and a Streamlit-based chat application to interact with the results.
# Features
- **Search PDFs**: Users can search for specific text within a folder of PDF documents.
- **Display Results**: Search results are displayed with checkboxes for users to select the files they want to interact with.
- **Chat Application**: A Streamlit-based app that allows users to ask questions based on the context of the selected PDFs using an AI model.
# Project Structure
- `index.php`: The main PHP file for the web interface.
- `search.py`: A Python script that searches for text within PDF files using the `PyMuPDF` library.
- `model.py`: A Python script using Streamlit to create a chat application for interacting with the content of selected PDF files.
# Requirements
# PHP
- PHP 7.x or higher
- COM extension enabled for Windows
# Python
- Python 3.10
- Required Python packages:
  - fitz (PyMuPDF)
  - streamlit
  - transformers
  - langchain_community
  - langchain_core
# Setup
# PHP Setup
1. Ensure PHP is installed and properly configured.
2. Enable COM extension in your `php.ini` file:
    ```ini
    extension=php_com_dotnet.dll
    ```
3. Place `index.php` in your web server's root directory.
# Python Setup
1. Install Python 3.10 if not already installed.
2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required Python packages:
    ```sh
    pip install fitz streamlit transformers langchain_community langchain_core
    ```
# Usage
1. **Start the Web Server**: Ensure your web server (e.g., Apache or Nginx) is running and properly configured to serve `index.php`.
2. **Search PDFs**: Open the web interface in your browser and enter the text to search within the PDFs.
3. **Select and Interact**: Select the desired PDFs from the search results and click the button to redirect to the chat application.
4. **Run the Chat Application**:
    ```sh
    streamlit run model.py
    ```
5. **Interact with PDFs**: In the Streamlit application, enter your query to interact with the content of the selected PDFs.
# Example Commands
# PHP Search Script Execution
The PHP script uses a shell command to call the Python script for searching PDFs:
```sh
C:\Users\inspi\AppData\Local\Programs\Python\Python310\python.exe search.py "path/to/pdf" "search_text"
```
# Streamlit Application
Start the Streamlit application:
```sh
streamlit run model.py
```
# Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request on GitHub.
