import cv2
import time
import numpy as np
import argparse
from threading import Timer
from datetime import datetime

from lib.core.api.facer import FaceAna
from lib.core.headpose.pose import get_head_pose, line_pairs


class Test:
    def __init__(self):
        self.facer = FaceAna()
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

        # vide_capture.set(3, 640)
        # vide_capture.set(4, 480)

        while 1:

            ret, image = vide_capture.read()
            self.frame += 1
            pattern = np.zeros_like(image)

            img_show = image.copy()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            star = time.time()
            boxes, landmarks, states = self.facer.run(image)

            duration = time.time() - star
            # print('one iamge cost %f s' % (duration))

            for face_index in range(landmarks.shape[0]):

                #######head pose
                reprojectdst, euler_angle = get_head_pose(landmarks[face_index], img_show)

                if args.mask:
                    face_bbox_keypoints = np.concatenate(
                        (landmarks[face_index][:17, :], np.flip(landmarks[face_index][17:27, :], axis=0)), axis=0)

                    pattern = cv2.fillPoly(pattern, [face_bbox_keypoints.astype(np.int)], (1., 1., 1.))

                for start, end in line_pairs:
                    cv2.line(img_show, reprojectdst[start], reprojectdst[end], (0, 0, 255), 2)

                cv2.putText(img_show, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)
                cv2.putText(img_show, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)
                cv2.putText(img_show, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)

                for landmarks_index in range(landmarks[face_index].shape[0]):
                    x_y = landmarks[face_index][landmarks_index]
                    cv2.circle(img_show, (int(x_y[0]), int(x_y[1])), 3,
                               (222, 222, 222), -1)

            cv2.namedWindow("capture", 0)
            cv2.imshow("capture", img_show)

            if args.mask:
                cv2.namedWindow("masked", 0)
                cv2.imshow("masked", image * pattern)

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
