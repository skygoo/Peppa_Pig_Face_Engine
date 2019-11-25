from enum import Enum
import numpy as np


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


# class FaceTracker:
#     def __init__(self):
#         self.H = 0.0
#         self.S = 0.0
#         self.V = 0.0
#         self.thresholdH
#
#     def a(self):
