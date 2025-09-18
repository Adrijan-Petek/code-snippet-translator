# translators/js_parser.py
"""
JavaScript Parser for Code Snippet Translator

Uses Node.js helper to parse JS and convert Babel AST to IR
"""

import json
import os
import subprocess
from typing import Any, Dict, List, Optional

from .ir import IRBuilder, IRNode


class JSToIR:
    """Converts JavaScript code to IR using Babel parser"""

    def __init__(self, source_code: str):
        self.source_code = source_code

    def parse(self) -> IRNode:
        """Parse JS code and return IR Module"""
        ast_json = self._get_ast_json()
        if "error" in ast_json:
            raise ValueError(f"JS parsing error: {ast_json['error']}")

        body = self._convert_program(ast_json["program"])
        return IRBuilder.module(body)

    def _get_ast_json(self) -> Dict[str, Any]:
        """Get AST JSON from Node.js parser"""
        try:
            # Get the absolute path to the tools directory
            tools_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"
            )
            script_path = os.path.join(tools_dir, "parse_js.js")

            result = subprocess.run(
                ["node", script_path],
                input=self.source_code,
                text=True,
                capture_output=True,
            )
            if result.returncode != 0:
                return {"error": result.stderr}
            return json.loads(result.stdout)  # type: ignore[no-any-return]
        except Exception as e:
            return {"error": str(e)}

    def _convert_program(self, program: Dict[str, Any]) -> List[IRNode]:
        """Convert Babel program body to IR nodes"""
        body = []
        for node in program.get("body", []):
            ir_node = self._convert_node(node)
            if ir_node:
                body.append(ir_node)
        return body

    def _convert_node(self, node: Dict[str, Any]) -> Optional[IRNode]:
        """Convert Babel AST node to IR"""
        node_type = node.get("type")

        if node_type == "FunctionDeclaration":
            return self._convert_function(node)
        elif node_type == "ReturnStatement":
            return self._convert_return(node)
        elif node_type == "BinaryExpression":
            return self._convert_binary_op(node)
        elif node_type == "Identifier":
            return IRBuilder.name(node["name"])
        elif node_type == "Literal":
            return IRBuilder.literal(node["value"])
        elif node_type == "NumericLiteral":
            return IRBuilder.literal(node["value"])
        elif node_type == "VariableDeclaration":
            # Simplified: handle first declarator
            if node.get("declarations"):
                decl = node["declarations"][0]
                init_node = self._convert_node(decl["init"]) if decl.get("init") else None
                return IRBuilder.assign(
                    IRBuilder.name(decl["id"]["name"]),
                    init_node if init_node is not None else IRBuilder.literal(None),
                )
        elif node_type == "IfStatement":
            return self._convert_if(node)
        elif node_type == "ForStatement":
            return self._convert_for(node)
        elif node_type == "WhileStatement":
            return self._convert_while(node)
        elif node_type == "CallExpression":
            return self._convert_call(node)
        elif node_type == "ClassDeclaration":
            return self._convert_class(node)

        # Skip unsupported nodes
        return None

    def _convert_function(self, node: Dict[str, Any]) -> IRNode:
        name = node["id"]["name"] if node.get("id") else "anonymous"
        params = []
        for p in node.get("params", []):
            if p["type"] == "Identifier":
                params.append(IRBuilder.param(p["name"]))
            elif p["type"] == "AssignmentPattern":
                param_name = p["left"]["name"]
                default_str = str(p["right"].get("value", "undefined"))
                params.append(IRBuilder.param(param_name, default_str))
        body = [
            ir_stmt
            for stmt in node.get("body", {}).get("body", [])
            if stmt and (ir_stmt := self._convert_node(stmt)) is not None
        ]
        return IRBuilder.function(name, params, body)

    def _convert_return(self, node: Dict[str, Any]) -> IRNode:
        value = self._convert_node(node["argument"]) if node.get("argument") else None
        return IRBuilder.return_stmt(value)

    def _convert_binary_op(self, node: Dict[str, Any]) -> IRNode:
        left = self._convert_node(node["left"])
        right = self._convert_node(node["right"])
        if left is None or right is None:
            return IRBuilder.literal(None)  # fallback
        op = node["operator"]
        return IRBuilder.binary_op(op, left, right)

    def _convert_if(self, node: Dict[str, Any]) -> IRNode:
        test = self._convert_node(node["test"])
        if test is None:
            return IRBuilder.literal(None)  # fallback
        body = [
            ir_stmt
            for stmt in node.get("consequent", {}).get("body", [])
            if stmt and (ir_stmt := self._convert_node(stmt)) is not None
        ]
        orelse = []
        if node.get("alternate"):
            if node["alternate"]["type"] == "BlockStatement":
                orelse = [
                    ir_stmt
                    for stmt in node["alternate"].get("body", [])
                    if stmt and (ir_stmt := self._convert_node(stmt)) is not None
                ]
            else:
                alt_node = self._convert_node(node["alternate"])
                if alt_node is not None:
                    orelse = [alt_node]
        return IRBuilder.if_stmt(test, body, orelse)

    def _convert_for(self, node: Dict[str, Any]) -> IRNode:
        # Simplified for loop conversion
        target = (
            self._convert_node(node["init"]["declarations"][0]["id"])
            if node.get("init")
            else IRBuilder.name("i")
        )
        if target is None:
            target = IRBuilder.name("i")
        iter = (
            self._convert_node(node["test"])
            if node.get("test")
            else IRBuilder.literal(10)
        )  # placeholder
        if iter is None:
            iter = IRBuilder.literal(10)
        body = [
            ir_stmt
            for stmt in node.get("body", {}).get("body", [])
            if stmt and (ir_stmt := self._convert_node(stmt)) is not None
        ]
        return IRBuilder.for_stmt(target, iter, body)

    def _convert_while(self, node: Dict[str, Any]) -> IRNode:
        test = self._convert_node(node["test"])
        if test is None:
            return IRBuilder.literal(None)  # fallback
        body = [
            ir_stmt
            for stmt in node.get("body", {}).get("body", [])
            if stmt and (ir_stmt := self._convert_node(stmt)) is not None
        ]
        return IRBuilder.while_stmt(test, body)

    def _convert_call(self, node: Dict[str, Any]) -> IRNode:
        func = self._convert_node(node["callee"])
        if func is None:
            return IRBuilder.literal(None)  # fallback
        args = [
            arg for arg in [
                self._convert_node(arg) for arg in node.get("arguments", [])
            ] if arg is not None
        ]
        return IRBuilder.call(func, args)

    def _convert_class(self, node: Dict[str, Any]) -> IRNode:
        name = node["id"]["name"]
        body = [
            ir_stmt
            for stmt in node.get("body", {}).get("body", [])
            if stmt and (ir_stmt := self._convert_node(stmt)) is not None
        ]
        return IRBuilder.class_def(name, body)


def parse_js_to_ir(source_code: str) -> IRNode:
    """Convenience function to parse JS code to IR"""
    parser = JSToIR(source_code)
    return parser.parse()
