import time
import os
from config import CONF
from utils import *
from .common import Common
import random
logger = LogHandler(__name__)

class Base(object):
    def __init__(self, data):
        self.statusCode = 200
        self.data = data
        self.headers = {'Content-Type':'application/json;charset=UTF-8'}
        self.db = Mysql(*(CONF['mysqlUrl'].split(';')))
        self.common = Common

    def generateWoNO(self):
        return  str(self.data['transType']) + str(round(time.time() * 1000000))

    def getWarehouseId(self):
        warehouseId = ''
        sql = "select warehouse_id from tes.warehouse where status=1 order by update_time desc limit 1"
        self.db.get_connection('tes')
        res = self.db.execute('tes', sql)
        if res:
            logger.info('[{} tes has WarehouseId:{}]'.format(self.data['sName'],res[0][0]))
            return res[0][0]
        else:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = '{}/tes/api/warehouse/register'.format(CONF['baseUrl'])
            data = {"warehouseName": "仓库名称", "userID": "6602126394707326280", "length": 100, "width": 100,
                    "hetuVersion": "hetu1.4.3"}
            res = RequestApi.sendReuest('getWarehouseId','POST',url,data=data,headers=headers,postType=2).json()
            logger.info('[getWarehouseId: res:{}]'.format(res))
            if res.get('returnCode', None) == 0:
                if res['data']:
                    logger.info('[register  WarehouseId:{}]'.format(res['data']['warehouseID']))
                    return res['data']['warehouseID']
            return warehouseId

    def creatAggs(self):
        data = {
                "warehouseCode": self.data['warehouseCode'],
                "workOrderList": [
                    {
                        "group4OpSeq": "",
                        "group4Pack": "",
                        "workOrderNo": self.data['no']
                    }
                ]
            }
        url = '{}/invtransaction/api/workorder/common/actionagg/execute'.format(CONF['baseUrl'])
        res = RequestApi.sendReuest('creatAggs', 'POST', url, data, headers=self.headers).json()
        logger.info('[{} creatAggs: res:{}]'.format(self.data['sName'],res))
        if res.get(self.data['returnCode'],None) == 0:
            return True
        return False

    def checkAggOpStatus(self):
        times = 0
        while True:
            sql = 'select action_status from process_flow_engine.action_aggregation where container_code={} order by id desc limit 1'.format(self.data['containerCode'])
            self.db.get_connection('process_flow_engine')
            res = self.db.execute('process_flow_engine', sql)
            if res:
                logger.info('[{} process_flow_engine has action_status:{} containerCode:{}]'.format(self.data['sName'],res[0][0], self.data['containerCode']))
                if res[0][0] == 2:
                    logger.info('[{} process_flow_engine containerCode:{} AggOpStatus ok ]'.format(self.data['sName'],self.data['containerCode']))
                    return
            time.sleep(CONF['delay'])
            times += 1
            if times >= CONF['times']:
                self.statusCode = 405
                raise Exception('{} checkAggOpStatus too many retries'.format(self.data['sName']))

    def checkBound(self):
        times = 0
        while True:
            sql = 'select * from invtransaction.{} where container_code={} ' \
                  'and trans_type={} and wo_status={} order by id desc limit 1'.format(self.data['checkPsTable'],
            self.data['containerCode'],self.data['transType'],self.data['woStatus'])
            self.db.get_connection('invtransaction')
            res = self.db.execute('invtransaction', sql)
            logger.info('[{} checkBound invtransaction:containerCode {}  res:{} ]'.format(self.data['sName'],self.data['containerCode'], res))
            if res:
                logger.info('[{} checkBound invtransaction has ok :{}]'.format(self.data['sName'],res))
                return
            time.sleep(CONF['delay'])
            times += 1
            if times >= CONF['times']:
                self.statusCode = 406
                raise Exception('{} checkBound too many retries'.format(self.data['sName']))

    def sqlRmAllPods(self):
        sql = 'delete from tes.frame where status=1;'
        self.db.get_connection('tes')
        res = self.db.execute('tes', sql)
        logger.info('[{} sqlRmAllPods tes res:{}]'.format(self.data['sName'],res))


    def __call__(self, codes):
        warehouseID = self.getWarehouseId()
        if warehouseID:
            self.data['warehouseID'] = warehouseID
        else:
            logger.error('[{} warehouseID is null]'.format(self.data['sName']))
            self.statusCode = 400
            os._exit(0)
        self.runModeOfContainerCode(codes)

    def runModeOfContainerCode(self, codes):
        for code in codes:
            self.data['no'] = self.generateWoNO()
            self.data['containerCode'] = code
            self.data['frameID'] = code
            logger.info('[{} runModeOfContainerCode data:{}]'.format(self.data['sName'],self.data))
            try:
                self.singleProcess()
            except Exception as e:
                logger.exception(e)
                self.statusCode = 500
                logger.error('[{} runModeOfContainerCode singleProcess statusCode:{}]'.format(self.data['sName'],self.statusCode))
                if self.data.get('isRaise',False):
                    raise Exception(str(e))