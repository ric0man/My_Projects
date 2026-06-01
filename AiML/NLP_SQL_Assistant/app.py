import sqlite3
import streamlit as st

from agent_builder import build_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from config import DB_PATH  # filesystem path for sqlite3.connect

st.set_page_config(page_title="NLP SQL Assistant", layout="wide")

st.title("NLP-Powered SQL Assistant")

st.markdown(
    """
Welcome! This assistant lets you query your SQLite database using plain English.

You can ask questions like:

- "List all employees who joined after 2021"
- "Show names of employees in the Marketing department"
- "How many employees are in Finance?"

Just type your question below and let the assistant do the rest!
"""
)

agent = build_agent()

if prompt := st.chat_input("Ask a question about your database"):
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())

        # Get SQL from LLM
        sql_query = agent.run({"question": prompt}, callbacks=[st_callback])

        # Defensive cleaning in case any markdown sneaks in
        sql_query = sql_query.strip()
        if "```" in sql_query:
            parts = sql_query.split("```")
            # pick the part that looks like it contains a SELECT
            for part in parts:
                if "select" in part.lower():
                    sql_query = part
                    break
            # remove leading 'sql' label if present
            if sql_query.lower().startswith("sql"):
                sql_query = sql_query[3:]
            sql_query = sql_query.strip()

        st.write("Generated SQL:")
        st.code(sql_query, language="sql")

        # Execute SQL and display results
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH)  # absolute path from config
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()

            # Display column names if possible
            colnames = (
                [description for description in cursor.description]
                if cursor.description
                else []
            )

            if results:
                st.write("Query Results:")
                st.dataframe([dict(zip(colnames, row)) for row in results])
            else:
                st.write("No results returned.")
        except Exception as e:
            st.error(f"Error executing SQL: {e}")
        finally:
            if conn is not None:
                conn.close()
