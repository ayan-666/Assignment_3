'''
Overview:
1. Import some neccessary package, add some other neccessary package along the development of the program
2. Create classes for image processing, image displaying, image croping etc requirements
3. In each class, create specific functions that fulfil the requirements of the program
4. In each function and each module, check the user input and other possible error
5. Try to optimize the whole code
'''

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import cv2
import numpy as np

class ImageProcessor:
    """Handling all image processing operations using OpenCV with some functions"""
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.undo_stack = []

    def load_image(self, file_path):
        """Load and validate image from file path using is_file function and checking if it matches the ending"""
        try:
            # Validate file path
            if not Path(file_path).is_file():
                raise FileNotFoundError("File does not exist")
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                raise ValueError("Unsupported image format")

            # Read image with OpenCV
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                raise ValueError("Failed to load image")
            
            self.current_image = self.original_image.copy()
            self.undo_stack = []  # Reset undo stack on new image load
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            return False
        
    def crop_image(self, x1, y1, x2, y2):
        """setting co-ordinates from where user can crop the particular image"""
        try:
            # Validate coordinates
            if not self.current_image is None:
                h, w = self.current_image.shape[:2]
                x1, x2 = max(0, min(x1, x2)), min(w, max(x1, x2))
                y1, y2 = max(0, min(y1, y2)), min(h, max(y1, y2))
                
                if x2 <= x1 or y2 <= y1:
                    raise ValueError("Invalid crop dimensions")
                
                # Save for undo operation if the user intends any changes
                self.undo_stack.append(self.current_image.copy())
                self.current_image = self.current_image[y1:y2, x1:x2]
                return True
        except Exception as e:
            messagebox.showerror("Error", f"Crop failed: {str(e)}")
            return False
        
    def resize_image(self, scale):
        """Resize image"""
        """Handling error if no image is loaded"""
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
            if not 0.1 <= scale <= 2.0:
                raise ValueError("Scale must be between 0.1 and 2.0")
            
            h, w = self.original_image.shape[:2]
            new_size = (int(w * scale), int(h * scale))
            self.current_image = cv2.resize(self.original_image, new_size, interpolation=cv2.INTER_AREA)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Resize failed: {str(e)}")
            return False


class ImageDisplay:

class ImageEditorApp:


if __name__ == "__main__":
