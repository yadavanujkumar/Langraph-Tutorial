# Basic Examples

This directory contains introductory examples to help you understand the fundamental concepts of LangGraph.

## Examples

### 1. simple_chain.py
**Difficulty**: ⭐ Beginner  
**Concepts**: Basic graph structure, nodes, edges, state management

A straightforward example showing how to create a sequential chain of processing steps. Perfect for understanding the basics of LangGraph.

**What you'll learn**:
- Creating a StateGraph
- Adding nodes to the graph
- Connecting nodes with edges
- Running the graph with initial state
- Understanding state flow

**Run it**:
```bash
python examples/01_basic/simple_chain.py
```

---

### 2. stateful_conversation.py
**Difficulty**: ⭐⭐ Beginner  
**Concepts**: State management, LLM integration, conversation history

Build a chatbot that maintains conversation history across multiple interactions. This example shows how to integrate Large Language Models with LangGraph.

**What you'll learn**:
- Integrating OpenAI's GPT models
- Managing conversation history
- Maintaining stateful interactions
- Working with message objects

**Requirements**: OpenAI API key in `.env` file

**Run it**:
```bash
python examples/01_basic/stateful_conversation.py
```

---

### 3. conditional_branching.py
**Difficulty**: ⭐⭐ Beginner  
**Concepts**: Conditional edges, dynamic routing, decision logic

Demonstrates how to create workflows that make decisions and branch to different paths based on the state.

**What you'll learn**:
- Using conditional edges
- Creating routing functions
- Implementing decision logic
- Building dynamic workflows

**Run it**:
```bash
python examples/01_basic/conditional_branching.py
```

---

## Key Takeaways

After completing these examples, you should understand:

1. ✅ How to structure a LangGraph workflow
2. ✅ How state flows through a graph
3. ✅ How to add conditional logic
4. ✅ How to integrate LLMs

## Next Steps

Once you're comfortable with these basics, move on to the intermediate examples in `examples/02_intermediate/`.
