cat > README.md << 'EOF'
# LangGraph FastAPI Agent

A FastAPI code generator that uses LangGraph workflows and Ollama with local LLMs to generate working FastAPI applications.

## Features

- 🤖 Uses local LLMs via Ollama (Qwen3:8b, DeepSeek-R1, etc.)
- 🚀 Generates complete FastAPI projects with working code
- 🔧 Automatic virtual environment setup and testing
- 📚 Includes API documentation and README files
- ⚡ Robust error handling and fallback templates
- 🎯 CRUD operations for task management APIs

## Requirements

- Python 3.9+
- Ollama installed and running
- A local LLM model (e.g., qwen3:8b, deepseek-r1:latest)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/langraph-fastapi-agent.git
cd langraph-fastapi-agent