import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os

import cv2
import pytesseract
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from detectors.utils import speak

class TextDetectorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Text Detector")

        # Create the camera label
        self.camera_label = tk.Label(master, bd=10)
        self.camera_label.pack(side=tk.LEFT)

        # Create a frame to hold the text label
        self.text_frame = tk.Frame(master, width=300, height=480, bg='white')
        self.text_frame.pack(side=tk.RIGHT)

        # Create the text label inside the frame
        self.text_label = tk.Text(self.text_frame, font=("Helvetica", 16), wrap='word')
        self.text_label.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        # Initialize the camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Start the update loop
        self.update()

    def update(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a threshold to the image
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Apply some morphological operations to the thresholded image
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=1)
        thresh = cv2.dilate(thresh, kernel, iterations=1)

        # Find the contours in the image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours on the frame
        cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

        # Get the text from the contours
        text = ""
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = thresh[y:y + h, x:x + w]
            text += pytesseract.image_to_string(roi, config="--psm 11").strip() + "\n"

        # Update the camera label with the new frame
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.camera_label.configure(image=self.photo)
        self.camera_label.image = self.photo

        # Update the text label with the detected text
        self.text_label.delete(1.0, tk.END)
        self.text_label.insert(tk.END, text)

        # Call the update method again after a short delay
        self.master.after(10, self.update)


#class OpenDetectorGUI:



class SaveFaceGUI:
    def __init__(self, master):
        self.master = master
        master.title("Save New Face")

        self.camera_label = tk.Label(master, bd=10)
        self.camera_label.pack(side=tk.RIGHT)

        # Initialize the camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Create the name prompt label and entry box
        self.name_label = tk.Label(master, text="Enter your name:", font=("Helvetica", 14))
        self.name_label.pack(side=tk.TOP, padx=10, pady=10)
        self.name_entry = tk.Entry(master, font=("Helvetica", 14))
        self.name_entry.pack(side=tk.TOP, padx=10, pady=10)

        # Create the save button
        self.save_button = tk.Button(master, text="Save", command=self.save_face, width=20, bg="#2ecc71", fg="white", font=("Helvetica", 12))
        self.save_button.pack(side=tk.TOP, padx=10, pady=10)

    def save_face(self):
        # Get the name entered by the user
        if not os.path.exists("./known_faces/"):
            os.makedirs("./known_faces/")
        # Save the image with the given name
        name = self.name_entry.get()
        if name == "":
            messagebox.showerror("Error", "Please enter a name.")
            return
        filename = os.path.join("./known_faces/", name + ".jpg")
        if os.path.exists(filename):
            return messagebox.showerror("Error", "A face with this name already exists.")
        # Show a pop-up message
        resp = messagebox.askokcancel("Cheese", "Smile for the camera! Click OK to click and image.")
        if resp:
            ret, frame = self.cap.read()
            if ret: cv2.imwrite(filename, frame)
            else: return messagebox.showerror("Error", "Could not save the image.")
        self.cap.release()
        cv2.destroyAllWindows()
        self.master.destroy()


class ProjectKritiGUI:
    def __init__(self, master):
        self.master = master
        master.title("Project Kriti")

        # Create the background and logo images
        self.bg_image = ImageTk.PhotoImage(Image.open("./Images/bg.jpg"))
        self.logo = tk.PhotoImage(file="./Images/logo.png")

        # Create the background label
        self.bg_label = tk.Label(master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create the logo label
        self.logo_label = tk.Label(master, image=self.logo)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, rowspan=6)

        # Create the project name label
        heading_label = tk.Label(master, text="Project Kriti", font=("Rage italic", 32, "bold"), fg="#e74c3c")
        heading_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Create the buttons
        enter_detector_button = tk.Button(master, text="Enter Detector", width=20, bg="#3498db", fg="white", font=("Helvetica", 12))
        enter_detector_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        save_face_button = tk.Button(master, text="Save New Face", command=self.open_save_face_window, width=20, bg="#2ecc71", fg="white", font=("Helvetica", 12))
        save_face_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        ocr_button = tk.Button(master, text="OCR", width=20, bg="#f1c40f", command=self.open_ocr_window, fg="white", font=("Helvetica", 12))
        ocr_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Set the active background color for all buttons
        for button in (enter_detector_button, save_face_button, ocr_button):
            button.config(activebackground="#34495e")

        # Create the footer label
        footer_label = tk.Label(master, text="A Project By WS And BS", font=("Helvetica", 16), bg="#2c3e50", fg="white", padx=10, pady=10)
        footer_label.grid(row=6, column=0, sticky="w")

        # Configure the grid
        master.columnconfigure(1, weight=1)
        master.rowconfigure(5, weight=1)

        # Resize and set the logo image to the logo label
        self.logo = self.logo.subsample(2)
        self.logo_label.config(image=self.logo)


    def open_save_face_window(self):
        speak("Opening save face window")
        # Create the save face window
        save_face_window = tk.Toplevel(self.master)
        SaveFaceGUI(save_face_window)


    def open_ocr_window(self):
        # Create the ocr window
        speak("Opening OCR window")
        ocr_window = tk.Toplevel(self.master)
        TextDetectorGUI(ocr_window)


if __name__ == '__main__':
    root = tk.Tk()
    gui = ProjectKritiGUI(root)
    root.mainloop()
