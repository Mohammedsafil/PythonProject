import cv2
import tkinter as tk
from tkinter import filedialog, Label
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time


def convert_to_sketch(image_path, callback):
    image = cv2.imread(image_path)
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(grey_img)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
    time.sleep(3)
    callback(sketch)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        status_label.config(text="⏳ Processing image, please wait...")
        loading_label.pack(pady=10)
        threading.Thread(target=convert_to_sketch, args=(file_path, on_sketch_ready)).start()

def on_sketch_ready(sketch):
    cv2.imwrite("sketch.png", sketch)
    display_image("sketch.png")
    status_label.config(text="🎉 Image processed successfully!")
    loading_label.pack_forget()

def display_image(image_path):
    window = tk.Toplevel(root)
    window.title("Pencil Sketch")
    window.geometry("400x400")

    img = Image.open(image_path)
    img = ImageTk.PhotoImage(img)

    panel = Label(window, image=img)
    panel.image = img
    panel.pack()

    show_completed_gesture(window)

def show_completed_gesture(window):
    completed_label = Label(window, text="🎉 Completed! 🎉", font=("Helvetica", 24, "bold"), fg='black', bg='#f0f0f0')
    completed_label.place_forget()

    def animate():
        completed_label.place(x=window.winfo_width() // 2, y=window.winfo_height() - 30, anchor='center')
        for i in range(0, 100, 2):
            alpha = i / 100.0
            completed_label.config(fg=f"#{int(255 * alpha):02x}{int(255 * alpha):02x}{int(255 * alpha):02x}")
            time.sleep(0.05)
        time.sleep(1)  # Hold the label for a second
        for i in range(100, 0, -2):
            alpha = i / 100.0
            completed_label.config(fg=f"#{int(255 * alpha):02x}{int(255 * alpha):02x}{int(255 * alpha):02x}")
            time.sleep(0.05)
        completed_label.place_forget()

    threading.Thread(target=animate).start()

root = tk.Tk()
root.title("Image to Pencil Sketch Converter")
root.geometry("400x300")

style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
style.configure('Green.TButton',
                background='#4CAF50',
                foreground='black',
                font=('Helvetica', 14, 'bold'),
                padding=10,
                borderwidth=2,
                relief='raised')
style.map('Green.TButton',
          background=[('pressed', '#45a049'), ('active', '#4CAF50')],
          relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

frame = ttk.Frame(root, padding="20 20 20 20", style='TFrame')
frame.pack(fill='both', expand=True)

greeting = ttk.Label(frame, text="Welcome! 😊", font=("Helvetica", 16, "bold"), style='TLabel')
greeting.pack(pady=10)

instructions = ttk.Label(frame, text="Click the button below to open an image file:", style='TLabel')
instructions.pack(pady=5)

open_button = ttk.Button(frame, text="Open Image", command=open_file, style='Green.TButton')
open_button.pack(pady=20)
open_button.bind("<ButtonPress-1>", lambda event: event.widget.state(['pressed']))

status_label = ttk.Label(root, text="", style='TLabel', foreground='red')
status_label.pack(pady=10)

loading_label = ttk.Label(root, text="⏳ Loading...", style='TLabel')

root.mainloop()
