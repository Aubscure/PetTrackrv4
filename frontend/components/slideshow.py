import customtkinter as ctk
import os
from PIL import Image, ImageTk
import threading
import time

class Slideshow(ctk.CTkFrame):
    def __init__(self, parent, image_folder="frontend/assets/slideshow1", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.image_folder = image_folder
        self.images = []
        self.current_index = 0
        self.is_running = False
        
        # Create label for displaying images
        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(expand=True, fill="both", padx=0, pady=0)
        
        # Bind resize event to update image size
        self.bind("<Configure>", self.on_resize)
        
        # Load images
        self.load_images()
        
        # Start slideshow
        self.start_slideshow()
    
    def on_resize(self, event):
        """Handle resize events to update image size"""
        if hasattr(self, 'original_images') and self.original_images:
            self.resize_current_image()
    
    def load_images(self):
        """Load all images from the slideshow folder"""
        self.original_images = []  # Store original images for resizing
        
        if os.path.exists(self.image_folder):
            image_files = [f for f in os.listdir(self.image_folder) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            image_files.sort()  # Sort to ensure consistent order
            
            for image_file in image_files:
                image_path = os.path.join(self.image_folder, image_file)
                try:
                    # Load original image
                    image = Image.open(image_path)
                    self.original_images.append(image)
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
        
        # If no images loaded, create a placeholder
        if not self.original_images:
            self.create_placeholder()
        else:
            # Resize the first image to fit the current frame
            self.resize_current_image()
    
    def resize_current_image(self):
        """Resize the current image to fill the frame"""
        if not self.original_images:
            return
            
        # Get current frame size
        frame_width = self.winfo_width()
        frame_height = self.winfo_height()
        
        if frame_width <= 1 or frame_height <= 1:
            return  # Frame not yet properly sized
        
        # Get current original image
        original_image = self.original_images[self.current_index]
        
        # Calculate aspect ratios
        img_width, img_height = original_image.size
        frame_ratio = frame_width / frame_height
        img_ratio = img_width / img_height
        
        # Resize image to fill frame while maintaining aspect ratio
        if frame_ratio > img_ratio:
            # Frame is wider than image - fit to height and crop width
            new_height = frame_height
            new_width = int(frame_height * img_ratio)
            resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop from center to fit frame width
            left = (new_width - frame_width) // 2
            right = left + frame_width
            cropped_image = resized_image.crop((left, 0, right, frame_height))
        else:
            # Frame is taller than image - fit to width and crop height
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
            resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop from center to fit frame height
            top = (new_height - frame_height) // 2
            bottom = top + frame_height
            cropped_image = resized_image.crop((0, top, frame_width, bottom))
        
        # Convert to PhotoImage and update display
        photo = ImageTk.PhotoImage(cropped_image)
        self.images = [photo]  # Keep only current image in memory
        self.image_label.configure(image=photo)
    
    def create_placeholder(self):
        """Create a placeholder when no images are available"""
        placeholder = ctk.CTkLabel(
            self, 
            text="🐾 PetTrackr\n\nNo slideshow images found",
            font=("Arial", 24, "bold"),
            text_color="#666666"
        )
        placeholder.pack(expand=True, fill="both", padx=20, pady=20)
    
    def start_slideshow(self):
        """Start the slideshow thread"""
        if self.original_images:
            self.is_running = True
            self.slideshow_thread = threading.Thread(target=self.slideshow_loop, daemon=True)
            self.slideshow_thread.start()
    
    def slideshow_loop(self):
        """Slideshow loop that runs in a separate thread"""
        while self.is_running and self.original_images:
            try:
                # Update image on main thread
                self.after(0, self.update_image)
                time.sleep(3)  # Change image every 3 seconds
                self.current_index = (self.current_index + 1) % len(self.original_images)
            except Exception as e:
                print(f"Error in slideshow: {e}")
                break
    
    def update_image(self):
        """Update the displayed image"""
        if self.original_images:
            self.resize_current_image()
    
    def stop_slideshow(self):
        """Stop the slideshow"""
        self.is_running = False 