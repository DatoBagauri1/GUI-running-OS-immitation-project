import tkinter as tk
from tkinter import filedialog

def open_notes(parent):
    notes = tk.Toplevel(parent)
    notes.title("Notes")
    notes.geometry("500x400")

    # Bring to front
    notes.lift()
    notes.attributes('-topmost', True)
    notes.after(100, lambda: notes.attributes('-topmost', False))

    text = tk.Text(notes, wrap="word")
    text.pack(fill="both", expand=True)

    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text.get("1.0", tk.END))

    menubar = tk.Menu(notes)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Exit", command=notes.destroy)
    menubar.add_cascade(label="File", menu=file_menu)
    notes.config(menu=menubar)
