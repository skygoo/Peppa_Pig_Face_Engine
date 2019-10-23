# User: sky
# DATE: 2019/10/23
# TIME: 下午5:31
import sys
import datetime
import concurrent.futures as futures
import grpc
import lib.protos.genpy.service_pb2_grpc as service
from lib.protos.genpy.api_pb2 import MarkRsp


class GrpcServer(service.FaceServerServicer):

    @staticmethod
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service.add_FaceServerServicer_to_server(
            GrpcServer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()

    def predict(self, request, context):
        return MarkRsp




if __name__ == '__main__':
    GrpcServer.serve()