# debug_js.py
from translators.js_parser import parse_js_to_ir
from translators.gen_py import generate_py_from_ir

js_code = """function add(a, b = 0) {
  return a + b;
}"""

print("JS code:")
print(repr(js_code))
print()

ir = parse_js_to_ir(js_code)
print("IR:")
print(ir)
print()

py_code = generate_py_from_ir(ir)
print("Generated Python:")
print(py_code)