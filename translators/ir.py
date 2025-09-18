# translators/ir.py
"""
Intermediate Representation (IR) for Code Snippet Translator

This module defines the structure for the language-agnostic IR used to represent
code snippets before translation to target languages.
"""

from typing import Any, Dict, List, Optional, Union
import json

# IR Node Types
IRNode = Dict[str, Any]

class IRBuilder:
    """Helper class to build IR nodes"""

    @staticmethod
    def module(body: List[IRNode]) -> IRNode:
        return {
            "type": "Module",
            "body": body
        }

    @staticmethod
    def function(name: str, params: List[Dict[str, Any]], body: List[IRNode]) -> IRNode:
        return {
            "type": "Function",
            "name": name,
            "params": params,
            "body": body
        }

    @staticmethod
    def param(name: str, default: Optional[str] = None) -> Dict[str, Any]:
        return {
            "name": name,
            "default": default
        }

    @staticmethod
    def return_stmt(value: IRNode) -> IRNode:
        return {
            "type": "Return",
            "value": value
        }

    @staticmethod
    def binary_op(op: str, left: IRNode, right: IRNode) -> IRNode:
        return {
            "type": "BinaryOp",
            "op": op,
            "left": left,
            "right": right
        }

    @staticmethod
    def name(id: str) -> IRNode:
        return {
            "type": "Name",
            "id": id
        }

    @staticmethod
    def literal(value: Union[str, int, float, bool, None]) -> IRNode:
        return {
            "type": "Literal",
            "value": value
        }

    @staticmethod
    def assign(target: IRNode, value: IRNode) -> IRNode:
        return {
            "type": "Assign",
            "target": target,
            "value": value
        }

    @staticmethod
    def if_stmt(test: IRNode, body: List[IRNode], orelse: List[IRNode] = None) -> IRNode:
        return {
            "type": "If",
            "test": test,
            "body": body,
            "orelse": orelse or []
        }

    @staticmethod
    def for_stmt(target: IRNode, iter: IRNode, body: List[IRNode]) -> IRNode:
        return {
            "type": "For",
            "target": target,
            "iter": iter,
            "body": body
        }

    @staticmethod
    def while_stmt(test: IRNode, body: List[IRNode]) -> IRNode:
        return {
            "type": "While",
            "test": test,
            "body": body
        }

    @staticmethod
    def call(func: IRNode, args: List[IRNode]) -> IRNode:
        return {
            "type": "Call",
            "func": func,
            "args": args
        }

    @staticmethod
    def class_def(name: str, body: List[IRNode]) -> IRNode:
        return {
            "type": "Class",
            "name": name,
            "body": body
        }

def serialize_ir(ir: IRNode) -> str:
    """Serialize IR to JSON string"""
    return json.dumps(ir, indent=2)

def deserialize_ir(json_str: str) -> IRNode:
    """Deserialize JSON string to IR"""
    return json.loads(json_str)