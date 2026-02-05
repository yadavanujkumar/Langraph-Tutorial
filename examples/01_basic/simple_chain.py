"""
Simple Chain Example
====================

This example demonstrates the most basic LangGraph structure:
a simple sequential chain of nodes.

Concepts covered:
- Creating a StateGraph
- Adding nodes
- Adding edges
- Compiling and running the graph
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define the state structure
class State(TypedDict):
    input: str
    output: str
    step_count: int


# Define node functions
def step_one(state: State) -> State:
    """First processing step"""
    print(f"Step 1: Processing input: {state['input']}")
    return {
        "input": state["input"],
        "output": f"Step 1 processed: {state['input']}",
        "step_count": state.get("step_count", 0) + 1
    }


def step_two(state: State) -> State:
    """Second processing step"""
    print(f"Step 2: Processing: {state['output']}")
    return {
        "input": state["input"],
        "output": f"{state['output']} -> Step 2 enhanced",
        "step_count": state["step_count"] + 1
    }


def step_three(state: State) -> State:
    """Final processing step"""
    print(f"Step 3: Finalizing: {state['output']}")
    return {
        "input": state["input"],
        "output": f"{state['output']} -> Step 3 complete!",
        "step_count": state["step_count"] + 1
    }


def create_simple_chain():
    """Create and return a simple chain graph"""
    # Initialize the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("step_1", step_one)
    workflow.add_node("step_2", step_two)
    workflow.add_node("step_3", step_three)
    
    # Define the flow
    workflow.set_entry_point("step_1")
    workflow.add_edge("step_1", "step_2")
    workflow.add_edge("step_2", "step_3")
    workflow.add_edge("step_3", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Run the simple chain example"""
    print("=" * 60)
    print("Simple Chain Example")
    print("=" * 60)
    
    # Create the graph
    app = create_simple_chain()
    
    # Run the graph
    initial_state = {
        "input": "Hello, LangGraph!",
        "output": "",
        "step_count": 0
    }
    
    result = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("Final Result:")
    print("=" * 60)
    print(f"Input: {result['input']}")
    print(f"Output: {result['output']}")
    print(f"Total steps: {result['step_count']}")


if __name__ == "__main__":
    main()
