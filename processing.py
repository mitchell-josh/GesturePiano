import cv2 as cv
import numpy as np
import canny

from scipy import ndimage


class ImageProcessor:
    def __init__(self, frame):
        self.frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    """
    Implements OpenCV simple threshold methods
    """
    def simple_binary(self, val):
        ret,thresh = cv.threshold(self.frame, val, 255, cv.THRESH_BINARY)
        return thresh

    def simple_binary_inv(self, val):
        ret, thresh = cv.threshold(self.frame, val, 255, cv.THRESH_BINARY_INV)
        return thresh

    def simple_trunc(self, val):
        ret, thresh = cv.threshold(self.frame, val, 255, cv.THRESH_TRUNC)
        return thresh

    def simple_tozero(self, val):
        ret, thresh = cv.threshold(self.frame, val, 255, cv.THRESH_TOZERO)
        return thresh

    def simple_tozero_inv(self, val):
        ret, thresh = cv.threshold(self.frame, val, 255, cv.THRESH_TOZERO_INV)
        return thresh

    """
    Implements OpenCV adaptive threshold methods
    """
    def adaptive_mean(self):
        thresh = cv.adaptiveThreshold(self.frame, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                      cv.THRESH_BINARY, 11, 2)
        return thresh

    def adaptive_gaussian(self):
        thresh = cv.adaptiveThreshold(self.frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
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

        # Returns the optimum threshold value
        return thresh


    """
    Performs edge detection on processed image
    """
    def sobel_edge(self):
        k_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.int32)
        k_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.int32)

        Ix = ndimage.convolve(self.frame, k_x)
        Iy = ndimage.convolve(self.frame, k_y)

        frame = np.hypot(Ix, Iy)

        return frame

    def canny(self):
        result = canny.Canny(self.frame, 200, 100)
        return result.process()


    """
    Note: Do not call this method unless input is a binary image
    """
    def simple_edge(self):
        # TODO: Refactor to kernels for optimisation
        height, width = self.frame.shape
        new_img = np.zeros((height, width, 1), np.float64)

        for x in range(1, (width-1)):
            for y in range(1, (height-1)):

                if ((self.frame[x + 1, y] - self.frame[x - 1, y] == 255)
                    or (self.frame[x + 1, y] - self.frame[x - 1, y] == 255)):
                    new_img[x, y] = 255
                elif (self.frame[x, y + 1] - self.frame[x, y - 1]) == 255:
                    new_img[x, y] = 255
                elif (self.frame[x, y + 1] - self.frame[x, y - 1]) == -255:
                    new_img[x, y] = 255
                else:
                    new_img[x, y] = 0

        return new_img




