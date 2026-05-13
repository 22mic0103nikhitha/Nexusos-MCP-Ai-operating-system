from typing import Dict, TypedDict
from langgraph.graph import StateGraph, END

# Define the state for the multi-agent graph
class AgentState(TypedDict):
    query: str
    plan: str
    code: str
    verification: str
    final_output: str

# Node functions
def planner(state: AgentState):
    print("Planner Agent: Breaking down the task.")
    return {"plan": f"Plan for: {state['query']}"}

def coder(state: AgentState):
    print("Coder Agent: Writing code based on plan.")
    return {"code": f"Code implementation for: {state['plan']}"}

def verifier(state: AgentState):
    print("Verifier Agent: Checking outputs.")
    return {"verification": "Verification passed."}

def finalize(state: AgentState):
    print("Finalizing output.")
    return {"final_output": f"Final result: {state['code']} (Verified)"}

# Build the LangGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner)
workflow.add_node("coder", coder)
workflow.add_node("verifier", verifier)
workflow.add_node("finalize", finalize)

# Add edges
workflow.set_entry_point("planner")
workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "verifier")
workflow.add_edge("verifier", "finalize")
workflow.add_edge("finalize", END)

# Compile the graph
app = workflow.compile()

if __name__ == "__main__":
    # Test the multi-agent workflow
    initial_state = {"query": "Create a hello world function"}
    result = app.invoke(initial_state)
    print("\nWorkflow complete!")
    print(result["final_output"])
