from olive.proto.health_pb2 import HealthCheckRequest, HealthCheckResponse
from olive.proto import health_pb2_grpc, health_pb2
import traceback


class HealthService(health_pb2_grpc.HealthServicer):
    def __init__(self, app):
        self.app = app

    def Check(self, request: HealthCheckRequest, context) -> HealthCheckResponse:
        try:
            self.app.log.info('Am healthy babe!')
            return health_pb2.HealthCheckResponse(
                status=health_pb2.HealthCheckResponse.SERVING
            )
        except Exception:
            self.app.log.error('Khak too saret -> {}'.format(traceback.format_exc()))
            return health_pb2.HealthCheckResponse(
                status=health_pb2.HealthCheckResponse.UNKNOWN
            )
