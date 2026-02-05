# Getting Started with LangGraph

## Introduction

Welcome to the LangGraph Tutorial! This guide will help you get started with LangGraph, a powerful library for building stateful, multi-actor applications with Large Language Models.

## What You'll Learn

By completing this tutorial, you will understand:

1. **Basic Concepts**
   - Graph structure and nodes
   - State management
   - Sequential workflows
   - Conditional branching

2. **Intermediate Concepts**
   - Multi-agent coordination
   - Human-in-the-loop workflows
   - State persistence and checkpointing

3. **Advanced Concepts**
   - Complex workflow orchestration
   - Sub-graphs and modularity
   - Error handling and escalation

## Prerequisites

Before starting, ensure you have:

- Python 3.8 or higher installed
- pip (Python package installer)
- An OpenAI API key (for examples that use LLMs)
- Basic Python programming knowledge

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yadavanujkumar/Langraph-Tutorial.git
cd Langraph-Tutorial
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid dependency conflicts:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```
OPENAI_API_KEY=your_api_key_here
```

## Running Your First Example

Let's start with the simplest example - a basic chain:

```bash
python examples/01_basic/simple_chain.py
```

You should see output showing the progression through three steps. This example demonstrates:
- How to create a graph
- How to add nodes
- How to connect nodes with edges
- How to run the graph with initial state

## Understanding the Code Structure

### Basic Example Structure

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. Define your state
class State(TypedDict):
    input: str
    output: str

# 2. Define node functions
def my_node(state: State) -> State:
    # Process the state
    return {"input": state["input"], "output": "processed"}

# 3. Create the graph
workflow = StateGraph(State)
workflow.add_node("my_node", my_node)
workflow.set_entry_point("my_node")
workflow.add_edge("my_node", END)

# 4. Compile and run
app = workflow.compile()
result = app.invoke({"input": "test", "output": ""})
```

## Learning Path

We recommend following this learning path:

### Level 1: Basic (Start Here)
1. `simple_chain.py` - Understand basic graph structure
2. `stateful_conversation.py` - Learn state management with LLMs
3. `conditional_branching.py` - Implement decision logic

### Level 2: Intermediate
4. `multi_agent.py` - Coordinate multiple AI agents
5. `human_in_loop.py` - Add human oversight
6. `persistence.py` - Save and resume workflows

### Level 3: Advanced
7. `complex_workflow.py` - Build sophisticated systems
8. `subgraphs.py` - Organize with modular components

## Key Concepts

### 1. State

State is the data that flows through your graph. It's defined as a TypedDict:

```python
class State(TypedDict):
    field1: str
    field2: int
```

### 2. Nodes

Nodes are functions that process state:

```python
def my_node(state: State) -> State:
    # Your logic here
    return updated_state
```

### 3. Edges

Edges connect nodes:
- **Regular edges**: Fixed connections (`add_edge`)
- **Conditional edges**: Dynamic routing (`add_conditional_edges`)

### 4. Compilation

Before running, compile the graph:

```python
app = workflow.compile()
result = app.invoke(initial_state)
```

## Tips for Success

1. **Start Simple**: Begin with basic examples before moving to complex ones
2. **Understand State**: Make sure you understand how state flows through the graph
3. **Use Print Statements**: Add logging to understand execution flow
4. **Experiment**: Modify examples to test your understanding
5. **Read Errors**: Error messages are helpful for debugging

## Common Issues

### Issue: "OPENAI_API_KEY not found"
**Solution**: Make sure you've created a `.env` file with your API key.

### Issue: "Module not found"
**Solution**: Ensure you've activated your virtual environment and installed requirements.

### Issue: "Graph doesn't execute as expected"
**Solution**: Check that all nodes return the correct state structure and edges are properly connected.

## Next Steps

1. Complete all basic examples
2. Modify examples to experiment with different behaviors
3. Try creating your own simple workflow
4. Move on to intermediate examples
5. Build a project combining multiple concepts

## Additional Resources

- [Official LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph GitHub Repository](https://github.com/langchain-ai/langgraph)
- [LangChain Discord Community](https://discord.gg/langchain)

## Getting Help

If you encounter issues:

1. Check the example code comments
2. Review the official documentation
3. Search for similar issues on GitHub
4. Ask questions in the LangChain Discord community

## Contributing

Found a bug or want to add an example? Contributions are welcome! Please submit a pull request or open an issue.

---

Happy learning! 🚀
