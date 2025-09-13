from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from config import OPENAI_API_KEY, DB_URI

def build_agent():
    db = SQLDatabase.from_uri(DB_URI)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    return agent