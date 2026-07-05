import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

def get_database_schema():
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    schema = ""
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema += f"\nTable: {table_name}\n"
        for col in columns:
            schema += f"  - {col[1]} ({col[2]})\n"
    conn.close()
    return schema

def run_sql(query):
    try:
        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return columns, results, None
    except Exception as e:
        return None, None, str(e)

def generate_sql(question, schema):
    # mock mode - no API needed
    mock_queries = {
        "highest": "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 1",
        "salary": "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department",
        "engineering": "SELECT name, salary FROM employees WHERE department='Engineering'",
        "sales": "SELECT * FROM sales ORDER BY amount DESC",
        "experience": "SELECT name, years_experience FROM employees ORDER BY years_experience DESC",
    }
    question_lower = question.lower()
    for keyword, query in mock_queries.items():
        if keyword in question_lower:
            return query
    return "SELECT * FROM employees LIMIT 5"

# streamlit UI
st.title("AI SQL Assistant")
st.write("Ask questions about your database in plain English!")

if "messages" not in st.session_state:
    st.session_state.messages = []

schema = get_database_schema()

with st.expander("View Database Schema"):
    st.text(schema)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask anything about the data...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Generating SQL..."):
            sql_query = generate_sql(question, schema)
            columns, results, error = run_sql(sql_query)

            if error:
                st.error(f"SQL Error: {error}")
            else:
                st.code(sql_query, language="sql")
                if results:
                    import pandas as pd
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df)
                    answer = f"Here are the results for: '{question}'"
                else:
                    answer = "No results found."

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"SQL: {sql_query}"
                })