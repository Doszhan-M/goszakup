from __future__ import print_function
from uuid import uuid4
from google.protobuf.wrappers_pb2 import BoolValue

import logging

import grpc
from pb2 import eds_pb2
from pb2 import eds_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = eds_pb2_grpc.EdsServiceStub(channel)

        # Отправляем запрос на проверку статуса EdsManager
        eds_manager_status = stub.SendStatus(eds_pb2.EdsManagerStatusCheck())
        for status in eds_manager_status:
            if not status.busy.value:
                print("EdsManager is not busy. You can proceed.")
                break
            else:
                print("EdsManager is busy. Waiting...")

        # Выполняем действие с EDS
        execute_response = stub.ExecuteSignByEds(eds_pb2.SignByEdsStart(type="your_type"))
        print("Response from ExecuteSignByEds:", execute_response.message)


if __name__ == '__main__':
    run()
