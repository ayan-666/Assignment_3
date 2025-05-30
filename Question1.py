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
from PIL import Image, ImageTk
import os
from pathlib import Path
import uuid


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
        

    def apply_grayscale(self):
        """Apply grayscale filter to the loaded image"""
        try:
            if self.current_image is None:
                raise ValueError("No image loaded")
            
            self.undo_stack.append(self.current_image.copy())
            self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            if len(self.current_image.shape) == 2:
                self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_GRAY2BGR)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Grayscale failed: {str(e)}")
            return False

    def save_image(self, file_path):
        """Save current image to specified path and handling error here"""
        try:
            if self.current_image is None:
                raise ValueError("No image to save")
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValueError("Unsupported save format")
            
            cv2.imwrite(file_path, self.current_image)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")
            return False

    def undo(self):
        """Revert to previous image state if the user intends"""
        if self.undo_stack:
            self.current_image = self.undo_stack.pop()
            return True
        return False


class ImageDisplay:
     """Handles image display and canvas operations"""
    def __init__(self, canvas):
        self.canvas = canvas
        self.photo = None
        self.display_image = None
        self.max_display_size = 600

    def update_display(self, image):
        """View the new image"""
        try:
            if image is None:
                raise ValueError("No image to display")
            
            # Calculate display size while maintaining aspect ratio
            h, w = image.shape[:2]
            scale = min(self.max_display_size/w, self.max_display_size/h)
            display_size = (int(w * scale), int(h * scale))
            
            # Resize and convert for display
            display_img = cv2.resize(image, display_size)
            display_img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
            self.display_image = Image.fromarray(display_img)
            self.photo = ImageTk.PhotoImage(self.display_image)
            
            # Update the view for the image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.canvas.config(width=display_size[0], height=display_size[1])
        except Exception as e:
            messagebox.showerror("Error", f"Display failed: {str(e)}")

    def draw_rectangle(self, start_x, start_y, current_x, current_y, rect_id):
        """Draw cropping rectangle on image"""
        if rect_id:
            self.canvas.delete(rect_id)
        return self.canvas.create_rectangle(
            start_x, start_y, current_x, current_y,
            outline="red", dash=(4, 4)
        )

class ImageEditorApp: 
     """Main application class coordinating UI and image processing."""
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1200x800")
        
        self.image_processor = ImageProcessor()
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.cropping = False
        
        self.setup_ui()
        self.bind_shortcuts()

    def setup_ui(self):
        """Set up the main UI components."""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for image display
        self.canvas = tk.Canvas(self.main_frame, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.image_display = ImageDisplay(self.canvas)

        # Control panel
        self.control_frame = ttk.Frame(self.main_frame, width=200)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Buttons
        ttk.Button(self.control_frame, text="Load Image (Ctrl+O)", command=self.load_image).pack(fill=tk.X, pady=5)
        ttk.Button(self.control_frame, text="Save Image (Ctrl+S)", command=self.save_image).pack(fill=tk.X, pady=5)
        ttk.Button(self.control_frame, text="Grayscale", command=self.apply_grayscale).pack(fill=tk.X, pady=5)
        ttk.Button(self.control_frame, text="Undo (Ctrl+Z)", command=self.undo).pack(fill=tk.X, pady=5)

        # Resize slider
        ttk.Label(self.control_frame, text="Resize Scale").pack(pady=5)
        self.scale_var = tk.DoubleVar(value=1.0)
        self.scale = ttk.Scale(self.control_frame, from_=0.1, to=2.0, orient=tk.HORIZONTAL,
                             variable=self.scale_var, command=self.resize_image)
        self.scale.pack(fill=tk.X, pady=5)

        # Canvas bindings for cropping
        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.draw_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

    def bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-o>", lambda event: self.load_image())
        self.root.bind("<Control-s>", lambda event: self.save_image())

    def load_image(self):
        """Handle image loading with file dialog."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path and self.image_processor.load_image(file_path):
            self.image_display.update_display(self.image_processor.current_image)

    def start_crop(self, event):
        """Start cropping operation."""
        if self.image_processor.current_image is None:
            return
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.cropping = True
        if self.rect_id:
            self.canvas.delete(self.rect_id)

    def draw_crop(self, event):
        """Draw cropping rectangle during mouse drag."""
        if not self.cropping:
            return
        current_x = self.canvas.canvasx(event.x)
        current_y = self.canvas.canvasy(event.y)
        self.rect_id = self.image_display.draw_rectangle(
            self.start_x, self.start_y, current_x, current_y, self.rect_id
        )

    def end_crop(self, event):
        """Complete cropping operation."""
        if not self.cropping:
            return
        self.cropping = False
        current_x = self.canvas.canvasx(event.x)
        current_y = self.canvas.canvasy(event.y)

        try:
            # Convert canvas coordinates to image coordinates
            h, w = self.image_processor.current_image.shape[:2]
            canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
            scale = min(canvas_w/w, canvas_h/h)
            
            x1 = int(min(self.start_x, current_x) / scale)
            y1 = int(min(self.start_y, current_y) / scale)
            x2 = int(max(self.start_x, current_x) / scale)
            y2 = int(max(self.start_y, current_y) / scale)

            if self.image_processor.crop_image(x1, y1, x2, y2):
                self.image_display.update_display(self.image_processor.current_image)
        except Exception as e:
            messagebox.showerror("Error", f"Crop failed: {str(e)}")
        finally:
            if self.rect_id:
                self.canvas.delete(self.rect_id)
                self.rect_id = None

    def resize_image(self, event=None):
        """Handle image resizing from slider."""
        if self.image_processor.resize_image(self.scale_var.get()):
            self.image_display.update_display(self.image_processor.current_image)

    def apply_grayscale(self):
        """Apply grayscale filter and update display."""
        if self.image_processor.apply_grayscale():
            self.image_display.update_display(self.image_processor.current_image)

    def save_image(self):
        """Handle image saving with file dialog."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        if file_path:
            self.image_processor.save_image(file_path)

    def undo(self):
        """Handle undo operation."""
        if self.image_processor.undo():
            self.image_display.update_display(self.image_processor.current_image)

    def run(self):
        """Start the main application loop."""
        self.root.mainloop()
    #Complete Image Editor App
    
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ImageEditorApp(root)
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")
    
    
