# -*- coding: utf-8 -*-
import os,csv
from itertools import islice

BASE_CONFIG_DICT = dict()
WAREHOUSE_CONFIG_DICT = dict()
chatroom_CONFIG_DICT = dict()

def load_base_cfg(file):
    print('base_cfg File: '+file)
    with open(file,'r') as f:
        data = csv.reader(f)
        # headers=data[0]
        # for row in data:
        global BASE_CONFIG_DICT
        for row in islice(data,1,None):
            # print(row)
            key=row[0].strip()
            value=row[1].strip()
            BASE_CONFIG_DICT[key] = value
    # #方式二：有序字段
    # reader = csv.DictReader(open(file,'r'))
    # for raw in reader:
    #     print(raw)

def load_subwaerhouse_cfg(file):
    with open(file,'r') as f:
        data = csv.reader(f)
        # headers=data[0]
        # for row in data:
        global WAREHOUSE_CONFIG_DICT
        # 方式二：有序字段
        reader = csv.DictReader(open(file,'r'))
        for raw in reader:
            print(raw)
            key=raw['名称'].strip()
            print(key)
            WAREHOUSE_CONFIG_DICT[key] = raw
        # for row in islice(data,1,None):
        #     print(row)
        #     key=row[0].strip()
        #     value=row[1].strip()
        #     G_CONFIG_DICT[key] = value

def load_chatroom_cfg(file):
    with open(file, 'r') as f:
        data = csv.reader(f)
        # headers=data[0]
        # for row in data:
        global WAREHOUSE_CONFIG_DICT
        # 方式二：有序字段
        reader = csv.DictReader(open(file, 'r'))
        for raw in reader:
            print(raw)
            key = raw['聊天室Topic'].strip()
            print(key)
            chatroom_CONFIG_DICT[key] = raw
                # for row in islice(data,1,None):
                #     print(row)
                #     key=row[0].strip()
                #     value=row[1].strip()
                #     G_CONFIG_DICT[key] = value



if __name__ == '__main__':
    pass
    # file_cfg_env='基本配置.csv'#cfg_env.csv
    # file_cfg_subwarehouse='子仓划分配置.csv'#cfg_subwarehouse
    # file_cfg_chatRoom='聊天室划分配置.csv'#cfg_chatroom.csv
    # file_cfg_channel='聊天室成员(子仓)通道配置 .csv'#cfg_channel.csv
    # file_cfg_path = os.path.dirname(__file__) +os.sep+ 'config'+os.sep
    # # SunriseConfig.load_env_cfg(file_cfg_path+os.sep+file_cfg_env)
    # load_base_cfg(file_cfg_path + file_cfg_env)
    # load_subwaerhouse_cfg(file_cfg_path + file_cfg_subwarehouse)

#




