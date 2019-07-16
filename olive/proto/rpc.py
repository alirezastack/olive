from olive.proto import zoodroom_pb2_grpc
from olive.toolbox import get_caller_name
from olive.proto import zoodroom_pb2
from olive.exc import QuitException
from olive.exc import GRPCError
from concurrent import futures
from grpc import RpcError
from retry import retry
import logging
import signal
import time
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

_DEFAULT_SERVER_MAX_WORKERS = 80
_DEFAULT_SERVER_MAX_CONCURRENT_RPCS = 3000

_SERVER_SHUTDOWN_DEFAULT_TIMEOUT = 15


class GRPCServerBase:
    def __init__(self, service, app):
        self.service_name = service.upper()
        self.app = app
        """
        if maximum_concurrent_rpcs has reached then the below error will be raised
            -> Concurrent RPC limit exceeded
        if maximum_concurrent_rpcs has not reached and max_workers are less than maximum_concurrent_rpcs
        and all workers are busy, then other requests will be queued
        """
        # create gRPC server
        self.server = grpc.server(futures.ThreadPoolExecutor(
            max_workers=os.environ.get('{}_MAX_WORKERS'.format(self.service_name), _DEFAULT_SERVER_MAX_WORKERS),
            thread_name_prefix=self.service_name.lower()
        ),
            maximum_concurrent_rpcs=os.environ.get('{}_MAX_CONCURRENT_RPCS'.format(self.service_name),
                                                   _DEFAULT_SERVER_MAX_CONCURRENT_RPCS))

    def start(self):
        # get host and port based on service name
        host = os.environ.get('{}_HOST'.format(self.service_name), _DEFAULT_SERVICE_HOST)
        port = os.environ.get('{}_PORT'.format(self.service_name), _DEFAULT_SERVICE_PORT)
        # start server
        self.app.log.info("listening on {}:{}".format(host, port))
        self.server.add_insecure_port('{}:{}'.format(host, port))
        self.server.start()
        self.app.log.info('-> {} <- Server Started!'.format(self.service_name))

        old1 = signal.signal(signal.SIGINT, self._signal_handler)
        old2 = signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            # keep alive
            while True:
                time.sleep(10000)
        except QuitException:
            self.app.log.debug("Quitting server...")
            shutdown_event = self.server.stop(5)
            shutdown_event.wait(timeout=_SERVER_SHUTDOWN_DEFAULT_TIMEOUT)
        finally:
            signal.signal(signal.SIGINT, old1)
            signal.signal(signal.SIGTERM, old2)

    def _signal_handler(self, signal_number, frame):
        raise QuitException


class RPCClient:
    def __init__(self, service, timeout=_DEFAULT_RPC_CALL_TIMEOUT):
        self.service = service.lower()
        self.timeout = timeout
        host = os.environ.get('{}_HOST'.format(self.service.upper()), _DEFAULT_SERVICE_HOST)
        port = os.environ.get('{}_PORT'.format(self.service.upper()), _DEFAULT_SERVICE_PORT)
        logging.debug('connecting to {}:{} {} gRPC...'.format(host, port, self.service))
        # get service address port by its environment variable
        self.channel = grpc.insecure_channel('{}:{}'.format(host, port))
        logging.debug('Successfully connected to {} service :)'.format(self.service))

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
        try:
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
        finally:
            logging.debug('closing gRPC channel...')
            self.channel.close()
            logging.info('gRPC channel closed')

    def call_async(self):
        pass


class Response:
    @staticmethod
    def message(calframe=2, **kwargs):
        caller_response = '{}Response'.format(get_caller_name(calframe_num=calframe))
        logging.debug('sending {} with below payload:\n{}'.format(caller_response, kwargs))
        return getattr(zoodroom_pb2, caller_response)(**kwargs)
