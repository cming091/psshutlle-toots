#encoding=utf-8
import requests
import logging
import json,time
from script.utils.rd_platform import RdPlatform
"""
接口调用
"""

class CommonClass():
    # def __init__(self, warehouse_id):
    #     self.warehouseID = warehouse_id

    #清除TES数据库并重启
    @staticmethod
    def init_server_before_test(tesConn, rd_platform):
        print('>>> 清除数据库并重启服务 ... ...')
        # 清数据库的表
        tables = ['robot', 't_navi', 't_navi_avoid', 't_navi_loop', 'session', 'task', 'task_dependency',
                  'signal_order', 'step', 'step_dependency', 'command', 'frame', 'warehouse_sn_info']
        for i in tables:
            sql = 'truncate table %s;' % (i)
            result = tesConn.query(sql)

        # 重启redis服务
        res = rd_platform.restart_service('redis')
        assert res == 'succ'

        # 重启tes服务
        res = rd_platform.restart_service('tes')
        assert res == 'succ'

        # 重启sim-device-common服务
        res = rd_platform.restart_service('sim-device-common')
        assert res == 'succ'
    #清除TES数据库
    @staticmethod
    def clearTesData(tesConn):
        print('>>>开始清除数据库  ... ...')
        # 清数据库的表
        tables = ['robot', 't_navi', 't_navi_avoid', 't_navi_loop', 'session', 'task', 'task_dependency',
                  'signal_order', 'step', 'step_dependency', 'command', 'frame', 'warehouse_sn_info']
        for i in tables:
            sql = 'truncate table %s;' % (i)
            result = tesConn.execute('tes',sql)
        # print('清空数据库结果： '+str(result))
        print('清除数据完成')

    #获取warehouseID
    @staticmethod
    def get_warehouse_id(mysqlConn,mapFileName):
        print('>>> 获取warehouseID ... ...')
        warehouse_id=None
        # warehouse_sql = "select warehouse_id from warehouse where file_name = 'shuttleMap-1-hetu1.4.hetu'"
        warehouse_sql = "select warehouse_id from tes.warehouse where status=1 order by update_time desc limit 1"
        mysqlConn.get_connection('tes')
        warehouse_query = mysqlConn.execute('tes',warehouse_sql)
        # print(f"sql: {warehouse_sql}, num of result: {warehouse_query},result:{warehouse_query}")
        if warehouse_query:
            warehouse_id = warehouse_query[0][0]
        return warehouse_id

    # # 初始化机器人和载具
    # @staticmethod
    # def tes_init_robot_frame(common_data, tes,pod_list,):
    #     print('>>> 初始化载具 ... ...')
    #     # 初始化载具
    #     if len(pod_list)==0:
    #         pod_list = [
    #             "1001", "1002", "1003",
    #         ]
    #     sql = 'select node_id from node where x=0 and map_id=1 and y between 2000 and 4000;'
    #     result = tes.query(sql)
    #     pos_list = []
    #     for i in result:
    #         r = i['node_id']
    #         pos_list.append(r)
    #
    #     pod_info = []
    #     for podID, posID in zip(pod_list, pos_list):
    #         podInfo = {"podID": podID, "posID": posID, "podType": 12, "posType": 2}
    #         # print("========", podInfo)
    #         pod_info.append(podInfo)
    #
    #     res = CommonClass.multi_add_pod(common_data['warehouseID'], json.dumps(pod_info))
    #     assert res == 'succ'
    #     res = CommonClass.all_resume_robots(common_data['warehouseID'])
    #     assert res == 'succ'
    #
    #     print('>>> 初始化sn ... ...')
    #     robot_list = [
    #         "1", "2", "3", "4", "5"
    #     ]
    #     sn_type = '12'
    #     for robot in robot_list:
    #         res = CommonClass.set_warehouse_sn(common_data['warehouseID'], sn_type, robot, robot)
    #         assert res == 'succ'
    #     # 添加提升机sn(warehouse_id, sn_type, robot_id, sn)
    #     res_elevator = CommonClass.set_warehouse_sn(common_data['warehouseID'], 262, 10, 'elevator001')
    #
    #     # 创建机器人
    #     data = {"simList": []}
    #     curX_list = [
    #         0, 0, 0, 3000, 3000
    #     ]
    #     curY_list = [
    #         2000, 3000, 4000, 0, 0
    #     ]
    #     curZ_list = [
    #         1, 1, 1, 2, 3,
    #     ]
    #     mapID_list = [
    #         1, 1, 1, 2, 3,
    #     ]
    #     ucPower_list = [
    #         80, 80, 80, 80, 80
    #     ]
    #     for robot, curX, curY, curZ, mapID, power in zip(robot_list, curX_list, curY_list, curZ_list, mapID_list,
    #                                                      ucPower_list):
    #         simlist = {"deviceConfID": "12", "deviceSN": str(robot), "curX": curX, "curY": curY, "curZ": curZ,
    #                    "mapID": mapID,
    #                    "ucPower": power, "liftState": 0}
    #         data['simList'].append(simlist)
    #     print('>>> 创建机器人 ... ...')
    #     res = sim.batch_create(data=json.dumps(data))
    #     assert res == 'succ'
    #
    #     # 创建提升机
    #     print('>>> 创建提升机 ... ...')
    #     data = {
    #         "simList": [{
    #             "deviceConfID": "262",
    #             "deviceSN": "elevator001",
    #             "mapID": 10,
    #             "curZ": 1,
    #             "layerCount": 3
    #         }]
    #     }
    #     res1 = sim.batch_create(data=json.dumps(data))
    #     # 全部运行机器人
    #     time.sleep(5)  # 等20秒机器人成功创建
    #     res = CommonClass.all_resume_robots(common_data['warehouseID'])
    #     assert res == 'succ'




    #货架初始化接口
    @staticmethod
    def multi_add_pod(url_base,warehouse_id, pod_info):
        url = url_base+ '/tes/apiv2/multiAddPod'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'warehouseID={warehouse_id}&podInfo={pod_info}'
        # data={
        #     "warehouseID":warehouse_id,
        #     "podInfo":pod_info
        # }
        result = 'fail'
        try:
            r = requests.post(url=url, data=data, headers=headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                else:
                    logging.error(f'multi add pod error, {res_data}')
            else:
                logging.error(f'multi add pod error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'multi add pod error, {e}')
        return result
    # resume robots
    @staticmethod
    def all_resume_robots(url_base,warehouse_id):
        url =url_base + '/tes/apiv2/resumeRobots'
        result = 'fail'
        try:
            data = {
                'warehouseID': warehouse_id,
                'all': 1
            }
            r = requests.post(url=url, data=data)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'all_resume_robots success, {res_data}')
                else:
                    logging.error(f'all_resume_robots error, {res_data}')
            else:
                logging.error(f'all_resume_robots, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'all_resume_robots, {e}')
        return result

    #
    @staticmethod
    def set_warehouse_sn(url_base,warehouse_id, sn_type, robot_id, sn):
        url = url_base + '/tes/api/warehouse/setWarehouseSNInfo'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'warehouseID={str(warehouse_id)}&snType={str(sn_type)}&robotID={str(robot_id)}&sn={str(sn)}'
        result = 'fail'
        try:
            r = requests.post(url=url, data=data, headers=headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'set warehouse sn success, {res_data}')
                else:
                    logging.error(f'set warehouse sn error, {res_data}')
            else:
                logging.error(f'set warehouse sn error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'set warehouse sn error, {e}')
        return result
    #添加sn
    @staticmethod
    def set_warehouse_sn(url_base,warehouse_id, sn_type, robot_id, sn):
        url =url_base + '/tes/api/warehouse/setWarehouseSNInfo'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'warehouseID={str(warehouse_id)}&snType={str(sn_type)}&robotID={str(robot_id)}&sn={str(sn)}'
        result = 'fail'
        try:
            r = requests.post(url=url, data=data, headers=headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'set warehouse sn success, {res_data}')
                else:
                    logging.error(f'set warehouse sn error, {res_data}')
            else:
                logging.error(f'set warehouse sn error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'set warehouse sn error, {e}')
        return result
    # 创建机器人
    @staticmethod
    def sim_create(url_base, data):
        url =url_base + '/sim-device-common/sim/create'
        # print(url)
        headers={'Content-Type': 'application/json'}
        data=json.dumps(data)

        result = 'fail'
        try:
            r = requests.post(url=url, data=data, headers=headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                else:
                    logging.error(f'simulator batch_create error, {res_data}')
            else:
                logging.error(f'simulator batch_create error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'simulator batch_create error, {e}')
        return result

     #批量创建机器人
    @staticmethod
    # 创建机器人
    def batch_create(url_base, data):
        url = url_base + '/sim/batchCreate'
        # print(url)
        headers={'Content-Type': 'application/json'}
        result = 'fail'
        try:
            r = requests.post(url=url, data=data, headers=headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                else:
                    logging.error(f'simulator batch_create error, {res_data}')
            else:
                logging.error(f'simulator batch_create error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'simulator batch_create error, {e}')
        return result

    #给定托盘一个当前位置
    @staticmethod
    def register_frame(url_base,warehouseID,frame_id, node_id):
        url = url_base + '/tes/api/frame/registerFrame'
        req_body = {
            "warehouseID":warehouseID,
            "frameID": frame_id,
            "nodeID": node_id,
            "dir": 1
        }
        res = requests.post(url, req_body)
        resp_data = res.json()
        # print(f"url: {url}, data: {req_body}, res: {resp_data}")
        return resp_data
    # @staticmethod
    # def rd_platform(url_base,rd_platform_host,user_email):
    #     return ps_rd_platform
    #重启服务
    @staticmethod
    def startService(url_base,serviceName,rd_platform_host,user_email):
        # 重启sim-device-common服务
        rd_platform = RdPlatform(url_base,rd_platform_host,user_email)
        res = rd_platform.restart_service(serviceName)

        assert res == 'succ'

    #注册warehouseID
    @staticmethod
    def register(url_base):
        res='fail'
        warehouseID=None
        url =url_base + '/tes/api/warehouse/register'
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
        # register={}
        data={"warehouseName":"仓库名称","userID":"6602126394707326280","length":100,"width":100,"hetuVersion":"hetu1.4.3"}

        try:
            r = requests.post(url=url, data=data, headers=headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    res = 'succ'
                    if res_data['data']:
                        warehouseID =res_data['data']['warehouseID']
                else:
                    logging.error(f'simulator batch_create error, {res_data}')
            else:
                logging.error(f'simulator batch_create error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'simulator batch_create error, {e}')
        return res, warehouseID
    #获取整仓ID
    @staticmethod
    def getWarehouseDetail(url_base):
        url =url_base + '/ui-manager/monitor/area/getWarehouseDetail'
        headers={'Content-Type': 'application/json'}
        data={"lang":"zh-CN"}
        result='fail'
        warehouseID = None
        try:
            r = requests.post(url=url, data=data, headers=headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    if res_data['data']:
                        warehouseID =res_data['data']['warehouseID']
                else:
                    logging.error(f'simulator batch_create error, {res_data}')
            else:
                logging.error(f'simulator batch_create error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'simulator batch_create error, {e}')
        return result, warehouseID
    #wareservice地图导入
    @staticmethod
    def importWareserviceByUrl(warehouseID,url_base,fileURL,md5,fileName):
        url = url_base + '/tes/api/warehouse/importByURL'
        result = 'fail'
        try:
            data = {
                'clearNodeTypeIndex': 1,
                'clearAllFrame': 1,
                'clearNodeTypeInsulate': 1,
                'md5': md5,
                'fileName': fileName,
                'fileURL': fileURL,
                'importType': 'COVER',
                'userName': 'admin',
                'warehouseID': warehouseID
            }
            r = requests.post(url=url, data=data)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'import wareservice success, {res_data}')
                else:
                    logging.error(f'import wareservice error, {res_data}')
            else:
                logging.error(f'import wareservice error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'import wareservice error, {e}')
        return result
    @staticmethod
    def importWarebaseByUrl(url_base,fileName, fileURL, warehouseID):
        url =url_base + '/warebase/api/warehouse/initWarehouseByUrl'
        result = 'fail'
        try:
            data = {
                'warehouseName': fileName,
                'fileURL': fileURL,
                'warehouseID': warehouseID
            }
            r = requests.post(url=url, data=data)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'import warebase success, {res_data}')
                else:
                    logging.error(f'import warebase error, {res_data}')
            else:
                logging.error(f'import warebase error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'import warebase error, {e}')
        return result

    #上传地图
    @staticmethod
    def upload(url_base,file):
        url = url_base + ':81'+'/upload'
        print(f"map file path: {file}")
        fileURL = None
        md5=None
        weburl=None
        try:
            data = {'house': open(file, 'rb')}
            r = requests.post(url=url, files=data)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    if res_data['data']:
                        md5 =res_data['data']['md5']
                        fileURL =res_data['data']['url']
                        weburl =res_data['data']['weburl']

                    logging.info(f'upload map success, {res_data}')
                else:
                    logging.error(f'import map error, {res_data}')
            else:
                logging.error(f'import map error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'import map error, {e}')
        return md5,fileURL,weburl



    @staticmethod
    def wesFollowInit(url_base,boxNo, rfid, sku, warehouseNo):
        url =url_base + '/assignmentdata/api/assignmentData/receive'
        result = 'fail'
        try:
            data = {
                'boxNo': boxNo,
                'rfid': rfid,
                'sku': sku,
                'updateFlg': 1,
                'updateDate':'2020-01-01 00:00:00',
                'warehouseNo':warehouseNo,
            }
            print('[url:{} data:{}]'.format(url,data))
            r = requests.post(url=url, data=data)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'wesFollowInit success, {res_data}')
                else:
                    logging.error(f'wesFollowInit error, {res_data}')
            else:
                logging.error(f'wesFollowInit, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'wesFollowInit error, {e}')
        return result

    @staticmethod
    def wesBindingRFIDandContainer(url_base, containerCode,rfidList, warehouseCode):
        url =url_base + '/assignmentdata/api/assignmentData/upload'
        result = 'fail'
        try:
            data = {
                'containerCode': containerCode,
                'rfidList': rfidList,
                'warehouseCode': warehouseCode,
            }
            print('[url:{} data:{}]'.format(url,data))
            r = requests.post(url=url, data=data)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'wesBindingRFIDandContainer success, {res_data}')
                else:
                    logging.error(f'wesBindingRFIDandContainer error, {res_data}')
            else:
                logging.error(f'wesBindingRFIDandContainer, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'wesBindingRFIDandContainer error, {e}')
        return result

    @staticmethod
    def wesBindingContainerandTray(url_base, trayContainerCode, containerCode, warehouseCode):
        url = url_base + '/assignmentdata/api/assignmentData/stacking'
        result = 'fail'
        try:
            data = {
                'containerCode': containerCode,
                'trayContainerCode': trayContainerCode,
                'warehouseCode': warehouseCode,
            }
            print('[url:{} data:{}]'.format(url,data))
            r = requests.post(url=url, data=data)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = 'succ'
                    logging.info(f'wesBindingContainerandTray success, {res_data}')
                else:
                    logging.error(f'wesBindingContainerandTray error, {res_data}')
            else:
                logging.error(f'wesBindingContainerandTray, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'wesBindingContainerandTray error, {e}')
        return result