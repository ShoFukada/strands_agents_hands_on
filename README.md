# strands-agents-hands-on

Hands-on project for building agents with Strands framework.

## Overview

This project provides practical examples and exercises for learning how to build AI agents using the Strands framework.

## Usage

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd strands-agents-hands-on

# Install dependencies
uv sync

# Install development dependencies
uv sync --dev
```

### Development

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run type checking
uv run pyright

# Format code
uv run ruff format .

uv run pre-commit install
```

### Running the application

```bash
uv run strands-agents-hands-on
```

## Project Structure

```
.
├── src/
│   └── strands_agents_hands_on/
├── tests/
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python >= 3.12
- uv package manager

## License

MIT License
