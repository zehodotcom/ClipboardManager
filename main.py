import tkinter as tk
from tkinter import scrolledtext
from clipboard_logic import ClipboardManager
import threading
import pyperclip
import time

class ClipboardApp:
    def __init__(self, root):
        self.manager = ClipboardManager()
        self.root = root
        self.root.title("Clipboard Manager")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Create a text display area with a dark gray background and white text
        self.text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=102, height=36, bg="#333333", fg="white")
        self.text_display.pack(pady=10)

        # Configure text colors for entry number, timestamp, and content
        self.text_display.tag_config("number", foreground="lightgreen")
        self.text_display.tag_config("timestamp", foreground="cyan")
        self.text_display.tag_config("text", foreground="lightyellow")
        self.text_display.tag_config("url", foreground="#FFB6C1")  # Rosa claro
        self.text_display.tag_config("email", foreground="orange")
        self.text_display.tag_config("image", foreground="magenta")

        # Check initial clipboard content at startup
        initial_content = pyperclip.paste()
        if initial_content.strip():
            self.manager.last_text_content = initial_content
            content_type = self.manager.detect_content_type(initial_content)
            self.update_display(content_type, initial_content, time.strftime("%Y-%m-%d %H:%M:%S"))

        # Start a thread to monitor the clipboard
        threading.Thread(target=self.manager.monitor_clipboard, args=(self.save_and_display_content,), daemon=True).start()

    def save_and_display_content(self, content_type, new_content, timestamp):
        self.update_display(content_type, new_content, timestamp)

    def update_display(self, content_type, new_content, timestamp):
        if self.text_display.get("1.0", tk.END).strip():
            self.text_display.insert(tk.END, "\n")  # Add a newline before the new entry

        entry_number = len(self.manager.get_history())
        self.text_display.insert(tk.END, f"{entry_number}. ", "number")
        self.text_display.insert(tk.END, f"[{timestamp}] ", "timestamp")

        # Apply color tags based on content type
        if content_type == "Text":
            self.text_display.insert(tk.END, f"TEXT: {new_content}", "text")
        elif content_type == "URL":
            self.text_display.insert(tk.END, f"URL: {new_content}", "url")
        elif content_type == "Email":
            self.text_display.insert(tk.END, f"EMAIL: {new_content}", "email")
        elif content_type == "Image":
            self.text_display.insert(tk.END, f"IMAGE: {new_content}", "image")
        else:
            self.text_display.insert(tk.END, new_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardApp(root)
    root.mainloop()
