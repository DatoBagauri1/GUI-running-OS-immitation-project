import tkinter as tk
import subprocess

def open_terminal(parent):
    term = tk.Toplevel(parent)
    term.title("Terminal")
    term.geometry("600x400")

    # Bring to front
    term.lift()
    term.attributes('-topmost', True)
    term.after(100, lambda: term.attributes('-topmost', False))

    output = tk.Text(term, bg="black", fg="white", insertbackground="white")
    output.pack(fill="both", expand=True)

    input_entry = tk.Entry(term, bg="black", fg="white", insertbackground="white")
    input_entry.pack(fill="x")

    def run_command(event=None):
        cmd = input_entry.get()
        input_entry.delete(0, tk.END)
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            result = e.output
        output.insert(tk.END, f"> {cmd}\n{result}\n")
        output.see(tk.END)

    input_entry.bind("<Return>", run_command)
    input_entry.focus()
