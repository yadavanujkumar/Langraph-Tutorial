"""
Complex Workflow Example
========================

This example demonstrates a sophisticated workflow that combines
multiple concepts: conditional routing, multiple agents, and
complex state management.

Concepts covered:
- Complex decision trees
- Multiple conditional branches
- Error handling
- Workflow orchestration
"""

import os
from typing import TypedDict, Literal, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Define the state structure
class WorkflowState(TypedDict):
    user_request: str
    category: Optional[str]
    complexity: Optional[str]
    agent_response: str
    requires_escalation: bool
    error: Optional[str]
    final_response: str


def analyze_request(state: WorkflowState) -> WorkflowState:
    """Analyze the user request to determine category and complexity"""
    print("\n🔍 Analyzing request...")
    
    if not os.getenv("OPENAI_API_KEY"):
        return {
            **state,
            "category": "general",
            "complexity": "simple",
            "error": None
        }
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""Analyze the user request and respond with ONLY:
        Category: [technical/billing/general]
        Complexity: [simple/moderate/complex]"""),
        HumanMessage(content=state["user_request"])
    ]
    
    response = llm.invoke(messages)
    analysis = response.content
    
    # Parse the response
    category = "general"
    complexity = "simple"
    
    if "technical" in analysis.lower():
        category = "technical"
    elif "billing" in analysis.lower():
        category = "billing"
    
    if "complex" in analysis.lower():
        complexity = "complex"
    elif "moderate" in analysis.lower():
        complexity = "moderate"
    
    print(f"  Category: {category}")
    print(f"  Complexity: {complexity}")
    
    return {
        **state,
        "category": category,
        "complexity": complexity,
        "error": None
    }


def handle_simple_request(state: WorkflowState) -> WorkflowState:
    """Handle simple requests directly"""
    print("\n✅ Handling simple request...")
    
    response = f"Simple {state['category']} request handled: {state['user_request'][:50]}..."
    
    return {
        **state,
        "agent_response": response,
        "requires_escalation": False
    }


def handle_technical_request(state: WorkflowState) -> WorkflowState:
    """Handle technical requests with specialized agent"""
    print("\n🔧 Technical specialist handling request...")
    
    if not os.getenv("OPENAI_API_KEY"):
        response = f"Technical response for: {state['user_request'][:50]}..."
    else:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        messages = [
            SystemMessage(content="You are a technical support specialist. Provide clear, technical solutions."),
            HumanMessage(content=state["user_request"])
        ]
        
        response = llm.invoke(messages).content
    
    return {
        **state,
        "agent_response": response,
        "requires_escalation": state["complexity"] == "complex"
    }


def handle_billing_request(state: WorkflowState) -> WorkflowState:
    """Handle billing requests with specialized agent"""
    print("\n💰 Billing specialist handling request...")
    
    if not os.getenv("OPENAI_API_KEY"):
        response = f"Billing response for: {state['user_request'][:50]}..."
    else:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        messages = [
            SystemMessage(content="You are a billing support specialist. Help with payment and account issues."),
            HumanMessage(content=state["user_request"])
        ]
        
        response = llm.invoke(messages).content
    
    return {
        **state,
        "agent_response": response,
        "requires_escalation": False
    }


def handle_general_request(state: WorkflowState) -> WorkflowState:
    """Handle general requests"""
    print("\n📋 General support handling request...")
    
    response = f"General response for: {state['user_request'][:50]}..."
    
    return {
        **state,
        "agent_response": response,
        "requires_escalation": False
    }


def escalate_to_human(state: WorkflowState) -> WorkflowState:
    """Escalate complex issues to human agent"""
    print("\n🚨 Escalating to human agent...")
    
    return {
        **state,
        "final_response": f"[ESCALATED] {state['agent_response']}\n\nThis request has been escalated to a human specialist."
    }


def finalize_response(state: WorkflowState) -> WorkflowState:
    """Finalize the response"""
    print("\n✅ Finalizing response...")
    
    return {
        **state,
        "final_response": state["agent_response"]
    }


def route_by_complexity(state: WorkflowState) -> Literal["simple", "complex"]:
    """Route based on complexity"""
    return "simple" if state["complexity"] == "simple" else "complex"


def route_by_category(state: WorkflowState) -> Literal["technical", "billing", "general"]:
    """Route based on category"""
    return state["category"]


def route_by_escalation(state: WorkflowState) -> Literal["escalate", "finalize"]:
    """Route based on escalation need"""
    return "escalate" if state.get("requires_escalation", False) else "finalize"


def create_complex_workflow():
    """Create and return a complex workflow graph"""
    workflow = StateGraph(WorkflowState)
    
    # Add all nodes
    workflow.add_node("analyze", analyze_request)
    workflow.add_node("simple", handle_simple_request)
    workflow.add_node("technical", handle_technical_request)
    workflow.add_node("billing", handle_billing_request)
    workflow.add_node("general", handle_general_request)
    workflow.add_node("escalate", escalate_to_human)
    workflow.add_node("finalize", finalize_response)
    
    # Set entry point
    workflow.set_entry_point("analyze")
    
    # First routing: by complexity
    workflow.add_conditional_edges(
        "analyze",
        route_by_complexity,
        {
            "simple": "simple",
            "complex": "general"  # Will route again by category
        }
    )
    
    # Simple requests go straight to finalize
    workflow.add_edge("simple", "finalize")
    
    # Complex requests route by category
    workflow.add_conditional_edges(
        "general",
        route_by_category,
        {
            "technical": "technical",
            "billing": "billing",
            "general": "general"
        }
    )
    
    # After specialized handling, check if escalation is needed
    workflow.add_conditional_edges(
        "technical",
        route_by_escalation,
        {
            "escalate": "escalate",
            "finalize": "finalize"
        }
    )
    
    workflow.add_edge("billing", "finalize")
    
    # Final edges
    workflow.add_edge("escalate", END)
    workflow.add_edge("finalize", END)
    
    return workflow.compile()


def main():
    """Run the complex workflow example"""
    print("=" * 60)
    print("Complex Workflow Example")
    print("=" * 60)
    
    # Create the workflow
    app = create_complex_workflow()
    
    # Test with various requests
    test_requests = [
        "How do I reset my password?",
        "My server is experiencing high latency and connection timeouts",
        "I was charged twice for my subscription",
        "What are your business hours?"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{'=' * 60}")
        print(f"REQUEST {i}: {request}")
        print("=" * 60)
        
        initial_state = {
            "user_request": request,
            "category": None,
            "complexity": None,
            "agent_response": "",
            "requires_escalation": False,
            "error": None,
            "final_response": ""
        }
        
        result = app.invoke(initial_state)
        
        print("\n📄 FINAL RESPONSE:")
        print("-" * 60)
        print(result["final_response"])


if __name__ == "__main__":
    main()
