from olive.exc import QuitException
from concurrent import futures
import signal
import grpc
import time
import os

_DEFAULT_SERVER_MAX_WORKERS = 80
_DEFAULT_SERVER_MAX_CONCURRENT_RPCS = 3000

_DEFAULT_SERVICE_HOST = '[::]'
_DEFAULT_SERVICE_PORT = '9000'

_SERVER_SHUTDOWN_DEFAULT_TIMEOUT = 15


class GRPCServerBase(object):
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
