from time import sleep
from logging import getLogger
from google.protobuf.wrappers_pb2 import BoolValue

from pb2 import eds_pb2
from pb2 import eds_pb2_grpc

logger = getLogger("grpc")


class EdsServicer(eds_pb2_grpc.EdsServiceServicer):
    def ExecuteSignByEds(self, request, context):
        type_ = request.type
        print('type_: ', type_)
        return eds_pb2.SignByEdsResult(message="EDS signing executed successfully")

    def SendStatus(self, request, context):
        while True:
            if not True:  # заменить на реальное условие
                yield eds_pb2.EdsManagerStatus(busy=BoolValue(value=False))
                break
            else:
                yield eds_pb2.EdsManagerStatus(busy=BoolValue(value=True))
                sleep(0.3)
                