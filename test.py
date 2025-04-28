import os

def print_tree(root, depth=0, max_depth=3, prefix=""):
    if depth > max_depth:
        return
    for i, item in enumerate(sorted(os.listdir(root))):
        path = os.path.join(root, item)
        connector = "└── " if i == len(os.listdir(root)) - 1 else "├── "
        print(f"{prefix}{connector}{item}")
        if os.path.isdir(path):
            extension = "    " if i == len(os.listdir(root)) - 1 else "│   "
            print_tree(path, depth + 1, max_depth, prefix + extension)

# Usage
print_tree(".", max_depth=2)