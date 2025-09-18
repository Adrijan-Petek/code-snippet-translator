# Code Snippet Translator - MVP Scope

This document defines the initial scope for the Code Snippet Translator project, supporting translations between Python, JavaScript, and Java.

## Supported Constructs (MVP)

### Expressions
- Literals (strings, numbers, booleans, null/None)
- Binary and unary operations (+, -, *, /, ==, !=, <, >, etc.)
- Variable names and identifiers

### Statements
- If/else conditional statements
- For and while loops
- Return statements
- Variable assignments

### Functions
- Function definitions with signatures
- Default arguments
- Simple function bodies
- Return statements

### Classes
- Simple class definitions
- Basic methods (no inheritance, metaclasses, or complex features)

### Basic Standard Calls
- print() ↔ console.log() ↔ System.out.println()
- len() ↔ .length/.size()
- .append() ↔ .push()
- dict/Object/Map conversions

## Out of Scope for MVP
- Async/await and generators
- Decorators and metaclasses
- Native threading
- Complex Java generics
- Advanced language-specific features
- Exception handling (initially)
- Modules and imports (basic only)

This scope will be expanded iteratively as the core translation engine proves stable.