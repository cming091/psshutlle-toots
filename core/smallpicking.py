import time
import os
from urllib import parse
from .nonsmallpicking import NonSmallPicking
from config import CONF
from utils import *
logger = LogHandler(__name__)

class SmallPicking(NonSmallPicking):
    def __init__(self, data):
        super(SmallPicking,self).__init__(data)

    def registerPod(self, barCode, rfidList):
        url='{}/sim-conveyor/api/registerPod'.format(CONF['baseUrl'])
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data=f'barCode={barCode}&lineID=line_1&pos=0&conveyorID=con_1&rfidList={rfidList}'
        res = RequestApi.sendReuest('registerPod', 'POST', url, data, headers=headers, postType=2).json()
        logger.info('[{} registerPod: res:{}]'.format(self.data['sName'], res))
        if res.get(self.data['returnCode'], None) == 0:
            return True
        return False

    def clearPod(self, barCode):
        url = '{}/sim-conveyor/api/clearPod'.format(CONF['baseUrl'])
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'barCode={barCode}&conveyorID=con_1'
        res = RequestApi.sendReuest('clearPod', 'POST', url, data, headers=headers, postType=2).json()
        logger.info('[{} clearPod: res:{}]'.format(self.data['sName'], res))
        if res.get(self.data['returnCode'], None) == 0:
            return True
        return False


    def getBoxCodeFromAssignmentdata(self, show='container_code'):
        result = []
        sql = "select {} from assignmentdata.container_rfid_relation where container_code={} LIMIT {};".format(show, self.data['containerCode'],self.data['quantity'])
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
        resultSrings = ','.join(result)
        return resultSrings

    def singleProcess(self):
        self.setDataNodeIdBypodID()
        barCode = ''
        if self.data.get('isNeedAssignAndStock',False):
            self.common.tearDownStockAndAssignTables(self.db, self.data,
                                                     defaultdbs=['assignSql', 'stockSql', 'wes'])
            assData,zcodes = Cfg.getLimtDataFromFile(os.path.join(os.path.abspath('config'), 'skuStock.csv'), self.data['quantity'],type='smallPicking')
            barCode = zcodes[0].get('containercode','')
            self.clearPod(barCode)
            logger.info('[codes:{}]'.format(assData))
            for row in assData:
                self.common.setUpStockAndAssignTables(row,self.data,self.db)
                self.common.deleteContainter(self.data, row, containerType=1)
                self.common.addContainer(self.data, row, containerType=1)
            self.common.deleteContainter(self.data, assData[1], containerType=3)
            self.common.addContainer(self.data, assData[1], containerType=3)
            self.common.setUpStockAndAssignTables2(assData[1], self.data, self.db)
            self.common.deleteContainter(self.data, zcodes[0], containerType=2)
            self.common.addContainer(self.data, zcodes[0], containerType=2)
        if self.addWorkOrder():
            logger.info('[{} addWorkOrder succ]'.format(self.data['sName']))
            time.sleep(CONF['delay'])
            if self.creatAggs():
                logger.info('[{}creatAggs succ]'.format(self.data['sName']))
                time.sleep(CONF['delay'])
                self.triggerBcr()
                time.sleep(CONF['delay'])
                if self.checkShelfIsArrive():
                    time.sleep(CONF['delay'])
                    if not self.labalCallBack():
                        self.statusCode = 405
                        raise Exception('[labalCallBack error]')
                        time.sleep(CONF['delay'])
                    rfids = self.getBoxCodeFromAssignmentdata(show='rfid')
                    if rfids:
                        logger.info('[rfids: {}]'.format(rfids))
                        if not self.registerPod(barCode, rfids):
                            self.statusCode =406
                            raise Exception('[registerPod error]')
                        time.sleep(CONF['delay'])
                    else:
                        raise Exception('[getBoxCodeFromAssignmentdata error]')
                        self.statusCode = 407
                    if self.checkAndLetPass():
                        if not self.labalCallBack():
                            self.statusCode = 408
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
        self.common.getTaskDetail(self.data, taskid)
        if self.data.get('isNeedAssignAndStock',False):
            self.common.tearDownStockAndAssignTables(self.db, self.data,
                                                     defaultdbs=['assignSql', 'stockSql', 'wes'])
            assData, zcodes = Cfg.getLimtDataFromFile(os.path.join(os.path.abspath('config'), 'skuStock.csv'),
                                                      self.data['quantity'], type='smallPicking')
            barCode = zcodes[0].get('containercode', '')
            logger.info('[codes:{}]'.format(assData))
            for row in assData:
                self.common.deleteContainter(self.data, row, containerType=1)
            self.common.deleteContainter(self.data, assData[1], containerType=3)
            self.common.deleteContainter(self.data, zcodes[0], containerType=2)
        return self.data['containerCode']
