import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

def apply_median_filter(image, kernel_size):
    padded_image = np.pad(image, kernel_size // 2, mode='constant', constant_values=0)
    filtered_image = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighborhood = padded_image[i:i + kernel_size, j:j + kernel_size]
            median_value = np.median(neighborhood.flatten())
            filtered_image[i, j] = median_value
    return filtered_image

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if file_path:
        global image, img_display
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        img_display = ImageTk.PhotoImage(Image.fromarray(image))
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)

def apply_filter():
    if image is None:
        messagebox.showerror("Error", "No image loaded!")
        return
    kernel_size = int(kernel_size_entry.get())
    filtered_image = apply_median_filter(image, kernel_size)
    cv2.imwrite("blurred_image.jpg", filtered_image)
    filtered_display = ImageTk.PhotoImage(Image.fromarray(filtered_image))
    canvas.create_image(0, 0, anchor=tk.NW, image=filtered_display)
    messagebox.showinfo("Success", "Filtered image saved as 'blurred_image.jpg'")

root = tk.Tk()
root.title("Order Statistics Filter")

image = None

frame = tk.Frame(root)
frame.pack()

open_button = tk.Button(frame, text="Open Image", command=open_image)
open_button.grid(row=0, column=0, padx=5, pady=5)

tk.Label(frame, text="Kernel Size:").grid(row=0, column=1, padx=5, pady=5)
kernel_size_entry = tk.Entry(frame)
kernel_size_entry.grid(row=0, column=2, padx=5, pady=5)
kernel_size_entry.insert(0, "3")

apply_button = tk.Button(frame, text="Apply Filter", command=apply_filter)
apply_button.grid(row=0, column=3, padx=5, pady=5)

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

root.mainloop()