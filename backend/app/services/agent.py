import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from app.services.tools import make_tools

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

SYSTEM_PROMPT = (
    "You are a CRM assistant for pharma sales reps. Use the available tools "
    "to log, search, summarize, or update doctor interactions. "
    "Always confirm what action you took."
)

def ask_ai(prompt: str, db) -> str:
    tools = make_tools(db)
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return result["messages"][-1].content