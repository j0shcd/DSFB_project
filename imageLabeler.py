import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import csv

class ImageLabeler:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Image Labeler")

        self.image_path = image_path
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Load image
        self.original_image = Image.open(image_path)
        self.image = self.original_image.copy()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.zoom_factor = 1.0

        self.add_navigation_buttons()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<MouseWheel>", self.on_mouse_wheel)

        self.root.mainloop()

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        label = simpledialog.askstring("Input", "Enter label for the selected area", parent=self.root)
        if label:
            x0, y0, x1, y1 = self.canvas.coords(self.rect)
            self.save_to_csv(label, (x0, y0, x1, y1))
            print(f"Coordinates: ({x0}, {y0}, {x1}, {y1}), Label: {label}")

    def on_mouse_wheel(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        factor = 1.1 if event.delta > 0 else 0.9
        self.zoom_image(x, y, factor)

    def zoom_image(self, x, y, factor):
        self.zoom_factor *= factor
        new_width = int(self.original_image.size[0] * self.zoom_factor)
        new_height = int(self.original_image.size[1] * self.zoom_factor)

        # Use Image.Resampling.LANCZOS for high-quality downscaling
        self.image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def add_navigation_buttons(self):
        # Create frame for navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(side="bottom", fill="x")

        # Add buttons
        up_button = tk.Button(nav_frame, text="Up", command=lambda: self.move_image(0, -20))
        up_button.pack(side="top")

        down_button = tk.Button(nav_frame, text="Down", command=lambda: self.move_image(0, 20))
        down_button.pack(side="bottom")

        left_button = tk.Button(nav_frame, text="Left", command=lambda: self.move_image(-20, 0))
        left_button.pack(side="left")

        right_button = tk.Button(nav_frame, text="Right", command=lambda: self.move_image(20, 0))
        right_button.pack(side="right")
    
    def move_image(self, x_delta, y_delta):
        # Move the canvas view
        self.canvas.xview_scroll(int(x_delta / 7), "units")
        self.canvas.yview_scroll(int(y_delta / 7), "units")

    def save_to_csv(self, label, coords):
        with open('labeled_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.image_path, label, coords])


# Directly load "test.png"
ImageLabeler('Josh/CMC_CCM_2018_01_30_23_39_33_5586076040C.png')