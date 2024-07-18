from time import sleep
from logging import getLogger
from google.protobuf.wrappers_pb2 import BoolValue

from pb2 import eds_pb2
from pb2 import eds_pb2_grpc
from managers import EdsManager


logger = getLogger("grpc")


class EdsServicer(eds_pb2_grpc.EdsServiceServicer):

    def SendStatus(self, request, context):
        if EdsManager.is_not_busy():
            yield eds_pb2.EdsManagerStatus(busy=BoolValue(value=False))
        else:
            yield eds_pb2.EdsManagerStatus(busy=BoolValue(value=True))

    def ExecuteSignByEds(self, request, context):
        eds_manager = EdsManager(request)
        eds_manager.execute_sign_by_eds()
        return eds_pb2.SignByEdsResult(result=BoolValue(value=True))
