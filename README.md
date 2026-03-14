# GenDB: AI SQL Assistant

GenDB is a Streamlit-based application that converts natural language questions into SQL queries using Google Gemini AI. It supports both SQLite and PostgreSQL databases.

## Prerequisites

- Python 3.8 or higher

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Senthil-Achievements/gendb.git
   cd gendb
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Gemini API key:**

   Create a `.streamlit/secrets.toml` file in the project directory:

   ```toml
   GEMINI_API_KEY = "your-gemini-api-key-here"
   ```

## Running the Application

```bash
streamlit run GenDB.py
```

The application will open in your default web browser. From there you can:

- Connect to a **SQLite** database (sample databases are auto-generated on first run)
- Connect to a **PostgreSQL** database by providing connection details
- Ask natural language questions about your data and get SQL queries generated automatically
