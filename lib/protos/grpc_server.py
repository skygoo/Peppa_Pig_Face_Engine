# User: sky
# DATE: 2019/10/23
# TIME: 下午5:31
import sys
import time
import lib.protos.genpy.service_pb2_grpc as service
from lib.protos.genpy.api_pb2 import MarkRsp, Point, Mask
import lib.protos.genpy.api_pb2

from lib.core.api.facer import FaceAna
import numpy as np
import cv2


def to_np_array(image_data, dtype=np.uint8):
    width = image_data.width
    height = image_data.height
    pixel_length = image_data.pixel_length
    data = image_data.data
    assert len(data) == width * height * pixel_length
    return np.frombuffer(data, dtype=dtype).reshape((height, width, pixel_length))


facer = FaceAna()
# remind 消除初始化时间
# facer.run(cv2.imread("/Users/sky/PycharmProjects/Peppa_Pig_Face_Engine/figure/png_300.png"))


class GrpcServer(service.FaceServerServicer):
    def predict(self, request, context):
        star = time.time()
        print(request.frame)
        image = to_np_array(request.img)
        print(image.shape)
        cv2.imwrite("/Users/sky/PycharmProjects/Peppa_Pig_Face_Engine/img/test_%d.jpg" % (request.frame), image)

        print(request.frame, 'reshape cost %f s' % (time.time() - star))
        boxes, landmarks, states = facer.run(image)
        print(request.frame, 'detect cost %f s' % (time.time() - star))
        mark = MarkRsp()
        mark.frame = request.frame
        for face_index in range(landmarks.shape[0]):
            mask = mark.l.add()
            for landmarks_index in range(landmarks[face_index].shape[0]):
                poi = mask.p.add()
                x_y = landmarks[face_index][landmarks_index]
                poi.x = x_y[0]
                poi.y = x_y[1]
        print(request.frame, 'one iamge cost %f s' % (time.time() - star))
        return mark
