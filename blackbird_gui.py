import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def run_blackbird():
    username = username_entry.get().strip()
    email = email_entry.get().strip()
    output_text.delete(1.0, tk.END)
    if not username and not email:
        output_text.insert(tk.END, "Error: Please enter a username or email.\n")
        return

    args = ["python", "blackbird.py"]
    if username:
        args += ["--username", username]
    if email:
        args += ["--email", email]
    args += ["--pdf"]

    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(args, capture_output=True, text=True, cwd=os.path.dirname(__file__), env=env)
        stdout = result.stdout if result.stdout is not None else ""
        stderr = result.stderr if result.stderr is not None else ""
        output = stdout + "\n" + stderr
        output_text.insert(tk.END, output)
        # Find the PDF file path in the output
        pdf_path = None
        for line in output.splitlines():
            if "Saved results to" in line and ".pdf" in line:
                pdf_path = line.split("to '")[-1].split("'")[0]
                break
        if pdf_path and os.path.exists(pdf_path):
            output_text.insert(tk.END, f"\nPDF saved at: {os.path.abspath(pdf_path)}\n")
    except Exception as e:
        output_text.insert(tk.END, f"Exception: {str(e)}\n")

root = tk.Tk()
root.title("Blackbird Minimal GUI")

tk.Label(root, text="Username:").grid(row=0, column=0, sticky="e")
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Email:").grid(row=1, column=0, sticky="e")
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=1, column=1, padx=5, pady=5)

search_btn = tk.Button(root, text="Search & Export to PDF", command=run_blackbird)
search_btn.grid(row=2, column=0, columnspan=2, pady=10)

# Output text box for showing output and errors
import tkinter.scrolledtext as st
output_text = st.ScrolledText(root, width=70, height=20, wrap=tk.WORD)
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()