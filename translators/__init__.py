# translators/__init__.py
"""
Main translation functions
"""

from .python_parser import parse_python_to_ir
from .js_parser import parse_js_to_ir
from .java_parser import parse_java_to_ir
from .gen_py import generate_py_from_ir
from .gen_js import generate_js_from_ir
from .gen_java import generate_java_from_ir
from .ir import IRNode


def translate_snippet(source_code: str, from_lang: str, to_lang: str) -> str:
    """Translate code snippet from one language to another"""
    # Parse source to IR
    if from_lang == "py":
        ir = parse_python_to_ir(source_code)
    elif from_lang == "js":
        ir = parse_js_to_ir(source_code)
    elif from_lang == "java":
        ir = parse_java_to_ir(source_code)
    else:
        raise ValueError(f"Unsupported source language: {from_lang}")

    # Generate target code
    if to_lang == "py":
        return generate_py_from_ir(ir)
    elif to_lang == "js":
        return generate_js_from_ir(ir)
    elif to_lang == "java":
        return generate_java_from_ir(ir)
    else:
        raise ValueError(f"Unsupported target language: {to_lang}")
