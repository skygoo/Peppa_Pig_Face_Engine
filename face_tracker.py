from enum import Enum
import numpy as np
import cv2


class Marker(Enum):
    JAW = 0
    LEFTOUTERBROW = 1
    LEFTINNERBROW = 2
    RIGHTINNERBROW = 3
    RIGHTOUTERBROW = 4
    LEFTCHEEK = 5
    RIGHTCHEEK = 6
    LEFTNOSE = 7
    NOSE = 8
    RIGHTNOSE = 9
    UPPERLIP = 10
    LEFTMOUTH = 11
    RIGHTMOUTH = 12
    LOWERLIP = 13
    MARKER_COUNT = 14


class TrackingData:
    def __init__(self):
        self.markers = list()
        for i in range(Marker.MARKER_COUNT.value):
            self.markers.append(np.array([0, 0]).astype('float32'))
        self.timeStep = -1


class FaceTracker:
    def __init__(self):
        self.H = 0.0
        self.S = 0.0
        self.V = 0.0
        self.thresholdH = 0.0
        self.thresholdS = 0.0
        self.thresholdV = 0.0
        self.face_cascade = cv2.CascadeClassifier()
        self.eyes_cascade = cv2.CascadeClassifier()
        self.saved_keypoints = list()
        self.face_rest_data = TrackingData()
        self.face_prev_data = TrackingData()
        self.face_rest_captured = False
        self.landmarks = None
        self.facemark = cv2.face.createFacemarkLBF()
        self.hasFoundFace = False
        self.face_rest_captured = False

        face_cascade_name = 'haarcascade_frontalface_alt2.xml'
        self.face_cascade.load(face_cascade_name)
        self.facemark.loadModel('lbfmodel.yaml')

    def detectAndShow(self, frame):
        frame_gray = frame.copy()
        cv2.rectangle()
        self.face_cascade.detectMultiScale(frame_gray, )
