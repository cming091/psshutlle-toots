import requests
import json
import yaml
import csv
from tenacity import retry, stop_after_attempt
from itertools import islice
import subprocess
from .log import *
logger = LogHandler(__name__)
retry = retry(stop=stop_after_attempt(1))


class RequestApi(object):
    @staticmethod
    @retry
    def sendReuest(name, method, url, data, headers={}, postType=1):
        logger.info('[name:{}\turl:{}\tdata:{}]\n'.format(name,url,data))
        if method=='POST':
            if postType == 1:
                return requests.post(url,json=data, headers=headers)
            elif postType ==2:
                return requests.post(url, data=data, headers=headers)
        else:
            return requests.get(url, headers=headers)


class Cfg(object):
    @staticmethod
    def getOneFieldFromFile(file, field):
        codes = []
        logger.info('[Cfg File:{}]'.format(file))
        with open(file, 'r') as f:
            data = csv.reader(f)
            for row in islice(data, 1, None):
                codes.append(row[field])
        return codes

    @staticmethod
    def getLimtDataFromFile(file,lineNum ,type='nonSmallPicking'):
        logger.info('[file:{} linenumber:{}]'.format(file,lineNum))
        codes = []
        zcodes = []
        reader = csv.DictReader(open(file, 'r'))
        for data in reader:
            codes.append(data)
        if len(codes)<lineNum:
            raise Exception('[file:{} read line number({}) < need number({})]'.format(file,len(codes),lineNum))
        if type=='smallPicking':
            for code in codes:
                if code.get('containertype') == '2':
                    zcodes.append(code)
        newcodes = codes[:lineNum]
        if zcodes:
            newcodes.extend(zcodes)
        if zcodes:
            return newcodes,zcodes
        else:
            return newcodes

    @staticmethod
    def loadConfig(file):
        _config = {}
        with open(file, encoding='utf-8') as f:
            _config = yaml.load(f, Loader=yaml.FullLoader)
        return Cfg.mergeConfig(_config)

    @staticmethod
    def mergeConfig(config):
        config['baseUrl'] = config['baseUrl'].format(config['ip'])
        config['mysqlUrl'] = config['mysqlUrl'].format(config['ip'])
        config['wholein'] = {**config['temp'],**config['wholein']}
        config['wholeout'] = {**config['temp'],**config['wholeout']}
        config['nonSmallPicking'] = {**config['temp'],**config['nonSmallPicking']}
        config['smallPicking'] = {**config['temp'],**config['smallPicking']}
        config.pop('temp')
        return config

class SysUtil(object):

    @staticmethod
    def read(path, mode):
        data = ''
        with open(path, mode) as f:
            data = f.read()
        return data

    @staticmethod
    def write(data, path, mode):
        with open(path,mode) as f:
            data = f.write(data)
        return data

    @staticmethod
    def helpInfo():
        text = """python %prog -m/--mode <select different service input conditions  eg:整托入库 详情查看readme>"""
        return text

    @staticmethod
    def executeCommand(cmd):
        f = os.popen(cmd)
        data = f.readlines()
        f.close()
        return data


