# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a hands-on learning repository for the Strands AI Agents framework. It provides progressive examples demonstrating core features of Strands through numbered, independent examples (01_basic through 07_multi_agents).

## Commands

### Development Setup
```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev
```

### Testing & Quality
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Type checking
uv run pyright
```

### Running Examples
```bash
# Run specific example module
uv run python -m strands_agents_hands_on.examples.01_basic.agent
uv run python -m strands_agents_hands_on.examples.02_session.local_session_management
```

## Architecture

### Core Structure
- **src/strands_agents_hands_on/config.py**: Centralized configuration using Pydantic settings. Uses `find_env_file()` to recursively locate `.env` file from project root. All settings are automatically exported to `os.environ`.
- **src/strands_agents_hands_on/examples/**: Numbered examples (01-07) for progressive learning. Each subdirectory is self-contained and independently runnable.

### Examples Organization
Examples are numbered to indicate learning progression:
1. **01_basic/**: Basic agent creation and usage
2. **02_session/**: Session management (local, S3, custom)
3. **03_hooks/**: Lifecycle hooks
4. **04_structured_output/**: Pydantic-based structured responses
5. **05_tools/**: Python tools and tool combinations
6. **06_streaming/**: Streaming responses
7. **07_multi_agents/**: Multi-agent patterns (Swarm and Agent-as-Tool)

### Multi-Agent Patterns

Two distinct patterns for agent collaboration:

**Agents as Tools (Hierarchical)**:
- Orchestrator agent delegates to specialized agents
- Clear top-down control flow
- Each specialist agent operates in isolated context
- Best for: predictable routing, simple delegation, easier debugging

**Swarm (Collaborative)**:
- Flat structure with autonomous handoffs between agents
- Shared context across all agents
- Agents self-coordinate using `handoff_to_agent` tool
- Configured with safety limits: `max_handoffs`, `max_iterations`, `execution_timeout`
- Best for: complex tasks requiring dynamic collaboration, emergent problem-solving

See docs/swarm_vs_agents_as_tools.md for detailed comparison and use cases.

## Configuration

### Environment Variables
Create `.env` file in project root with:
```
OPENAI_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

Settings class automatically finds `.env` via recursive parent directory search and exports values to environment.

## Code Standards

### Ruff Configuration
- Line length: 120 characters
- Most rules enabled (`select = ["ALL"]`)
- Notable exceptions: docstrings optional (D1), print() allowed (T201), todo tags allowed (TD)
- Tests have relaxed rules: asserts allowed (S101), magic values OK (PLR2004)

### Type Checking
- Pyright with "standard" mode
- Target Python 3.12

## Dependencies

Core dependencies:
- strands-agents >= 1.10.0 (main framework)
- boto3 >= 1.40.41 (for S3 session management)
- pydantic-settings >= 2.10.1 (configuration management)
