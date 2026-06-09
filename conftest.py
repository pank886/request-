import pytest
from common.recordlog import logs
from common.readyaml import ReadYamlData

read = ReadYamlData()

@pytest.fixture(scope='session', autouse=True)
def clear_extract_data():
    read.clear_yaml_data()

@pytest.fixture(scope='function', autouse=True, name='Testadd', params = [1])
def fixture_test(request):
    """前后置处理"""
    logs.info('------------接口测试开始----------------')
    yield
    logs.info('------------接口测试结束----------------')
    return request.param