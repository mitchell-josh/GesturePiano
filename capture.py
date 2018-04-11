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

        image_processor = processing.ImageProcessor(frame)
        frame = image_processor.simple_binary(157)

        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)

        return frame

    def is_open(self):
        return self.cap.isOpened()

    def destroy(self):
        self.cap.release()
