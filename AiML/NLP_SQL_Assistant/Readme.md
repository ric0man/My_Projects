# 🧠 NLP-Powered SQL Assistant

A modular assistant that converts natural language queries into executable SQL using LangChain and LLMs. Built with Streamlit and SQLite for lightweight demos and recruiter-friendly visibility.

## 🚀 Features
- 🔍 NLP-to-SQL conversion using LangChain
- 🧠 LLM orchestration with fallback logic
- 🧱 Modular codebase with reproducible setup
- 🧰 Streamlit UI for interactive querying
- 🗃️ SQLite backend for simplicity and portability

## 🛠️ Tech Stack
- Python
- LangChain
- OpenAI API
- Streamlit
- SQLite

## 📦 Setup

```bash
git clone https://github.com/ric0man/NLP_SQL_Assistant.git
cd NLP_SQL_Assistant
pip install -r requirements.txt


------------------------------------------------------------------------------
Create a .env file and add your OpenAI API key:
OPENAI_API_KEY=your-key-here

Run Locally: streamlit run app.py

Project Structure
├── app.py
├── sql_generator/
│   ├── __init__.py
│   ├── prompt_builder.py
│   └── query_executor.py
├── .env
├── .gitignore
├── .gitattributes
└── README.md


📌 Notes
- Modularized for easy onboarding and demo sharing
- API fallback logic ensures robustness across providers
- SQLite used for simplicity; can be swapped with Snowflake or Delta Lake
- .env, .gitignore, and .gitattributes included for secure and cross-platform setup
- README designed for clarity and reproducibility
