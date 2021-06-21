import requests
import json
from string import Template
import time
from config import CONF
from utils import *
from psgrpc import *
logger = LogHandler(__name__)


class Common():
    db = Mysql(*(CONF['mysqlUrl'].split(';')))
    setUp = {'stockSql':"""stock*INSERT INTO container_stock (warehouse_code, region_code, container_code, sku_code, container_type, pallet_model, lot, grade, qty, abnormal_qty, reserved_qty, create_by, create_at, update_at, version, delete_flag)
            VALUES('${warehouseCode}','${regionCode}','${containercode}', '${skucode}', '${containertype}', '${palletmodal}', 0, 0, '${qty}', 0, 0, 'test', NOW(), NOW(), 1, 0);*
            INSERT INTO container_relation(warehouse_code,region_code,container_code,create_by,create_at,update_at,delete_flag)
            VALUES('${warehouseCode}', '${regionCode}', '${containercode}','test', NOW(), NOW(), 0);*
            INSERT region_stock (warehouse_code,region_code,sku_code,qty,abnormal_qty,reserved_qty,create_by,create_at,update_at,version,delete_flag,lot)
            VALUES('${warehouseCode}', '${regionCode}', '${skucode}' , '${qty}', 0, 0, 'test', NOW(), NOW(), 1, 0,'${lot}');  """,
             'stockSql2':"""stock*INSERT INTO container_stock (warehouse_code, region_code, container_code, sku_code, container_type, pallet_model, lot, grade, qty, abnormal_qty, reserved_qty, create_by, create_at, update_at, version, delete_flag)
            VALUES('${warehouseCode}','${regionCode}','${containercode}', '${skucode}', '${containertype}', '${palletmodal}','${lot}', 0, '${qty}', 0, 0, 'test', NOW(), NOW(), 1, 0);*
            INSERT INTO container_relation(warehouse_code,region_code,container_code,create_by,create_at,update_at,delete_flag)
            VALUES('${warehouseCode}', '${regionCode}', '${containercode}','test', NOW(), NOW(), 0);"""}

    tearDown = {
        'stockSql': "stock*delete from container_stock where create_by=\'test\';*delete from container_relation where create_by=\'test\';*delete from region_stock where create_by=\'test\';",
        'assignSql': "assignmentdata*delete from assignment_data;*delete from container_relation;*delete from container_rfid_relation;",
        'wes': """invtransaction*truncate table invtransaction.wo4ib;*truncate table invtransaction.wo4ob;*truncate table invtransaction.wo_rely;*truncate table invtransaction.wo_index;*truncate table process_flow_engine.action_aggregation;*
                            truncate table process_flow_engine.work_order;*truncate table process_flow_engine.work_order_action;*truncate table process_flow_engine.container_context;*
                            truncate table frworkstation.ps_inbound;*truncate table frworkstation.ps_pick;*truncate table frworkstation.ps_pick_station;*truncate table frworkstation.ps_pick_result;*truncate table invtransaction.wo4transfer;*truncate table invtransaction.wo4exchange;""",
        'wes_pick':"""invtransaction*delete from invtransaction.wo4ib where container_code='$containerCode';*delete from invtransaction.wo4ob where container_code='$containerCode';*delete from invtransaction.wo_rely where 1=1;*delete from invtransaction.wo_index where container_code='$containerCode';*delete from process_flow_engine.action_aggregation where container_code='$containerCode';*
                            delete from process_flow_engine.work_order where container_code='$containerCode';*delete from process_flow_engine.container_context where container_code='$containerCode';*
                            delete from frworkstation.ps_inbound where container_code='$containerCode';*delete from frworkstation.ps_pick where from_container_code='$containerCode';*delete from frworkstation.ps_pick_station where 1=1;*delete from frworkstation.ps_pick_result where 1=1;*delete from invtransaction.wo4transfer where container_code='$containerCode';*delete from invtransaction.wo4exchange where from_container_code='$containerCode';""",
        'wes_nopick':"""invtransaction*delete from invtransaction.wo4ib where container_code='$containerCode';*delete from invtransaction.wo4ob where container_code='$containerCode';*delete from invtransaction.wo_rely where 1=1;*delete from invtransaction.wo_index where container_code='$containerCode';*delete from process_flow_engine.action_aggregation where container_code='$containerCode';*
                            delete from process_flow_engine.work_order where container_code='$containerCode';*delete from process_flow_engine.container_context where container_code='$containerCode';*
                            delete from frworkstation.ps_inbound where container_code='$containerCode';*delete from invtransaction.wo4transfer where container_code='$containerCode';*delete from invtransaction.wo4exchange where from_container_code='$containerCode';""",
        }

    @staticmethod
    def openSession(configData):
        url="{}/tes/apiv2/openSession".format(CONF['baseUrl'])
        data = {
            'warehouseID': configData['warehouseID'],
            'requestID': str(round(time.time() * 1000000)),
            'clientCode':'SUPER'
        }
        res = RequestApi.sendReuest('openSession', 'POST', url, data, postType=2).json()
        logger.info('[{} openSession: res:{}]'.format(configData['sName'], res))
        if res.get(configData['returnCode'], None) == 0:
            return res['data']['sessionID']
        return ''



   #desType： 默认=2 储位  3 zone
    @staticmethod
    def addMovePodTask(configData, clientCode='SUPER', desType=2, desZoneID=''):
        url="{}/tes/apiv2/addMovePodTask".format(CONF['baseUrl'])
        sessionID = Common.openSession(configData)
        if not sessionID:
            logger.error('[openSession is null]')
            raise Exception('[openSession is null error]')
        data = {
            'warehouseID': configData['warehouseID'],
            'requestID': str(round(time.time() * 1000000)),
            'clientCode': clientCode,
            'podID': configData['containerCode'],
            'sessionID': sessionID,
            'priority': 3,
            'srcType': 1,
            'extParams': json.dumps({"unload": 1, "carryMode": 1}),
            'desType': desType,
            'desStorageID': configData['desStorageID']
           # 'desZoneID': desZoneID
        }
        res = RequestApi.sendReuest('addMovePodTask', 'POST', url, data, postType=2).json()
        logger.info('[{} addMovePodTask: res:{}]'.format(configData['sName'], res))
        if res.get(configData['returnCode'], None) == 0:
            return res['data']['taskID']
        return ''

    @staticmethod
    def assignFollowInit(row, configData):
        url = '{}/assignmentdata/api/assignmentData/receive'.format(CONF['baseUrl'])
        data = {
            'boxNo': row.get('containercode',' ').strip(),
            'rfid': row.get('rfid',' ').strip(),
            'sku': row.get('skucode',' ').strip(),
            'updateFlg': 1,
            'updateDate': '2020-01-01 00:00:00',
            'warehouseNo': configData['warehouseCode'],
        }
        res = RequestApi.sendReuest('assignFollowInit', 'POST', url, data, postType=2).json()
        logger.info('[{} assignFollowInit: res:{}]'.format(configData['sName'], res))
        if res.get(configData['returnCode'], None) == 0:
            return True
        return False

    @staticmethod
    def assigBindingRFIDandContainer(row, configData):
        url = '{}/assignmentdata/api/assignmentData/upload'.format(CONF['baseUrl'])
        data = {
            'containerCode': row.get('containercode',' ').strip(),
            'rfidList': row.get('rfid',' ').strip(),
            'warehouseCode': configData['warehouseCode'],
        }
        res = RequestApi.sendReuest('assigBindingRFIDandContainer', 'POST', url, data, postType=2).json()
        logger.info('[{} assigBindingRFIDandContainer: res:{}]'.format(configData['sName'], res))
        if res.get(configData['returnCode'], None) == 0:
            return True
        return False

    @staticmethod
    def assignBindingContainerandTray(row, configData):
        url = '{}/assignmentdata/api/assignmentData/stacking'.format(CONF['baseUrl'])
        data = {
            'containerCode': row.get('containercode',' ').strip(),
            'trayContainerCode': configData['containerCode'],
            'warehouseCode': configData['warehouseCode'],
        }
        res = RequestApi.sendReuest('assignBindingContainerandTray', 'POST', url, data, postType=2).json()
        logger.info('[{} assignBindingContainerandTray: res:{}]'.format(configData['sName'], res))
        if res.get(configData['returnCode'], None) == 0:
            return True
        return False


    @staticmethod
    def setUpStockAndAssignTables2(row, configData, mysqlConn):
        stockSqlTemp2 = Template(Common.setUp['stockSql2'])
        stockSql2 = stockSqlTemp2.safe_substitute(warehouseCode=configData['warehouseCode'],
                                                  regionCode=row['regionCode'].strip(),
                                                  containercode=configData['containerCode'],
                                                  skucode=row['skucode'].strip(),
                                                  qty=configData['iqty'], containertype=row['containertype'].strip(),
                                                  palletmodal=row['palletmodal'].strip(),lot='')
        sqlList2 = stockSql2.split('*')
        mysqlConn.get_connection(sqlList2[0])
        for sql in sqlList2[1:]:
            logger.info('[sql:{} ]'.format(sql))
            try:
                results = mysqlConn.execute(sqlList2[0], sql)
                if results is None:
                    logger.error("setUpStockAndAssignTables tuopan:{}".format(sql))
                else:
                    logger.info('[setUpStockAndAssignTables sql tuopan:{} ok]'.format(sql))
            except Exception as e:
                logger.exception(e)


    @staticmethod
    def setUpStockAndAssignTables(row, configData, mysqlConn):
        row['qty'] = configData['quantity']
        stockSqlTemp = Template(Common.setUp['stockSql'])
        stockSql = stockSqlTemp.safe_substitute(warehouseCode=configData['warehouseCode'], regionCode=row['regionCode'].strip(),
                                              containercode=row['containercode'].strip(), skucode=row['skucode'].strip(),
                                              qty=row['qty'], containertype=row['containertype'].strip(),
                                              palletmodal= row['palletmodal'].strip(), lot= row['ID'].strip())
        sqlList = stockSql.split('*')
        mysqlConn.get_connection(sqlList[0])
        newSqlList = []
        if not row['regionCode']:
            newSqlList = sqlList[1:3]
        else:
            newSqlList = sqlList[1:]
        for no, sql in enumerate(newSqlList):
            # logger.info('[sql:{}]'.format(sql))
            # try:
            #     results = mysqlConn.execute(sqlList[0], sql)
            #     if results is None:
            #         logger.error("setUpStockAndAssignTables:{}".format(sql))
            #     else:
            #         logger.info('[setUpStockAndAssignTables sql:{} ok]'.format(sql))
            # except Exception as e:
            #     logger.exception(e)
            if no == 2:
                Common.assignFollowInit(row,configData)
                Common.assigBindingRFIDandContainer(row,configData)
                Common.assignBindingContainerandTray(row,configData)

    @staticmethod
    def tearDownStockAndAssignTables(mysqlConn, configData,defaultdbs=['assignSql','stockSql']):
        containerCode = configData['containerCode']
        for db in defaultdbs:
            stockSql = Common.tearDown[db].replace("'$containerCode'",containerCode)
            logger.info('[tearDownStockAndAssignTables sql:{} ]'.format(stockSql))
            sqlList = stockSql.split('*')
            mysqlConn.get_connection(sqlList[0])
            for sql in sqlList[1:]:
                logger.info('[sql:{}]'.format(sql))
                results = mysqlConn.execute(sqlList[0], sql)
                if results is None:
                    logger.error("tearDownStockAndAssignTables:{}".format(sql))
                else:
                    logger.info('[tearDownStockAndAssignTables sql:{} ok]'.format(sql))


    @staticmethod
    def getTaskDetail(configData, taskID):
        url = '{}/tes/apiv2/getTaskDetail'.format(CONF['baseUrl'])
        while True:
            data = {
                'warehouseID': configData['warehouseID'],
                'requestID': str(int(time.time())),
                'requestTime': '',
                'clientCode': 'biz_test',
                'tokenCode': '',
                'taskID': taskID,
                'requestTime': '',
            }
            res = RequestApi.sendReuest('getTaskDetail', 'POST', url, data, postType=2).json()
            logger.info('[{} getTaskDetail: res:{}]'.format(configData['sName'], res))
            if res.get(configData['returnCode'], None) == 0:
                if res['data']['detail']['status'] == 4:
                    return True
                elif res['data']['detail']['status'] == 5:
                    time.sleep(30)
                    return False
            time.sleep(2)


    @staticmethod
    def getWarehouseId():
        warehouseId = ''
        sql = "select warehouse_id from tes.warehouse where status=1 order by update_time desc limit 1"
        Common.db.get_connection('tes')
        res = Common.db.execute('tes', sql)
        if res:
            logger.info('[{} tes has WarehouseId:{}]'.format('Common',res[0][0]))
            warehouseId = res[0][0]
        return warehouseId

    @staticmethod
    def getPodList(mapID=1):
        podList=[]
        url = '{}/tes/apiv2/getPodList'.format(CONF['baseUrl'])
        warehouseId = Common.getWarehouseId()
        if not warehouseId:
            raise Exception('[NO warehouseId]')
        data = {
            'warehouseID': warehouseId
        }
        res = RequestApi.sendReuest('getPodList', 'POST', url, data, postType=2).json()
        logger.info('[{} getPodList: res:{}]'.format('Common', res))
        if res.get('returnCode', None) == 0:
            podList = res['data']['podList']
            if not podList:
                raise Exception('[getPodList no podList]')
            return [pod.get('podID') for pod in podList if pod.get('mapID')==mapID]
        return []

    @staticmethod
    def addContainer(data, row, containerType):
        res = addContainer(data, row, containerType)
        logger.info('[{} addContainer res:{}]\n'.format(data['sName'],res))

    @staticmethod
    def deleteContainter(data, row, containerType):
        res = deleteContainter(data,row,containerType)
        logger.info('[{} deleteContainter res:{}]\n'.format(data['sName'], res))


    @staticmethod
    def conveyorRoll(configData):
        url = '{}/tes/apiv2/conveyor/conveyorRoll'.format(CONF['baseUrl'])
        data = {
            'warehouseID':configData['warehouseID'],
            'zoneID': '309680989251860492',
        }
        res = RequestApi.sendReuest('conveyorRoll', 'POST', url, data, postType=2).json()
        logger.info('[{} conveyorRoll: res:{}]'.format(configData['sName'], res))
        if res.get(configData['returnCode'], None) == 0:
            return True
        return False

    @staticmethod
    def ifEndPointHasBox(configData, containerCodelist):
        # Common.conveyorRoll(configData)
        i = 0
        while i < len(containerCodelist):
            Common.conveyorRoll(configData)
            logger.info('excute conveyorRoll')
            time.sleep(3)
            i += 1




