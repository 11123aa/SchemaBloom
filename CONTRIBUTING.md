# Contributing to SchemaBloom

Thank you for your interest in contributing to SchemaBloom! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature
4. Make your changes
5. Add tests for your changes
6. Run the test suite
7. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/SchemaBloom.git
cd SchemaBloom

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pre-commit**: Git hooks

```bash
# Format code
black src/ tests/

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/
```

## Testing

We use pytest for testing. All new features should include tests.

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/

# Run specific test file
pytest tests/test_generators.py
```

## Adding New ORM Support

To add support for a new ORM:

1. Create a new generator class in `src/json_to_orm/generators/`
2. Inherit from `BaseGenerator`
3. Implement required methods
4. Add templates in `src/json_to_orm/templates/`
5. Add type mapping in `src/json_to_orm/utils/template_filters.py`
6. Add tests in `tests/test_generators.py`
7. Update CLI to include the new format

## Submitting Changes

1. Ensure all tests pass
2. Update documentation if needed
3. Add a descriptive commit message
4. Submit a pull request with a clear description

## Pull Request Guidelines

- Provide a clear description of the changes
- Include tests for new functionality
- Update documentation if needed
- Ensure the test suite passes
- Follow the existing code style

## Issues

When reporting issues:

- Use the issue template
- Provide a clear description
- Include steps to reproduce
- Share relevant code snippets
- Specify your environment (OS, Python version, etc.)

## License

By contributing to SchemaBloom, you agree that your contributions will be licensed under the MIT License. 