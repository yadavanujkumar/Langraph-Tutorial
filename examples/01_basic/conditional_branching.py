"""
Conditional Branching Example
=============================

This example demonstrates how to use conditional edges to create
dynamic workflows that branch based on the state.

Concepts covered:
- Conditional edges
- Dynamic routing
- Decision-making in graphs
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Define the state structure
class State(TypedDict):
    number: int
    result: str
    path_taken: str


def check_number(state: State) -> State:
    """Analyze the input number"""
    number = state["number"]
    print(f"Checking number: {number}")
    return {
        "number": number,
        "result": f"Analyzed: {number}",
        "path_taken": ""
    }


def process_positive(state: State) -> State:
    """Process positive numbers"""
    print("Taking POSITIVE path")
    return {
        "number": state["number"],
        "result": f"{state['result']} -> Positive number processed",
        "path_taken": "positive"
    }


def process_negative(state: State) -> State:
    """Process negative numbers"""
    print("Taking NEGATIVE path")
    return {
        "number": state["number"],
        "result": f"{state['result']} -> Negative number processed",
        "path_taken": "negative"
    }


def process_zero(state: State) -> State:
    """Process zero"""
    print("Taking ZERO path")
    return {
        "number": state["number"],
        "result": f"{state['result']} -> Zero detected and processed",
        "path_taken": "zero"
    }


def finalize(state: State) -> State:
    """Final processing step"""
    print("Finalizing result")
    return {
        "number": state["number"],
        "result": f"{state['result']} -> Finalized",
        "path_taken": state["path_taken"]
    }


def route_by_number(state: State) -> Literal["positive", "negative", "zero"]:
    """
    Routing function that determines which path to take
    based on the number's value
    """
    number = state["number"]
    
    if number > 0:
        return "positive"
    elif number < 0:
        return "negative"
    else:
        return "zero"


def create_conditional_graph():
    """Create and return a graph with conditional branching"""
    # Initialize the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("check", check_number)
    workflow.add_node("positive", process_positive)
    workflow.add_node("negative", process_negative)
    workflow.add_node("zero", process_zero)
    workflow.add_node("finalize", finalize)
    
    # Define the flow
    workflow.set_entry_point("check")
    
    # Add conditional edge that routes based on the number
    workflow.add_conditional_edges(
        "check",
        route_by_number,
        {
            "positive": "positive",
            "negative": "negative",
            "zero": "zero"
        }
    )
    
    # All paths converge to finalize
    workflow.add_edge("positive", "finalize")
    workflow.add_edge("negative", "finalize")
    workflow.add_edge("zero", "finalize")
    workflow.add_edge("finalize", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Run the conditional branching example"""
    print("=" * 60)
    print("Conditional Branching Example")
    print("=" * 60)
    
    # Create the graph
    app = create_conditional_graph()
    
    # Test with different numbers
    test_numbers = [42, -15, 0, 7, -3]
    
    for number in test_numbers:
        print(f"\n{'=' * 60}")
        print(f"Testing with number: {number}")
        print("=" * 60)
        
        initial_state = {
            "number": number,
            "result": "",
            "path_taken": ""
        }
        
        result = app.invoke(initial_state)
        
        print(f"\nResult: {result['result']}")
        print(f"Path taken: {result['path_taken']}")


if __name__ == "__main__":
    main()
