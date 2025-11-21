import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests
from common.recordlog import logs
from base.apiutil import RequestsBase


@allure.feature('商品管理')
class TestGetGoodlist:

    @allure.story('商品列表获取')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/getGoodlist/getGoodlist.yaml'))
    def test_Goodlist(self, params):
        RequestsBase().specification_yaml(params)

    @allure.story('商品详情查看')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/getGoodlist/productDetail.yaml'))
    def test_productDetail(self, params):
        RequestsBase().specification_yaml(params)