import cv2
from PIL import Image
import threading

class VideoInput:
    def __init__(self, camera_index=0):
        """
        A class to read frames from a video camera source using the PIL library and constantly update the frames.
        :param camera_index: int, index of the camera to read from.
        """
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(self.camera_index)
        self.frame = None
        self.is_running = False
        self.is_recording = False
        self.out = None
        self.image_name = 0

    def start(self):
        """
        Start the video capture in a separate thread.
        """
        self.is_running = True
        threading.Thread(target=self.update_frame, daemon=True).start()

    def update_frame(self):
        """
        Continuously read frames from the camera and update the frame attribute, rotating the image by 180 degrees.
        """
        while self.is_running:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)  # Rotate the image by 180 degrees
                self.frame = Image.fromarray(rotated_frame)
                
                if self.is_recording and self.out:
                    # Write the frame to the video file
                    self.out.write(cv2.cvtColor(rotated_frame, cv2.COLOR_RGB2BGR))
            else:
                raise RuntimeError("Failed to read frame from camera")

        self.camera.release()
        cv2.destroyAllWindows()

    def stop(self):
        """
        Stop the video capture.
        """
        self.is_running = False

    def start_recording(self, filename="files/output.mp4"):
        """
        Start recording the video to a file.
        """
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        frame_width = int(self.camera.get(3))
        frame_height = int(self.camera.get(4))
        print(frame_width, frame_height)
        self.out = cv2.VideoWriter(filename, fourcc, 30.0, (frame_width, frame_height))
        self.is_recording = True

    def stop_recording(self):
        """
        Stop recording and save the video file.
        """
        self.is_recording = False
        if self.out:
            self.out.release()
            self.out = None

    def capture_image(self,):
        """
        Capture the current frame as an image and save it to a file.
        """
        if self.frame:
            self.frame.save("files/images/capture_"+str(self.image_name)+".png")
            self.image_name +=1