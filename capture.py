import logging
import cv2 as cv


class VideoStream:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        if not self.is_open():
            logging.error("Failed to open capture device")

    """
        Returns raw image directly from the camera without processing
    """
    def get_next_frame_raw(self):
        ret, frame = self.cap.read()
        return cv.flip(frame, 1)

    """
        Returns processed image frame
    """
    def get_next_frame(self):
        frame = self.get_next_frame_raw()

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.GaussianBlur(frame, (15, 15), 0)
        _, thresh = cv.threshold(frame, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        frame = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)

        cv.rectangle(frame, (340, 180), (639, 479), (105,187,1), 7)

        return frame

    def is_open(self):
        return self.cap.isOpened()

    def destroy(self):
        self.cap.release()
