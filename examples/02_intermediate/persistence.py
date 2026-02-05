"""
Persistence Example
==================

This example demonstrates how to save and resume workflow state,
allowing for long-running processes and error recovery.

Concepts covered:
- State persistence with checkpoints
- Resuming workflows
- Thread-based state management
"""

import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# Define the state structure
class PersistentState(TypedDict):
    step: int
    data: str
    checkpoints: list


def step_one(state: PersistentState) -> PersistentState:
    """First step in the workflow"""
    print("🔵 Executing Step 1...")
    
    return {
        **state,
        "step": 1,
        "data": "Step 1 completed",
        "checkpoints": state.get("checkpoints", []) + ["Step 1 checkpoint"]
    }


def step_two(state: PersistentState) -> PersistentState:
    """Second step in the workflow"""
    print("🟢 Executing Step 2...")
    
    return {
        **state,
        "step": 2,
        "data": f"{state['data']} -> Step 2 completed",
        "checkpoints": state["checkpoints"] + ["Step 2 checkpoint"]
    }


def step_three(state: PersistentState) -> PersistentState:
    """Third step in the workflow"""
    print("🟡 Executing Step 3...")
    
    return {
        **state,
        "step": 3,
        "data": f"{state['data']} -> Step 3 completed",
        "checkpoints": state["checkpoints"] + ["Step 3 checkpoint"]
    }


def create_persistent_workflow():
    """Create a workflow with persistence enabled"""
    # Initialize the graph with a memory saver for checkpointing
    workflow = StateGraph(PersistentState)
    
    # Add nodes
    workflow.add_node("step_1", step_one)
    workflow.add_node("step_2", step_two)
    workflow.add_node("step_3", step_three)
    
    # Define the flow
    workflow.set_entry_point("step_1")
    workflow.add_edge("step_1", "step_2")
    workflow.add_edge("step_2", "step_3")
    workflow.add_edge("step_3", END)
    
    # Compile with checkpointer
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def demonstrate_persistence():
    """Demonstrate workflow persistence and resumption"""
    print("=" * 60)
    print("Persistence Example")
    print("=" * 60)
    
    # Create the workflow
    app = create_persistent_workflow()
    
    # Define a thread ID for this execution
    thread_id = "example_thread_1"
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial state
    initial_state = {
        "step": 0,
        "data": "Starting workflow",
        "checkpoints": []
    }
    
    print("\n📍 Starting new workflow with persistence...")
    print(f"Thread ID: {thread_id}\n")
    
    # Run the complete workflow
    print("Running all steps:")
    print("-" * 60)
    result = app.invoke(initial_state, config)
    
    print("\n✅ Workflow completed!")
    print("=" * 60)
    print("Final State:")
    print(f"  Current Step: {result['step']}")
    print(f"  Data: {result['data']}")
    print(f"  Checkpoints saved: {len(result['checkpoints'])}")
    for i, checkpoint in enumerate(result['checkpoints'], 1):
        print(f"    {i}. {checkpoint}")
    
    # Demonstrate retrieving state
    print("\n" + "=" * 60)
    print("Demonstrating State Retrieval")
    print("=" * 60)
    
    # Get the current state from the checkpoint
    current_state = app.get_state(config)
    print(f"\n📌 Retrieved state for thread '{thread_id}':")
    print(f"  Step: {current_state.values['step']}")
    print(f"  Data: {current_state.values['data']}")
    
    # Demonstrate starting a new thread
    print("\n" + "=" * 60)
    print("Starting a separate workflow thread")
    print("=" * 60)
    
    thread_id_2 = "example_thread_2"
    config_2 = {"configurable": {"thread_id": thread_id_2}}
    
    print(f"\n📍 Starting workflow with thread ID: {thread_id_2}")
    
    initial_state_2 = {
        "step": 0,
        "data": "Starting second workflow",
        "checkpoints": []
    }
    
    result_2 = app.invoke(initial_state_2, config_2)
    
    print("\n✅ Second workflow completed!")
    print(f"  Data: {result_2['data']}")
    
    # Show that both threads maintain separate states
    print("\n" + "=" * 60)
    print("Verifying Thread Isolation")
    print("=" * 60)
    
    state_1 = app.get_state(config)
    state_2 = app.get_state(config_2)
    
    print(f"\nThread 1 final data: {state_1.values['data']}")
    print(f"Thread 2 final data: {state_2.values['data']}")
    print("\n✓ Each thread maintains its own independent state!")


def main():
    """Run the persistence example"""
    demonstrate_persistence()


if __name__ == "__main__":
    main()
