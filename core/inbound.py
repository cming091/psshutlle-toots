import time
import os
from .base import Base
from config import CONF
from utils import *
from psgrpc import wholeInboundBcr
logger = LogHandler(__name__)


class Inbound(Base):
    def __init__(self, data):
        super(Inbound,self).__init__(data)


    def singleProcess(self):
        self.common.tearDownStockAndAssignTables(self.db,self.data, defaultdbs=['wes'])
        if self.data['isSimulate']:
            status = self.registerFrame()
            if not status:
                self.statusCode = 402
                raise Exception('[{} registerFrame error]'.format(self.data['sName']))
            else:
                logger.info('[{} registerFrame succ]'.format(self.data['sName']))
                time.sleep(CONF['delay'])


        if self.addWorkOrder():
            logger.info('[{} addWorkOrder succ]'.format(self.data['sName']))
            time.sleep(CONF['delay'])
            if self.creatAggs():
                logger.info('[{} creatAggs succ]'.format(self.data['sName']))
                time.sleep(CONF['delay'])
                self.triggerBcr()
                self.checkAggOpStatus()
                self.checkBound()
            else:
                self.statusCode = 404
        else:
            self.statusCode = 403
        return self.data['containerCode']


    def registerFrame(self):
        self.sqlRmStartNodePods()
        data = {
            "warehouseID": self.data['warehouseID'],
            "frameID": self.data['frameID'],
            "nodeID": self.data['nodeID'],
            "dir": 1
            }
        url = '{}/tes/api/frame/registerFrame'.format(CONF['baseUrl'])
        res = RequestApi.sendReuest('registerFrame', 'POST', url, data).json()
        logger.info('[{} registerFrame: res:{}]'.format(self.data['sName'],res))
        if res.get(self.data['returnCode'], None) == 0:
            return True
        return False

    def init(self):
        logger.info('[{} init ]'.format(self.data['sName']))
        self.sqlRmAllPods()

    def triggerBcr(self):
        info = wholeInboundBcr(self.data['ip'],self.data['warehouseCode'],self.data['containerCode'],self.data['warehouseID'])
        logger.info('[{} bcr res:{}]'.format(self.data['sName'],info))

    def addWorkOrder(self):
        url = '{}/invtransaction/api/workorder/inbound/add'.format(CONF['baseUrl'])
        data ={
            "woNo": self.data['no'],
            "warehouseCode": self.data['warehouseCode'],
            "regionCode": self.data['regionCode'],
            "waveNo": self.data['no'],
            "inBoundNo": self.data['no'],
            "originStation": "PS-IN-001",
            "priority": 0,
            "transportUnit": self.data['containerCode'],
            "containerCode": self.data['containerCode'],
            "skuCode": self.data['skuCode'],
            "skuName": self.data['skuName'],
            "lot": "",
            "grade": 0,
            "quantity": self.data['quantity'],
            "boxQuantity": 1,
            "bizType": 1,
            "transType": self.data['transType'],
            "bizDate": 1594292882000,
            "destination": "309843433806102535",
            "rely_wo_no": "",
            "extension": "",
            "user": "user",
            'palletModel':0,
        }
        res = RequestApi.sendReuest('addWorkOrder', 'POST', url, data, headers=self.headers).json()
        logger.info('[{} addWorkOrder: res:{}]'.format(self.data['sName'],res))
        if res.get(self.data['returnCode'],None) == 0:
            return True
        return False

    def sqlRmStartNodePods(self):
        sql = 'delete from tes.frame where status=1 and node=\'{}\';'.format(self.data['startNodeId'])
        self.db.get_connection('tes')
        res = self.db.execute('tes', sql)
        logger.info('[{} sqlRmStartNodePods tes res:{}]'.format(self.data['sName'],res))







