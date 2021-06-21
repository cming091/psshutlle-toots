import os
import random
from config import *
from core import *
import time
from utils import *
logger = LogHandler(__name__)

logger.warning('raw config \t{}\n'.format(CONF))

def main():
    pass

#整托入库 算法 执行一个循环或者指定code
def testalgoWholein():
    # codeslist = Cfg.getOneFieldFromFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config', 'frame.csv'),
    #                                 field=1)
    codeslist= ['20006']
    for codes in codeslist:
        logger.info('[codes:{}]'.format(codes))
        allwholein = Inbound(CONF['wholein'])
        allwholein([codes])
        logger.info('[allwholein.statusCode:{}]'.format(allwholein.statusCode))

#整托出库 算法 执行一次
def testalgoWholeout():
    codelist = Common.getPodList(1)
    logger.info('[getPodList {}]'.format(codelist))
    if codelist:
        codes = [random.choice(codelist)]
        wholeout = Outbound(CONF['wholeout'])
        wholeout(codes)
        logger.info('[allwholein.statusCode:{}]'.format(wholeout.statusCode))

#非超小件算法 每次执行一次
def testAlgoNonSmallPicking():
    codelist = Common.getPodList(1)
    logger.info('[getPodList {}]'.format(codelist))
    if codelist:
        codes = [random.choice(codelist)]
        nonSmallPicking = NonSmallPicking(CONF['nonSmallPicking'])
        nonSmallPicking(codes)
        print(nonSmallPicking.statusCode)

#超小件算法 每次执行一次
def testAlgoSmallPicking():
    codelist = Common.getPodList(1)
    logger.info('[getPodList {}]'.format(codelist))
    if codelist:
        codes = [random.choice(codelist)]
        smallPicking = SmallPicking(CONF['smallPicking'])
        smallPicking(codes)
        print(smallPicking.statusCode)



if __name__=="__main__":
    main()