# translators/python_parser.py
"""
Python Parser for Code Snippet Translator

Converts Python AST to intermediate representation (IR)
"""

from typing import List

import ast

from .ir import IRBuilder, IRNode


class PythonToIR(ast.NodeVisitor):
    """Converts Python AST nodes to IR"""

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.ir_body: List[IRNode] = []

    def parse(self) -> IRNode:
        """Parse source code and return IR Module"""
        tree = ast.parse(self.source_code)
        self.visit(tree)
        return IRBuilder.module(self.ir_body)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        params = []
        for arg in node.args.args:
            default = None
            if node.args.defaults:
                # Handle defaults (simplified)
                idx = len(node.args.args) - len(node.args.defaults)
                if arg.arg in [a.arg for a in node.args.args[idx:]]:
                    default_idx = [a.arg for a in node.args.args].index(arg.arg) - idx
                    if default_idx >= 0 and default_idx < len(node.args.defaults):
                        default = ast.unparse(node.args.defaults[default_idx])
            params.append(IRBuilder.param(arg.arg, default))

        body = []
        for stmt in node.body:
            ir_stmt = self.visit(stmt)
            if ir_stmt is not None:
                body.append(ir_stmt)

        self.ir_body.append(IRBuilder.function(node.name, params, body))

    def visit_Return(self, node: ast.Return) -> IRNode:
        value = self.visit(node.value) if node.value else None
        return IRBuilder.return_stmt(value)

    def visit_BinOp(self, node: ast.BinOp) -> IRNode:
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self._get_op(node.op)
        return IRBuilder.binary_op(op, left, right)

    def visit_Name(self, node: ast.Name) -> IRNode:
        return IRBuilder.name(node.id)

    def visit_Constant(self, node: ast.Constant) -> IRNode:
        return IRBuilder.literal(node.value)

    def visit_Assign(self, node: ast.Assign) -> IRNode:
        # Simplified: assume single target
        target = self.visit(node.targets[0])
        value = self.visit(node.value)
        return IRBuilder.assign(target, value)

    def visit_If(self, node: ast.If) -> IRNode:
        test = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        orelse = [self.visit(stmt) for stmt in node.orelse] if node.orelse else []
        return IRBuilder.if_stmt(test, body, orelse)

    def visit_For(self, node: ast.For) -> IRNode:
        target = self.visit(node.target)
        iter = self.visit(node.iter)
        body = [self.visit(stmt) for stmt in node.body]
        return IRBuilder.for_stmt(target, iter, body)

    def visit_While(self, node: ast.While) -> IRNode:
        test = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        return IRBuilder.while_stmt(test, body)

    def visit_Call(self, node: ast.Call) -> IRNode:
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return IRBuilder.call(func, args)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        body = [self.visit(stmt) for stmt in node.body]
        self.ir_body.append(IRBuilder.class_def(node.name, body))

    def visit_Module(self, node: ast.Module) -> None:
        for stmt in node.body:
            self.visit(stmt)

    def visit_Compare(self, node: ast.Compare) -> IRNode:
        if len(node.ops) == 1 and len(node.comparators) == 1:
            left = self.visit(node.left)
            op = self._get_op(node.ops[0])
            right = self.visit(node.comparators[0])
            return IRBuilder.binary_op(op, left, right)
        # For multiple comparisons, not supported for MVP
        return IRBuilder.literal(True)  # placeholder

    def visit_Expr(self, node: ast.Expr) -> None:
        """Handle expression statements (like docstrings) - skip them for MVP"""
        pass

    def _get_op(self, op: ast.operator) -> str:
        """Convert AST operator to string"""
        op_map = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.Gt: ">",
            ast.LtE: "<=",
            ast.GtE: ">=",
        }
        return op_map.get(type(op), str(op))

    def generic_visit(self, node):
        """Fallback for unsupported nodes"""
        # For MVP, skip unsupported constructs
        pass


def parse_python_to_ir(source_code: str) -> IRNode:
    """Convenience function to parse Python code to IR"""
    parser = PythonToIR(source_code)
    return parser.parse()
