import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from src.agent import AgentState, research_node, writer_node

load_dotenv()

def create_app():
    workflow = StateGraph(AgentState)

    workflow.add_node("researcher", research_node)
    workflow.add_node("writer", writer_node)

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)

    
    return workflow.compile()

if __name__ == "__main__":
    
    app = create_app()

    
    target = input("\nEnter company to research: ")

  
    print(f"\n--- Starting Workflow for {target} ---")
    result = app.invoke({"target_company": target})

    
    print("\n" + "="*60)
    print(" GENERATED OUTREACH EMAIL")
    print("="*60 + "\n")
    
    print(result.get("final_output", "Error: No output generated."))
    
    print("\n" + "="*60)
    print("WORKFLOW COMPLETE")
    print("="*60)