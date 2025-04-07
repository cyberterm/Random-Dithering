import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from dithering import sequencial_dithering
import numpy as np

class DitheringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sequential Dithering App")

        # Variables for sliders
        self.size_multiplier = tk.IntVar(value=1)
        self.samples = tk.IntVar(value=1)
        self.stretch_factor = tk.DoubleVar(value=1.0)

        # Image containers
        self.original_image = None
        self.dithered_image = None
        self.original_filepath = None

        # Layout setup
        self.setup_widgets()

    def setup_widgets(self):
        # Frames for images
        image_frame = tk.Frame(self.root)
        image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Original image display
        self.original_canvas = tk.Label(image_frame, text="Click to load image", bg="gray", width=50, height=25)
        self.original_canvas.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='both')
        self.original_canvas.bind("<Button-1>", self.load_image)

        # Dithered image display
        self.dithered_canvas = tk.Label(image_frame, text="Dithered image will appear here", bg="gray", width=50, height=25)
        self.dithered_canvas.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill='both')

        # Sliders frame
        sliders_frame = tk.Frame(self.root)
        sliders_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Size Multiplier slider
        tk.Label(sliders_frame, text="Size Multiplier").grid(row=0, column=0, sticky="w")
        size_multiplier_scale = tk.Scale(sliders_frame, from_=1, to=8, orient=tk.HORIZONTAL, variable=self.size_multiplier)
        size_multiplier_scale.grid(row=0, column=1, sticky="ew")
        size_multiplier_scale.bind("<ButtonRelease-1>", self.process_image)

        # Samples slider
        tk.Label(sliders_frame, text="Samples").grid(row=1, column=0, sticky="w")
        samples_scale = tk.Scale(sliders_frame, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.samples)
        samples_scale.grid(row=1, column=1, sticky="ew")
        samples_scale.bind("<ButtonRelease-1>", self.process_image)

        # Stretch Factor slider
        tk.Label(sliders_frame, text="Stretch Factor").grid(row=2, column=0, sticky="w")
        stretch_factir_scale = ttk.Scale(sliders_frame, from_=0.01, to=2.0, variable=self.stretch_factor, orient=tk.HORIZONTAL)
        stretch_factir_scale.grid(row=2, column=1, sticky="ew")
        stretch_factir_scale.bind("<ButtonRelease-1>", self.process_image)

        # Process button
        process_button = tk.Button(self.root, text="Save", command=self.save_image)
        process_button.pack(side=tk.BOTTOM, pady=10)

    def load_image(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.original_canvas)
            self.original_filepath = file_path
        self.process_image()

    def display_image(self, image, canvas):
        # Resize image to fit canvas
        max_size = (800, 800)
        thumbnail = image.copy()
        thumbnail.thumbnail(max_size, Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(thumbnail)
        canvas.config(image=photo, width=photo.width(), height=photo.height())
        canvas.image = photo

    def process_image(self, event=None):
        if self.original_image is None:
            tk.messagebox.showerror("Error", "No image loaded!")
            return

        # Convert image to numpy array
        image_array = np.array(self.original_image.convert("L"))

        # Apply dithering
        dithered_array = sequencial_dithering(
            image_array,
            size_multiplier=self.size_multiplier.get(),
            samples=self.samples.get(),
            stretch_factor=self.stretch_factor.get()
        )

        # Convert back to image
        dithered_image = Image.fromarray(dithered_array)
        self.dithered_image = dithered_image
        self.display_image(dithered_image, self.dithered_canvas)

    def save_image(self):
        dithered_filepath = self.original_filepath.split('.')[0] + '_dithered.png'
        self.dithered_image.save(dithered_filepath)

if __name__ == "__main__":
    root = tk.Tk()
    app = DitheringApp(root)
    root.mainloop()
