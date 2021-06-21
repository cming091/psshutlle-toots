import grpc
from psgrpc import common
from psgrpc.common import container_pb2
from psgrpc.common import containerTypeEnum_pb2
from psgrpc.warebasic import container_pb2_grpc
from psgrpc.processflowengine import processflowengine_pb2_grpc
from psgrpc.processflowengine import processflowengine_pb2
import json
def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('10.170.124.92:50051')
    # 调用 rpc 服务
    stub = processflowengine_pb2_grpc.ProcessFlowEngineServiceStub(channel)
    #整托入库inbound
    # messge={"actionType": 3, "containerCodeList": ["70008"], "stationCode": "PS-IN-001", "stationType": 1,
    #  "warehouseCode": "JY"}
    warehouseID='12121'
    warehouseCode="JY"
    stationType=1
    actionType=3
    containerCode=['70008']
    stationCode= 'PS-IN-001'
    response = stub.OnceChannel(common.ServerPackage(serial=1,invoke=common.InvokeRequest(
                                                     method='onDeviceMessage',
                                                     stationCode = stationCode,
                                                     stationGroupCode = stationCode,
                                                     containerCode=containerCode,
                                                     warehouseCode=warehouseCode,
                                                     conveyor=common.TesConveyorIndex(
                                                       warehouseID=warehouseID,
                                                       conveyorID='1',
                                                       barCode=[containerCode],
                                                       reporterID="10",
                                                       reporterType=0)
                                                     )))
    return response

    #整托入库inbound
    # messge={"actionType": 3, "containerCodeList": ["70008"], "stationCode": "PS-IN-001", "stationType": 1,
    #  "warehouseCode": "JY"}
def addContainer():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('10.170.124.92:50051')
    # 调用 rpc 服务
    stub = container_pb2_grpc.ContainerServiceStub(channel)
    #整托入库inbound
    # messge={"actionType": 3, "containerCodeList": ["70008"], "stationCode": "PS-IN-001", "stationType": 1,
    #  "warehouseCode": "JY"}
    warehouseCode="JY"
    containerID='1001'
    stationType=1
    containerCode ='3'
    containerCodeList=['70008']
    containerType =3
    specsID='1001'
    response =  stub.AddContainer(container_pb2.AddContainerRequest (
        warehouseCode=warehouseCode,
        containerID =containerID,
        containerCode =containerCode ,
        containerType=containerType,
        cartonTypeID=''

    ))
    print(str(response))
    #整托入库inbound
    # messge={"actionType": 3, "containerCodeList": ["70008"], "stationCode": "PS-IN-001", "stationType": 1,
    #  "warehouseCode": "JY"}
if __name__ == '__main__':
    addContainer()