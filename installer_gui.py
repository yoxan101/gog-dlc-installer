import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from installer_logic import Installer  # Import installation logic
import os
import subprocess
import threading
import logging
import psutil
import base64
import tempfile

# Create the main window
root = tk.Tk()
root.title("GOG DLC Installer")
root.geometry("800x600")

def load_icon_from_base64():
    if 'ICON_BASE64' in globals():
        icon_data = base64.b64decode(ICON_BASE64)
        icon_path = tempfile.NamedTemporaryFile(delete=False, suffix=".ico").name
        with open(icon_path, "wb") as icon_file:
            icon_file.write(icon_data)
        return icon_path
    return None

# 🔹 Load the icon into the Tkinter window
icon_path = load_icon_from_base64()
if icon_path:
    root.iconbitmap(icon_path)

# Load the background
def set_background():
    global bg_image
    try:
        image = Image.open("logo.png")
        image = image.resize((800, 600))
        bg_image = ImageTk.PhotoImage(image)

        canvas = tk.Canvas(root, width=800, height=600)
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.create_image(0, 0, anchor="nw", image=bg_image)

        main_frame.lift()
    except Exception as e:
        print(f"Failed to load background: {e}")

# Directory selection
def select_directory(entry_widget):
    path = filedialog.askdirectory()
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)

# File selection
def select_file(entry_widget, initial_dir):
    path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Executables", "*.exe")])
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)

# Logging to the interface
def update_log(message):
    log_text.config(state=tk.NORMAL)

    # Check the last line in the log to avoid duplicates
    last_log = log_text.get("end-2l", "end-1l")
    if message.strip() == last_log.strip():
        log_text.config(state=tk.DISABLED)
        return  # Do not add a duplicate

    log_text.insert(tk.END, message + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)

# Start installation
installer = None

def start_installation():
    global installer

    if installer is not None and installer.installing:
        update_log("⚠️ Installation is already running. Please wait.")
        return

    install_dir = install_dir_entry.get()
    target_dir = target_dir_entry.get()
    file_path = file_entry.get()

    if os.path.exists(install_dir) and os.path.exists(target_dir) and os.path.exists(file_path):
        install_button.config(text="Cancel", command=cancel_installation)

        installer = Installer(install_dir, target_dir, file_path, True, update_log, progress_bar, progress_label)

        install_thread = threading.Thread(target=installer.install_all, daemon=True)
        install_thread.start()
    else:
        update_log("❌ Invalid paths. Please check your directories.")

# Cancel installation
def cancel_installation():
    global installer

    if installer is not None and installer.installing:
        install_button.config(state=tk.DISABLED)
        installer.cancel_installation()
        install_button.config(text="Start install", command=start_installation, state=tk.NORMAL)

# Create the interface
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(column=0, row=0, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(9, weight=1)

# Fields and buttons
ttk.Label(main_frame, text="Installers directory:").grid(column=0, row=1, sticky="w")
install_dir_entry = ttk.Entry(main_frame, width=50)
install_dir_entry.grid(column=1, row=1, sticky="ew")
ttk.Button(main_frame, text="Browse", command=lambda: select_directory(install_dir_entry)).grid(column=2, row=1, sticky="w")

ttk.Label(main_frame, text="Target directory:").grid(column=0, row=2, sticky="w")
target_dir_entry = ttk.Entry(main_frame, width=50)
target_dir_entry.grid(column=1, row=2, sticky="ew")
ttk.Button(main_frame, text="Browse", command=lambda: select_directory(target_dir_entry)).grid(column=2, row=2, sticky="w")

ttk.Label(main_frame, text="First installer:").grid(column=0, row=3, sticky="w")
file_entry = ttk.Entry(main_frame, width=50)
file_entry.grid(column=1, row=3, sticky="ew")
ttk.Button(main_frame, text="Select file", command=lambda: select_file(file_entry, install_dir_entry.get())).grid(column=2, row=3, sticky="w")

install_button = ttk.Button(main_frame, text="Start install", command=start_installation)
install_button.grid(column=1, row=6, pady=10, sticky="ew")

progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate", maximum=100)
progress_bar.grid(column=0, row=8, columnspan=2, sticky="ew", pady=10)

progress_label = ttk.Label(main_frame, text="0 / 0 Installed")
progress_label.grid(column=2, row=8, sticky="w", padx=10)

log_text = tk.Text(main_frame, height=10, width=60)
log_text.grid(column=0, row=9, columnspan=3, sticky="nsew")
log_text.config(state=tk.DISABLED)

# Set the background
set_background()

# Run the GUI
root.mainloop()