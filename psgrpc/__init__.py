import grpc
from psgrpc.processflowengine import processflowengine_pb2_grpc
from psgrpc.processflowengine import processflowengine_pb2
from psgrpc.frworkstation import frworkstation_pb2
from psgrpc.frworkstation import frworkstation_pb2_grpc
from psgrpc.warebasic import container_pb2_grpc
from psgrpc.common import container_pb2
from psgrpc.wareshuttle import *
from psgrpc import common
import json
import time
from utils import *
logger = LogHandler(__name__)

def wholeInboundBcr123(ip, warehouseCode, containerCode):
    channel = grpc.insecure_channel('{}:50051'.format(ip))
    stub = processflowengine_pb2_grpc.ProcessFlowEngineServiceStub(channel)
    data={"warehouseCode":warehouseCode,
          "stationType":1,
          "actionType":3,
          "containerCode":[containerCode],
          "stationCode":'PS-IN-001',

          }
    response = stub.ListActAggByContainer(processflowengine_pb2.ListActAggContainerRequest(**data))
    return response



def wholeInboundBcr(ip, warehouseCode, containerCode, warehouseID):
    logger.info('[wholeInboundBcr ip:{} \t warehouseCode:{} \t containerCode:{} \t warehouseID{}]\n'.format(ip, warehouseCode, containerCode, warehouseID))
    channel = grpc.insecure_channel('{}:50051'.format(ip))
    stub = frworkstation_pb2_grpc.ProcessFlowEngineStub(channel)
    response = stub.OnceChannel(common.ServerPackage(serial=1,invoke=common.InvokeRequest(
                                                     method='onDeviceMessage',
                                                     stationCode = 'PS-IN-001',
                                                     stationGroupCode = 'PS-IN-001',
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


def wholeOutboundBcr(ip, warehouseCode, containerCode, warehouseID, transType):
    logger.info('[wholeOutboundBcr ip:{} \t warehouseCode:{} \t containerCode:{} \t warehouseID{}]\n'.format(ip, warehouseCode, containerCode, warehouseID))
    channel = grpc.insecure_channel('{}:50051'.format(ip))
    stub = frworkstation_pb2_grpc.ProcessFlowEngineStub(channel)
    response = stub.OnceChannel(common.ServerPackage(serial=1,invoke=common.InvokeRequest(
                                                     method='receiveTask',
                                                     stationCode = 'PS-Schedule',
                                                     stationGroupCode='',
                                                     containerCode=containerCode,
                                                     warehouseCode=warehouseCode,
                                                     task=common.TesTaskIndex(warehouseID=warehouseID),
                                                     action=common.ActAgg(
                                                             actionStatus=1,
                                                             actionType=1,
                                                             containerCode=containerCode,
                                                             stationCode="PS-Schedule",
                                                             warehouseCode=warehouseCode,
                                                             transType=transType)
                                                     )))
    return response


def outboundBcr(data):
    channel = grpc.insecure_channel('{}:50051'.format(data['ip']))
    stub = mastercontrol_pb2_grpc.MasterControlStub(channel)
    response = stub.WaveTrigger(WareTriggerRequest(traceID='',
                                                           warehouseCode=data['warehouseCode'],
                                                           regionCode=data['regionCode'],
                                                           waveNoList=[data['no']],
                                                           ))
    return response



def addContainer(data, row, containerType):
    channel = grpc.insecure_channel('{}:50051'.format(data['ip']))
    stub = container_pb2_grpc.ContainerServiceStub(channel)
    if containerType==1:#原箱
        containerCode= row['containercode'].strip()
    elif containerType ==2:#周转箱
        containerCode= row['containercode'].strip()
    else: #托盘
        containerCode = data['containerCode']
    response =  stub.AddContainer(container_pb2.AddContainerRequest(
        warehouseCode=data['warehouseCode'],
        containerID =str(round(time.time() * 10000))[-5:-1],
        containerCode = containerCode,
        containerType=containerType,
        cartonTypeID=''

    ))
    return response

def deleteContainter(data, row, containerType):
    channel = grpc.insecure_channel('{}:50051'.format(data['ip']))
    stub = container_pb2_grpc.ContainerServiceStub(channel)
    if containerType == 1:  # 原箱
        containerCode = row['containercode'].strip()
    elif containerType == 2:  # 周转箱
        containerCode = row['containercode'].strip()
    else:  # 托盘
        containerCode = data['containerCode']
    response = stub.DeleteContainer(container_pb2.DeleteContainerRequest (
        warehouseCode=data['warehouseCode'],
        containerCode=containerCode,
    ))
    return response
# data = {'containerCode':'10010','warehouseCode':'JY','ip':'10.170.124.11'}
# row = {'containercode':'101'}
# print(deleteContainter(data,row,3))
#outboundBcr('10.170.124.11', "JY", 'PSRegion', ['01711'])