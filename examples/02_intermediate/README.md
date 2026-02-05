# Intermediate Examples

This directory contains intermediate-level examples that build upon the basics and introduce more advanced concepts.

## Examples

### 1. multi_agent.py
**Difficulty**: ⭐⭐⭐ Intermediate  
**Concepts**: Multiple agents, agent coordination, collaborative workflows

Demonstrates how to coordinate multiple specialized AI agents working together to accomplish a task. Each agent has its own role and expertise.

**What you'll learn**:
- Creating multiple specialized agents
- Coordinating agent workflows
- Sequential agent collaboration
- Task delegation patterns

**Requirements**: OpenAI API key in `.env` file

**Run it**:
```bash
python examples/02_intermediate/multi_agent.py
```

**Use cases**:
- Content creation pipelines (research → write → review)
- Multi-step analysis workflows
- Specialized task processing

---

### 2. human_in_loop.py
**Difficulty**: ⭐⭐⭐ Intermediate  
**Concepts**: Human oversight, approval workflows, interactive processing

Shows how to add human approval steps in automated workflows, allowing for human oversight and intervention when needed.

**What you'll learn**:
- Pausing execution for human input
- Implementing approval workflows
- Handling user feedback
- Resuming execution after approval

**Run it**:
```bash
python examples/02_intermediate/human_in_loop.py
```

**Use cases**:
- Content moderation
- Critical decision approval
- Quality assurance workflows
- Sensitive data processing

---

### 3. persistence.py
**Difficulty**: ⭐⭐⭐ Intermediate  
**Concepts**: State persistence, checkpoints, thread management, recovery

Demonstrates how to save and resume workflow state, essential for long-running processes and error recovery.

**What you'll learn**:
- Using checkpointers to save state
- Thread-based state isolation
- Resuming workflows from checkpoints
- Managing multiple concurrent workflows

**Run it**:
```bash
python examples/02_intermediate/persistence.py
```

**Use cases**:
- Long-running batch processes
- Workflows that span multiple sessions
- Error recovery and retry logic
- Multi-user applications

---

## Key Takeaways

After completing these examples, you should understand:

1. ✅ How to build multi-agent systems
2. ✅ How to incorporate human oversight
3. ✅ How to persist and resume workflows
4. ✅ How to handle complex state management

## Design Patterns

These examples introduce important design patterns:

- **Collaboration Pattern**: Multiple agents working sequentially
- **Approval Pattern**: Human checkpoints in automation
- **Persistence Pattern**: Saving and resuming state

## Next Steps

Ready for more advanced concepts? Check out the examples in `examples/03_advanced/`.
