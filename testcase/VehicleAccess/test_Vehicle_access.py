import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests
from common.recordlog import logs
from base.apiutil import RequestsBase

@allure.story('临停车辆：进主场-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_005:

    @allure.title("01_车辆进场")
    @pytest.mark.order(1)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carin_random.yaml'))
    def test_CarIn(self, params):
        RequestsBase().specification_yaml(params)

    @allure.title("02_车辆出场_失败")
    @pytest.mark.order(2)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carout_false.yaml'))
    def test_CarOut(self, params):
        RequestsBase().specification_yaml(params)

    @allure.title("03_获取应缴金额")
    @pytest.mark.order(3)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carpay.yaml'))
    def test_CarPay(self, params):
        RequestsBase().specification_yaml(params)

    @allure.title("04_在场车辆查询")
    @pytest.mark.order(4)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carquery.yaml'))
    def test_CarExit(self, params):
        RequestsBase().specification_yaml(params)

@allure.story('包月车辆：进主场-扫车牌包月车出场-免费')#需车辆code，删除入场记录接口
@pytest.mark.danyuan
class TestVehicleAccess_001:

    @allure.title('添加包月车')
    @pytest.mark.order(1)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/addBycVehicle.yaml'))
    def test_AddBycVehicle(self, params):
        RequestsBase().specification_yaml(params)

    @allure.title('包月车辆进场')
    @pytest.mark.order(2)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carin.yaml'))
    def test_CarIn(self, params):
        RequestsBase().specification_yaml(params)

    @allure.title('车辆出场_成功')
    @pytest.mark.order(3)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carout_ture.yaml'))
    def test_CarOut(self, params):
        RequestsBase().specification_yaml(params)

    @allure.title('删除包月车')
    @pytest.mark.order(4)
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/deleteBycVehicle.yaml'))
    def test_DeleteBycVehicle(self, params):
        RequestsBase().specification_yaml(params)

@allure.feature('白名单车辆：进主场-扫车牌白名单出场-免费')
# @pytest.mark.danyuan
class TestVehicleAccess_012:
    @allure.story('添加白名单')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/addBmdVehicle.yaml'))
    def test_AddBmdVehicle(self, params):
        RequestsBase().specification_yaml(params)

    @allure.story('车辆进场')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carin.yaml'))
    def test_CarIn(self, params):
        RequestsBase().specification_yaml(params)

    @allure.story('车辆出场_成功')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/carout_ture.yaml'))
    def test_CarOut(self, params):
        RequestsBase().specification_yaml(params)

    @allure.story('删除白名单')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/VehicleAccess/deleteBmdVehicle.yaml'))
    def test_DeleteBmdVehicle(self, params):
        RequestsBase().specification_yaml(params)

@allure.story('包月车：进主场-同人员包月车在主场-扫车牌临停出场-收费')#需一人多车白名单接口
@pytest.mark.danyuan
class TestVehicleAccess_002:
    pass

@allure.story('包月车：进主场-包月变更为临停车-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_003:
    pass

@allure.story('包月车：进主场-同人员包月车在主场-包月变更为临停车-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_004:
    pass

@allure.story('临停车：进主场-临停车变更为包月车-扫车牌包月车出场-收临停费')
@pytest.mark.danyuan
class TestVehicleAccess_006:
    pass

@allure.story('临停车：进主场-临停车变更为白名单-扫车牌白名单出场-收临停费')
@pytest.mark.danyuan
class TestVehicleAccess_007:
    pass

@allure.story('临停车：进主场-同人员包月车在主场-临停车变更为包月车-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_008:
    pass

@allure.story('临停车：进主场-同人员白名单车在主场-临停车变更为白名单-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_009:
    pass

@allure.story('临停车：进主场-临停车变更为包月车-包月车变更为临停车-扫车牌临停出场-收临停费')
@pytest.mark.danyuan
class TestVehicleAccess_010:
    pass

@allure.story('临停车：进主场-临停车变更为白名单-白名单变更为临停车-扫车牌临停出场-收临停费')
@pytest.mark.danyuan
class TestVehicleAccess_011:
    pass

@allure.story('白名单：进主场-同人员白名单车在主场-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_013:
    pass

@allure.story('白名单：进主场-同人员白名单车在主场-白名单变更为临停车-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_014:
    pass

@allure.story('白名单：进主场-白名单变更为临停车-扫车牌临停出场-收临停费')
@pytest.mark.danyuan
class TestVehicleAccess_015:
    pass

@allure.story('临停车：主场到子场-扫车牌临停出场-收子场+主场费')
@pytest.mark.danyuan
class TestVehicleAccess_016:
    pass

@allure.story('临停车：主场到子场-子场变更包月-扫车牌子场包月出场-收子场临停+主场费')
@pytest.mark.danyuan
class TestVehicleAccess_017:
    pass

@allure.story('临停车：主场到子场-同人员子场包月在场-子场变更包月-扫车牌临停出场-收子场+主场费')
@pytest.mark.danyuan
class TestVehicleAccess_018:
    pass

@allure.story('临停车：主场到子场-子场变更白名单-扫车牌子场白名单出场-收子场临停+主场费')
@pytest.mark.danyuan
class TestVehicleAccess_019:
    pass

@allure.story('临停车：主场到子场-同人员子场白名单在场-子场变更白名单-扫车牌临停出场-收子场+主场费')
@pytest.mark.danyuan
class TestVehicleAccess_020:
    pass

@allure.story('临停车：主场到子场-主场变更包月-子场变更包月-扫车牌包月出场-收子场临停+主场临停费')
@pytest.mark.danyuan
class TestVehicleAccess_021:
    pass

@allure.story('临停车：主场到子场-主场变更白名单-子场变更白名单-扫车牌白名单出场-收子场临停+主场临停费')
@pytest.mark.danyuan
class TestVehicleAccess_022:
    pass

@allure.story('子场包月车：进主场-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_023:
    pass

@allure.story('子场包月车：主场到子场-扫车牌子场包月出场-收主场临停费')
@pytest.mark.danyuan
class TestVehicleAccess_024:
    pass

@allure.story('子场包月车：主场到子场-子场包月变更临停-扫车牌临停出场-收子场临停+主场费')
@pytest.mark.danyuan
class TestVehicleAccess_025:
    pass

@allure.story('子场白名单：进主场-扫车牌临停出场-收费')
@pytest.mark.danyuan
class TestVehicleAccess_026:
    pass

@allure.story('子场白名单：主场到子场-扫车牌子场白名单出场-收主场临停费')
@pytest.mark.danyuan
class TestVehicleAccess_027:
    pass

@allure.story('子场白名单：主场到子场-子场白名单变更临停-扫车牌临停出场-收子场临停+主场费')
@pytest.mark.danyuan
class TestVehicleAccess_028:
    pass