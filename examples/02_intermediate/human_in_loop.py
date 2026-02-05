"""
Human-in-the-Loop Example
=========================

This example demonstrates how to add human approval steps
in your workflows, allowing for human oversight and intervention.

Concepts covered:
- Interrupt nodes for human input
- Resuming execution after approval
- Human oversight in automated workflows
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# Define the state structure
class State(TypedDict):
    input: str
    processed_data: str
    human_feedback: str
    approved: bool
    final_output: str


def process_input(state: State) -> State:
    """Initial processing step"""
    print(f"\n📊 Processing input: {state['input']}")
    processed = f"Processed: {state['input'].upper()}"
    print(f"✓ Result: {processed}")
    
    return {
        **state,
        "processed_data": processed
    }


def request_approval(state: State) -> State:
    """Request human approval"""
    print("\n⏸️  HUMAN APPROVAL REQUIRED")
    print("=" * 60)
    print(f"Processed Data: {state['processed_data']}")
    print("=" * 60)
    
    # In a real application, this would pause and wait for external input
    # For this demo, we'll simulate human interaction
    approval = input("\nApprove this output? (yes/no): ").strip().lower()
    
    if approval in ['yes', 'y']:
        feedback = input("Any feedback? (press Enter to skip): ").strip()
        return {
            **state,
            "approved": True,
            "human_feedback": feedback or "Approved without changes"
        }
    else:
        feedback = input("Please provide feedback for improvement: ").strip()
        return {
            **state,
            "approved": False,
            "human_feedback": feedback or "Rejected without specific feedback"
        }


def finalize_output(state: State) -> State:
    """Finalize the output"""
    print("\n✅ Finalizing output...")
    
    if state.get("human_feedback") and state["human_feedback"] != "Approved without changes":
        final = f"{state['processed_data']} (Note: {state['human_feedback']})"
    else:
        final = state['processed_data']
    
    return {
        **state,
        "final_output": final
    }


def handle_rejection(state: State) -> State:
    """Handle rejected output"""
    print("\n❌ Output was rejected. Reprocessing...")
    
    # Incorporate feedback
    reprocessed = f"REVISED - {state['processed_data']} - {state['human_feedback']}"
    
    return {
        **state,
        "processed_data": reprocessed,
        "approved": False
    }


def route_after_approval(state: State) -> Literal["approved", "rejected"]:
    """Route based on approval status"""
    if state.get("approved", False):
        return "approved"
    else:
        return "rejected"


def create_human_in_loop_workflow():
    """Create and return a workflow with human-in-the-loop"""
    # Initialize the graph with checkpointer for state persistence
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("process", process_input)
    workflow.add_node("approval", request_approval)
    workflow.add_node("finalize", finalize_output)
    workflow.add_node("handle_rejection", handle_rejection)
    
    # Define the flow
    workflow.set_entry_point("process")
    workflow.add_edge("process", "approval")
    
    # Add conditional routing after approval
    workflow.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "approved": "finalize",
            "rejected": "handle_rejection"
        }
    )
    
    # After handling rejection, go back to approval
    workflow.add_edge("handle_rejection", "approval")
    workflow.add_edge("finalize", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Run the human-in-the-loop example"""
    print("=" * 60)
    print("Human-in-the-Loop Workflow")
    print("=" * 60)
    print("\nThis example demonstrates human oversight in automated workflows.")
    print("You'll be asked to approve the processed output.\n")
    
    # Create the workflow
    app = create_human_in_loop_workflow()
    
    # Get user input
    user_input = input("Enter some text to process: ").strip()
    
    if not user_input:
        user_input = "Hello, LangGraph with human-in-the-loop!"
    
    # Run the workflow
    initial_state = {
        "input": user_input,
        "processed_data": "",
        "human_feedback": "",
        "approved": False,
        "final_output": ""
    }
    
    result = app.invoke(initial_state)
    
    # Display final result
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(f"Original Input: {result['input']}")
    print(f"Final Output: {result['final_output']}")
    print(f"Status: {'✓ Approved' if result['approved'] else '✗ Modified after rejection'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
