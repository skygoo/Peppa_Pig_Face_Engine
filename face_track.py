import cv2
import time
import numpy as np
import argparse
import time
from datetime import datetime
from threading import Timer

from lib.core.api.facer import FaceAna
from lib.core.headpose.pose import get_head_pose, line_pairs
from lib.core.track.socket import MayaSocket, Marker


class Test:
    def __init__(self):
        self.facer = FaceAna()
        self.ms = MayaSocket()

        self.frame = 0
        self.inc = 1

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
            boxes, landmarks, states = self.facer.run(image)

            if len(landmarks) > 0:
                keypoints = []
                keypoints.append(landmarks[0][19])
                keypoints.append(landmarks[0][21])
                keypoints.append(landmarks[0][22])
                keypoints.append(landmarks[0][24])
                keypoints.append(landmarks[0][41])
                keypoints.append(landmarks[0][46])
                keypoints.append(landmarks[0][31])
                keypoints.append(landmarks[0][35])
                keypoints.append(landmarks[0][48])
                keypoints.append(landmarks[0][51])
                keypoints.append(landmarks[0][54])
                keypoints.append(landmarks[0][57])

                # print(time.time() - str_time)



                for landmarks_index in range(12):
                    x_y = keypoints[landmarks_index]
                    cv2.circle(img_show, (int(x_y[0]), int(x_y[1])), 3,
                               (0, 0, 225), -1)


            cv2.imshow("capture", img_show)

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


if __name__ == '__main__':
    p = Test()

    args = build_argparse()

    p.printTime()
    if args.video is not None:
        p.video(args.video)
    else:
        p.video(args.cam_id)
