# translators/java_parser.py
"""
Java Parser for Code Snippet Translator

Uses javalang to parse Java code and convert to IR
"""

from typing import List, Optional

import javalang

from .ir import IRBuilder, IRNode


class JavaToIR:
    """Converts Java code to IR using javalang"""

    def __init__(self, source_code: str):
        self.source_code = source_code

    def parse(self) -> IRNode:
        """Parse Java code and return IR Module"""
        try:
            tree = javalang.parse.parse(self.source_code)
            body = self._convert_compilation_unit(tree)
            return IRBuilder.module(body)
        except Exception as e:
            raise ValueError(f"Java parsing error: {str(e)}")

    def _convert_compilation_unit(self, tree) -> List[IRNode]:
        """Convert compilation unit to IR nodes"""
        body = []
        for type_decl in tree.types:
            ir_node = self._convert_type_declaration(type_decl)
            if ir_node:
                body.append(ir_node)
        return body

    def _convert_type_declaration(self, node) -> IRNode:
        """Convert type declaration (class) to IR"""
        if isinstance(node, javalang.tree.ClassDeclaration):
            body = []
            for member in node.body:
                ir_member = self._convert_member(member)
                if ir_member:
                    body.append(ir_member)
            return IRBuilder.class_def(node.name, body)
        return IRBuilder.literal(None)  # fallback for unsupported types

    def _convert_member(self, node) -> Optional[IRNode]:
        """Convert class member to IR"""
        if isinstance(node, javalang.tree.MethodDeclaration):
            params = [IRBuilder.param(p.name) for p in node.parameters]
            body = self._convert_block(node.body) if node.body else []
            return IRBuilder.function(node.name, params, body)
        elif isinstance(node, javalang.tree.FieldDeclaration):
            # Simplified field handling
            if node.declarators:
                decl = node.declarators[0]
                init_expr = (
                    self._convert_expression(decl.initializer)
                    if decl.initializer
                    else None
                )
                return IRBuilder.assign(
                    IRBuilder.name(decl.name),
                    init_expr if init_expr is not None else IRBuilder.literal(None),
                )
        return None

    def _convert_block(self, block) -> List[IRNode]:
        """Convert block statement to IR nodes"""
        if not block:
            return []
        body = []
        for stmt in block:
            ir_stmt = self._convert_statement(stmt)
            if ir_stmt:
                body.append(ir_stmt)
        return body

    def _convert_statement(self, node) -> Optional[IRNode]:
        """Convert statement to IR"""
        if isinstance(node, javalang.tree.ReturnStatement):
            value = (
                self._convert_expression(node.expression) if node.expression else None
            )
            return IRBuilder.return_stmt(value)
        elif isinstance(node, javalang.tree.IfStatement):
            test = self._convert_expression(node.condition)
            if test is None:
                test = IRBuilder.literal(True)  # fallback
            body = self._convert_block(node.then_statement)
            orelse = (
                self._convert_block(node.else_statement) if node.else_statement else []
            )
            return IRBuilder.if_stmt(test, body, orelse)
        elif isinstance(node, javalang.tree.ForStatement):
            # Simplified
            target = IRBuilder.name("i")  # placeholder
            iter_expr = (
                self._convert_expression(node.condition) if node.condition else None
            )
            iter = iter_expr if iter_expr is not None else IRBuilder.literal(10)
            body = self._convert_block(node.body)
            return IRBuilder.for_stmt(target, iter, body)
        elif isinstance(node, javalang.tree.WhileStatement):
            test = self._convert_expression(node.condition)
            if test is None:
                test = IRBuilder.literal(True)  # fallback
            body = self._convert_block(node.body)
            return IRBuilder.while_stmt(test, body)
        elif isinstance(node, javalang.tree.StatementExpression):
            expr = self._convert_expression(node.expression)
            return expr if expr is not None else IRBuilder.literal(None)
        return None

    def _convert_expression(self, node) -> Optional[IRNode]:
        """Convert expression to IR"""
        if isinstance(node, javalang.tree.BinaryOperation):
            left = self._convert_expression(node.operandl)
            right = self._convert_expression(node.operandr)
            if left is None or right is None:
                return IRBuilder.literal(None)  # fallback
            op = node.operator
            return IRBuilder.binary_op(op, left, right)
        elif isinstance(node, javalang.tree.Literal):
            return IRBuilder.literal(node.value)
        elif isinstance(node, javalang.tree.MemberReference):
            return IRBuilder.name(node.member)
        elif isinstance(node, javalang.tree.MethodInvocation):
            func = IRBuilder.name(node.member)
            args = [
                arg
                for arg in [self._convert_expression(arg) for arg in node.arguments]
                if arg is not None
            ]
            return IRBuilder.call(func, args)
        elif isinstance(node, javalang.tree.Assignment):
            target = self._convert_expression(node.expressionl)
            value = self._convert_expression(node.value)
            if target is None or value is None:
                return IRBuilder.literal(None)  # fallback
            return IRBuilder.assign(target, value)
        return IRBuilder.literal(str(node))  # fallback


def parse_java_to_ir(source_code: str) -> IRNode:
    """Convenience function to parse Java code to IR"""
    parser = JavaToIR(source_code)
    return parser.parse()
