#!/usr/bin/env python3

import ast
from pathlib import Path

IGNORE_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    "build",
    "dist",
    "node_modules",
}

def format_args(node):
    args = []

    # 普通参数
    for arg in node.args.args:
        text = arg.arg

        if arg.annotation:
            text += f": {ast.unparse(arg.annotation)}"

        args.append(text)

    # *args
    if node.args.vararg:
        text = f"*{node.args.vararg.arg}"

        if node.args.vararg.annotation:
            text += f": {ast.unparse(node.args.vararg.annotation)}"

        args.append(text)

    # keyword only
    for arg in node.args.kwonlyargs:
        text = arg.arg

        if arg.annotation:
            text += f": {ast.unparse(arg.annotation)}"

        args.append(text)

    # **kwargs
    if node.args.kwarg:
        text = f"**{node.args.kwarg.arg}"

        if node.args.kwarg.annotation:
            text += f": {ast.unparse(node.args.kwarg.annotation)}"

        args.append(text)

    return ", ".join(args)


def format_return(node):
    if node.returns:
        return f" -> {ast.unparse(node.returns)}"
    return ""


def print_node(node, indent=0):
    prefix = "│   " * indent

    if isinstance(node, ast.ClassDef):
        if node.bases:
            bases = ", ".join(ast.unparse(x) for x in node.bases)
            print(f"{prefix}├── class {node.name}({bases})")
        else:
            print(f"{prefix}├── class {node.name}")

        for item in node.body:
            print_node(item, indent + 1)

    elif isinstance(node, ast.FunctionDef):
        args = format_args(node)

        print(
            f"{prefix}├── def {node.name}"
            f"({args})"
            f"{format_return(node)}"
        )

        for item in node.body:
            if isinstance(item, (ast.FunctionDef,
                                 ast.AsyncFunctionDef,
                                 ast.ClassDef)):
                print_node(item, indent + 1)

    elif isinstance(node, ast.AsyncFunctionDef):
        args = format_args(node)

        print(
            f"{prefix}├── async def {node.name}"
            f"({args})"
            f"{format_return(node)}"
        )

        for item in node.body:
            if isinstance(item, (ast.FunctionDef,
                                 ast.AsyncFunctionDef,
                                 ast.ClassDef)):
                print_node(item, indent + 1)


def should_ignore(path: Path):
    return any(part in IGNORE_DIRS for part in path.parts)


def scan_project(root="."):
    for file in sorted(Path(root).rglob("*.py")):
        if should_ignore(file):
            continue

        try:
            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
            tree = ast.parse(source)
        except Exception as e:
            print(f"\n{file}")
            print(f"└── [PARSE ERROR] {e}")
            continue

        print(f"\n{file}")

        found = False

        for node in tree.body:
            if isinstance(
                node,
                (
                    ast.ClassDef,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                found = True
                print_node(node)

        if not found:
            print("└── (no top-level classes/functions)")


if __name__ == "__main__":
    scan_project(".")