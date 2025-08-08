import threading
import subprocess
import os
import time
import socket
import webview
from flask import Flask, render_template, request, redirect, url_for
import tkinter as tk
import queue

# === Flask App ===
app = Flask(__name__, template_folder="templates", static_folder="static")
logged_in = False

@app.route('/')
def home():
    if not logged_in:
        return redirect(url_for('login'))
    return render_template('desktop.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in
    if request.method == 'POST':
        if request.form.get('username') == 'user' and request.form.get('password') == '123':
            logged_in = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# === Tkinter Apps ===
from apps.terminal import open_terminal
from apps.notes import open_notes
from apps.file_explorer import open_file_explorer

gui_queue = queue.Queue()
root = None  # global tkinter root

@app.route('/terminal')
def terminal():
    print("[DEBUG] Launching Terminal")
    try:
        gui_queue.put(lambda: open_terminal(root))
        return '', 204
    except Exception as e:
        print("[ERROR] Terminal failed:", e)
        return str(e), 500

@app.route('/notes')
def notes():
    print("[DEBUG] Launching Notes")
    try:
        gui_queue.put(lambda: open_notes(root))
        return '', 204
    except Exception as e:
        print("[ERROR] Notes failed:", e)
        return str(e), 500

@app.route('/files')
def files():
    print("[DEBUG] Launching Files")
    try:
        gui_queue.put(lambda: open_file_explorer(root))
        return '', 204
    except Exception as e:
        print("[ERROR] File Explorer failed:", e)
        return str(e), 500

# === Flask Server ===
def start_flask():
    app.run(debug=False, use_reloader=False)

def wait_for_flask():
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", 5000), timeout=1)
            return True
        except:
            time.sleep(0.1)
    return False

# === Tkinter loop that handles GUI app launches ===
def gui_loop():
    global root
    root = tk.Tk()
    root.withdraw()

    def poll_queue():
        while not gui_queue.empty():
            try:
                func = gui_queue.get_nowait()
                func()
            except Exception as e:
                print("[ERROR] Running GUI task:", e)
        root.after(100, poll_queue)

    root.after(100, poll_queue)
    root.mainloop()

# === MAIN ===
if __name__ == '__main__':
    threading.Thread(target=gui_loop, daemon=True).start()        # Tkinter loop
    threading.Thread(target=start_flask, daemon=True).start()     # Flask server
    wait_for_flask()

    # Start Webview on MAIN THREAD
    webview.create_window("PyLinux", "http://127.0.0.1:5000", width=1024, height=768)
    webview.start(gui='edgechromium')
