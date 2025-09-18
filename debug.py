# debug.py
import ast
from translators.python_parser import parse_python_to_ir
from translators.gen_js import generate_js_from_ir

py_code = """def add(a, b=0):
    return a + b"""

print("Python code:")
print(repr(py_code))
print()

tree = ast.parse(py_code)
print("AST dump:")
print(ast.dump(tree, indent=2))
print()

ir = parse_python_to_ir(py_code)
print("IR:")
print(ir)
print()

js_code = generate_js_from_ir(ir)
print("Generated JS:")
print(js_code)