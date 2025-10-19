import tkinter as tk
from tkinter import messagebox
from logger import logger

log = logger()
log.debug("Logger initialized.")

def launchGUI(callback):
    # Create main window
    root = tk.Tk()
    root.title("CyberPatriot Security Tool")
    # root.geometry("540x360")
    root.state("zoomed")
    root.configure(bg="#1c1c3c")  # DarkBlue3-ish background

    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    title_font_size = int(height / 15)
    button_font_size = int(height / 80)

    # Title label
    title = tk.Label(root, text="CyberPatriot Security Tool", font=("Helvetica", title_font_size), fg="white", bg="#1c1c3c")
    title.pack(pady=150)

    # Button frame
    button_frame = tk.Frame(root, bg="#1c1c3c")
    button_frame.pack()

    def on_run(x: int=0, category: str=""):
        message = callback(x)
        messagebox.showinfo(category, f"{category}:\n{message}")

    def on_exit():
        root.destroy()

    run_all_button = tk.Button(button_frame, text="Run All Security Checks", command=lambda: on_run(0, "Security Checks"), width=20, font=("Helvetica", button_font_size))
    security_policies_button = tk.Button(button_frame, text="Security Policy Checks", command=lambda: on_run(1, "Security Policy Checks"), width=20, font=("Helvetica", button_font_size))
    user_accounts_button = tk.Button(button_frame, text="User Accounts Checks", command=lambda: on_run(2, "User Accounts Checks"), width=20, font=("Helvetica", button_font_size))
    exit_button = tk.Button(button_frame, text="Exit", command=on_exit, width=20, font=("Helvetica", button_font_size))

    run_all_button.grid(row=0, column=0, columnspan=2, padx=40, pady=25)
    security_policies_button.grid(row=1, column=0, padx=40, pady=25)
    user_accounts_button.grid(row=1, column=1, padx=40, pady=25)
    exit_button.grid(row=2, column=0, columnspan=2, padx=40, pady=25)

    root.mainloop()