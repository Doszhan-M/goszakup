from time import sleep
from logging import getLogger
from google.protobuf.wrappers_pb2 import BoolValue

from pb2 import eds_pb2
from pb2 import eds_pb2_grpc
from managers import EdsManager
from core.config import settings


logger = getLogger("grpc")


class EdsServicer(eds_pb2_grpc.EdsServiceServicer):

    def __init__(self):
        super().__init__()
        if settings.RESTART_NCALAYER:
            EdsManager.restart_ncalayer()

    def SendStatus(self, request, context):
        while True:
            if EdsManager.is_not_busy():
                yield eds_pb2.EdsManagerStatus(busy=BoolValue(value=False))
                break
            else:
                logger.info("EdsManager is busy. Waiting...")
                yield eds_pb2.EdsManagerStatus(busy=BoolValue(value=True))
                sleep(0.2)

    def ExecuteSignByEds(self, request, context):
        eds_manager = EdsManager(request)
        eds_manager.execute_sign_by_eds()
        return eds_pb2.SignByEdsResult(result=BoolValue(value=True))

    def RestartNCALayer(self, request, context):
        EdsManager.restart_ncalayer()
        return eds_pb2.RestartResult(result=BoolValue(value=True))
