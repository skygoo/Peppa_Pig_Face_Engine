# User: sky
# DATE: 2019/10/24
# TIME: 上午10:35


import cv2
import time
import numpy as np
import argparse
import concurrent.futures as futures
import grpc
import lib.protos.genpy.service_pb2_grpc as service
from lib.protos.grpc_server import GrpcServer


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service.add_FaceServerServicer_to_server(
        GrpcServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
