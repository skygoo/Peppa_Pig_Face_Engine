# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import lib.protos.genpy.api_pb2 as api__pb2


class FaceServerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.predict = channel.unary_unary(
        '/org.seekloud.theia.faceAnalysis.pb.FaceServer/predict',
        request_serializer=api__pb2.ImageReq.SerializeToString,
        response_deserializer=api__pb2.MarkRsp.FromString,
        )


class FaceServerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def predict(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_FaceServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'predict': grpc.unary_unary_rpc_method_handler(
          servicer.predict,
          request_deserializer=api__pb2.ImageReq.FromString,
          response_serializer=api__pb2.MarkRsp.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.seekloud.theia.faceAnalysis.pb.FaceServer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
