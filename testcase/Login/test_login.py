import pytest
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests
from common.recordlog import logs

class TestLogin:

    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/Login/logen.yaml'))
    def test_login(self, params):
        print(params)
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + str(url)

        logs.info("获取接口地址 : {}".format(new_url))

        method = params['baseInfo']['method']
        header = params['baseInfo']['header']
        data = params['testCase'][0]['data']

        send = SendRequests()
        res = send.run_main(url = new_url, method = method, header = None, data = data)
        print(res)

        assert res['msg'] == '登陆成功'