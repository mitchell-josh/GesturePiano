import logging

import cv2 as cv

import processing


class FrameProcessor:
    def __init__(self, frame):
        self.frame = frame
        self.image_processor = processing.ImageProcessor(frame)

    def process(self):
        if self.frame is not None:
            # do image process stuffs here

            self.frame = cv.flip(self.frame, 1)
            self.frame = cv.cvtColor(self.frame, cv.COLOR_GRAY2BGR)


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
        Returns an Image Frame processed by Frame Processor
    """
    def get_next_frame(self):
        frame = self.get_next_frame_raw()

        frame_processor = FrameProcessor(frame)
        frame_processor.process()

        frame = frame_processor.frame
        return frame

    def is_open(self):
        return self.cap.isOpened()

    def destroy(self):
        self.cap.release()
