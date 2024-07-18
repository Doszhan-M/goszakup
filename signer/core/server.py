import grpc
from concurrent import futures

from pb2 import eds_pb2_grpc
from .logging import CustomLogger
from handlers.eds import EdsServicer


def start_server(mode):
    logger = CustomLogger.setup()
    logger.info(mode)
    logger.info("Start gRPC server")
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    eds_pb2_grpc.add_EdsServiceServicer_to_server(EdsServicer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()
