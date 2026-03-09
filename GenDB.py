import streamlit as st
import pandas as pd
import sqlite3
import time
import os
import glob
from sqlalchemy import create_engine, inspect
import google.generativeai as genai

# ─── Auto-generate databases if they don't exist ───
def ensure_databases():
    db_dir = os.path.dirname(os.path.abspath(__file__))
    # Generate product_offers.db
    if not os.path.exists(os.path.join(db_dir, "product_offers.db")):
        import subprocess, sys
        subprocess.run([sys.executable, os.path.join(db_dir, "offer db.py")], cwd=db_dir)
    # Generate company.db
    if not os.path.exists(os.path.join(db_dir, "company.db")):
        import subprocess, sys
        subprocess.run([sys.executable, os.path.join(db_dir, "company.py")], cwd=db_dir)

ensure_databases()


st.set_page_config(page_title="GenDB", layout="wide", initial_sidebar_state="expanded")

# ─── Custom Dark Theme CSS ───
st.markdown("""
    <style>
    body {
        background-color: #202124;
        color: #e8eaed;
    }
    .main {
        background-color: #202124;
        color: #e8eaed;
    }
    pre code {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-x: auto;
        background-color: #2a2b2d !important;
        color: #e8eaed !important;
        border-radius: 8px;
        padding: 1rem;
    }
    .stApp {
        background-color: #202124;
    }
    .stSidebar {
        background-color: #303134;
    }
    h1, h2, h3, h4 {
        color: #8ab4f8;
    }
    .stButton > button {
        background-color: #8ab4f8;
        color: black;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #669df6;
        color: black;
    }
    .stTextInput input {
        background-color: #3c4043;
        color: white;
        border-radius: 6px;
    }
    .stJson {
        background-color: #303134;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 1rem;
    }
    .stCodeBlock {
        background-color: #2a2b2d;
        color: #e8eaed;
    }
    .stDataFrame {
        background-color: #2a2b2d;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ─── Gemini API Configuration ───
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ─── Utility: Get schema from SQLite ───
def get_sqlite_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema[table_name] = columns
    conn.close()
    return schema

# ─── Utility: Get schema from PostgreSQL ───
def get_postgres_schema(engine):
    inspector = inspect(engine)
    schema = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        pk_cols = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
        schema[table_name] = [
            (col["name"], col["name"] in pk_cols) for col in columns
        ]
    return schema

# ─── Generate SQL from Gemini ───
def get_sql_from_gemini(question, schema):
    schema_text = "\n".join([
        f"{table}: {', '.join([f'{col[0]}{" (PK)" if len(col) > 1 and col[1] else ""}' for col in cols])}"
        for table, cols in schema.items()
    ])
    prompt = f"""
You are a professional SQL assistant.

Given the following database schema:
{schema_text}

Write a valid SQL query for this question:
{question}

Only return the SQL query without any explanation or formatting.
"""
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    response = model.generate_content(prompt)
    return response.text.replace("```sql", "").replace("```", "").strip()

# ─── Session State ───
if "connected" not in st.session_state:
    st.session_state.connected = False
if "engine" not in st.session_state:
    st.session_state.engine = None
if "schema" not in st.session_state:
    st.session_state.schema = {}


# ─── Show Welcome Animation Only Once ───
if "animation_shown" not in st.session_state:
    st.session_state.animation_shown = False

if not st.session_state.animation_shown:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
            .big-font {
                font-size:50px !important;
                color: #4285F4;
                text-align: center;
                margin-top: 100px;
            }
            </style>
            <div class="big-font">Welcome to AI SQL Studio ✨</div>
        """, unsafe_allow_html=True)
        time.sleep(2)
    placeholder.empty()
    st.session_state.animation_shown = True

# ─── Sidebar: DB Selection ───
st.sidebar.title("Database Connection")
db_type = st.sidebar.selectbox("Choose Database Type", ["SQLite", "PostgreSQL"])

# ─── PostgreSQL Config ───
if db_type == "PostgreSQL":
    st.sidebar.subheader("PostgreSQL Configuration")
    pg_user = st.sidebar.text_input("Username", value="postgres")
    pg_password = st.sidebar.text_input("Password", type="password")
    pg_host = st.sidebar.text_input("Host", value="localhost")
    pg_port = st.sidebar.text_input("Port", value="5432")
    pg_db = st.sidebar.text_input("Database", value="hospital")

    if st.sidebar.button("Connect to PostgreSQL"):
        try:
            db_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
            engine = create_engine(db_url)
            with engine.connect():
                schema = get_postgres_schema(engine)
                st.session_state.connected = True
                st.session_state.engine = engine
                st.session_state.schema = schema
                st.success("✅ Connected to PostgreSQL database!")
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")

# ─── SQLite Config ───
elif db_type == "SQLite":
    st.sidebar.subheader("SQLite Configuration")
    db_dir = os.path.dirname(os.path.abspath(__file__))
    available_dbs = sorted(glob.glob(os.path.join(db_dir, "*.db")))
    db_names = [os.path.basename(db) for db in available_dbs]
    if not db_names:
        st.sidebar.warning("No .db files found in the project directory.")
        db_file = None
    else:
        db_file = st.sidebar.selectbox("Choose SQLite File", db_names)
    if st.sidebar.button("Connect to SQLite"):
        try:
            raw_schema = get_sqlite_schema(db_file)
            formatted_schema = {}
            for table, columns in raw_schema.items():
                formatted_schema[table] = [
                    (col[1], col[5] == 1) for col in columns  # col[5] == 1 means PRIMARY KEY
                ]
            st.session_state.connected = True
            st.session_state.engine = db_file
            st.session_state.schema = formatted_schema
            st.success("✅ Connected to SQLite database!")
        except Exception as e:
            st.error(f"❌ Failed to connect to SQLite: {e}")

# ─── Main UI ───
st.title("GenDB: SQL Assistant")
st.caption("Powered by Google Gemini | Natural Language to SQL")
if st.session_state.connected:
    if st.button("🔍 View Schema"):
        formatted = {
            table: [
                f"{col} (PK)" if is_pk else col
                for col, is_pk in cols
            ]
            for table, cols in st.session_state.schema.items()
        }
        st.json(formatted)

    question = st.text_input("Ask your database question:")

    if st.button("Generate SQL and Run"):
        with st.spinner("Generating SQL and executing..."):
            sql = get_sql_from_gemini(question, st.session_state.schema)
            st.code(sql, language="sql")
            try:
                if db_type == "SQLite":
                    conn = sqlite3.connect(st.session_state.engine)
                    df = pd.read_sql_query(sql, conn)
                    conn.close()
                else:
                    df = pd.read_sql_query(sql, st.session_state.engine)
                st.success("✅ Query executed successfully!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"❌ Error executing query: {e}")

# ─── Sidebar Footer ───
st.sidebar.markdown("""
    <hr style='border-top: 1px solid #555;' />
    <div style='text-align: center; padding-top: 10px; color: #888; font-size: 0.9em;'>
        Developed by <b>Team Vikings</b> 
    </div>
""", unsafe_allow_html=True)