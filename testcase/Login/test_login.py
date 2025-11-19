import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests
from common.recordlog import logs
from base.apiutil import RequestsBase


@allure.feature('登录接口')
class TestLogin:

    @allure.story('用户名和密码登录正常校验')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/Login/logen.yaml'))
    def test_login(self, params):
        RequestsBase().specification_yaml(params)
