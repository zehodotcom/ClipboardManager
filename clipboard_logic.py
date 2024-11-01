import pyperclip
import time


class ClipboardManager:
    def __init__(self):
        self.clipboard_history = []
        self.last_content = ""

    def monitor_clipboard(self, callback):
        while True:
            current_content = pyperclip.paste()
            # Check if the current clipboard content is different from the last saved content
            if current_content != self.last_content and current_content.strip():
                self.last_content = current_content
                # Get the current timestamp with day of the week in English
                timestamp = time.strftime("%A, %Y-%m-%d %H:%M:%S")
                self.clipboard_history.append((current_content, timestamp))
                callback(
                    current_content, timestamp
                )  # Call the callback function with the new content
            time.sleep(1)

    def get_history(self):
        return self.clipboard_history
