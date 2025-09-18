# Code Snippet Translator

[![CI](https://github.com/yourusername/code-snippet-translator/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/code-snippet-translator/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/yourusername/code-snippet-translator/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/code-snippet-translator)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful tool to translate code snippets between Python, JavaScript, and Java using an intermediate representation approach.

## ✨ Features

- 🔄 **Bidirectional Translation**: Python ↔ JavaScript ↔ Java
- 🏗️ **Intermediate Representation**: Clean, extensible IR for accurate translations
- ⚡ **Fast CLI**: Command-line interface for quick translations
- 🧪 **Well Tested**: Comprehensive test suite with pytest
- 📦 **Easy Installation**: Simple setup with pip
- 🎯 **MVP Focused**: Supports essential language constructs

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/code-snippet-translator.git
cd code-snippet-translator

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Translate Python to JavaScript
python cli.py --from-lang py --to-lang js examples/add.py

# Translate JavaScript to Python
python cli.py --from-lang js --to-lang py examples/add.js

# Translate Python to Java
python cli.py --from-lang py --to-lang java examples/add.py
```

## 📖 Examples

### Python to JavaScript

**Input (examples/add.py):**
```python
def add(a, b=0):
    if a > 0:
        return a + b
    else:
        return 0
```

**Output:**
```javascript
function add(a, b = 0) {
  if (a > 0) {
    return a + b;
  } else {
    return 0;
  }
}
```

### JavaScript to Python

**Input (examples/add.js):**
```javascript
function multiply(x, y = 1) {
  return x * y;
}
```

**Output:**
```python
def multiply(x, y=1):
    return x * y
```

## 🏗️ Architecture

```
Source Code → AST Parser → Intermediate Representation → Code Generator → Target Code
```

### Components

- **`translators/`**: Core translation logic
  - `python_parser.py`: Python AST parsing
  - `js_parser.py`: JavaScript parsing via Babel
  - `java_parser.py`: Java parsing via javalang
  - `gen_*.py`: Target language code generators
  - `ir.py`: Intermediate representation definitions

- **`cli.py`**: Command-line interface
- **`tests/`**: Unit tests and integration tests
- **`examples/`**: Sample code snippets

## 🎯 Supported Constructs

### Expressions
- Literals (strings, numbers, booleans)
- Binary operations (+, -, *, /, ==, !=, <, >, etc.)
- Variable names

### Statements
- If/else conditional statements
- Return statements
- Variable assignments

### Functions
- Function definitions with parameters
- Default parameter values
- Simple function bodies

See [SCOPE.md](SCOPE.md) for complete details.

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=translators

# Run specific test
pytest tests/test_basic.py::test_python_to_javascript_function
```

### Code Quality

```bash
# Format Python code
black translators/ cli.py tests/

# Lint Python code
flake8 translators/ cli.py tests/

# Type checking
mypy translators/ cli.py
```

### Adding New Features

1. Update `SCOPE.md` with new constructs
2. Add parser support in appropriate `*_parser.py`
3. Update IR definitions in `ir.py` if needed
4. Implement code generation in `gen_*.py`
5. Add comprehensive tests
6. Update documentation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/code-snippet-translator.git
cd code-snippet-translator

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Make changes and submit PR
```

## 📋 Roadmap

- [ ] Web interface with Monaco editor
- [ ] Support for more language constructs (loops, classes)
- [ ] VS Code extension
- [ ] API for programmatic usage
- [ ] Docker containerization
- [ ] Performance optimizations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Python `ast` module for robust parsing
- Babel for JavaScript AST parsing
- javalang for Java parsing
- Click for CLI framework
- pytest for testing framework