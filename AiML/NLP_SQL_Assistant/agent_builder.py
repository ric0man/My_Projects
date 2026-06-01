import requests
from langchain.llms.base import LLM
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import PERPLEXITY_API_KEY, DB_URI


class PerplexityLLM(LLM):
    def _call(self, prompt, stop=None):
        print("PERPLEXITY_API_KEY loaded is:", PERPLEXITY_API_KEY)

        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "sonar",  # or another valid model
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=payload,
            headers=headers,
        )

        print("Status:", response.status_code)
        print("Text:", response.text)

        try:
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Raw response:", response.text)
            print("Error:", e)
            raise e

    @property
    def _llm_type(self):
        return "perplexity"


def build_agent():
    # This ensures the DB URI is valid and accessible at import time
    db = SQLDatabase.from_uri(DB_URI)
    llm = PerplexityLLM()
    prompt = PromptTemplate.from_template(
        "Translate this question into SQL: {question}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain
