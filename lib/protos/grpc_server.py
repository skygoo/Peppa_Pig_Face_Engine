# User: sky
# DATE: 2019/10/23
# TIME: 下午5:31
import sys
import time
import lib.protos.genpy.service_pb2_grpc as service
from lib.protos.genpy.api_pb2 import MarkRsp, Point, Mask

from lib.core.api.facer import FaceAna
import numpy as np


def to_np_array(image_data, dtype=np.uint8):
    width = image_data.width
    height = image_data.height
    pixel_length = image_data.pixel_length
    data = image_data.data
    assert len(data) == width * height * pixel_length
    return np.frombuffer(data, dtype=dtype).reshape((height, width, pixel_length))


facer = FaceAna()


class GrpcServer(service.FaceServerServicer):
    def predict(self, request, context):
        image = to_np_array(request.img)
        star = time.time()
        boxes, landmarks, states = facer.run(image)
        mark = []
        for face_index in range(landmarks.shape[0]):
            mask = []
            for landmarks_index in range(landmarks[face_index].shape[0]):
                x_y = landmarks[face_index][landmarks_index]
                mask.append(Point(x=x_y[0],y=x_y[1]))
            mark.append(Mask(mask=mask))

        duration = time.time() - star
        print('one iamge cost %f s' % (duration))

        return MarkRsp(request.frame, mark)
