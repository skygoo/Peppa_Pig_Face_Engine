# User: sky
# DATE: 2019/10/24
# TIME: 下午4:35
import cv2
import grpc
import sys
import lib.protos.genpy.service_pb2_grpc as service
from lib.protos.genpy.api_pb2 import ImageReq, ImgData
import time


def img2buffer(img):
    b = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                b.append(img[i][j][k])

    # print(type(b))
    return b


channel = grpc.insecure_channel('[::]:50051')
try:
    grpc.channel_ready_future(channel).result(timeout=10)
except grpc.FutureTimeoutError:
    sys.exit('Error connecting to server')
else:
    stub = service.FaceServerStub(channel)
    t1 = time.time()
    img = cv2.imread('/Users/sky/PycharmProjects/Peppa_Pig_Face_Engine/img/test_1.jpg')
    # print(type(img))
    #
    # print(img.shape[1])
    # print(img.shape[0])
    # print(img.shape[0] * img.shape[1] * img.shape[2])
    #
    # b = img2buffer(img)
    #
    # print(len(b))

    img_data = ImgData(width=img.shape[1], height=img.shape[0], pixel_length=img.shape[2], data=img.tobytes())

    response = stub.predict(ImageReq(frame=0, img=img_data))

    if response:
        print(time.time()-t1)
        print(response.frame)
        # print(response.l)
        for mask in response.l:
            # print(mask)
            for p in mask.p:
                cv2.circle(img, (int(p.x), int(p.y)), 3,  (222, 222, 222), -1)
        cv2.namedWindow("masked", 0)
        cv2.imshow("masked", img)
        cv2.waitKey(0)
    else:
        print("error")
