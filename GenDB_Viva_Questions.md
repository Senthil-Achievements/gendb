# GenDB: SQL Assistant — Viva Questions & Answers

---

## 1. What is GenDB?
**Answer:** GenDB is an AI-powered SQL assistant built using Streamlit and Google Gemini. It allows users to ask natural language questions about a database, which are then converted into SQL queries and executed automatically.

---

## 2. What technologies are used in this project?
**Answer:** The project uses Python, Streamlit (for the web UI), Google Gemini API (for AI-based SQL generation), SQLite and PostgreSQL (as supported databases), SQLAlchemy (for PostgreSQL schema inspection), Pandas (for displaying query results), and Faker (for generating sample data).

---

## 3. What is Streamlit and why was it chosen for this project?
**Answer:** Streamlit is an open-source Python framework for building data-driven web applications quickly. It was chosen because it allows rapid prototyping of interactive UIs with minimal frontend code, making it ideal for a data/AI project like GenDB.

---

## 4. What is the role of Google Gemini API in this project?
**Answer:** The Google Gemini API is used to convert natural language questions into valid SQL queries. The app sends the user's question along with the database schema to Gemini, which generates the corresponding SQL query.

---

## 5. What Gemini model is used in this project?
**Answer:** The project uses the `gemini-2.5-flash-preview-04-17` model from Google's Generative AI library.

---

## 6. How is the API key managed in the deployed version?
**Answer:** The API key is stored securely using Streamlit's Secrets Management (`st.secrets["GEMINI_API_KEY"]`) instead of being hardcoded, ensuring it is not exposed in the source code or public repository.

---

## 7. What databases does GenDB support?
**Answer:** GenDB supports two types of databases: SQLite (file-based) and PostgreSQL (server-based). Users can choose the database type from the sidebar.

---

## 8. How does the application connect to a SQLite database?
**Answer:** The app uses Python's built-in `sqlite3` module to connect to a `.db` file. The available database files are dynamically listed from the project directory using `glob`.

---

## 9. How does the application connect to a PostgreSQL database?
**Answer:** It uses SQLAlchemy's `create_engine()` function with a connection URL constructed from user-provided credentials (host, port, username, password, and database name).

---

## 10. What is SQLAlchemy and how is it used here?
**Answer:** SQLAlchemy is a Python SQL toolkit and ORM. In this project, it is used to create database engine connections for PostgreSQL and to inspect the database schema using `inspect()`.

---

## 11. How is the database schema extracted for SQLite?
**Answer:** The app queries `sqlite_master` to get all table names, then uses `PRAGMA table_info()` for each table to retrieve column details including names and primary key status.

---

## 12. How is the database schema extracted for PostgreSQL?
**Answer:** The app uses SQLAlchemy's `inspect()` function to call `get_table_names()`, `get_columns()`, and `get_pk_constraint()` to build the schema dictionary.

---

## 13. What is the purpose of the `get_sql_from_gemini()` function?
**Answer:** This function takes a user's natural language question and the database schema, constructs a prompt, sends it to the Gemini API, and returns the generated SQL query after cleaning up any markdown formatting.

---

## 14. Explain the prompt engineering used in this project.
**Answer:** The prompt instructs Gemini to act as a "professional SQL assistant," provides the database schema with column names and primary key annotations, includes the user's question, and explicitly asks for only the SQL query without any explanation or formatting.

---

## 15. What is the `company.py` file used for?
**Answer:** `company.py` is a database seeder script that generates a `company.db` SQLite database with 15 tables containing realistic sample data (employees, departments, projects, payroll, etc.) using the Faker library.

---

## 16. What is the Faker library and how is it used?
**Answer:** Faker is a Python library that generates realistic fake data such as names, emails, dates, and sentences. In this project, it is used in `company.py` to populate tables with realistic employee names, email addresses, project names, and performance review comments.

---

## 17. How many tables does the company database contain? Name at least five.
**Answer:** The company database contains 15 tables: DEPARTMENT, EMPLOYEE, PROJECT, ASSIGNMENT, SKILL, EMPLOYEE_SKILL, ATTENDANCE, LEAVE_REQUEST, PAYROLL, PERFORMANCE_REVIEW, TRAINING, EMPLOYEE_TRAINING, ASSET, MEETING, and EMPLOYEE_MEETING.

---

## 18. What is the `offer db.py` file used for?
**Answer:** `offer db.py` creates a `product_offers.db` database with 6 tables for a product offer management system, including item types, item details, item properties, offers, and offer criteria.

---

## 19. Explain the foreign key relationships in the product_offers database.
**Answer:** `item_details` references `item_types` via `type_id`. `assoc_items_props` references `item_details` via `item_id`. `offer_items` references `item_offers` via `offer_id` with ON DELETE CASCADE. `offer_item_criteria` references `offer_items` via `source_id` with ON DELETE CASCADE.

---

## 20. What does `ON DELETE CASCADE` mean in SQL?
**Answer:** It means that when a parent record is deleted, all related child records are automatically deleted as well. For example, deleting an offer from `item_offers` will automatically delete its associated entries in `offer_items`.

---

## 21. What is Streamlit Session State and how is it used here?
**Answer:** Session State allows storing data across reruns of a Streamlit app. In GenDB, it stores the connection status (`connected`), the database engine/file path (`engine`), and the extracted schema (`schema`), so users don't lose their connection when interacting with the UI.

---

## 22. How does the welcome animation work?
**Answer:** The app uses a `st.empty()` placeholder to display a styled "Welcome to AI SQL Studio" message, pauses for 2 seconds using `time.sleep(2)`, then clears the placeholder. A session state flag `animation_shown` ensures it only runs once per session.

---

## 23. How are the databases auto-generated on deployment?
**Answer:** The `ensure_databases()` function checks if `product_offers.db` and `company.db` exist. If not, it runs the respective seeder scripts (`offer db.py` and `company.py`) using `subprocess.run()` to generate them automatically.

---

## 24. What is the `requirements.txt` file and why is it needed?
**Answer:** `requirements.txt` lists all Python package dependencies required by the project. Streamlit Community Cloud reads this file during deployment to install the necessary packages automatically.

---

## 25. How was the app deployed to Streamlit Community Cloud?
**Answer:** The code was pushed to a public GitHub repository. Then, through the Streamlit Community Cloud dashboard, the repository, branch (`master`), and main file (`GenDB.py`) were configured. The Gemini API key was added to the Secrets section in Advanced Settings, and the app was deployed.

---

## 26. What is the `.gitignore` file and what does it exclude?
**Answer:** `.gitignore` tells Git which files to exclude from version control. In this project, it excludes `__pycache__/`, `.pyc` files, `.streamlit/secrets.toml` (to protect the API key), and `*.db` files (since they are auto-generated).

---

## 27. What is Pandas and how is it used in this project?
**Answer:** Pandas is a Python data manipulation library. In GenDB, `pd.read_sql_query()` is used to execute the AI-generated SQL query and load the results into a DataFrame, which is then displayed as an interactive table using `st.dataframe()`.

---

## 28. How does the app handle errors during query execution?
**Answer:** The app uses a try-except block around the query execution. If the SQL query fails (e.g., due to a syntax error or invalid table reference), it catches the exception and displays a user-friendly error message using `st.error()`.

---

## 29. What security measures are implemented in this project?
**Answer:** The Gemini API key is stored using Streamlit Secrets Management instead of being hardcoded. The `.gitignore` file prevents the secrets file from being pushed to GitHub. The app also uses parameterized schema inspection rather than raw SQL for schema extraction.

---

## 30. How can the app be updated after deployment?
**Answer:** Any code changes pushed to the `master` branch of the GitHub repository will trigger an automatic redeployment on Streamlit Community Cloud. No manual intervention is needed — Streamlit detects the new commits and rebuilds the app.

---

*Prepared for: GenDB SQL Assistant Project*
*Developed by: Lavanya*
