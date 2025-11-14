import pytest
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests
from common.recordlog import logs
from base.apiutil import RequestsBase

class TestLogin:

    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/Login/logen.yaml'))
    def test_login(self, params):
        RequestsBase().specifcation_yaml(params)
