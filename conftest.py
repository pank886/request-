import pytest

@pytest.fixture(scope='function', autouse=True, name='Testadd', params = [1, 2])
def fixture_test(request):
    """前后置处理"""
    print('------------接口测试开始----------------')
    yield
    print('------------接口测试结束----------------')
    return request.param