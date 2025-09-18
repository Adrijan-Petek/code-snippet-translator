# translators/gen_java.py
"""
Java Code Generator from IR

Generates Java code from intermediate representation
"""

from typing import cast

from .ir import IRNode


class JavaGenerator:
    """Generates Java code from IR"""

    def __init__(self, ir: IRNode):
        self.ir = ir

    def generate(self) -> str:
        """Generate Java code from IR"""
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
        node_type = cast(str, node["type"])

        if node_type == "Function":
            return self._generate_function(node)
        elif node_type == "Return":
            return self._generate_return(node)
        elif node_type == "BinaryOp":
            return self._generate_binary_op(node)
        elif node_type == "Name":
            return str(node["id"])
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

        return "// Unsupported: " + str(node_type)

    def _generate_function(self, node: IRNode) -> str:
        """Generate function code (as static method)"""
        name = node["name"]
        params = []
        for param in node["params"]:
            # Simplified: use Object type
            param_str = f"Object {param['name']}"
            params.append(param_str)

        params_str = ", ".join(params)
        body = "\n".join(
            [f"        {self._generate_node(stmt)}" for stmt in node["body"]]
        )

        return f"    public static Object {name}({params_str}) {{\n{body}\n    }}"

    def _generate_return(self, node: IRNode) -> str:
        """Generate return statement"""
        value = self._generate_node(node["value"]) if node.get("value") else ""
        return f"return {value};"

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
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def _generate_assign(self, node: IRNode) -> str:
        """Generate assignment"""
        target = self._generate_node(node["target"])
        value = self._generate_node(node["value"])
        return f"Object {target} = {value};"

    def _generate_if(self, node: IRNode) -> str:
        """Generate if statement"""
        test = self._generate_node(node["test"])
        body = "\n".join(
            [f"        {self._generate_node(stmt)}" for stmt in node["body"]]
        )
        code = f"if ({test}) {{\n{body}\n    }}"

        if node.get("orelse"):
            orelse_body = "\n".join(
                [f"        {self._generate_node(stmt)}" for stmt in node["orelse"]]
            )
            code += f" else {{\n{orelse_body}\n    }}"

        return code

    def _generate_for(self, node: IRNode) -> str:
        """Generate for loop (simplified)"""
        target = self._generate_node(node["target"])
        iter = self._generate_node(node["iter"])
        body = "\n".join(
            [f"        {self._generate_node(stmt)}" for stmt in node["body"]]
        )
        template = (
            "for (int {target} = 0; {target} < (Integer){iter}; "
            "{target}++) {{\n{body}\n    }}"
        )
        return template.format(target=target, iter=iter, body=body)

    def _generate_while(self, node: IRNode) -> str:
        """Generate while loop"""
        test = self._generate_node(node["test"])
        body = "\n".join(
            [f"        {self._generate_node(stmt)}" for stmt in node["body"]]
        )
        return f"while ({test}) {{\n{body}\n    }}"

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
        return f"public class {name} {{\n{body}\n}}"


def generate_java_from_ir(ir: IRNode) -> str:
    """Convenience function to generate Java from IR"""
    generator = JavaGenerator(ir)
    return generator.generate()
