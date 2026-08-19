import pytest
import requests
import urllib3
from common.recordlog import logs
from common.readyaml import ReadYamlData
from data_factory.plate_generator import PlateGenerator
from conf.operationConfig import OperationConfig

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
read = ReadYamlData()

@pytest.fixture(scope='session', autouse=True)
def login_and_get_token():
    """登录获取token并存入extract.yaml"""
    url = "https://dev.damaiiot.com:40443/park-base-auth/login"
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    payload = {
        "identityCode": "",
        "name": "admin",
        "password": "889d0039326ce09aa2ae27401967411f",
        "randomStr": "",
        "yqAppCode": "test"
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    data = response.json()
    token = data['data']['token']
    read.write_yaml_data({'accessToken': token})
    logs.info("登录成功，token已存入extract.yaml")

@pytest.fixture(scope='session', autouse=True)
def get_yq_app_code():
    """从config.ini读取yqAppCode，写入extract.yaml，apiutil.py自动注入到每个请求的header
    特殊环境不需要此配置时，在config.ini中将code置空即可（code =）"""
    conf = OperationConfig()
    yq_app_code = conf.get_section_for_data('yqAppCode', 'code')
    if yq_app_code:
        read.write_yaml_data({'yqAppCode': yq_app_code})
        logs.info(f"yqAppCode已从config.ini读取并存入extract.yaml: {yq_app_code}")
    else:
        logs.info("yqAppCode未配置或为空，跳过header自动注入")


@pytest.fixture(scope='session', autouse=True)
def clear_extract_data():
    yield
    # 后置处理：所有用例执行完后清空extract.yaml
    read.clear_yaml_data()
    logs.info("extract.yaml已清空")

@pytest.fixture(scope='session', autouse=True)
def clear_license_plates():
    """清空已生成的车牌记录，避免max_total=2000 上限导致车牌生成为空"""
    PlateGenerator().generate("clear")
    logs.info("随机车牌记录已清空")

@pytest.fixture(scope='function', autouse=True, name='Testadd', params = [1])
def fixture_test(request):
    """前后置处理"""
    logs.info('------------接口测试开始----------------')
    yield
    logs.info('------------接口测试结束----------------')
    return request.param