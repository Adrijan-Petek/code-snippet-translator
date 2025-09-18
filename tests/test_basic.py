# tests/test_basic.py
"""
Basic tests for Code Snippet Translator
"""

import pytest

from translators import translate_snippet


def test_python_to_javascript_function():
    """Test translating a simple Python function to JavaScript"""
    py_code = """def add(a, b=0):
    return a + b"""

    js_code = translate_snippet(py_code, "py", "js")

    assert "function add(a, b = 0)" in js_code
    assert "return a + b;" in js_code


def test_python_to_java_function():
    """Test translating a simple Python function to Java"""
    py_code = """def add(a, b=0):
    return a + b"""

    java_code = translate_snippet(py_code, "py", "java")

    assert "public static Object add(Object a, Object b)" in java_code
    assert "return a + b;" in java_code


def test_javascript_to_python_function():
    """Test translating a simple JavaScript function to Python"""
    js_code = """function add(a, b = 0) {
  return a + b;
}"""

    py_code = translate_snippet(js_code, "js", "py")

    assert "def add(a, b=0):" in py_code
    assert "return a + b" in py_code


def test_literal_translations():
    """Test literal value translations"""
    py_code = """def test():
    return "hello" """

    js_code = translate_snippet(py_code, "py", "js")
    assert '"hello"' in js_code

    java_code = translate_snippet(py_code, "py", "java")
    assert '"hello"' in java_code


def test_binary_operations():
    """Test binary operations"""
    py_code = """def calc(a, b):
    return a + b * 2"""

    js_code = translate_snippet(py_code, "py", "js")
    assert "a + b * 2" in js_code


def test_if_statement():
    """Test if statement translation"""
    py_code = """def check(x):
    if x > 0:
        return "positive"
    else:
        return "non-positive" """

    js_code = translate_snippet(py_code, "py", "js")
    assert "if (x > 0)" in js_code
    assert 'return "positive";' in js_code
    assert "else" in js_code


if __name__ == "__main__":
    pytest.main([__file__])
