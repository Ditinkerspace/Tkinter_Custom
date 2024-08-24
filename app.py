import threading
import customtkinter
import cv2
from PIL import Image, ImageTk
from videoInput import VideoInput


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("420x380")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.start_camera = VideoInput()
        self.start_camera.start()

        if self.start_camera.camera.isOpened():
            # Initialize self.my_image with an empty PIL Image
            empty_image = Image.new('RGB', (352, 640), (0, 0, 0))
            self.my_image = customtkinter.CTkImage(light_image=empty_image, size=(352, 250))

            self.image_label = customtkinter.CTkLabel(self, image=self.my_image, text="")
            self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

            self.update_image()  # Start updating the image after initialization

            # Buttons for start, stop, and capture
            self.start_button = customtkinter.CTkButton(self, text="Start", command=self.start_recording)
            self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

            self.stop_button = customtkinter.CTkButton(self, text="Stop", command=self.stop_recording)
            self.stop_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

            self.capture_button = customtkinter.CTkButton(self, text="Capture", command=self.capture_image)
            self.capture_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
            
            self.schedule_button = customtkinter.CTkButton(self, text="Schedule", command=self.schedule_record)
            self.schedule_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        else:
            print("Failed to open the camera.")

    def update_image(self):
        """
        Update the image label with the current frame.
        """
        if self.start_camera.frame:
            self.my_image.configure(light_image=self.start_camera.frame)  # Update the image

        self.after(10, self.update_image)  # Update every 10 milliseconds

    def start_recording(self):
        """
        Start video recording.
        """
        self.start_camera.start_recording()

    def stop_recording(self):
        """
        Stop and save the video recording.
        """
        self.start_camera.stop_recording()

    def capture_image(self):
        """
        Capture an image from the video feed.
        """
        self.start_camera.capture_image()
    def schedule_record(self):
        """
        Capture an image from the video feed.
        """
        self.start_camera.schedule_record()


app = App()
app.mainloop()
