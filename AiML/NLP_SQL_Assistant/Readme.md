# NLP-Powered SQL Assistant

A modular assistant that converts natural language queries into executable SQL using LangChain and Perplexity Pro. Built with Streamlit and SQLite for lightweight demos and recruiter-friendly visibility.

## Features

- Natural language to SQL conversion using LangChain
- Perplexity Pro integration via custom LLM wrapper
- Modular codebase with reproducible setup
- Streamlit UI for interactive querying
- SQLite backend for simplicity and portability

## Tech Stack

- Python
- LangChain
- Perplexity Pro API
- Streamlit
- SQLite

## Setup

git clone https://github.com/ric0man/NLP_SQL_Assistant.git
cd NLP_SQL_Assistant
pip install -r requirements.txt

##Create a .env file and add your Perplexity API key:

PERPLEXITY_API_KEY=your-key-here

## Run locally

streamlit run app.py

## Project Structure

├── app.py
├── agent_builder.py
├── config.py
├── db_setup.py
├── .env
├── .gitignore
├── .gitattributes
└── README.md