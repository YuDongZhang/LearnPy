---
name: "code-assistant"
description: "AI coding assistant with code analysis, documentation generation, and testing capabilities. Invoke when user asks for code review, documentation, or test generation."
---

# Code Assistant

This skill provides comprehensive coding assistance including:

## Features

### Code Analysis
- Analyze code structure and complexity
- Detect potential issues and bugs
- Check code style and best practices

### Documentation Generation
- Generate docstrings in multiple styles (Google, NumPy, Sphinx)
- Create README files
- Generate inline comments

### Test Generation
- Create unit tests
- Generate test cases for edge cases
- Support multiple testing frameworks

## Usage

```python
# Analyze code
result = await skill.execute("analyze_code", {"code": "def foo(): pass"})

# Generate documentation
result = await skill.execute("generate_docstring", {"code": "def add(a, b): return a + b"})

# Generate tests
result = await skill.execute("generate_tests", {"code": "def add(a, b): return a + b"})
```

## Parameters

- `code`: Code to process (required)
- `language`: Programming language (optional, default: python)
- `style`: Documentation style (optional, default: google)

## Examples

**Code Review:**
```
User: Review this code
Skill: Analyzes code and provides detailed feedback
```

**Documentation:**
```
User: Generate docs for this function
Skill: Creates comprehensive docstring
```

**Testing:**
```
User: Write tests for this
Skill: Generates unit test cases
```
