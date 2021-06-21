pallet shuttle测试工具


git 地址: 

    
使用方法：

    1.clone 项目到本地,切换到适当的分支
    
    2.安装python3，下载最新的版本即可，我用的是3.7.3
    
    3.安装python依赖库，在psshutlle-toots目录下执行
    
    pip install -r requirement.txt
    
初始化环境入口&执行方法：

    配置入口 psshutlle-toots/config/base-env.csv
    
    入口 psshutlle-toots/main.py
    
    执行命令 python main.py
    
业务测试入口&执行方法：

    配置入口 psshutlle-toots/config/conf.yml
    
    入口 psshutlle-toots/run.py
    
    执行命令 python run.py

业务配置说明

    入口 psshutlle-toots/config/conf.yml
    
    每个业务一个模块，业务名称为模块名称
    
    主要配置 ip 修改成自己的ip
    
    delay 请求delay 时间/秒
    
    rmFlag 清除数据
    
    isSimulate 是否是模拟器环境
    
    isRaise 失败重试后时候抛出异常
    
    isNeedAssignAndStock 是否需要初始化assignmentdata 跟stock 数据
    
    changeBox  只在超小件业务中有 换箱箱数
    
    reportLess 报缺数量 超小件非超小件业务