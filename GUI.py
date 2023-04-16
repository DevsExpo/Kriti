from threading import Thread
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import pytesseract
from detectors.utils import group_words_to_sentences, speak, threads_list


class DetectorGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Detector")
        
        self.camera = cv2.VideoCapture(0)
        self.delay = 10
    
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        # create the camera label and text label
        self.camera_label = tk.Label(self.frame)
        self.camera_label.pack(side="left")
        self.text_label = tk.Label(self.frame, text="Hello World", font=("Helvetica", 20), width=20, height=5)
        self.text_label.pack(side="right", padx=10, pady=10)
        
        self.update()
        
        
    def update(self):
        ret, frame = self.camera.read()
        if ret:
            # convert the frame from OpenCV to PIL format
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            self.camera_label.config(image=image)
            self.camera_label.image = image
        
        self.text_label.config(text="Test" if self.text_label.cget("text") == "Nah" else "Nah")
        #self.window.after(self.delay, self.update)
        self.window.update()
        
    def start_camera(self):
        self.start_button.pack_forget()
        self.update()

class TextDetectorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Text Detector")
        self.camera_label = tk.Label(master, bd=10)
        self.camera_label.pack(side=tk.LEFT)
        self.text_frame = tk.Frame(master, width=300, height=480, bg='white')
        self.text_frame.pack(side=tk.RIGHT)
        self.text_label = tk.Text(self.text_frame, font=("Helvetica", 16), wrap='word')
        self.text_label.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stop = False
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.thread = Thread(target=self.read, args=(), daemon=True)
        self.thread.start()
        self.update()


    def on_close(self):
        self.stop = True
        self.thread.join()
        self.cap.release()
        self.master.destroy()

    def read(self):
        while not self.stop:
            self.ret, self.frame = self.cap.read()
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    def update(self):
        while (not self.stop):
            try: 
                data = pytesseract.image_to_data(self.thresh, output_type=pytesseract.Output.DICT, config="--psm 6", lang="eng")
                self.frame
            except AttributeError: continue
            words = []
            prev_ss = ""
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 55:
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    text = data['text'][i]
                    words.append((x, y, w, h, text))
            if words:
                sentences = group_words_to_sentences(words)
                ss = ""
                for sentence in sentences:
                    ss += sentence + "\n"
                if prev_ss != ss:
                    self.text_label.delete(1.0, tk.END)
                    self.text_label.insert(tk.END, ss)
                    speak(ss)
                prev_ss = ss
            else:
                self.text_label.delete(1.0, tk.END)
                self.text_label.insert(tk.END, "No text detected")
            frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.camera_label.configure(image=self.photo)
            self.camera_label.image = self.photo
            self.master.update()


class SaveFaceGUI:
    def __init__(self, master):
        self.master = master
        master.title("Save New Face")

        self.camera_label = tk.Label(master, bd=10)
        self.camera_label.pack(side=tk.RIGHT)
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
        if not os.path.exists("./known_faces/"):
            os.makedirs("./known_faces/")
        name = self.name_entry.get()
        if name == "":
            tk.messagebox.showerror("Error", "Please enter a name.")
            return
        filename = os.path.join("./known_faces/", name + ".jpg")
        if os.path.exists(filename):
            return tk.messagebox.showerror("Error", "A face with this name already exists.")
        # Show a pop-up message
        resp = tk.messagebox.askokcancel("Cheese", "Smile for the camera! Click OK to click and image.")
        if resp:
            ret, frame = self.cap.read()
            if ret: cv2.imwrite(filename, frame)
            else: return tk.messagebox.showerror("Error", "Could not save the image.")
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
        enter_detector_button = tk.Button(master, text="Enter Detector", width=20, bg="#3498db", fg="white", font=("Helvetica", 12), command=self.open_detector_window)
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

    def open_detector_window(self):
        speak("Opening Main Detector window")
        dec_window = tk.Toplevel(self.master)
        DetectorGUI(dec_window)


if __name__ == '__main__':
    root = tk.Tk()
    gui = ProjectKritiGUI(root)
    root.mainloop()
