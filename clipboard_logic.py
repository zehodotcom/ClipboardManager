import os
import pyperclip
import time
from PIL import Image, ImageGrab
import re

class ClipboardManager:
    def __init__(self):
        self.clipboard_history = []
        self.last_text_content = ""
        self.last_image_content = None  # To store the last saved image
        self.image_folder = "clipboard_images"  # Folder to save images
        os.makedirs(self.image_folder, exist_ok=True)  # Create the folder if it doesn't exist

    def sanitize_filename(self, filename):
        # Sanitize filename to avoid invalid characters
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def is_url(self, text):
        # Simple regex pattern to check for URLs
        url_pattern = re.compile(r'^(https?://)')
        return bool(url_pattern.match(text))

    def monitor_clipboard(self, callback):
        while True:
            # Check for text content in the clipboard
            current_text_content = pyperclip.paste()
            if current_text_content != self.last_text_content and current_text_content.strip():
                self.last_text_content = current_text_content
                timestamp = time.strftime("%A, %Y-%m-%d %H:%M:%S")
                
                # Determine if the content is a URL or general text
                if self.is_url(current_text_content):
                    content_type = "URL"
                else:
                    content_type = "Text"
                
                self.clipboard_history.append((content_type, current_text_content, timestamp))
                callback(content_type, current_text_content, timestamp)
            
            else:
                # Check for image content in the clipboard
                image = ImageGrab.grabclipboard()
                if isinstance(image, Image.Image):
                    # Check if the image is different from the last saved image
                    if image.tobytes() != (self.last_image_content.tobytes() if self.last_image_content else None):
                        timestamp = time.strftime("%A, %m-%d-%Y %H-%M-%S")  # Safe format for filename
                        filename = f"clipboard_image_{timestamp}.png"
                        filename = self.sanitize_filename(filename)  # Sanitize the filename
                        full_path = os.path.join(self.image_folder, filename)  # Full path to save the image
                        image.save(full_path)  # Save the image to file
                        self.clipboard_history.append(("Image", full_path, timestamp))
                        callback("Image", full_path, timestamp)
                        self.last_image_content = image  # Update the last saved image
            time.sleep(1)

    def get_history(self):
        return self.clipboard_history
