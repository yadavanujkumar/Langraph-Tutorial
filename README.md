# LangGraph Tutorial

A comprehensive tutorial for learning LangGraph - LangChain's library for building stateful, multi-actor applications with Large Language Models (LLMs).

## 📚 What is LangGraph?

LangGraph is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. It extends LangChain Expression Language with the ability to coordinate multiple chains (or actors) across multiple steps of computation in a cyclic manner.

## 🌟 Key Features

- **Stateful Graphs**: Build applications that maintain state across multiple steps
- **Cycles and Branches**: Create complex workflows with conditional logic
- **Human-in-the-Loop**: Add human approval steps in your workflows
- **Persistence**: Save and resume workflow state
- **Multi-Agent Systems**: Coordinate multiple AI agents working together

## 📋 Prerequisites

- Python 3.8 or higher
- Basic understanding of Python
- Familiarity with LangChain (recommended but not required)
- OpenAI API key (or other LLM provider)

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yadavanujkumar/Langraph-Tutorial.git
cd Langraph-Tutorial
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## 📖 Tutorial Structure

### 1. Basic Examples
- **[Simple Chain](examples/01_basic/simple_chain.py)**: Introduction to basic graph structure
- **[Stateful Conversation](examples/01_basic/stateful_conversation.py)**: Building a chatbot that remembers context
- **[Conditional Branching](examples/01_basic/conditional_branching.py)**: Using conditional edges for dynamic workflows

### 2. Intermediate Examples
- **[Multi-Agent System](examples/02_intermediate/multi_agent.py)**: Coordinating multiple agents
- **[Human-in-the-Loop](examples/02_intermediate/human_in_loop.py)**: Adding human approval steps
- **[Persistence](examples/02_intermediate/persistence.py)**: Saving and loading workflow state

### 3. Advanced Examples
- **[Complex Workflow](examples/03_advanced/complex_workflow.py)**: Building sophisticated multi-step applications
- **[Sub-graphs](examples/03_advanced/subgraphs.py)**: Organizing complex graphs with sub-graphs

## 🏃 Running Examples

Each example can be run independently:

```bash
# Basic examples
python examples/01_basic/simple_chain.py
python examples/01_basic/stateful_conversation.py
python examples/01_basic/conditional_branching.py

# Intermediate examples
python examples/02_intermediate/multi_agent.py
python examples/02_intermediate/human_in_loop.py
python examples/02_intermediate/persistence.py

# Advanced examples
python examples/03_advanced/complex_workflow.py
python examples/03_advanced/subgraphs.py
```

## 📚 Learn More

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph GitHub Repository](https://github.com/langchain-ai/langgraph)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [LangChain](https://github.com/langchain-ai/langchain)
