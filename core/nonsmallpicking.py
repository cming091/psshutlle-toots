import time
import os
from urllib import parse
from .outbound import Outbound
from config import CONF
from utils import *
logger = LogHandler(__name__)

class NonSmallPicking(Outbound):
    def __init__(self, data):
        super(Outbound,self).__init__(data)

    def setDataNodeIdBypodID(self):
        sql = 'select node from tes.frame where frame_id=\'{}\' and status=1'.format(
            self.data['containerCode'])
        self.db.get_connection('tes')
        res = self.db.execute('tes', sql)
        logger.info('[{} setDataNodeIdBypodID containerCode {}  res:{} ]'.format(self.data['sName'], self.data['containerCode'],res))
        if res:
            logger.info('[{} setDataNodeIdBypodID has node :{}]'.format(self.data['sName'], res[0][0]))
            self.data['desStorageID'] = res[0][0]
            return
        raise Exception('[not frame_id={} error'.format(self.data['containerCode']))


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
            "skuCode": self.data['skuCode'],
            "skuName": self.data['skuName'],
            "lot": "",
            "grade": 0,
            "quantity": self.data['quantity'],
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


    def labalCallBack(self):
        data ={
            "deviceType": 778,
            "deviceSN": self.data['deviceSN'],
            "channel": 0,
            "warehouseID": self.data['warehouseID'],
            "type": "callback",
            "msgMode": 0,
            "msgSeq": 305496504368365571,
            "params": json.dumps({"content":"","pressAction":"confirm","tagID":self.data['tagID'],"warehouseID":self.data['warehouseID']}),
            "deviceMode": 0
        }
        logger.info(data)
        data = f'data={json.dumps(data)}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = '{}/processflowengine/api/label/callback'.format(CONF['baseUrl'])
        res = RequestApi.sendReuest('labalCallBack', 'POST', url, data, headers=headers,postType=2).json()
        logger.info('[{} labalCallBack: res:{}]'.format(self.data['sName'],res))
        if res.get(self.data['returnCode'],None) == 0:
            return True
        return False

    def registerPod(self, barCode):
        url='{}/sim-conveyor/api/registerPod'.format(CONF['baseUrl'])
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data=f'barCode={barCode}&lineID=line_1&pos=0&conveyorID=con_1'
        res = RequestApi.sendReuest('registerPod', 'POST', url, data, headers=headers, postType=2).json()
        logger.info('[{} registerPod: res:{}]'.format(self.data['sName'], res))
        if res.get(self.data['returnCode'], None) == 0:
            return True
        return False

    def getBoxCodeFromAssignmentdata(self, show='container_code'):
        result = []
        sql = "select {} from assignmentdata.container_relation where p_container_code={} LIMIT {};".format(show, self.data['containerCode'],self.data['quantity'])
        self.db.get_connection('assignmentdata')
        res = self.db.execute('assignmentdata', sql)
        logger.info(
            '[{} getBoxCodeFromAssignmentdata containerCode {}  res:{} ]'.format(self.data['sName'], self.data['containerCode'],
                                                                      res))
        if res:
            result = [i[0] for i in res]
        if result:
            logger.info('[{} getBoxCodeFromAssignmentdata has ok :{}]'.format(self.data['sName'], result))

        if len(result) < self.data['quantity']:
            raise Exception('[{} getBoxCodeFromAssignmentdata result:{} < qty:{}]'.format(self.data['sName'], result,
                                                                                          self.data['quantity']))
        return result


    def checkShelfIsArrive(self):
        while True:
            sql = 'select * from tes.frame where frame_id=\'{}\' and status=1 and node=\'{}\''.format(self.data['containerCode'],self.data['endNodeId'])
            self.db.get_connection('tes')
            res = self.db.execute('tes', sql)
            logger.info('[{} checkShelfIsArrive containerCode {}  res:{} ]'.format(self.data['sName'],self.data['containerCode'], res))
            if res:
                logger.info('[{} checkShelfIsArrive has ok :{}]'.format(self.data['sName'],res))
                return True
            time.sleep(CONF['delay'])

    def checkAndLetPass(self):
        while True:
            sql = 'select * from frworkstation.ps_pick where from_container_code=\'{}\' and status=3'.format(self.data['containerCode'])
            self.db.get_connection('frworkstation')
            res = self.db.execute('frworkstation', sql)
            logger.info('[{} checkAndLetPass containerCode {}  res:{} ]'.format(self.data['sName'],self.data['containerCode'], res))
            if res:
                logger.info('[{} checkAndLetPass has ok :{}]'.format(self.data['sName'],res))
                return True
            time.sleep(CONF['delay'])

    def singleProcess(self):
        endFlag = str(round(time.time() * 1000000))[-9:-3]
        containerCodeList = []
        assData = []
        self.setDataNodeIdBypodID()
        if self.data.get('isNeedAssignAndStock',False):
            self.common.tearDownStockAndAssignTables(self.db,self.data,defaultdbs=['assignSql','stockSql','wes'])
            assData = Cfg.getLimtDataFromFile(os.path.join(os.path.abspath('config'), 'skuStock.csv'), self.data['quantity'])
            logger.info('[codes:{}]'.format(assData))
            for row in assData:
                row['containercode'] = row['containercode'] + endFlag
                self.common.setUpStockAndAssignTables(row,self.data,self.db)
                self.common.deleteContainter(self.data,row,containerType=1)
                self.common.addContainer(self.data, row,containerType=1)
            self.common.deleteContainter(self.data, assData[1], containerType=3)
            self.common.addContainer(self.data,assData[1],containerType=3)
            self.common.setUpStockAndAssignTables2(assData[1],self.data,self.db)
        if self.addWorkOrder():
            logger.info('[{} addWorkOrder succ]'.format(self.data['sName']))
            time.sleep(CONF['delay'])
            if self.creatAggs():
                logger.info('[{}creatAggs succ]'.format(self.data['sName']))
                time.sleep(CONF['delay'])
                self.triggerBcr()
                time.sleep(CONF['delay'])
                if self.checkShelfIsArrive():
                    for i in range(self.data['quantity']):
                        logger.info('[i: {}]'.format(i))
                        if not self.labalCallBack():
                            self.statusCode = 405
                            raise Exception('[labalCallBack error]')
                        time.sleep(CONF['delay'])
                    containerCodeList = self.getBoxCodeFromAssignmentdata()
                    for barCode in containerCodeList:
                        logger.info('[barCode: {}]'.format(barCode))
                        if not self.registerPod(barCode):
                            self.statusCode =406
                            raise Exception('[registerPod error]')
                        time.sleep(CONF['delay'])
                    if self.checkAndLetPass():
                        if not self.labalCallBack():
                            self.statusCode = 407
                            raise Exception('[goback labalCallBack error]')
                        time.sleep(CONF['delay'])
                        # self.checkAggOpStatus()
                        # self.checkBound()
                else:
                    self.statusCode = 404
            else:
                self.statusCode = 403
        else:
            self.statusCode = 402
        taskid = self.common.addMovePodTask(self.data)
        if not taskid:
            self.statusCode = 408
            raise Exception('[goback addMovePodTask error]')
        self.common.getTaskDetail(self.data,taskid)
        #self.common.ifEndPointHasBox(self.data, containerCodeList)
        if self.data.get('isNeedAssignAndStock',False):
            self.common.tearDownStockAndAssignTables(self.db, self.data,
                                                     defaultdbs=['assignSql', 'stockSql', 'wes'])
            # assData = Cfg.getLimtDataFromFile(os.path.join(os.path.abspath('config'), 'skuStock.csv'),
            #                                   self.data['quantity'])
            # logger.info('[codes:{}]'.format(assData))
            for row in assData:
                self.common.deleteContainter(self.data, row, containerType=1)
            self.common.deleteContainter(self.data, assData[1], containerType=3)
        return self.data['containerCode']
