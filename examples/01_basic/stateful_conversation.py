"""
Stateful Conversation Example
=============================

This example demonstrates how to build a chatbot that maintains
conversation history using LangGraph's state management.

Concepts covered:
- Maintaining conversation state
- Using LLMs with LangGraph
- Message history management
"""

import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Define the state structure
class ConversationState(TypedDict):
    messages: List
    current_response: str


def chatbot_node(state: ConversationState) -> ConversationState:
    """Process user input and generate response"""
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Get the response from the LLM
    response = llm.invoke(state["messages"])
    
    # Update the state with the new message
    return {
        "messages": state["messages"] + [response],
        "current_response": response.content
    }


def create_chatbot():
    """Create and return a stateful chatbot graph"""
    # Initialize the graph
    workflow = StateGraph(ConversationState)
    
    # Add the chatbot node
    workflow.add_node("chatbot", chatbot_node)
    
    # Define the flow
    workflow.set_entry_point("chatbot")
    workflow.add_edge("chatbot", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Run the stateful conversation example"""
    print("=" * 60)
    print("Stateful Conversation Chatbot")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    # Create the chatbot
    app = create_chatbot()
    
    # Initialize conversation with a system message
    messages = [
        SystemMessage(content="You are a helpful assistant. Keep your responses concise and friendly.")
    ]
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        messages.append(HumanMessage(content=user_input))
        
        # Run the graph
        state = {
            "messages": messages,
            "current_response": ""
        }
        
        result = app.invoke(state)
        
        # Update messages with the full history including the response
        messages = result["messages"]
        
        # Print the response
        print(f"Chatbot: {result['current_response']}\n")


if __name__ == "__main__":
    main()
