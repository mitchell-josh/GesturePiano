import cv2 as cv
import numpy as np
import tensorflow as tf
import logging

class AI:
    def __init__(self):
        with tf.gfile.FastGFile("res/retrained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')
        with tf.Session() as self.sess:
            self.softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')

        logging.debug("AI Initialized")

    def detect_gesture(self, frame):
        # Region of Interest
        roi = frame[180:479, 340:639]

        # Transform OpenCV VideoCapture to TensorFlow input
        resize_frame = cv.resize(roi, (299, 299), interpolation=cv.INTER_CUBIC)
        tf_frame = np.asarray(resize_frame)
        tf_frame = cv.normalize(tf_frame.astype('float'), None, -0.5, .5, cv.NORM_MINMAX)
        tf_final = np.expand_dims(tf_frame, axis=0)

        # Predictions
        predictions = self.sess.run(self.softmax_tensor, {'Mul:0': tf_final})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        # Assign predictions
        for node_id in top_k:
            score_pinky = predictions[0][0]
            score_middle = predictions[0][1]
            score_ring = predictions[0][2]
            score_thumb = predictions[0][3]
            score_index = predictions[0][4]

        # Based on score, do something
        if score_index > 0.55:
            return "D-1"
        elif score_thumb > 0.98:
            return "C-1"
        elif score_pinky > 0.92:
            return "G-1"
        elif score_middle > 0.55:
            return "E-1"
        elif score_ring > 0.65:
            return "F-1"