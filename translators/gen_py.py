# translators/gen_py.py
"""
Python Code Generator from IR

Generates Python code from intermediate representation
"""

from typing import Any, Dict, List
from .ir import IRNode


class PyGenerator:
    """Generates Python code from IR"""

    def __init__(self, ir: IRNode):
        self.ir = ir

    def generate(self) -> str:
        """Generate Python code from IR"""
        if self.ir["type"] == "Module":
            return self._generate_module(self.ir)
        return self._generate_node(self.ir)

    def _generate_module(self, module: IRNode) -> str:
        """Generate module code"""
        code = []
        for node in module["body"]:
            code.append(self._generate_node(node))
        return "\n\n".join(code)

    def _generate_node(self, node: IRNode) -> str:
        """Generate code for a single IR node"""
        node_type = node["type"]

        if node_type == "Function":
            return self._generate_function(node)
        elif node_type == "Return":
            return self._generate_return(node)
        elif node_type == "BinaryOp":
            return self._generate_binary_op(node)
        elif node_type == "Name":
            return node["id"]
        elif node_type == "Literal":
            return self._generate_literal(node)
        elif node_type == "Assign":
            return self._generate_assign(node)
        elif node_type == "If":
            return self._generate_if(node)
        elif node_type == "For":
            return self._generate_for(node)
        elif node_type == "While":
            return self._generate_while(node)
        elif node_type == "Call":
            return self._generate_call(node)
        elif node_type == "Class":
            return self._generate_class(node)

        return f"# Unsupported: {node_type}"

    def _generate_function(self, node: IRNode) -> str:
        """Generate function code"""
        name = node["name"]
        params = []
        for param in node["params"]:
            param_str = param["name"]
            if param.get("default"):
                param_str += f"={param['default']}"
            params.append(param_str)

        params_str = ", ".join(params)
        body = "\n".join([f"    {self._generate_node(stmt)}" for stmt in node["body"]])

        return f"def {name}({params_str}):\n{body}"

    def _generate_return(self, node: IRNode) -> str:
        """Generate return statement"""
        value = self._generate_node(node["value"]) if node.get("value") else ""
        return f"return {value}"

    def _generate_binary_op(self, node: IRNode) -> str:
        """Generate binary operation"""
        left = self._generate_node(node["left"])
        right = self._generate_node(node["right"])
        op = node["op"]
        return f"{left} {op} {right}"

    def _generate_literal(self, node: IRNode) -> str:
        """Generate literal value"""
        value = node["value"]
        if isinstance(value, str):
            return f'"{value}"'
        elif value is None:
            return "None"
        elif isinstance(value, bool):
            return "True" if value else "False"
        return str(value)

    def _generate_assign(self, node: IRNode) -> str:
        """Generate assignment"""
        target = self._generate_node(node["target"])
        value = self._generate_node(node["value"])
        return f"{target} = {value}"

    def _generate_if(self, node: IRNode) -> str:
        """Generate if statement"""
        test = self._generate_node(node["test"])
        body = "\n".join([f"    {self._generate_node(stmt)}" for stmt in node["body"]])
        code = f"if {test}:\n{body}"

        if node.get("orelse"):
            orelse_body = "\n".join(
                [f"    {self._generate_node(stmt)}" for stmt in node["orelse"]]
            )
            code += f"\nelse:\n{orelse_body}"

        return code

    def _generate_for(self, node: IRNode) -> str:
        """Generate for loop (simplified)"""
        target = self._generate_node(node["target"])
        iter = self._generate_node(node["iter"])
        body = "\n".join([f"    {self._generate_node(stmt)}" for stmt in node["body"]])
        return f"for {target} in range({iter}):\n{body}"

    def _generate_while(self, node: IRNode) -> str:
        """Generate while loop"""
        test = self._generate_node(node["test"])
        body = "\n".join([f"    {self._generate_node(stmt)}" for stmt in node["body"]])
        return f"while {test}:\n{body}"

    def _generate_call(self, node: IRNode) -> str:
        """Generate function call"""
        func = self._generate_node(node["func"])
        args = [self._generate_node(arg) for arg in node["args"]]
        args_str = ", ".join(args)
        return f"{func}({args_str})"

    def _generate_class(self, node: IRNode) -> str:
        """Generate class"""
        name = node["name"]
        body = "\n".join(
            [f"    {self._generate_node(member)}" for member in node["body"]]
        )
        return f"class {name}:\n{body}"


def generate_py_from_ir(ir: IRNode) -> str:
    """Convenience function to generate Python from IR"""
    generator = PyGenerator(ir)
    return generator.generate()
