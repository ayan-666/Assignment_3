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

class ImageDisplay:

class ImageEditorApp:


if __name__ == "__main__":
