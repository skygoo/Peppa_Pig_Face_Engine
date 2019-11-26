import cv2
import time
import numpy as np
import argparse
import time
from datetime import datetime
from threading import Timer
import math

from face_tracker import TrackingData
from lib.core.api.facer import FaceAna
from lib.core.headpose.pose import get_head_pose, line_pairs
from lib.core.track.socket import MayaSocket, Marker


class Test:
    def __init__(self):
        self.facer = FaceAna()
        self.ms = MayaSocket()

        self.frame = 0
        self.inc = 1
        self.saved_keypoints = list()
        self.face_rest_data = TrackingData()
        self.face_prev_data = TrackingData()
        self.face_rest_captured = False

    # 被周期性调度触发函数
    def printTime(self):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.frame)
        self.frame = 0
        t = Timer(self.inc, self.printTime, ())
        t.start()

    def video(self, video_path_or_cam):
        vide_capture = cv2.VideoCapture(video_path_or_cam)

        while 1:

            ret, image = vide_capture.read()

            self.frame += 1

            pattern = np.zeros_like(image)

            img_show = image.copy()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # str_time = time.time()

            boxes, landmarks_standardized, landmarks, states = self.facer.run(image)

            keypoints = []
            if len(landmarks) > 0:
                keypoints.append(landmarks[0][27])
                keypoints.append(landmarks[0][19])
                keypoints.append(landmarks[0][21])
                keypoints.append(landmarks[0][22])
                keypoints.append(landmarks[0][24])
                keypoints.append(landmarks[0][41])
                keypoints.append(landmarks[0][46])
                keypoints.append(landmarks[0][31])
                keypoints.append(landmarks[0][30])
                keypoints.append(landmarks[0][35])
                keypoints.append(landmarks[0][48])
                keypoints.append(landmarks[0][51])
                keypoints.append(landmarks[0][54])
                keypoints.append(landmarks[0][57])

                # if len(self.saved_keypoints) > 0:
                #     for i in range(len(keypoints)):
                #         keypoints[i][0] = keypoints[i][0] * 0.7 + self.saved_keypoints[i][0] * 0.3
                #         keypoints[i][1] = keypoints[i][1] * 0.7 + self.saved_keypoints[i][1] * 0.3
                # self.saved_keypoints = []
                # self.saved_keypoints.extend(keypoints)

                # print(time.time() - str_time)

                for landmarks_index in range(len(keypoints)):
                    x_y = keypoints[landmarks_index]
                    cv2.circle(img_show, (int(x_y[0]), int(x_y[1])), 3,
                               (0, 0, 225), -1)

                cv2.imshow("capture", img_show)

                keypoints = []
                keypoints.append(landmarks_standardized[0][27])
                keypoints.append(landmarks_standardized[0][19])
                keypoints.append(landmarks_standardized[0][21])
                keypoints.append(landmarks_standardized[0][22])
                keypoints.append(landmarks_standardized[0][24])
                keypoints.append(landmarks_standardized[0][41])
                keypoints.append(landmarks_standardized[0][46])
                keypoints.append(landmarks_standardized[0][31])
                keypoints.append(landmarks_standardized[0][30])
                keypoints.append(landmarks_standardized[0][35])
                keypoints.append(landmarks_standardized[0][48])
                keypoints.append(landmarks_standardized[0][51])
                keypoints.append(landmarks_standardized[0][54])
                keypoints.append(landmarks_standardized[0][57])
                face_data = TrackingData()
                for i in range(Marker.MARKER_COUNT.value - 4):
                    face_data.markers[i] = keypoints[i]
                # mouse
                face_data.markers[Marker.LEFTMOUTH.value] = keypoints[10]
                face_data.markers[Marker.UPPERLIP.value] = keypoints[11]
                face_data.markers[Marker.RIGHTMOUTH.value] = keypoints[12]
                face_data.markers[Marker.LOWERLIP.value] = keypoints[13]

                if not self.face_rest_captured:
                    cv2.imshow("first", img_show)
                    for i in range(Marker.MARKER_COUNT.value):
                        self.face_rest_data.markers[i] = face_data.markers[i] - face_data.markers[Marker.JAW.value]
                        self.face_prev_data.markers[i] = face_data.markers[i].copy()
                    self.face_rest_captured = True
                else:
                    for i in range(Marker.MARKER_COUNT.value):
                        if distance(self.face_prev_data.markers[i], face_data.markers[i]) > 100:
                            continue
                        self.face_prev_data.markers[i] = face_data.markers[i].copy()

                    rest_dist = distance(self.face_rest_data.markers[Marker.JAW.value], self.face_rest_data.markers[Marker.NOSE.value])
                    fn_v_r = (self.face_rest_data.markers[Marker.JAW.value] - self.face_rest_data.markers[Marker.NOSE.value]) / rest_dist

                    curr_dist = distance(face_data.markers[Marker.JAW.value], face_data.markers[Marker.NOSE.value])
                    fn_v_c = (face_data.markers[Marker.JAW.value] - face_data.markers[Marker.NOSE.value]) / curr_dist

                    cos_theta = sum(fn_v_r * fn_v_c)
                    if cos_theta < 1:
                        sin_theta = math.sqrt(1 - cos_theta * cos_theta)
                        if fn_v_c[0] < fn_v_r[0]:
                            sin_theta = -sin_theta

                        trans_scale = curr_dist / rest_dist

                        face_move_data = TrackingData()
                        for i in range(Marker.MARKER_COUNT.value):
                            rest = self.face_rest_data.markers[i] * trans_scale
                            rest[0] = rest[0] * cos_theta - rest[1] * sin_theta
                            rest[1] = rest[0] * sin_theta + rest[1] * cos_theta

                            curr = face_data.markers[i] - face_data.markers[Marker.JAW.value]
                            face_move_data.markers[i] = (curr - rest) / curr_dist
                            # for j in range(2):
                            #     if face_move_data.markers[i][j] < 0.03:
                            #         face_move_data.markers[i][j] = 0
                        self.ms.send(face_move_data.markers)

            key = cv2.waitKey(1)
            if key == ord('q'):
                return


def build_argparse():
    parser = argparse.ArgumentParser(description='Start train.')
    parser.add_argument('--video', dest='video', type=str, default=None, \
                        help='the camera id (default: 0)')
    parser.add_argument('--cam_id', dest='cam_id', type=int, default=0, \
                        help='the camera to use')
    parser.add_argument('--mask', dest='mask', type=bool, default=False, \
                        help='mask the face or not')
    args = parser.parse_args()
    return args


def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return math.sqrt(dx * dx + dy * dy)


if __name__ == '__main__':
    p = Test()

    args = build_argparse()

    p.printTime()
    if args.video is not None:
        p.video(args.video)
    else:
        p.video(args.cam_id)
