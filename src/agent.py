from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools import get_search_tool
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    target_company: str
    research_notes: str
    final_output: str

def research_node(state: AgentState):
    print(f"--- Researching {state['target_company']} ---")
    search_tool = get_search_tool()
    query = f"Latest news and core services of {state['target_company']}"
    results = search_tool.invoke({"query": query})
    return {"research_notes": str(results)}

def writer_node(state: AgentState):
    print("--- Gemini is drafting the pitch ---")
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.3)
    
    prompt = (
        f"Context: {state['research_notes']}\n\n"
        f"Task: Write a highly personalized partnership email to {state['target_company']}. "
        f"Mention specific services they offer and how we can collaborate."
    )
    
    response = llm.invoke(prompt)
    return {"final_output": response.content}