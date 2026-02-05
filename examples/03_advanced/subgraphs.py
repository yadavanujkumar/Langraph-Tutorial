"""
Sub-graphs Example
==================

This example demonstrates how to organize complex workflows using
sub-graphs, allowing for better modularity and reusability.

Concepts covered:
- Creating sub-graphs
- Composing graphs
- Modular workflow design
- Reusable workflow components
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define state structures
class InputValidationState(TypedDict):
    input_text: str
    is_valid: bool
    validation_message: str


class ProcessingState(TypedDict):
    text: str
    processed: str
    word_count: int


class MainState(TypedDict):
    user_input: str
    is_valid: bool
    validation_message: str
    processed_output: str
    word_count: int
    status: str


# ===== INPUT VALIDATION SUB-GRAPH =====

def check_length(state: InputValidationState) -> InputValidationState:
    """Check if input has minimum length"""
    print("  📏 Checking input length...")
    
    text = state["input_text"]
    min_length = 3
    
    if len(text) >= min_length:
        return {
            **state,
            "is_valid": True,
            "validation_message": "Length check passed"
        }
    else:
        return {
            **state,
            "is_valid": False,
            "validation_message": f"Input too short (minimum {min_length} characters)"
        }


def check_content(state: InputValidationState) -> InputValidationState:
    """Check if input contains valid content"""
    print("  📝 Checking content validity...")
    
    text = state["input_text"]
    
    # Check if not just whitespace or special characters
    if text.strip() and any(c.isalnum() for c in text):
        return {
            **state,
            "is_valid": state["is_valid"] and True,
            "validation_message": f"{state['validation_message']} | Content check passed"
        }
    else:
        return {
            **state,
            "is_valid": False,
            "validation_message": "Invalid content"
        }


def create_validation_subgraph():
    """Create a sub-graph for input validation"""
    subgraph = StateGraph(InputValidationState)
    
    subgraph.add_node("length_check", check_length)
    subgraph.add_node("content_check", check_content)
    
    subgraph.set_entry_point("length_check")
    subgraph.add_edge("length_check", "content_check")
    subgraph.add_edge("content_check", END)
    
    return subgraph.compile()


# ===== TEXT PROCESSING SUB-GRAPH =====

def clean_text(state: ProcessingState) -> ProcessingState:
    """Clean and normalize text"""
    print("  🧹 Cleaning text...")
    
    cleaned = state["text"].strip()
    
    return {
        **state,
        "processed": cleaned
    }


def count_words(state: ProcessingState) -> ProcessingState:
    """Count words in text"""
    print("  🔢 Counting words...")
    
    words = state["processed"].split()
    
    return {
        **state,
        "word_count": len(words)
    }


def enhance_text(state: ProcessingState) -> ProcessingState:
    """Enhance text with formatting"""
    print("  ✨ Enhancing text...")
    
    enhanced = f"[PROCESSED] {state['processed']} [Words: {state['word_count']}]"
    
    return {
        **state,
        "processed": enhanced
    }


def create_processing_subgraph():
    """Create a sub-graph for text processing"""
    subgraph = StateGraph(ProcessingState)
    
    subgraph.add_node("clean", clean_text)
    subgraph.add_node("count", count_words)
    subgraph.add_node("enhance", enhance_text)
    
    subgraph.set_entry_point("clean")
    subgraph.add_edge("clean", "count")
    subgraph.add_edge("count", "enhance")
    subgraph.add_edge("enhance", END)
    
    return subgraph.compile()


# ===== MAIN WORKFLOW WITH SUB-GRAPHS =====

def validate_input_node(state: MainState) -> MainState:
    """Node that calls the validation sub-graph"""
    print("\n🔍 VALIDATION SUB-GRAPH")
    print("-" * 40)
    
    # Create validation sub-graph
    validation_graph = create_validation_subgraph()
    
    # Prepare input for sub-graph
    validation_input = {
        "input_text": state["user_input"],
        "is_valid": True,
        "validation_message": ""
    }
    
    # Run sub-graph
    validation_result = validation_graph.invoke(validation_input)
    
    # Update main state with validation results
    return {
        **state,
        "is_valid": validation_result["is_valid"],
        "validation_message": validation_result["validation_message"],
        "status": "validated"
    }


def process_text_node(state: MainState) -> MainState:
    """Node that calls the processing sub-graph"""
    print("\n⚙️ PROCESSING SUB-GRAPH")
    print("-" * 40)
    
    # Create processing sub-graph
    processing_graph = create_processing_subgraph()
    
    # Prepare input for sub-graph
    processing_input = {
        "text": state["user_input"],
        "processed": "",
        "word_count": 0
    }
    
    # Run sub-graph
    processing_result = processing_graph.invoke(processing_input)
    
    # Update main state with processing results
    return {
        **state,
        "processed_output": processing_result["processed"],
        "word_count": processing_result["word_count"],
        "status": "processed"
    }


def handle_invalid_input(state: MainState) -> MainState:
    """Handle invalid input"""
    print("\n❌ HANDLING INVALID INPUT")
    print("-" * 40)
    
    return {
        **state,
        "processed_output": f"ERROR: {state['validation_message']}",
        "status": "error"
    }


def finalize_result(state: MainState) -> MainState:
    """Finalize the result"""
    print("\n✅ FINALIZING")
    print("-" * 40)
    
    return {
        **state,
        "status": "complete"
    }


def route_after_validation(state: MainState):
    """Route based on validation result"""
    if state["is_valid"]:
        return "process"
    else:
        return "invalid"


def create_main_workflow_with_subgraphs():
    """Create the main workflow that uses sub-graphs"""
    workflow = StateGraph(MainState)
    
    # Add nodes
    workflow.add_node("validate", validate_input_node)
    workflow.add_node("process", process_text_node)
    workflow.add_node("invalid", handle_invalid_input)
    workflow.add_node("finalize", finalize_result)
    
    # Define flow
    workflow.set_entry_point("validate")
    
    # Conditional routing after validation
    workflow.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "process": "process",
            "invalid": "invalid"
        }
    )
    
    workflow.add_edge("process", "finalize")
    workflow.add_edge("invalid", "finalize")
    workflow.add_edge("finalize", END)
    
    return workflow.compile()


def main():
    """Run the sub-graphs example"""
    print("=" * 60)
    print("Sub-graphs Example")
    print("=" * 60)
    print("\nThis example demonstrates modular workflow design")
    print("using sub-graphs for validation and processing.\n")
    
    # Create the main workflow
    app = create_main_workflow_with_subgraphs()
    
    # Test cases
    test_inputs = [
        "Hello, this is a valid input for testing LangGraph!",
        "Hi",  # Too short
        "   ",  # Invalid content
        "LangGraph makes building AI workflows easier"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{'=' * 60}")
        print(f"TEST CASE {i}: '{user_input}'")
        print("=" * 60)
        
        initial_state = {
            "user_input": user_input,
            "is_valid": False,
            "validation_message": "",
            "processed_output": "",
            "word_count": 0,
            "status": "pending"
        }
        
        result = app.invoke(initial_state)
        
        print("\n📋 RESULT:")
        print("-" * 40)
        print(f"Status: {result['status']}")
        print(f"Valid: {result['is_valid']}")
        if result['is_valid']:
            print(f"Word Count: {result['word_count']}")
        print(f"Output: {result['processed_output']}")


if __name__ == "__main__":
    main()
