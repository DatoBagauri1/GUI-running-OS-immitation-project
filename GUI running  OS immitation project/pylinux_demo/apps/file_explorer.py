import tkinter as tk
from tkinter import ttk
import os

def open_file_explorer(parent):
    explorer = tk.Toplevel(parent)
    explorer.title("File Explorer")
    explorer.geometry("500x400")

    # Bring to front
    explorer.lift()
    explorer.attributes('-topmost', True)
    explorer.after(100, lambda: explorer.attributes('-topmost', False))

    tree = ttk.Treeview(explorer)
    tree.pack(fill="both", expand=True)

    abspath = os.path.abspath('.')
    root_node = tree.insert('', 'end', text=abspath, open=True)

    def process_directory(parent_node, path):
        try:
            for p in os.listdir(path):
                full_path = os.path.join(path, p)
                node = tree.insert(parent_node, 'end', text=p)
                if os.path.isdir(full_path):
                    tree.insert(node, 'end')  # Dummy child to make it expandable
        except PermissionError:
            pass

    def open_node(event):
        node = tree.focus()
        path = get_full_path(node)
        if not tree.get_children(node):
            process_directory(node, path)

    def get_full_path(node):
        path_parts = []
        while node:
            path_parts.insert(0, tree.item(node)['text'])
            node = tree.parent(node)
        return os.path.join(*path_parts)

    tree.bind('<<TreeviewOpen>>', open_node)
    process_directory(root_node, abspath)
