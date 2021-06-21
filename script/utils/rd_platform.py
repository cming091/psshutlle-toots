import base64
import fileinput
import json
import logging
# from utils import cfg
import requests
import time


class RdPlatform:
    def __init__(self, url_base,rd_platform_host,user_email,is_cluster=False):
        # 公共参数
        self.ip = url_base
        self.url_base = 'http://' + rd_platform_host
        self.user_email = user_email
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.token = self.get_user_token()
        if self.token == '':
            exit(1)

        # 单机版本专用参数
        self.env_uuid = ''

        # 集群版本专用参数
        self.cluster_env_info = {}
        self.cluster_service_dict = {}
        if is_cluster:
            # 获取集群环境信息
            self.cluster_env_info = self.get_cluster_env_info()
            if len(self.cluster_env_info.keys()) == 0:
                exit(1)

            # 获取集群服务列表，分为有状态服务和无状态服务
            self.cluster_service_dict = self.get_cluster_services()
            if len(self.cluster_service_dict) == 0:
                exit(1)
        else:
            self.env_uuid = self.get_env_uuid(self.token)
            if self.env_uuid == '':
                exit(1)

    # -------------------------------- 以下为集群版本接口封装 --------------------------------

    def get_cluster_env_info(self):
        """
        获取集群的环境信息
        :return: env_info dict
        """
        url = self.url_base + '/v2/clusterEnv/getEnvList'
        env_info = {}
        params = {'userToken': self.token}
        try:
            r = requests.get(url=url, params=params)
            if r.status_code == 200:
                res_data = r.json()
                if res_data.get('returnCode') == 0:
                    envs = res_data['data']['envs']
                    for env in envs:
                        if self.ip == env['xip']:
                            env_info = env
                            break
                    if len(env_info.keys()) == 0:
                        logging.error(f'get_cluster_env_info error, can not find env {self.ip}')
                else:
                    logging.error(f'get_cluster_env_info {self.ip} error, {res_data}')
            else:
                logging.error(f'get_cluster_env_info {self.ip} error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'get_cluster_env_info {self.ip} error, {e}')

        return env_info

    def get_cluster_services(self):
        """
        获取集群中的服务列表，分为有状态和无状态服务两种，分别获取
        :return: dict, keys: deployments or statefulsets, value: service list
        """
        cluster = self.cluster_env_info['cluster']
        namespace = self.cluster_env_info['namespace']
        service_dict = {}

        url = self.url_base + f'/v2/cluster/k8s/{cluster}/apis/core/v1/namespaces/{namespace}/pods'
        params = {'userToken': self.token}

        try:
            r_d = requests.get(url=url, params=params)
            if r_d.status_code == 200:
                res_data = r_d.json()
                if res_data.get('returnCode') == 0:
                    items = res_data['data']['pods']['items']
                    # 以labels下的app为key
                    for item in items:
                        app_name = item['metadata']['labels']['app']
                        if service_dict.get(app_name) is None:
                            service_dict[app_name] = {}
                        service_dict[app_name][item['metadata']['name']] = item['metadata']['uid']
                        # service_dict[app_name].append(item['metadata']['name'])
                else:
                    logging.error(f'get cluster server list error, {res_data}')
            else:
                logging.error(f'get cluster server list error, http response code is {r_d.status_code}')
        except Exception as e:
            logging.error(f'get cluster server list error, {e}')

        return service_dict

    def recreate_cluster_service(self, app_name):
        if self.cluster_service_dict.get(app_name) is None:
            logging.error(f'can not find service {app_name} in cluster')
            return False

        old_pods = self.cluster_service_dict.get(app_name).values()

        result = 'fail'
        for app in self.cluster_service_dict.get(app_name).keys():
            result = 'fail'
            cluster = self.cluster_env_info['cluster']
            namespace = self.cluster_env_info['namespace']
            url = self.url_base + f'/v2/cluster/k8s/{cluster}/apis/core/v1/namespaces/{namespace}/pods/{app}?userToken={self.token}'

            try:
                r = requests.delete(url=url)
                if r.status_code == 200:
                    res_data = r.json()
                    if res_data.get('returnCode') == 0:
                        result = 'succ'
                    else:
                        logging.error(f'recreate_cluster_service {app_name} error, {res_data}')
                else:
                    logging.error(f'recreate_cluster_service {app_name} error, http response code is {r.status_code}')
            except Exception as e:
                logging.error(f'recreate_cluster_service {app_name} error, {e}')

        wait_times = 0
        if result == 'succ':
            # 刷新一下服务列表
            # 每2秒刷新一次，等待重建完毕
            while True:
                self.cluster_service_dict = self.get_cluster_services()
                # print(self.cluster_service_dict.get(app_name).values())
                if len(self.cluster_service_dict.get(app_name).values()) == len(old_pods):
                    flag = False
                    for new_pod in self.cluster_service_dict.get(app_name).values():
                        if new_pod not in old_pods:
                            # print(f'recreate service {new_pod} done!')
                            logging.info(f'recreate service {new_pod} done!')
                            flag = True
                        else:
                            flag = False
                    if flag is True:
                        break
                # print(f'waiting for recreate service {app_name}')
                logging.info(f'waiting for recreate service {app_name}')
                time.sleep(2)
                wait_times += 1
                if wait_times > 20:
                    logging.error(f'wait for recreate service {app_name} too long, quit!')
                    result = 'fail'
                    break
        return result

    # -------------------------------- 以下为单机版本接口封装 --------------------------------

    def __exec_command(self, command, args, service):
        url = self.url_base + '/v2/env/exec'
        data = {
            'userToken': self.token,
            'envUuid': self.env_uuid,
            'command': command,
            'args': json.dumps(args),
            'service': service
        }
        result = False
        output = ''
        try:
            r = requests.post(url=url, data=data, headers=self.headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    result = True
                    output = res_data['data']['output']
                else:
                    logging.error(f'exec_command error, {res_data}')
            else:
                logging.error(f'exec_command {command} error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'exec_command error, {e}')
        return result, output

    def get_user_token(self):
        url = self.url_base + '/api/getUserToken'
        data = 'email=' + self.user_email
        token = ""
        try:
            r = requests.post(url=url, data=data, headers=self.headers, timeout=5)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    token = res_data['data']['user']['userToken']
                else:
                    logging.error(f'get_user_token error, {res_data}')
            else:
                logging.error(f'get_user_token error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'get_user_token error, {e}')
        return token

    def get_env_uuid(self, token):
        uuid = ''
        if token is not '':
            url = self.url_base + '/api/env/getEnvList'
            data = 'userToken=' + str(token)
            try:
                r = requests.post(url=url, data=data, headers=self.headers)
                if r.status_code == 200:
                    res_data = r.json()
                    if res_data['returnCode'] == 0:
                        data_list = res_data['data']['envs']
                        for env in data_list:
                            if self.ip == env['nip'] or self.ip == env['xip']:
                                uuid = env['uuid']
                                break
                    else:
                        logging.error(f'get_env_uuid error, {res_data}')
                else:
                    logging.error(f'get_env_uuid error, http response code is {r.status_code}')
            except Exception as e:
                logging.error(f'get_env_uuid error, {e}')
        if uuid == '':
            logging.error(f'get_env_uuid error, can not find {self.ip} in your env list')
        return uuid

    def __get_service_list(self):
        service_list = []
        url = self.url_base + '/api/env/getEnvInfo'
        data = f'envUuid={self.env_uuid}&userToken={self.token}'
        try:
            r = requests.post(url=url, data=data, headers=self.headers)
            if r.status_code == 200:
                res_data = r.json()
                if res_data['returnCode'] == 0:
                    env_status = res_data['data']['status']
                    if env_status == 1:
                        service_list = res_data['data']['runServices']
                    else:
                        logging.error(f'get_env_info error, env is not ready, status is {env_status}')
                else:
                    logging.error(f'get_env_info error, {res_data}')
            else:
                logging.error(f'get_env_info error, http response code is {r.status_code}')
        except Exception as e:
            logging.error(f'get_env_info error, {e}')
        return service_list

    def __find_service(self, service_name):
        service_list = self.__get_service_list()
        find_service = False
        for service in service_list:
            if service_name == service['service']:
                find_service = True
                break
        return find_service

    def __service_operation(self, service_name, operation, version=''):
        result = 'fail'
        find_service = self.__find_service(service_name)

        if find_service:
            url = f'{self.url_base}/api/env/{operation}'
            data = f'envUuid={self.env_uuid}&service={service_name}&userToken={self.token}'
            if operation == 'updateService':
                data = data + '&version=' + version
            try:
                r = requests.post(url=url, data=data, headers=self.headers)
                if r.status_code == 200:
                    res_data = r.json()
                    if res_data['returnCode'] == 0:
                        result = 'succ'
                        logging.info(f'{operation} {service_name} in {self.ip} successfully!')
                    else:
                        logging.error(f'{operation} {service_name} error, {res_data}')
                else:
                    logging.error(f'{operation} {service_name} error, http response code is {r.status_code}')
            except Exception as e:
                logging.error(f'{operation} {service_name} error, {e}')
        else:
            logging.error(f'{operation} {service_name} error, can not find service {service_name} in {self.ip}')
        return result

    def update_service(self, service_name, version):
        return self.__service_operation(service_name, 'updateService', version)

    def restart_service(self, service_name):
        return self.__service_operation(service_name, 'restartService')

    def stop_service(self, service_name):
        return self.__service_operation(service_name, 'stopService')

    def start_service(self, service_name):
        return self.__service_operation(service_name, 'startService')

    def recreate_service(self, service_name):
        return self.__service_operation(service_name, 'recreateService')

    def kill_service(self, key, service_name):
        """ 杀掉docker内的进程 """
        ok, _ = self.__exec_command('/bin/sh',
                            ["-c", "ps -ef | grep " + key + " | grep -v grep | awk '{print $1}' | xargs kill"],
                            service_name)
        return ok

    def get_file_from_docker(self, service_name):
        # todo: 多个覆盖率文件合并支持,
        #  https://stackoverflow.com/questions/26469072/is-there-anyway-to-merge-cobertura-coverage-xml-reports-together
        ok, output = self.__exec_command('cat', ['/go/src/coverage.xml'], service_name)
        if not ok:
            return ok
        try:
            content = base64.b64decode(output).decode("utf-8")
            f = open('coverage.xml', 'w')
            f.write(str(content))
            f.close()

            for line in fileinput.input('coverage.xml', inplace=1):
                if not fileinput.isfirstline():
                    print(line.replace("\n", ""))
        except Exception as e:
            logging.error(f'get_file_from_docker error, {e}')
            return False
        return True


if __name__ == '__main__':
    import os
    import time

    root_path = os.path.dirname(os.path.dirname(__file__))
    cfg_path = os.path.join(root_path, './conf/config.ini')
    # cfg.load_cfg(cfg_path)
    # is_cluster = True
    # rdp = RdPlatform(is_cluster)
    # print(rdp.cluster_env_info)
    # print(rdp.cluster_service_dict)
    # ret = rdp.recreate_cluster_service('sim-device-common')
    # print('recreate ret: ', ret)
    # print(rdp.cluster_service_dict)
    rdp = RdPlatform()
    ret = rdp.get_file_from_docker('tes')
    print('get file: ', ret)
#     print('token is ', rdp.token)
#     print('env_uuid is ', rdp.env_uuid)
#
#     t1 = time.time()
#     service_name = 'ui-manager'
#     res = rdp.stop_service(service_name)
#     t2 = time.time()
#     print(res)
#     print(f'time: {t2 - t1}')
