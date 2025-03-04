
```markdown
# Code Assistant and Chat using Streamlit and LangChain

This project is a web application built with Streamlit that utilizes LangChain and Groq to analyze code or convert ideas into code. It also allows users to save and view previous conversations.

## Features

- Enter code to be analyzed.
- Convert descriptions or ideas into code.
- Save and view previous conversations.
- Store analysis results in an SQLite database.
- Display previous conversations in the sidebar.
- Start a new conversation at any time.

## Requirements

Before running the app, ensure you have the following installed:

- Python 3.x
- Streamlit
- LangChain
- Groq API
- peewee (for database management)
- python-dotenv

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/code-assistant.git
   cd code-assistant
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Running the App

1. After setting up the environment, run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501` to access the app.

## How to Use

1. On the homepage, you can either enter code for analysis or describe an idea to convert into code.
2. Once you enter the text, the app will analyze the code or convert the idea into code using the Groq model.
3. Previous conversations will be saved in the database and can be viewed in the sidebar.
4. You can switch between previous conversations or start a new conversation at any time.

## Project Structure

```
.
├── app.py                # Main Streamlit app
├── .env                  # Environment file for API keys
├── code_analysis.db      # SQLite database to store analysis results
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Requirements

Make sure to install the following Python packages:

```txt
streamlit
langchain
groq
peewee
python-dotenv
```

You can install them using:

```bash
pip install -r requirements.txt
```

Make sure to update the `git clone` link with your actual GitHub username. You can also add or modify sections to fit your specific needs.
