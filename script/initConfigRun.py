#encoding=utf-8
import os,csv,json
import time
from script import cfg
from string import Template
from script.commonClass import CommonClass
class configCreater():
    @staticmethod
    def importMapByUrl(warehouseID, url_base,file_cfg_path,fileName):
        #步骤： 上传地图
        md5,fileURL,weburl= CommonClass.upload(url_base=url_base,file=file_cfg_path+fileName)
        if fileURL == None:
            exit(1)

        result=CommonClass.importWareserviceByUrl(warehouseID=warehouseID, url_base=url_base, fileURL=fileURL,md5=md5,fileName=fileName)
        if result=='fail':
            exit(1)

        res=CommonClass.importWarebaseByUrl(warehouseID=warehouseID, url_base=url_base, fileURL=fileURL, fileName=fileName)
        if res=='fail':
            exit(1)

    # tes.sql#
    @staticmethod
    def excuteTesSQL(warehouseID,mysqlConn,sqlFile):
        print('>>> 开始执行TES-SQL配置')
        # warehouseID = cfg.BASE_CONFIG_DICT['warehouseID'].strip()
        #获取location.sql的语句
        with open(sqlFile, 'r+') as f:
            sql=f.read().strip()
            tmp = Template(sql)
            safe_substitute = tmp.safe_substitute(warehouseID=warehouseID)
            sql_list =safe_substitute.split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
            ##执行sql语句，使用循环执行sql语句
            mysqlConn.get_connection('tes')
            for sql_item in sql_list:
                results = mysqlConn.execute('tes', sql_item)
                if results is None:
                    print ("执行sql失败！！sql: :"+sql_item)
        print('添加注册托盘线SQL配置完成')

    # stock.sql
    @staticmethod
    def initStock(url_base, warehouseID, warehouseCode,mysqlConn, sqlFile, paramFile):
        # print('[{},{},{},{},{}]\n'.format(warehouseID,mysqlConn,sqlFile,paramFile,removeSql))
        print('>>> WES 库存初始化')
        reader = csv.DictReader(open(paramFile, 'r'))
        for raw in reader:
            # print(raw)
            # ID,region_code,container_code,sku_code,qty,container_type,pallet_model
            regionCode = raw['regionCode'].strip()
            containercode = raw['containercode'].strip()
            skucode = raw['skucode'].strip()
            qty = raw['qty'].strip()
            containertype = raw['containertype'].strip()
            palletmodal = raw['palletmodal'].strip()
            batchid = raw['ID'].strip()
            # 获取location.sql的语句
            with open(sqlFile, 'r+') as f:
                sql = f.read().strip()
                tmp = Template(sql)
                safe_substitute = tmp.safe_substitute(warehouseCode=warehouseCode,regionCode=regionCode,
                                                      containercode=containercode, skucode=skucode,
                                                      qty=qty, containertype=containertype, palletmodal=palletmodal,lot=batchid
                                                      )
            sql_list = safe_substitute.split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
            ##执行sql语句，使用循环执行sql语句
            mysqlConn.get_connection(sql_list[0])
            new_list = []
            if not regionCode:
                new_list = sql_list[1:3]
            else:
                new_list = sql_list[1:]
            for no, sql_item in enumerate(new_list):
                #print(sql_list[0],sql_item)
                results = mysqlConn.execute(sql_list[0], sql_item)
                if results is None:
                    print("执行sql失败！！sql: :" + sql_item)
                if no == 2:
                    configCreater.wesFollowInit(url_base, warehouseCode, raw)
                    configCreater.wesBindingRFIDandContainer(url_base, warehouseCode, raw)
                    configCreater.wesBindingContainerandTray(url_base, warehouseCode, raw)
        print('WES 库存初始化完成')


    @staticmethod
    def excuteWarebasicSQL(warehouseID,warehouseCode,mysqlConn,sqlFile):
        print('>>> 开始执行Warebasic-SQL配置')
        with open(sqlFile, 'r+') as f:
            sql=f.read().strip()
            tmp = Template(sql)
            safe_substitute = tmp.safe_substitute(warehouseID=warehouseID,warehouseCode=warehouseCode)
            sql_list =safe_substitute.split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
            ##执行sql语句，使用循环执行sql语句
            mysqlConn.get_connection('warebasic')
            for sql_item in sql_list:
                sql_item=sql_item.strip()+';'
                results = mysqlConn.execute('warebasic', sql_item)
                if results is None:
                    print ("执行sql失败！！sql: "+sql_item)
            print('执行Warebasic-SQL配置 完成！')

    def addSubWarehouse_sqlExc(self,mysqlConn,sqlFile,csvFile):
        warehouseID = cfg.BASE_CONFIG_DICT['warehouseID'].strip()
        #获取location.sql的语句
        with open(sqlFile, 'r+') as f:
            sql=f.read().strip()
        #csv配置文件
        reader = csv.DictReader(open(csvFile, 'r'))
        for raw in reader:
            # print(raw)
            subwarehouseID = raw['子仓身份ID'].strip()
            config=raw['配置'].strip()
            name= raw['名称'].strip()
            ext= raw['扩展配置'].strip()
            tmp = Template(sql)
            safe_substitute = tmp.safe_substitute(subwarehouseID=subwarehouseID, name=name,warehouseID=warehouseID,config=config,ext=ext)
            sql_list =safe_substitute.split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
            ##执行sql语句，使用循环执行sql语句
            mysqlConn.get_connection('sunrisewarebase')
            for sql_item in sql_list:
                results = mysqlConn.execute('sunrisewarebase', sql_item)
                if results is None:
                    print ("执行sql失败！！sql: :"+sql_item)
            print('添加子仓配置：'+subwarehouseID)


    #添加提升机
    @staticmethod
    def create_elevator_sim(url_base,warehouseID,file):
        print('>>> 开始注册提升机')

        reader = csv.DictReader(open(file, 'r'))
        for raw in reader:
            # print(raw)
            robotID = int(raw['robotID'].strip())
            deviceConfID = raw['deviceConfID'].strip()
            deviceSN = raw['deviceSN'].strip()
            curZ=int(raw['curZ'].strip())
            mapID=int(raw['mapID'].strip())
            layerCount=int(raw['layerCount'].strip())
            #注册sn
            result =CommonClass.set_warehouse_sn(url_base=url_base,warehouse_id=warehouseID, sn_type=deviceConfID, robot_id=robotID,sn=deviceSN)
            if result == 'fail':
                return
            data={
                "deviceConfID": deviceConfID,
                "deviceSN": deviceSN,
                "curZ": curZ,
                "mapID": mapID,
                "layerCount": layerCount,
            }
            result=CommonClass.sim_create(url_base=url_base,data=data)
            # 判断返回结果
            if result =='fail':
                print('创建失败')
        print('注册提升机机器人完成')

    #添加pshuttle机器人
    @staticmethod
    def create_pshuttle_sim(url_base, warehouseID, file):
        print('>>> 开始注册机器人')
        reader = csv.DictReader(open(file, 'r'))
        for raw in reader:
            # print(raw)
            robotID = raw['robotID'].strip()
            deviceConfID = raw['deviceConfID'].strip()
            deviceSN = raw['deviceSN'].strip()
            curX = raw['curX'].strip()
            curY = raw['curY'].strip()
            curZ = raw['curZ'].strip()
            mapID = raw['mapID'].strip()
            ucPower = raw['ucPower'].strip()

            if ucPower == '':
                ucPower = 100
            #注册sn
            result =CommonClass.set_warehouse_sn(url_base=url_base,warehouse_id=warehouseID, sn_type=deviceConfID, robot_id=robotID,sn=deviceSN)
            if result == 'fail':
                return
            #注册机器人
            data = {
                "deviceConfID": deviceConfID,
                "deviceSN": deviceSN,
                "curX": int(curX),
                "curY": int(curY),
                "curZ": int(curZ),
                "mapID": int(mapID),
                "liftState": 0,
                "ucPower": int(ucPower)
            }
            result = CommonClass.sim_create(url_base=url_base, data=data)
            # 判断返回结果
            if result =='fail':
                print('创建失败')
        print('注册机器人完成')
    #托盘线registerPalletLine
    @staticmethod
    def registerPalletLine(url_base,warehouseID,file):
        print('>>> 开始注册托盘线')
        # print(url_base)
        reader = csv.DictReader(open(file, 'r'))
        for raw in reader:
            # print(raw)
            robotID = int(raw['robotID'].strip())
            deviceConfID = raw['deviceConfID'].strip()
            deviceSN = raw['deviceSN'].strip()
            #注册sn
            result =CommonClass.set_warehouse_sn(url_base=url_base,warehouse_id=warehouseID, sn_type=deviceConfID, robot_id=robotID,sn=deviceSN)
            if result == 'fail':
                return
        print('注册托盘线完成')

    #添加箱线
    @staticmethod
    def registerConveyor(url_base,warehouseID,file):
        print('>>> 开始注册箱线')
        reader = csv.DictReader(open(file, 'r'))
        for raw in reader:
            # print(raw)
            robotID = raw['robotID'].strip()
            deviceType = raw['deviceType'].strip()
            deviceSN = raw['deviceSN'].strip()
            #注册sn
            result =CommonClass.set_warehouse_sn(url_base=url_base,warehouse_id=warehouseID, sn_type=deviceType, robot_id=robotID,sn=deviceSN)
            if result == 'fail':
                return
        print('注册箱线完成')

    #注册非储位货架
    @staticmethod
    def registerFrame(url_base,warehouseID,file):
        print('>>> 注册非储位货架')
        # print(url_base)
        reader = csv.DictReader(open(file, 'r'))
        for raw in reader:
            # print(raw)
            frame_id = raw['frameID'].strip()
            node_id = raw['nodeID'].strip()
            result=CommonClass.register_frame(url_base=url_base,warehouseID=warehouseID,frame_id=frame_id, node_id=node_id)
            # 判断返回结果
            if result == 'fail':
                print('创建失败')
        print('非储位初始化货架')

    #初始化货架
    @staticmethod
    def multiAddPod(url_base,warehouseID,file):
        print('>>>开始初始化货架')
        reader = csv.DictReader(open(file, 'r'))
        podInfo = []
        for raw in reader:
            # print(raw)
            frame_id = raw['frameID'].strip()
            node_id = raw['nodeID'].strip()
            mapID = raw['mapID'].strip()
            podItem={
                     "podID": frame_id,
                     "podType": 12,
                     "posType": 2,
                     "posID": node_id
                     }
            podInfo.append(podItem)
        podInfo=json.dumps(podInfo)
        result=CommonClass.multi_add_pod(url_base=url_base,warehouse_id=warehouseID,pod_info=podInfo)
        # 判断返回结果
        if result == 'fail':
            print('创建失败')
        print('注册托盘线完成')

    #WES追踪初始化
    @staticmethod
    def wesFollowInit(url_base,warehouseCode,data):
        print('>>>WES追踪初始化')
        boxNo = data['containercode'].strip()
        rfid = data['rfid'].strip()
        sku = data['ID'].strip()
        result=CommonClass.wesFollowInit(url_base, boxNo,rfid, sku, warehouseCode)
        # 判断返回结果
        if result == 'fail':
            print('创建失败')
        print('WES追踪初始化完成')

    #绑定 RFID - Container
    @staticmethod
    def wesBindingRFIDandContainer(url_base,warehouseCode,raw):
        print('>>>WES bindingRFIDandContainer')
        containerCode = raw['containercode'].strip()
        rfidList = raw['rfid'].strip()
        result=CommonClass.wesBindingRFIDandContainer(url_base, containerCode,rfidList, warehouseCode)
        # 判断返回结果
        if result == 'fail':
            print('创建失败')
        print('WESbindingRFIDandContainer完成')

    #绑定 Container - 托盘
    @staticmethod
    def wesBindingContainerandTray(url_base,warehouseCode,raw):
        print('>>>WES wesBindingContainerandTray')
        trayContainerCode = raw['trayContainerCode'].strip()
        containerCode = raw['containercode'].strip()
        result=CommonClass.wesBindingContainerandTray(url_base, trayContainerCode,containerCode, warehouseCode)
        # 判断返回结果
        if result == 'fail':
            print('创建失败')
        print('WESwesBindingContainerandTray完成')
    #清除TES数据库
    @staticmethod
    def clearTesData(mysqlConn,sqlFile):
        print('>>>开始清除TES数据库  ... ...')
        # 清数据库的表
        with open(sqlFile, 'r+') as f:
            sql = f.read().strip()
            tmp = Template(sql)
            safe_substitute = tmp.safe_substitute()
            sql_list = safe_substitute.split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
            ##执行sql语句，使用循环执行sql语句
            mysqlConn.get_connection('tes')
            for sql_item in sql_list:
                sql_item = sql_item.strip() + ';'
                results = mysqlConn.execute('tes', sql_item)
                if results is None:
                    print("执行sql失败！！sql: " + sql_item)
        print('清除数据完成')
    #清除WES数据库
    @staticmethod
    def clearWesData(mysqlConn,sqlFile):
        print('>>>开始清除WES数据库  ... ...')
        # 清数据库的表
        with open(sqlFile, 'r+') as f:
            sql = f.read().strip()
            tmp = Template(sql)
            safe_substitute = tmp.safe_substitute()
            sql_list = safe_substitute.split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
            ##执行sql语句，使用循环执行sql语句
            mysqlConn.get_connection('warebasic')
            for sql_item in sql_list:
                sql_item = sql_item.strip() + ';'
                results = mysqlConn.execute('warebasic', sql_item)
                if results is None:
                    print("执行sql失败！！sql: " + sql_item)
        print('清除数据完成')

    #重启服务
    @staticmethod
    def startService(serviceName):

        url_base = cfg.BASE_CONFIG_DICT['ip'].strip()
        rd_platform_host = cfg.BASE_CONFIG_DICT['rd_platform_host'].strip()
        user_email = cfg.BASE_CONFIG_DICT['user_email'].strip()
        CommonClass.startService(url_base, serviceName, rd_platform_host, user_email)

if __name__ == '__main__':


    file_cfg_env='env-base.csv'#环境配置信息
    file_cfg_frame='frame.csv'#货架数据
    file_cfg_pShuttle='pShuttle.csv'#四向穿梭车数据
    file_cfg_channel='elevator.csv'#提升机数据
    file_cfg_path =os.path.dirname(os.path.realpath(__file__))+ '/config/'
    print('file_cfg_path: '+file_cfg_path)
    sql_base_path =os.path.dirname(os.path.realpath(__file__))+ '/sql/'

    #加载基本配置Coifg到缓存
    cfg.load_base_cfg(file_cfg_path + file_cfg_env)
    print('端口号'+ cfg.BASE_CONFIG_DICT.get('mysql_port'))
    # try:
#         #连接mysql连接,默认端口3306
#         mysql_port=3306
#         if cfg.BASE_CONFIG_DICT.get('mysql_port'):
#             mysql_port=cfg.BASE_CONFIG_DICT['mysql_port']
#         mysqlConn = Mysql(cfg.BASE_CONFIG_DICT['mysql_host'], mysql_port, 'root', '1234567890///')
#         #添加整仓ID
#         file_warehouse_sql='warehouse.sql'
#         configCreater().addWarehouse_sqlExc(mysqlConn,sql_cfg_path + file_warehouse_sql)
#         #添加子仓数据到location
#         file_subwarehouse_sql='location.sql'
#         configCreater().addSubWarehouse_sqlExc(mysqlConn,sql_cfg_path + file_subwarehouse_sql,file_cfg_path + file_cfg_subwarehouse)
#     except Exception as e:
#         print('执行sql文件失败：'+e)
#     finally:
#         mysqlConn.disconnect('chatroom')




