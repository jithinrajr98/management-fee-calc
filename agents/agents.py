from crewai import Agent
from tools.data_loaders import ExcelToSQLiteTool
from groq import Groq
from dotenv import load_dotenv
import os
from config.settings import GROQ_MODEL
from langchain_groq import ChatGroq
load_dotenv()


# configure Groq
api_key = None

if 'GROQ_API_KEY' in os.environ:
    api_key = os.environ['GROQ_API_KEY']
elif not api_key:
    raise ValueError("GROQ_API_KEY not found in Streamlit secrets or environment variables.")
else:
    pass

groq_llm =  ChatGroq(model=GROQ_MODEL, api_key=api_key)

#define the agent for loading excel data and writing to sqlite
data_pipeline_agent = Agent(
    role="Data Pipeline Agent",
    goal="to load data from Excel and write to SQLite",
    backstory="An experience agent that loads data from Excel files and writes it to SQLite databases.",
    tools=[ExcelToSQLiteTool()],
    llm= groq_llm,
    verbose=True,  
)