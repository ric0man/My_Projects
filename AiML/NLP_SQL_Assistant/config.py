import os
from dotenv import load_dotenv

# 🔄 Load environment variables from .env or fallback to .env.template
# ⚠️ IMPORTANT: Ensure .env is saved as UTF-8 (no BOM), especially if edited in Notepad.
#               Incorrect encoding (e.g., UTF-16 or ANSI) will cause UnicodeDecodeError.

if os.path.exists(".env"):
    load_dotenv(".env", encoding="utf-8")
elif os.path.exists(".env.template"):
    load_dotenv(".env.template", encoding="utf-8")

# 🔐 OpenAI API Key Setup
# This assistant supports two options:
#
# Option 1: Personal key via `.env` file
#           OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# Option 2: Shared service key via `.env.template` (for demos or onboarding)
#           OPENAI_API_KEY=sk-svcacct-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "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"


# ✅ Validate key format (temporarily disabled due to service key format)
# valid_prefixes = ("sk-", "sk-svcacct-", "Open")
# if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith(valid_prefixes):
#     raise ValueError(
#         "❌ OPENAI_API_KEY is missing or invalid.\n"
#         "Please set it in your .env file or use the provided .env.template.\n"
#         "Supported formats include keys starting with 'sk-', 'sk-svcacct-', or 'Open'."
#     )

# 🧠 SQLite DB URI used by LangChain SQL agent
DB_URI = "sqlite:///data/sample.db"

# 🧩 Future Expansion: Multi-LLM Support
# -------------------------------------
# To support other LLMs, add their keys and endpoints here.
# Then update `agent_builder.py` to switch dynamically.
#
# Examples:
# GROQ_API_KEY       = os.getenv("GROQ_API_KEY")
# GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY")
# CLAUDE_API_KEY     = os.getenv("CLAUDE_API_KEY")
# HUGGINGFACE_API_KEY= os.getenv("HF_API_KEY")
#
# You can also define a selector:
# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
#
# Then use conditional logic in your agent builder to route accordingly.