# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from olive.proto import zoodroom_pb2 as zoodroom__pb2


class CranberryServiceStub(object):
  """python3 -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./zoodroom.proto
  ----------------- Cranberry service (OAuth 2.0) -----------------

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ResourceOwnerPasswordCredential = channel.unary_unary(
        '/zoodroom.CranberryService/ResourceOwnerPasswordCredential',
        request_serializer=zoodroom__pb2.ResourceOwnerPasswordCredentialRequest.SerializeToString,
        response_deserializer=zoodroom__pb2.ResourceOwnerPasswordCredentialResponse.FromString,
        )
    self.CreateClient = channel.unary_unary(
        '/zoodroom.CranberryService/CreateClient',
        request_serializer=zoodroom__pb2.CreateClientRequest.SerializeToString,
        response_deserializer=zoodroom__pb2.CreateClientResponse.FromString,
        )
    self.VerifyAccessToken = channel.unary_unary(
        '/zoodroom.CranberryService/VerifyAccessToken',
        request_serializer=zoodroom__pb2.VerifyAccessTokenRequest.SerializeToString,
        response_deserializer=zoodroom__pb2.VerifyAccessTokenResponse.FromString,
        )
    self.GetClientByClientId = channel.unary_unary(
        '/zoodroom.CranberryService/GetClientByClientId',
        request_serializer=zoodroom__pb2.GetClientByClientIdRequest.SerializeToString,
        response_deserializer=zoodroom__pb2.GetClientByClientIdResponse.FromString,
        )


class CranberryServiceServicer(object):
  """python3 -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./zoodroom.proto
  ----------------- Cranberry service (OAuth 2.0) -----------------

  """

  def ResourceOwnerPasswordCredential(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateClient(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def VerifyAccessToken(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetClientByClientId(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CranberryServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ResourceOwnerPasswordCredential': grpc.unary_unary_rpc_method_handler(
          servicer.ResourceOwnerPasswordCredential,
          request_deserializer=zoodroom__pb2.ResourceOwnerPasswordCredentialRequest.FromString,
          response_serializer=zoodroom__pb2.ResourceOwnerPasswordCredentialResponse.SerializeToString,
      ),
      'CreateClient': grpc.unary_unary_rpc_method_handler(
          servicer.CreateClient,
          request_deserializer=zoodroom__pb2.CreateClientRequest.FromString,
          response_serializer=zoodroom__pb2.CreateClientResponse.SerializeToString,
      ),
      'VerifyAccessToken': grpc.unary_unary_rpc_method_handler(
          servicer.VerifyAccessToken,
          request_deserializer=zoodroom__pb2.VerifyAccessTokenRequest.FromString,
          response_serializer=zoodroom__pb2.VerifyAccessTokenResponse.SerializeToString,
      ),
      'GetClientByClientId': grpc.unary_unary_rpc_method_handler(
          servicer.GetClientByClientId,
          request_deserializer=zoodroom__pb2.GetClientByClientIdRequest.FromString,
          response_serializer=zoodroom__pb2.GetClientByClientIdResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'zoodroom.CranberryService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
