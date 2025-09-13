import streamlit as st
from agent_builder import build_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

st.set_page_config(page_title="🧠 NLP SQL Assistant", layout="wide")
st.title("🧠 NLP-Powered SQL Assistant")

# 🧾 Intro Message
st.markdown("""
Welcome! This assistant lets you query your **SQLite database** using plain English.

You can ask questions like:
- 🔍 *"List all employees who joined after 2021"*
- 🧑‍💼 *"Show names of employees in the Marketing department"*
- 📊 *"How many employees are in Finance?"*

Just type your question below and let the assistant do the rest!
""")

agent = build_agent()

# 💬 Chat Interface
if prompt := st.chat_input("Ask a question about your database"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)