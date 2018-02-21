import cv2
import numpy as np
from scipy import ndimage

class Canny:

    def __init__(self, frame, upperThresh, lowerThresh):
        self.frame = frame
        self.size = 3
        self.upperThresh = upperThresh
        self.lowerThresh = lowerThresh

    def process(self):
        self.frame = self.noise_reduction(self.frame)
        self.frame, direction = self.gradient_calc(self.frame)
        self.frame = self.suppress(self.frame, direction)
        self.frame = self.threshold(self.frame)
        self.frame = self.perform_edge_detect(self.frame)

        return self.frame

    def angle(self, angle):
        angle = np.rad2deg(angle) % 180
        if (0 <= angle < 22.5) or (157.5 <= angle < 180):
            angle = 0
        elif 22.5 <= angle < 67.5:
            angle = 45
        elif 67.5 <= angle < 112.5:
            angle = 90
        elif 112.5 <= angle < 157.5:
            angle = 135
        return angle

    def noise_reduction(self, frame):
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        return frame

    def gradient_calc(self, frame):
        k_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.int32)
        k_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.int32)

        Ix = ndimage.convolve(frame, k_x)
        Iy = ndimage.convolve(frame, k_y)

        frame = np.hypot(Ix, Iy)
        direction = np.arctan2(Iy, Ix)

        return frame, direction

    def suppress(self, frame, direction):
        width, height = frame.shape
        z = np.zeros((width, height), dtype=np.int32)

        for x in range(width):
            for y in range(height):
                val = self.angle(direction[x, y])

                try:
                    if val == 0:
                        if (frame[x, y] >= frame[x, y - 1]) and (frame[x, y] >= frame[x, y + 1]):
                            z[x, y] = frame[x, y]
                    elif val == 90:
                        if (frame[x, y] >= frame[x - 1, y]) and (frame[x, y] >= frame[x + 1, y]):
                            z[x, y] = frame[x, y]
                    elif val == 135:
                        if (frame[x, y] >= frame[x - 1, y - 1]) and (frame[x, y] >= frame[x + 1, y + 1]):
                            z[x, y] = frame[x, y]
                    elif val == 45:
                        if (frame[x, y] >= frame[x - 1, x + 1]) and (frame[x, y] >= frame[x + 1, x - 1]):
                            z[x, y] = frame[x, y]
                except IndexError as e:
                    pass

        return z

    def threshold(self, frame):
        cf = {
            'w': np.int32(50),
            's': np.int32(255)
        }

        str_x, str_y = np.where(frame > self.upperThresh)
        wk_x, wk_y = np.where((frame >= self.lowerThresh) & (frame <= self.upperThresh))
        zero_x, zero_y = np.where(frame < self.lowerThresh)

        frame[str_x, str_y] = cf.get('s')
        frame[wk_x, wk_y] = cf.get('w')
        frame[zero_x, zero_y] = np.int32(0)

        return frame

    def perform_edge_detect(self, frame):
        width, height = frame.shape

        for x in range(width):
            for y in range(height):
                print(frame[x, y])
                if frame[x, y] == 50:
                    try:
                        if ((frame[x + 1, y] == 255) or (frame[x - 1, y] == 255)
                            or (frame[x, y + 1] == 255) or (frame[x, y - 1]) == 255
                            or (frame[x + 1, y + 1] == 255) or (frame[x - 1, y - 1] == 255)):
                            frame[x, y] = 255
                        else:
                            frame[x, y] = 0
                    except IndexError as e:
                        pass

        return frame
