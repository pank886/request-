import re
import json
import allure
import jsonpath_ng

from common.readyaml import get_testcase_yaml, ReadYamlData
from common.debugtilk import DebugTalk
from conf.operationConfig import OperationConfig
from common.sendrequests import SendRequests
from common.recordlog import logs
from common.assertions import Assertions

assert_res = Assertions()

class RequestsBase:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()
        self.send = SendRequests()

    def replace_load(self, data):
        """
        yaml文件替换解析有${}格式的数据
        """
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)

        for i in range(str_data.count('${')):

            if '${' in str_data and '}' in str_data:
                #index检测字符串是否是子字符串，并找到字符串的索引位置
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                #取出函数名
                func_name = ref_all_params[2:ref_all_params.index('(')]
                #取里面的函数值
                #取出函数里面的参数值
                funcs_params = ref_all_params[ref_all_params.index('(') + 1:ref_all_params.index(')')]
                #传入替换的参数获取对应的值
                extract_data = getattr(DebugTalk(), func_name)(*funcs_params.split(',') if funcs_params else [])
                str_data = str_data.replace(ref_all_params, str(extract_data))
        #还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification_yaml(self, case_info):
        """
        规范yaml测试用例写法
        case_info: list类型，调试取case_info[0]-->dict
        """
        #限定参数类型
        params_type = ['params', 'data', 'json']
        #获取yaml文件请求头信息
        try:
            base_url = self.conf.get_envi('host')
            url = base_url + case_info['baseInfo']['url']
            allure.attach(url, f'接口地址:{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name, f'接口名称:{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method, f'请求方法:{method}')
            header = case_info['baseInfo']['header']
            # 多个请求头以文本形式展示
            allure.attach(str(header), f'请求头:{header}', allure.attachment_type.TEXT)
            try:
                cookies = self.replace_load(case_info['baseInfo']['cookies'])
                allure.attach(cookies, f'请求方法:{cookies}', allure.attachment_type.TEXT)
            except:
                cookies = None
            #获取参数信息
            for tc in case_info['testCase']:
                case_name = tc.pop('case_name', '未命名用例')
                allure.attach(case_name, f'测试用例名称:{case_name}')
                validation = tc.pop('validation', '未配置断言')
                extract = tc.pop('extract', None)
                extract_list = tc.pop('extract_list', None)
                for key, value in tc.items():
                    if key in params_type:
                        tc[key] = self.replace_load(value)

                res = self.send.run_main(name = api_name, case_name = case_name, url = url, header = header, method = method,
                                         cookies = cookies, files = None, **tc)
                res_text = res.text
                allure.attach(res.text, f'接口响应信息', allure.attachment_type.TEXT)
                allure.attach(str(res.status_code), f'接口状态码: {res.status_code}', allure.attachment_type.TEXT)

                res_json = res.json()

                if extract is not None:
                    self.extract_data(extract, res_text)
                if extract_list is not None:
                    self.extract_list_data(extract_list, res_text)

                #处理接口断言
                assert_res.assert_result(validation, res_json, res.status_code)
        except AssertionError:
            raise
        except Exception as e:
            
            logs.error("请求处理异常: %s", str(e))
            raise

    def extract_data(self, testcase_extract, response):
        """
        提取接口返回值：支持 JSONPath（$开头）和正则表达式
        """
        if not testcase_extract:
            return

        json_obj = None  # 缓存解析后的 JSON

        for key, value in testcase_extract.items():
            try:
                value_str = str(value)

                # ========== 1. JSONPath 提取（以 $ 开头）==========
                if value_str.strip().startswith("$"):
                    if json_obj is None:
                        try:
                            json_obj = json.loads(response)
                        except json.JSONDecodeError:
                            logs.error("响应不是合法 JSON，跳过所有 JSONPath 提取")
                            json_obj = False  # 标记失败，避免重复尝试
                    if json_obj is False:
                        continue

                    matches = jsonpath_ng.parse(value_str).find(json_obj)
                    result = matches[0].value if matches else "未提取到数据，该接口返回结果可能为空"
                    logs.info(f'JSON 提取 [{key}]: {result}')
                    self.read.write_yaml_data({key: result})

                # ========== 2. 正则提取（其他情况）==========
                else:
                    match = re.search(value_str, response, re.S)
                    if match:
                        result = match.group(1)  # 始终返回字符串，不自动转 int
                        logs.info(f'正则提取 [{key}]: {result}')
                        self.read.write_yaml_data({key: result})
                    else:
                        logs.warning(f"正则未匹配 [{key}]: {value_str}")

            except Exception as e:
                logs.error(f"提取 [{key}] 时异常，表达式: {value}, 错误: {e}", exc_info=True)

    def extract_list_data(self, testcase_extract_list, response):
        """读取列表数据"""
        try:
            for key, value in testcase_extract_list.items():

                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json_ql = jsonpath_ng.parse(value).find(json.loads(response))
                    ext_json = [match.value for match in ext_json_ql] if ext_json_ql else "未提取到数据，该接口返回结果可能为空"
                    extract_list_data = {key: ext_json}
                    logs.info('json提取到参数：%s' % extract_list_data)
                    self.read.write_yaml_data(extract_list_data)

                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_list_data = {key: ext_list}
                        logs.info(f'正则表达式提取到的参数:{extract_list_data}')
                        self.read.write_yaml_data(extract_list_data)
        except Exception as e:
            logs.error("接口返回值提取异常，检查yaml文件extract表达式是否正确: %s", str(e))


if __name__ == '__main__':
    req = RequestsBase()
    data = get_testcase_yaml('../testcase/Login/logen.yaml')[0]
    print(req.specification_yaml(data))
