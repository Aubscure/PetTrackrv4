# frontend/components/image_uploader.py
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import os
import uuid
from math import degrees, radians

class ImageUploader(ctk.CTkFrame):
    def __init__(self, parent, temp_dir="backend/data/temp"):
        super().__init__(parent)
        self.temp_dir = temp_dir
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.rotation_angle = 0
        self.crop_coords = None
        self.pan_start = None
        self.image_offset = [0, 0]
        self.zoom_factor = 1.0
        self.min_zoom = 0.5  # Can now zoom out to 50%
        self.max_zoom = 3.0
        
        # Create widgets
        self.image_status = ctk.CTkLabel(self, text="📂 No image selected.", font=("Segoe UI", 10))
        self.image_status.pack(anchor="w")
        
        # Image display canvas
        self.canvas = ctk.CTkCanvas(self, width=300, height=300, bg="#f0f0f0")
        self.canvas.pack(pady=10)
        
        # Control buttons frame
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(fill="x", pady=5)
        
        # Upload button
        self.upload_btn = ctk.CTkButton(
            self.controls_frame,
            text="📸 Select Photo", 
            command=self.upload_image,
            width=100
        )
        self.upload_btn.grid(row=0, column=0, padx=5)
        
        # Rotation buttons
        self.rotate_left_btn = ctk.CTkButton(
            self.controls_frame,
            text="↩ Rotate Left",
            command=lambda: self.rotate_image(90),
            width=100,
            state="disabled"
        )
        self.rotate_left_btn.grid(row=0, column=1, padx=5)
        
        self.rotate_right_btn = ctk.CTkButton(
            self.controls_frame,
            text="↪ Rotate Right",
            command=lambda: self.rotate_image(-90),
            width=100,
            state="disabled"
        )
        self.rotate_right_btn.grid(row=0, column=2, padx=5)
        
        # Removed the square crop toggle button since it's always active now
        
        # Reset button
        self.reset_btn = ctk.CTkButton(
            self.controls_frame,
            text="🔄 Reset",
            command=self.reset_edits,
            width=100,
            state="disabled"
        )
        self.reset_btn.grid(row=0, column=3, padx=5)
        
        # Zoom controls frame
        self.zoom_frame = ctk.CTkFrame(self)
        self.zoom_frame.pack(fill="x", pady=5)
        
        self.zoom_out_btn = ctk.CTkButton(
            self.zoom_frame,
            text="🔍−",
            command=lambda: self.adjust_zoom(0.9),
            width=50,
            state="disabled"
        )
        self.zoom_out_btn.grid(row=0, column=0, padx=5)
        
        self.zoom_label = ctk.CTkLabel(self.zoom_frame, text="Zoom: 100%")
        self.zoom_label.grid(row=0, column=1, padx=5)
        
        self.zoom_in_btn = ctk.CTkButton(
            self.zoom_frame,
            text="🔍+",
            command=lambda: self.adjust_zoom(1.1),
            width=50,
            state="disabled"
        )
        self.zoom_in_btn.grid(row=0, column=2, padx=5)
        
        # Bind mouse events for panning
        self.canvas.bind("<ButtonPress-1>", self.on_pan_start)
        self.canvas.bind("<B1-Motion>", self.on_pan_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_pan_end)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        
    def upload_image(self):
        """Handle image upload"""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if not path:
            self.image_status.configure(text="📂 No image selected.")
            return
        
        try:
            self.original_image = Image.open(path).convert("RGB")
            self.current_image = self.original_image.copy()
            self.rotation_angle = 0
            self.image_offset = [0, 0]
            self.zoom_factor = 1.0
            
            self.display_image()
            self.enable_controls()
            self.image_status.configure(text="✅ Image loaded. Drag to position and scroll to zoom.")
            
        except Exception as e:
            self.image_status.configure(text=f"❌ Error: {str(e)}")
            self.disable_controls()
    
    def display_image(self):
        """Display the current image on canvas with square crop frame"""
        if not self.current_image:
            return
            
        # Clear canvas
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Create a working copy of the image
        img = self.current_image.copy()
        
        # Apply rotation for display (doesn't modify original)
        if self.rotation_angle != 0:
            img = img.rotate(self.rotation_angle, expand=True)
        
        # Calculate the size of the square crop area (80% of canvas size)
        square_size = min(canvas_width, canvas_height) * 0.8
        self.crop_size = square_size
        
        # Calculate the position of the square crop area (centered)
        self.crop_x1 = (canvas_width - square_size) / 2
        self.crop_y1 = (canvas_height - square_size) / 2
        self.crop_x2 = self.crop_x1 + square_size
        self.crop_y2 = self.crop_y1 + square_size
        
        # Draw the square crop area (always visible after upload)
        self.canvas.create_rectangle(
            self.crop_x1, self.crop_y1,
            self.crop_x2, self.crop_y2,
            outline="red", width=2, dash=(5,5))
            
        # Calculate the image size after zoom
        img_width, img_height = img.size
        zoomed_width = int(img_width * self.zoom_factor)
        zoomed_height = int(img_height * self.zoom_factor)
        
        # Resize the image with the current zoom factor
        img = img.resize((zoomed_width, zoomed_height), Image.Resampling.LANCZOS)
        
        # Calculate the position to display the image with current offset
        img_x = (canvas_width - zoomed_width) / 2 + self.image_offset[0]
        img_y = (canvas_height - zoomed_height) / 2 + self.image_offset[1]
        
        # Convert to PhotoImage
        self.tk_image = ImageTk.PhotoImage(img)
        
        # Display the image
        self.canvas.create_image(img_x, img_y, anchor="nw", image=self.tk_image)
        
        # Draw the square crop area again on top
        self.canvas.create_rectangle(
            self.crop_x1, self.crop_y1,
            self.crop_x2, self.crop_y2,
            outline="red", width=2, dash=(5,5))
    
    def rotate_image(self, angle):
        """Rotate the image by specified angle (degrees)"""
        self.rotation_angle += angle
        # Reset offset when rotating to avoid confusion
        self.image_offset = [0, 0]
        self.display_image()
    
    def on_pan_start(self, event):
        """Handle panning start"""
        if not self.current_image:
            return
            
        self.pan_start = (event.x, event.y)
    
    def on_pan_drag(self, event):
        """Handle panning drag"""
        if not self.current_image or not self.pan_start:
            return
            
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]
        
        self.image_offset[0] += dx
        self.image_offset[1] += dy
        
        self.pan_start = (event.x, event.y)
        self.display_image()
    
    def on_pan_end(self, event):
        """Handle panning end"""
        self.pan_start = None
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel zooming"""
        if not self.current_image:
            return
            
        # Determine zoom direction
        if event.delta > 0:
            self.adjust_zoom(1.1)
        else:
            self.adjust_zoom(0.9)
    
    def adjust_zoom(self, factor):
        """Adjust the zoom level"""
        if not self.current_image:
            return
            
        new_zoom = self.zoom_factor * factor
        
        # Apply zoom limits
        if new_zoom < self.min_zoom:
            new_zoom = self.min_zoom
        elif new_zoom > self.max_zoom:
            new_zoom = self.max_zoom
            
        if new_zoom != self.zoom_factor:
            self.zoom_factor = new_zoom
            self.zoom_label.configure(text=f"Zoom: {int(self.zoom_factor * 100)}%")
            self.display_image()
    
    def apply_crop(self):
        """Apply the crop to the current image"""
        if not self.current_image:
            return False
            
        try:
            # Create a working copy of the image
            img = self.current_image.copy()
            
            # Apply rotation if needed
            if self.rotation_angle != 0:
                img = img.rotate(self.rotation_angle, expand=True)
            
            # Get image and canvas dimensions
            img_width, img_height = img.size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Calculate the actual displayed image size (after zoom)
            displayed_width = int(img_width * self.zoom_factor)
            displayed_height = int(img_height * self.zoom_factor)
            
            # Calculate the visible area of the image within the square
            # First, find the image position relative to the canvas
            img_x = (canvas_width - displayed_width) / 2 + self.image_offset[0]
            img_y = (canvas_height - displayed_height) / 2 + self.image_offset[1]
            
            # Calculate what part of the image is visible in the square
            square_x1 = max(self.crop_x1 - img_x, 0)
            square_y1 = max(self.crop_y1 - img_y, 0)
            square_x2 = min(self.crop_x2 - img_x, displayed_width)
            square_y2 = min(self.crop_y2 - img_y, displayed_height)
            
            # Convert these coordinates back to original image coordinates
            orig_x1 = square_x1 / self.zoom_factor
            orig_y1 = square_y1 / self.zoom_factor
            orig_x2 = square_x2 / self.zoom_factor
            orig_y2 = square_y2 / self.zoom_factor
            
            # Crop the image
            cropped_img = img.crop((orig_x1, orig_y1, orig_x2, orig_y2))
            
            # Resize to match the square size (for consistent output)
            output_size = int(self.crop_size)
            cropped_img = cropped_img.resize((output_size, output_size), Image.Resampling.LANCZOS)
            
            # Update the current image
            self.current_image = cropped_img
            self.rotation_angle = 0  # Reset rotation since we've applied it
            self.image_offset = [0, 0]
            self.zoom_factor = 1.0
            self.zoom_label.configure(text="Zoom: 100%")
            
            self.display_image()
            self.image_status.configure(text="✅ Image cropped")
            
            return True
            
        except Exception as e:
            self.image_status.configure(text=f"❌ Crop failed: {str(e)}")
            return False
    
    def reset_edits(self):
        """Reset all edits to original image"""
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.rotation_angle = 0
            self.image_offset = [0, 0]
            self.zoom_factor = 1.0
            self.zoom_label.configure(text="Zoom: 100%")
            self.display_image()
            self.image_status.configure(text="🔄 All edits reset to original image")
    
    def enable_controls(self):
        """Enable all editing controls"""
        self.rotate_left_btn.configure(state="normal")
        self.rotate_right_btn.configure(state="normal")
        self.reset_btn.configure(state="normal")
        self.zoom_in_btn.configure(state="normal")
        self.zoom_out_btn.configure(state="normal")
    
    def disable_controls(self):
        """Disable all editing controls"""
        self.rotate_left_btn.configure(state="disabled")
        self.rotate_right_btn.configure(state="disabled")
        self.reset_btn.configure(state="disabled")
        self.zoom_in_btn.configure(state="disabled")
        self.zoom_out_btn.configure(state="disabled")
    
    def save_image(self):
        """Save the edited image to temp directory"""
        if not self.current_image:
            return None
            
        # Apply the crop before saving
        if not self.apply_crop():
            return None
            
        try:
            # Create final image (rotation is already applied in apply_crop)
            final_image = self.current_image.copy()
            
            # Ensure temp directory exists
            os.makedirs(self.temp_dir, exist_ok=True)
            
            # Generate unique filename
            ext = ".jpg"  # Save as JPEG by default
            unique_name = f"{uuid.uuid4().hex[:8]}{ext}"
            final_path = os.path.join(self.temp_dir, unique_name)
            
            # Save the final image
            final_image.save(final_path, quality=95)
            self.image_path = final_path
            self.image_status.configure(text="✅ Image saved and ready to use")
            return final_path
            
        except Exception as e:
            self.image_status.configure(text=f"❌ Error saving image: {str(e)}")
            return None
    
    def get_image_path(self):
        """Return the path of the uploaded and saved image"""
        return self.save_image()  # Save when getting path to ensure latest edits
    
    def reset(self):
        """Reset the uploader to initial state"""
        self.image_status.configure(text="📂 No image selected.")
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.rotation_angle = 0
        self.image_offset = [0, 0]
        self.zoom_factor = 1.0
        self.zoom_label.configure(text="Zoom: 100%")
        self.canvas.delete("all")
        self.disable_controls()