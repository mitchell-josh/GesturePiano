import logging

import cv2 as cv

import processing


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
        return frame

    """
        Returns processed image frame
    """
    def get_next_frame(self):
        frame = self.get_next_frame_raw()

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.GaussianBlur(frame, (15, 15), 0)
        _, thresh = cv.threshold(frame, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        thresh = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)

        frame = cv.flip(thresh, 1)
        cv.rectangle(frame, (340, 180), (639, 479), (105,187,1), 1)

        return frame

        # Filtering
        # gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (15, 15), 0)
        # _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    def is_open(self):
        return self.cap.isOpened()

    def destroy(self):
        self.cap.release()
