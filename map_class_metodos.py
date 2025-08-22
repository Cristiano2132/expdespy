import ast
import os

SRC_DIR = "/Users/cristianooliveira/Documents/expdespy/src/expdespy"
OUTPUT_FILE = "/Users/cristianooliveira/Documents/expdespy/classes_methods_map.txt"

def scan_file(filepath, out):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            print(f"\nClass: {node.name} (File: {filepath})", file=out)
            doc = ast.get_docstring(node)
            if doc:
                print(f"  Docstring: {doc[:80]}{'...' if len(doc)>80 else ''}", file=out)
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    print(f"  Method: {item.name}", file=out)
                    doc_m = ast.get_docstring(item)
                    if doc_m:
                        print(f"    Docstring: {doc_m[:80]}{'...' if len(doc_m)>80 else ''}", file=out)
        elif isinstance(node, ast.FunctionDef):
            # Top-level functions
            if hasattr(node, "parent") and isinstance(node.parent, ast.Module):
                print(f"\nFunction: {node.name} (File: {filepath})", file=out)
                doc = ast.get_docstring(node)
                if doc:
                    print(f"  Docstring: {doc[:80]}{'...' if len(doc)>80 else ''}", file=out)

def add_parents(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source, filename=path)
                add_parents(tree)
                scan_file(path, out)