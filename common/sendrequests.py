import json
import time
import allure
import pytest
import requests

from common.recordlog import logs
from common.readyaml import ReadYamlData
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 重试配置
RETRY_TOTAL = 3           # 最大重试次数
RETRY_BACKOFF = 2         # 退避因子（秒）：第n次重试等待 backoff * (2^n) 秒
RETRY_STATUS_CODES = [500, 502, 503, 504]  # 哪些状态码触发重试
RETRY_TIMEOUT = 30        # 单次请求超时（秒）


class SendRequests(object):
    def __init__(self):
        self.read = ReadYamlData()

    def send_request(self, **kwargs):
        """发起请求（带超时重试）"""
        session = requests.session()

        # 配置重试策略
        retry = Retry(
            total=RETRY_TOTAL,
            backoff_factor=RETRY_BACKOFF,
            status_forcelist=RETRY_STATUS_CODES,
            allowed_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        kwargs.setdefault('timeout', RETRY_TIMEOUT)
        result = None
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                self.read.write_yaml_data(set_cookie)
                logs.info(f'cookie:{set_cookie}')
            logs.info(f'接口实际返回信息{result.text if result.text else result}')
        except requests.exceptions.ConnectionError as e:
            logs.error(f'接口连接服务器异常（已重试{RETRY_TOTAL}次）: {e}')
            pytest.fail('接口请求异常，可能是request的连接数过多或者请求速度过快导致程序报错！')
        except requests.exceptions.HTTPError as e:
            logs.error(f'http异常{e}')
            pytest.fail('http请求异常！')
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail('请求异常，请检查系统或者数据是否正常！')
        return result

    def run_main(self, name, case_name, url, header, method, cookies = None, files = None, **kwargs):
        """

        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :param method: 请求方法
        :return:
        """
        try:
            #收集报告日志信息
            logs.info(f'接口名称:{name}')
            logs.info(f'接口请求地址:{url}')
            logs.info(f'请求方法:{method}')
            logs.info(f'测试用例名称:{case_name}')
            logs.info(f'请求头:{header}')
            logs.info(f'Cookies:{cookies}')
            #请求参数处理
            req_params = json.dumps(kwargs, ensure_ascii=False)
            if any(key in kwargs for key in ('data', 'json', 'params')):
                logs.info(f'请求参数:{kwargs}')
                allure.attach(req_params, f'请求参数:{req_params}', allure.attachment_type.TEXT)
        except Exception as e:
            logs.error(f'错误日志：{e}')
        response = self.send_request(method = method, url = url, headers = header,
                          cookies = cookies, files = files, verify = False, **kwargs)
        return response