import tkinter as tk
from pynput import keyboard
import json

# ---------------- GLOBAL VARIABLES ----------------
keys = []
pressed_keys = set()
listener = None
is_logging = False

LOG_FILE = "logs.json"

# ---------------- FILE HANDLING ----------------
def save_to_json():
    with open(LOG_FILE, "w") as file:
        json.dump(keys, file, indent=4)

# ---------------- KEYBOARD EVENTS ----------------
def on_press(key):
    if key not in pressed_keys:
        pressed_keys.add(key)
        keys.append({"Pressed": str(key)})
        save_to_json()

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)
        keys.append({"Released": str(key)})
        save_to_json()

    # Stop logging if ESC is pressed
    if key == keyboard.Key.esc:
        stop_logging()

# ---------------- CONTROL FUNCTIONS ----------------
def start_logging():
    global listener, is_logging

    if not is_logging:
        is_logging = True
        status_label.config(text="Status: Logging Started", fg="green")

        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        listener.start()

def stop_logging():
    global listener, is_logging

    if listener:
        listener.stop()
        listener = None

    is_logging = False
    status_label.config(text="Status: Logging Stopped", fg="red")

def exit_app():
    stop_logging()
    root.destroy()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Educational Key Logger")
root.geometry("300x220")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Key Logger (Educational)",
    font=("Arial", 14, "bold")
)
title_label.pack(pady=10)

info_label = tk.Label(
    root,
    text="Click START to log keys\nPress ESC or STOP to end",
    fg="blue"
)
info_label.pack(pady=5)

status_label = tk.Label(
    root,
    text="Status: Not Logging",
    fg="red",
    font=("Arial", 10, "bold")
)
status_label.pack(pady=5)

start_btn = tk.Button(
    root,
    text="Start",
    width=15,
    bg="green",
    fg="white",
    command=start_logging
)
start_btn.pack(pady=5)

stop_btn = tk.Button(
    root,
    text="Stop",
    width=15,
    bg="red",
    fg="white",
    command=stop_logging
)
stop_btn.pack(pady=5)

exit_btn = tk.Button(
    root,
    text="Exit",
    width=15,
    command=exit_app
)
exit_btn.pack(pady=10)

root.mainloop()
