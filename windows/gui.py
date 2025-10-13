import tkinter as tk
from tkinter import messagebox
from logger import logger

log = logger()
log.debug("Logger initialized.")

def launchGUI(callback):
    # Create main window
    root = tk.Tk()
    root.title("CyberPatriot Security Tool")
    root.geometry("300x150")
    root.configure(bg="#1c1c3c")  # DarkBlue3-ish background

    # Title label
    title = tk.Label(root, text="CyberPatriot Security Tool", font=("Helvetica", 16), fg="white", bg="#1c1c3c")
    title.pack(pady=20)

    # Button frame
    button_frame = tk.Frame(root, bg="#1c1c3c")
    button_frame.pack()

    def on_run():
        callback()
        messagebox.showinfo("Security Checks", "Security checks completed.")

    def on_exit():
        root.destroy()

    run_button = tk.Button(button_frame, text="Run Security Checks", command=on_run, width=20)
    exit_button = tk.Button(button_frame, text="Exit", command=on_exit, width=20)

    run_button.grid(row=0, column=0, padx=10, pady=5)
    exit_button.grid(row=1, column=0, padx=10, pady=5)

    root.mainloop()