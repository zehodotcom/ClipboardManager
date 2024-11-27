import os
import pyperclip
import time
from PIL import Image, ImageGrab
import re
import ctypes

class ClipboardManager:
    def __init__(self):
        self.clipboard_history = []
        self.last_text_content = ""
        self.last_image_content = None
        self.image_folder = "clipboard_images"
        os.makedirs(self.image_folder, exist_ok=True)

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', "", filename)

    def monitor_clipboard(self, callback):
        while True:
            current_text_content = pyperclip.paste()
            if current_text_content != self.last_text_content and current_text_content.strip():
                self.last_text_content = current_text_content
                timestamp = time.strftime("%A, %Y-%m-%d %H:%M:%S")
                content_type = self.detect_content_type(current_text_content)
                self.clipboard_history.append((content_type, current_text_content, timestamp))
                callback(content_type, current_text_content, timestamp)
            else:
                image = ImageGrab.grabclipboard()
                if isinstance(image, Image.Image):
                    if image.tobytes() != (self.last_image_content.tobytes() if self.last_image_content else None):
                        timestamp = time.strftime("%A, %m-%d-%Y %H-%M-%S")
                        filename = f"clipboard_image_{timestamp}.png"
                        filename = self.sanitize_filename(filename)
                        full_path = os.path.join(self.image_folder, filename)
                        image.save(full_path)
                        self.clipboard_history.append(("Image", full_path, timestamp))
                        callback("Image", full_path, timestamp)
                        self.last_image_content = image
            time.sleep(1)

    def detect_content_type(self, clipboard_content):
        # Check for URL
        if clipboard_content.startswith("http://") or clipboard_content.startswith("https://"):
            return "URL"
        # Check for Email
        elif re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", clipboard_content):
            return "Email"
        return "Text"

    def detect_files_from_explorer(self, callback):
        clipboard = ctypes.windll.user32
        if clipboard.OpenClipboard(0):
            try:
                if clipboard.IsClipboardFormatAvailable(15):  # CF_HDROP format
                    message = "File copied from explorer."
                    timestamp = time.strftime("%A, %Y-%m-%d %H:%M:%S")
                    self.clipboard_history.append((message, "", timestamp))
                    callback("File", message, timestamp)
            finally:
                clipboard.CloseClipboard()

    def get_history(self):
        return self.clipboard_history
