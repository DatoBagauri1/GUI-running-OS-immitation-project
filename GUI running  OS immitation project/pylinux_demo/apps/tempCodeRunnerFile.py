import tkinter as tk

def open_notes(parent):
    notes = tk.Toplevel(parent)
    notes.title("Notes")
    notes.geometry("400x300")

    text = tk.Text(notes)
    text.pack(fill="both", expand=True)

    def save():
        content = text.get("1.0", tk.END)
        with open("notes.txt", "w") as f:
            f.write(content)

    def load():
        try:
            with open("notes.txt", "r") as f:
                text.insert("1.0", f.read())
        except FileNotFoundError:
            pass

    load()
    notes.protocol("WM_DELETE_WINDOW", lambda: (save(), notes.destroy()))
