import time
import os
from urllib import parse
from .base import Base
from config import CONF
from utils import *
from psgrpc import *
logger = LogHandler(__name__)

class ManualCounting(Base):
    def __init__(self, data):
        super(Outbound,self).__init__(data)

    def triggerBcr(self):
        info = outboundBcr(self.data)
        logger.info('[{} bcr res:{}]\n'.format(self.data['sName'],info))

    def addWorkOrder(self):
        url = '{}/invtransaction/api/workorder/outbound/add'.format(CONF['baseUrl'])
        data={
            "woNo": self.data['no'],
            "warehouseCode": self.data['warehouseCode'],
            "regionCode": self.data['regionCode'],
            "waveNo": self.data['no'],
            "outBoundNo":self.data['no'],
            "originStation": "PS-Schedule",
            "priority": 0,
            "transportUnit": self.data['containerCode'],
            "containerCode": self.data['containerCode'],
            "skuCode": "6",
            "skuName": "skuname2",
            "lot": "",
            "grade": 0,
            "quantity": 10,
            "boxQuantity": 1,
            "bizType": 1,
            "transType": self.data['transType'],
            "bizDate": 1594292882000,
            "destination": "PS-MOCK-BCR",
            "rely_wo_no": "",
            "extension": "",
            "user": "user",
            "palletModel": 0,
        }
        res = RequestApi.sendReuest('addWorkOrder', 'POST', url, data, headers=self.headers).json()
        logger.info('[{} addWorkOrder: res:{}]'.format(self.data['sName'],res))
        if res.get(self.data['returnCode'],None) == 0:
            return True
        return False


    def isShelfInStock(self):
        sql = 'select * from stock.container_stock where container_code={} ' \
              'and lock_flag=0 and delete_flag=0 and qty>reserved_qty'.format(self.data['containerCode'])
        self.db.get_connection('stock')
        res = self.db.execute('stock', sql)
        logger.info('[{} isShelfInStock container_stock:containerCode {}  res:{} ]'.format(self.data['sName'],self.data['containerCode'], res))
        if res:
            logger.info('[{} isShelfInStock container_stock has ok :{}]'.format(self.data['sName'],res))
            return True
        return False

    def multiRemovePod(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = 'warehouseID={}&podIDs={}'.format(self.data['warehouseID'],self.data['frameID'])
        url = '{}/tes/apiv2/multiRemovePod'.format(CONF['baseUrl'])
        res = RequestApi.sendReuest('multiRemovePod', 'POST', url, data, headers=headers, postType=2).json()
        logger.info('[{} multiRemovePod: res:{}]'.format(self.data['sName'],res))
        self.sqlRmPods()
        if res.get(self.data['returnCode'],None) == 0:
            return True
        return False

    def sqlRmPods(self):
        sql = 'delete from tes.frame where status=1 and frame_id={};'.format(self.data['frameID'])
        self.db.get_connection('tes')
        res = self.db.execute('tes', sql)
        logger.info('[{} sqlRmPods tes res:{} frameID:{} ]'.format(self.data['sName'],res,self.data['frameID']))

    def singleProcess(self):
        self.common.tearDownStockAndAssignTables(self.db, self.data,defaultdbs=['wes'])
        if self.addWorkOrder():
            logger.info('[{} addWorkOrder succ]'.format(self.data['sName']))
            time.sleep(CONF['delay'])
            if self.creatAggs():
                logger.info('[{}creatAggs succ]'.format(self.data['sName']))
                time.sleep(CONF['delay'])
                self.triggerBcr()
                self.checkAggOpStatus()
                self.checkBound()
            else:
                self.statusCode = 403
        else:
            self.statusCode = 402
        if self.data['isSimulate']:
            self.multiRemovePod()
        return self.data['containerCode']






