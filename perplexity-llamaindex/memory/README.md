Here’s a brief README for the `memory` directory:
# Memory Management with LlamaIndex and Perplexity Sonar API

## Overview
This directory explores solutions for preserving conversational memory in applications powered by large language models (LLMs). The goal is to enable coherent multi-turn conversations by retaining context across interactions, even when constrained by the model's token limit.

## Problem Statement

LLMs have a limited context window, making it challenging to maintain long-term conversational memory. Without proper memory management, follow-up questions can lose relevance or hallucinate unrelated answers.

## Approaches
Using LlamaIndex, we implemented two distinct strategies for solving this problem:

### 1. **Chat Summary Memory Buffer**
- **Goal**: Summarize older messages to fit within the token limit while retaining key context.
- **Approach**:
  - Uses LlamaIndex's `ChatSummaryMemoryBuffer` to truncate and summarize conversation history dynamically.
  - Ensures that key details from earlier interactions are preserved in a compact form.
- **Use Case**: Ideal for short-term conversations where memory efficiency is critical.

### 2. **Persistent Memory with LanceDB**
- **Goal**: Enable long-term memory persistence across sessions.
- **Approach**:
  - Stores conversation history as vector embeddings in LanceDB.
  - Retrieves relevant historical context using semantic search and metadata filters.
  - Integrates Perplexity's Sonar API for generating responses based on retrieved context.
- **Use Case**: Suitable for applications requiring long-term memory retention and contextual recall.

## Directory Structure
```
memory/
├── chat_summary_memory_buffer/   # Implementation of summarization-based memory
├── chat_with_persistence/        # Implementation of persistent memory with LanceDB
```

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/api-cookbook.git
   cd api-cookbook/perplexity-llamaindex/memory
   ```
2. Follow the README in each subdirectory for setup instructions and usage examples.

## Contributions

If you have found another way to do tackle the same issue using LlamaIndex please feel free to open a PR! Check out our `CONTRIBUTING.md` file for more guidance. 

---

