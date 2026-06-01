import os
from dotenv import load_dotenv

# ---------- Paths ----------
# Project root: C:\Users\rohan\Desktop\Job\Projects\AiML\NLP_SQL_Assistant
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "sample.db")  # ...\NLP_SQL_Assistant\data\sample.db

# ---------- Env loading ----------
# Load environment variables from .env.txt or fallback to .env.template
env_path_txt = os.path.join(BASE_DIR, ".env.txt")
env_path_template = os.path.join(BASE_DIR, ".env.template")

if os.path.exists(env_path_txt):
    load_dotenv(env_path_txt, encoding="utf-8")
elif os.path.exists(env_path_template):
    load_dotenv(env_path_template, encoding="utf-8")

# ---------- API keys ----------
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

GROQ_API_KEY        = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY      = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY      = os.getenv("CLAUDE_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "perplexity")

# ---------- Database ----------
# 1) Raw filesystem path for sqlite3.connect()
DB_PATH = DB_FILE

# 2) SQLAlchemy-style URI for LangChain SQLDatabase.from_uri()
DB_URI = f"sqlite:///{DB_FILE.replace(os.sep, '/')}"
