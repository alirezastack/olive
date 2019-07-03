from olive.proto import zoodroom_pb2, zoodroom_pb2_grpc
from olive.exc import GRPCError
from grpc import RpcError
from retry import retry
import logging
import grpc
import os

_DEFAULT_SERVICE_HOST = '[::]'
_DEFAULT_SERVICE_PORT = '9000'

# timeout in seconds
_DEFAULT_RPC_CALL_TIMEOUT = 3

# number of retries in case of rpc call failure
_DEFAULT_RETRY_COUNT = 3
_DEFAULT_RETRY_BACKOFF = 2
_DEFAULT_RETRY_DELAY = 2


class RPCClient:
    def __init__(self, service, timeout=_DEFAULT_RPC_CALL_TIMEOUT):
        # get host and port based on service name
        self.service = service
        self.timeout = timeout
        host = os.environ.get('{}_HOST'.format(self.service.upper()), _DEFAULT_SERVICE_HOST)
        port = os.environ.get('{}_PORT'.format(self.service.upper()), _DEFAULT_SERVICE_PORT)
        logging.debug('connecting to {}:{} {} gRPC...'.format(host, port, service))
        # get service address port by its environment variable
        self.channel = grpc.insecure_channel('{}:{}'.format(host, port))
        logging.debug('Successfully connected to {} service :)'.format(service))

    # Protocol of services & methods are as below:
    # Service name:     YourservicenameService  -> CartService
    # Method name:      YourMethodName          -> AddItem
    # Method input:     YourMethodNameRequest   -> AddItemRequest
    # Method response:  YourMethodNameResponse  -> AddItemResponse
    @retry(exceptions=(RpcError,),
           tries=_DEFAULT_RETRY_COUNT,
           delay=_DEFAULT_RETRY_DELAY,
           backoff=_DEFAULT_RETRY_BACKOFF)
    def call(self, method, **kwargs):
        """
        :param method: remote gRPC method name
        :param kwargs: remote method input parameters
        :return: method response
        """
        logging.debug('getting {} stub'.format(self.service))
        _stub = getattr(zoodroom_pb2_grpc, '{}ServiceStub'.format(self.service.capitalize()))(self.channel)
        logging.debug('form gRPC request with input parameters')
        _request = getattr(zoodroom_pb2, '{}Request'.format(method))(**kwargs)
        logging.debug('Calling {}.{}...'.format(self.service, method))
        # .future is used to set timeout on the gRPC client
        # old way -> res = getattr(_stub, method)(_request)
        future_res = getattr(_stub, method).future(_request)
        res = future_res.result(timeout=self.timeout)
        if hasattr(res, 'error') and res.error.code:
            logging.error('Remote rpc call error: \r\n{}'.format(res.error))
            raise GRPCError('Remote procedure call exception', res.error)

        logging.info('Fetched information: \r\n{}'.format(res))
        return res

    def call_async(self):
        pass
