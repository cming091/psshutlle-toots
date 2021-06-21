#encoding=utf-8
import os,csv,time
import sys
from script import cfg
from script.utils.mysql import Mysql
from script.commonClass import CommonClass
from script.initConfigRun import configCreater
import logging

def main():
    file_cfg_env='base-env.csv'#环境配置信息
    file_cfg_frame='frame.csv'#货架数据
    file_cfg_frameStatoin='frame-station.csv'#入库站点货架
    file_cfg_pShuttle='pShuttle.csv'#四向穿梭车数据
    file_cfg_elevator='elevator.csv'#提升机数据
    file_cfg_conveyor='conveyor.csv'#箱线机器人
    file_cfg_palletLine='palletLine.csv'#
    file_map='xiangxianMap-hetu1.4.hetu'#提升机数据
    file_sqlFile = 'stock.sql'
    file_paramFile = 'skuStock.csv'
    warehouseCode='JY'
    base_path=os.path.dirname(os.path.realpath(__file__))
    # file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', file_name)
    file_cfg_path =base_path+ '/config/'
    sql_base_path =base_path+ '/sql/'
    print('file_cfg_path: '+file_cfg_path)
    print('sql_base_path: '+sql_base_path)
    #加载基本配置Coifg到缓存
    cfg.load_base_cfg(file_cfg_path + file_cfg_env)
    url_base=cfg.BASE_CONFIG_DICT.get('url_base')
    print('端口号'+ cfg.BASE_CONFIG_DICT.get('mysql_port'))
    try:
        #连接mysql连接,默认端口3306
        mysql_port=3306
        if cfg.BASE_CONFIG_DICT.get('mysql_port'):
            mysql_port=cfg.BASE_CONFIG_DICT['mysql_port']
        mysqlConn = Mysql(cfg.BASE_CONFIG_DICT['mysql_host'], mysql_port, 'root', '1234567890///')
        # mysqlConn.get_connection('tes')
        #步骤：获取整仓ID
        warehouseID = CommonClass.get_warehouse_id(mysqlConn, file_map)
        if warehouseID ==None:
            res, warehouseID = CommonClass.register(url_base=url_base)
        time.sleep(1)


        # #步骤： 导入地图
        #configCreater.importMapByUrl(warehouseID=warehouseID,url_base=url_base,file_cfg_path=file_cfg_path,fileName=file_map)


        # 如果需要恢复数据，则清数据库的表
        file_Tes_sql = 'clearTesData.sql'
        configCreater.clearTesData(mysqlConn, sqlFile=sql_base_path + file_Tes_sql)
        file_wes_sql = 'clearWesData.sql'
        configCreater.clearWesData(mysqlConn, sqlFile=sql_base_path + file_wes_sql)
        time.sleep(2)

        # 重启服务
        serviceList=['sim-device-common','sim-conveyor']
        for s in serviceList:
            configCreater.startService(s)
        time.sleep(4)
        print('重启服务完成')

        # 注册机器人
        configCreater.create_pshuttle_sim(warehouseID=warehouseID,url_base=url_base,file=file_cfg_path+file_cfg_pShuttle)


        # 注册提升机机器人
        configCreater.create_elevator_sim(warehouseID=warehouseID,url_base=url_base,file=file_cfg_path+file_cfg_elevator)

        # 注册箱线
        configCreater.registerConveyor(url_base=url_base,warehouseID=warehouseID,file=file_cfg_path+file_cfg_conveyor)

        # 注册托盘线&重启sim-conveyor服务
        configCreater.registerPalletLine(url_base=url_base,warehouseID=warehouseID,file=file_cfg_path+file_cfg_palletLine)

        #添加托盘线的zone信息
        file_tes_sql='tes.sql'
        configCreater.excuteTesSQL(warehouseID=warehouseID,mysqlConn=mysqlConn,sqlFile=sql_base_path + file_tes_sql)

        # 初始化货架
        #configCreater.multiAddPod(url_base=url_base,warehouseID=warehouseID,file=file_cfg_path+file_cfg_frame)

        # 非储位初始化货架
        #configCreater.registerFrame(url_base=url_base,warehouseID=warehouseID,file=file_cfg_path+file_cfg_frameStatoin)
        #WES工艺路线-配置
        file_warebasic_sql='warebasic.sql'
        configCreater.excuteWarebasicSQL(warehouseID=warehouseID,warehouseCode=warehouseCode,mysqlConn=mysqlConn,sqlFile=sql_base_path + file_warebasic_sql)
        #WES-库存和rfid绑定
        #configCreater.initStock(url_base,warehouseID,warehouseCode,mysqlConn,sql_base_path+file_sqlFile, file_cfg_path+file_paramFile)

        #重起相关服务
        serviceList = ['sim-conveyor','tes','frworkstation','invtransaction','pallet_shuttle_algorithm', 'warebasic','processflowengine','wareshuttle']
        for s in serviceList:
            print('[开始{}重启]'.format(s))
            configCreater.startService(s)
            print('[重启{}完成]'.format(s))
            time.sleep(2)
        print('重启服务完成')

    except Exception as e:
        print('执行sql文件失败：'+str(e))
    finally:
        mysqlConn.disconnect(close_all=True)


def testwes():
    warehouseCode='JY'

    file_cfg_env = 'base-env.csv'  # 环境配置信息
    file_cfg_frame = 'frame.csv'  # 货架数据
    file_cfg_frameStatoin = 'frame-station.csv'  # 入库站点货架
    file_cfg_pShuttle = 'pShuttle.csv'  # 四向穿梭车数据
    file_cfg_elevator = 'elevator.csv'  # 提升机数据
    file_cfg_conveyor = 'conveyor.csv'  # 箱线机器人
    file_cfg_palletLine = 'palletLine.csv'  #
    file_map = 'xiangxianMap-hetu1.4.hetu'  # 提升机数据
    file_sqlFile = 'stock.sql'
    file_paramFile = 'skuStock.csv'
    file_wesfollowinit = 'wesfollowinit.csv'
    file_wesbindingrfidandcontainer = 'wesbindingrfidandcontainer.csv'
    file_wesBindingContainerandTray = 'wesbindingcontainerandtray.csv'
    base_path = os.path.dirname(os.path.realpath(__file__))
    # file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', file_name)
    file_cfg_path = base_path + '/config/'
    sql_base_path = base_path + '/sql/'
    print('file_cfg_path: ' + file_cfg_path)
    print('sql_base_path: ' + sql_base_path)
    # 加载基本配置Coifg到缓存
    cfg.load_base_cfg(file_cfg_path + file_cfg_env)
    url_base = cfg.BASE_CONFIG_DICT.get('url_base')
    print('端口号' + cfg.BASE_CONFIG_DICT.get('mysql_port'))
    # 连接mysql连接,默认端口3306
    mysql_port = 3306
    if cfg.BASE_CONFIG_DICT.get('mysql_port'):
        mysql_port = cfg.BASE_CONFIG_DICT['mysql_port']
    mysqlConn = Mysql(cfg.BASE_CONFIG_DICT['mysql_host'], mysql_port, 'root', '1234567890///')
    # 步骤：获取整仓ID
    warehouseID = CommonClass.get_warehouse_id(mysqlConn, file_map)
    if warehouseID == None:
        res, warehouseID = CommonClass.register(url_base=url_base)
    configCreater.initStock(url_base,warehouseID,warehouseCode,mysqlConn,sql_base_path+file_sqlFile, file_cfg_path+file_paramFile)
    # file_tes_sql = 'tes.sql'
    # configCreater.excuteTesSQL(warehouseID='314449700784701462', mysqlConn=mysqlConn, sqlFile=sql_base_path + file_tes_sql)


def registagv():
    file_cfg_env = 'base-env.csv'  # 环境配置信息
    file_cfg_frame = 'frame.csv'  # 货架数据
    file_cfg_frameStatoin = 'frame-station.csv'  # 入库站点货架
    file_cfg_pShuttle = 'pShuttle.csv'  # 四向穿梭车数据
    file_cfg_elevator = 'elevator.csv'  # 提升机数据
    file_cfg_conveyor = 'conveyor.csv'  # 箱线机器人
    file_cfg_palletLine = 'palletLine.csv'  #
    file_map = 'xiangxianMap-hetu1.4.hetu'  # 提升机数据
    file_sqlFile = 'stock.sql'
    file_paramFile = 'skuStock.csv'
    file_wesfollowinit = 'wesfollowinit.csv'
    file_wesbindingrfidandcontainer = 'wesbindingrfidandcontainer.csv'
    file_wesBindingContainerandTray = 'wesbindingcontainerandtray.csv'
    base_path = os.path.dirname(os.path.realpath(__file__))
    # file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'map_data', file_name)
    file_cfg_path = base_path + '/config/'
    sql_base_path = base_path + '/sql/'
    print('file_cfg_path: ' + file_cfg_path)
    print('sql_base_path: ' + sql_base_path)
    # 加载基本配置Coifg到缓存
    cfg.load_base_cfg(file_cfg_path + file_cfg_env)
    url_base = cfg.BASE_CONFIG_DICT.get('url_base')
    configCreater.create_pshuttle_sim(warehouseID='313726586400538653', url_base=url_base,
                                      file=file_cfg_path + file_cfg_pShuttle)

if __name__ == '__main__':
    main()




