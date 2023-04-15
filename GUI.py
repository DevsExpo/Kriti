import tkinter as tk
from PIL import Image, ImageTk


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
        
        save_face_button = tk.Button(master, text="Save New Face", width=20, bg="#2ecc71", fg="white", font=("Helvetica", 12))
        save_face_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        ocr_button = tk.Button(master, text="OCR", width=20, bg="#f1c40f", fg="white", font=("Helvetica", 12))
        ocr_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        credits_button = tk.Button(master, text="Credits & More", width=20, bg="#e74c3c", fg="white", font=("Helvetica", 12))
        credits_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Set the active background color for all buttons
        for button in (enter_detector_button, save_face_button, ocr_button, credits_button):
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


if __name__ == '__main__':
    root = tk.Tk()
    gui = ProjectKritiGUI(root)
    root.mainloop()
