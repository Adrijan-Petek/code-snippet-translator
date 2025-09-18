# Contributing to Code Snippet Translator

Thank you for your interest in contributing to the Code Snippet Translator! We welcome contributions from everyone.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/code-snippet-translator.git`
3. Create a virtual environment: `python -m venv .venv`
4. Activate: `.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (Unix)
5. Install dependencies: `pip install -r requirements.txt`
6. Install dev dependencies: `pip install -r requirements-dev.txt`
7. Run tests: `pytest`

## 🧪 Development Workflow

### 1. Choose an Issue
- Check the [Issues](https://github.com/yourusername/code-snippet-translator/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes
- Write clear, concise commit messages
- Follow the existing code style
- Add tests for new features
- Update documentation as needed

### 4. Run Quality Checks
```bash
# Format code
black translators/ cli.py tests/

# Sort imports
isort translators/ cli.py tests/

# Lint
flake8 translators/ cli.py tests/

# Type check
mypy translators/ cli.py

# Run tests
pytest
```

### 5. Submit a Pull Request
- Push your branch to GitHub
- Create a Pull Request with a clear description
- Reference any related issues
- Wait for review and address feedback

## 📝 Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Pre-commit Hooks (Recommended)

Install pre-commit to run quality checks automatically:

```bash
pip install pre-commit
pre-commit install
```

## 🏗️ Architecture Guidelines

### Adding New Language Support

1. **Parser**: Create `translators/<lang>_parser.py`
2. **Generator**: Create `translators/gen_<lang>.py`
3. **Tests**: Add tests in `tests/test_<lang>.py`
4. **CLI**: Update CLI options if needed
5. **Documentation**: Update README and SCOPE.md

### Extending the IR

When adding new constructs:

1. Update `translators/ir.py` with new node types
2. Update all parsers to handle the new construct
3. Update all generators to emit the new construct
4. Add comprehensive tests
5. Update SCOPE.md

### Example: Adding Class Support

```python
# 1. Update IR
class IRBuilder:
    @staticmethod
    def class_def(name: str, bases: List[str], body: List[IRNode]) -> IRNode:
        return {
            "type": "Class",
            "name": name,
            "bases": bases,
            "body": body
        }

# 2. Update parsers
def visit_ClassDef(self, node: ast.ClassDef) -> IRNode:
    # Implementation

# 3. Update generators
def _generate_class(self, node: IRNode) -> str:
    # Implementation
```

## 🧪 Testing

### Unit Tests
- Place in `tests/` directory
- Name files `test_*.py`
- Use descriptive test names
- Test both success and failure cases

### Integration Tests
- Test end-to-end functionality
- Use the `integration` marker
- Place complex test files in `examples/`

### Running Tests
```bash
# All tests
pytest

# Specific test
pytest tests/test_basic.py::test_python_to_javascript_function

# With coverage
pytest --cov=translators --cov-report=html

# Integration tests only
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## 📚 Documentation

### Code Documentation
- Use docstrings for all public functions
- Follow Google style guide
- Include type hints

### README Updates
- Update examples when adding features
- Keep installation instructions current
- Update supported constructs list

## 🔒 Security

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Run security scans: `bandit` and `safety`
- Report security issues privately

## 🤝 Code Review Process

### For Contributors
- Be patient and responsive to feedback
- Make requested changes promptly
- Ask questions if unclear

### For Reviewers
- Be constructive and specific
- Focus on code quality and correctness
- Suggest improvements, don't dictate
- Approve when requirements are met

## 📋 Commit Guidelines

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

### Examples
```
feat(parser): add support for async functions

fix(generator): handle empty function bodies

docs(readme): update installation instructions

test(parser): add tests for error handling
```

## 🎯 Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or improvement
- `documentation`: Documentation needed
- `good first issue`: Ideal for newcomers
- `help wanted`: Community contribution welcome
- `question`: Question or discussion needed

## 📞 Getting Help

- 📧 Email: your.email@example.com
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/code-snippet-translator/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/code-snippet-translator/issues)

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Recognized in documentation

Thank you for contributing to Code Snippet Translator! 🎉