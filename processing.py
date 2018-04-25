import cv2 as cv
import numpy as np
import canny
import itertools as IT

from scipy import ndimage


class ImageProcessor:
    def __init__(self, frame):
        self.frame = frame


    """
    Implements OpenCV simple threshold methods
    """
    def simple_binary(self, val):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        ret,thresh = cv.threshold(frame, val, 255, cv.THRESH_BINARY)
        return thresh

    def simple_binary_inv(self, val):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(frame, val, 255, cv.THRESH_BINARY_INV)
        return thresh

    def simple_trunc(self, val):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(frame, val, 255, cv.THRESH_TRUNC)
        return thresh

    def simple_tozero(self, val):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(frame, val, 255, cv.THRESH_TOZERO)
        return thresh

    def simple_tozero_inv(self, val):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(frame, val, 255, cv.THRESH_TOZERO_INV)
        return thresh

    """
    Implements OpenCV adaptive threshold methods
    """
    def adaptive_mean(self):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        thresh = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                      cv.THRESH_BINARY, 11, 2)
        return thresh

    def adaptive_gaussian(self):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        thresh = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv.THRESH_BINARY, 11, 2)
        return thresh

    """
    Implements custom thresholding
    """
    def otsu(self):
        # TODO: Implement 2D-OTSU for optimisation
        # get raw image function
        np_img_data_raw = cv.GaussianBlur(self.frame, (5, 5), 0)
        cv_histogram = cv.calcHist(np_img_data_raw, [0], None, [256], [0, 256])
        cv_histogram_n = cv_histogram.ravel() / cv_histogram.max()
        Q = cv_histogram_n.cumsum()

        min_func = np.inf
        thresh = -1
        bins = np.arange(256)

        # optimise for max in range
        for i in range(0, 256):
            w1 = np.split(cv_histogram_n, [i])

            p1, p2 = np.hsplit(cv_histogram_n, [i])
            s1, s2 = Q[i], Q[255] - Q[i]
            w1, w2 = np.hsplit(bins, [i])

            m1, m2 = np.dot(p1, w1), np.dot(p2, w2)
            v1, v2 = np.dot(((w1 - m1) ** 2), p1) / s1, np.dot(((w2 - m2) ** 2), p2) / s2

            within_class_variance = v1 * s1 + v2 * s2
            if within_class_variance < min_func:
                min_func = within_class_variance;
                thresh = i

        # Returns the binary frame
        return self.simple_binary(thresh)


    """
    Performs edge detection on processed image
    """
    def sobel_edge(self):

        Ix = cv.Sobel(self.frame,cv.CV_64F,1,0,ksize=5)
        Iy = cv.Sobel(self.frame,cv.CV_64F,0,1,ksize=5)

        frame = np.hypot(Ix, Iy)
        frame *= 255.0 / np.max(self.frame)

        return self.frame

    """
    Canny edge detection on image
    """
    def canny(self):
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        result = canny.Canny(frame, 200, 100)
        return result.process()


    """
    Note: Do not call this method unless input is a binary image
    """
    def simple_edge(self):
        frame = self.frame
        height, width = frame.shape
        new_img = np.zeros((height, width), np.uint8)

        for x in range(width):
            for y in range(height):
                try:
                    if (frame[x + 1, y] - frame[x - 1, y] == 255) or (frame[x + 1, y] - frame[x - 1, y] == 255) or (
                            frame[x, y + 1] - frame[x, y - 1] == 255) or (frame[x, y + 1] - frame[x, y - 1] == -255):
                        new_img[x, y] = 255
                    else:
                        new_img[x, y] = 0
                except IndexError as e:
                    pass

        return new_img





