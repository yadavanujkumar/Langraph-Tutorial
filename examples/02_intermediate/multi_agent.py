"""
Multi-Agent System Example
==========================

This example demonstrates how to coordinate multiple AI agents
working together to accomplish a task.

Concepts covered:
- Multiple specialized agents
- Agent coordination
- Task delegation
- Collaborative problem-solving
"""

import os
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Define the state structure
class MultiAgentState(TypedDict):
    task: str
    researcher_output: str
    writer_output: str
    reviewer_output: str
    final_output: str
    current_agent: str


def researcher_agent(state: MultiAgentState) -> MultiAgentState:
    """Research agent - gathers information about the topic"""
    print("\n🔍 Researcher Agent working...")
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are a research assistant. Your job is to provide 
        key facts and information about the given topic. Be concise and factual."""),
        HumanMessage(content=f"Research this topic and provide key facts: {state['task']}")
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "researcher_output": response.content,
        "current_agent": "researcher"
    }


def writer_agent(state: MultiAgentState) -> MultiAgentState:
    """Writer agent - creates content based on research"""
    print("\n✍️ Writer Agent working...")
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are a creative writer. Your job is to take 
        research information and create engaging, well-written content."""),
        HumanMessage(content=f"""Based on this research: {state['researcher_output']}
        
        Write a brief, engaging article about: {state['task']}""")
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "writer_output": response.content,
        "current_agent": "writer"
    }


def reviewer_agent(state: MultiAgentState) -> MultiAgentState:
    """Reviewer agent - reviews and improves the content"""
    print("\n👀 Reviewer Agent working...")
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are an editor and reviewer. Your job is to 
        review content and provide a polished final version. Make it concise and impactful."""),
        HumanMessage(content=f"""Review and improve this article: {state['writer_output']}
        
        Provide the final polished version.""")
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "reviewer_output": response.content,
        "final_output": response.content,
        "current_agent": "reviewer"
    }


def create_multi_agent_system():
    """Create and return a multi-agent graph"""
    # Initialize the graph
    workflow = StateGraph(MultiAgentState)
    
    # Add agent nodes
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("reviewer", reviewer_agent)
    
    # Define the sequential flow
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "reviewer")
    workflow.add_edge("reviewer", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Run the multi-agent system example"""
    print("=" * 60)
    print("Multi-Agent System Example")
    print("=" * 60)
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    # Create the multi-agent system
    app = create_multi_agent_system()
    
    # Define a task
    task = "The benefits of using LangGraph for building AI applications"
    
    print(f"\n📋 Task: {task}")
    print("=" * 60)
    
    # Run the graph
    initial_state = {
        "task": task,
        "researcher_output": "",
        "writer_output": "",
        "reviewer_output": "",
        "final_output": "",
        "current_agent": ""
    }
    
    result = app.invoke(initial_state)
    
    # Display results
    print("\n" + "=" * 60)
    print("FINAL ARTICLE")
    print("=" * 60)
    print(result["final_output"])
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
