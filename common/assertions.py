from common.recordlog import logs
import jsonpath_ng

class Assertions:
    """
    接口断言模式封装：
    1。字符串包含
    2.结果相等断言
    3.结果不相等断言
    4.接口返回值的任意一个值
    5.数据库断言
    """
    def contains_assert(self, value, response, status_code):
        """
        第一种模式，字符串包含断言，断言预期结果的字符串在接口的实际返回结果中
        :param value:预期结果，yaml文件当中validation关键字下的结果
        :param response:实际返回值
        :param startus_code:响应参数
        :return:
        """
        for assert_key, assert_value in value.items():
            if assert_key == 'status_code':
                if assert_value != status_code:
                    msg = f'状态码断言失败：期望 {assert_value}，实际 {status_code}'
                    logs.error(msg)
                    raise AssertionError(msg)
                else:
                    logs.info(f'状态码断言成功：期望 {assert_value}，实际 {status_code}')
            else:
                try:
                    expr = jsonpath_ng.parse(assert_key)
                    resp_list = [match.value for match in expr.find(response)]
                    if not resp_list:
                        msg = f'JSONPath "{assert_key}" 未匹配到任何值'
                        logs.error(msg)
                        raise AssertionError(msg)
                    resp_value = resp_list[0]
                    if isinstance(resp_value, list):
                        resp_text = ''.join(str(x) for x in resp_value)
                    else:
                        resp_text = str(resp_value)
                    if assert_value in resp_text:
                        logs.info('字符串包含断言成功，预期结果：【%s】, 实际结果:【%s】' % (assert_value, resp_text))
                    else:
                        msg = f'包含断言失败：期望 "{assert_value}" 在字段 "{assert_key}" 的值 "{resp_text}" 中'
                        logs.error(msg)
                        raise AssertionError(msg)
                except Exception as e:
                    logs.error(f'JSONPath 解析或断言异常: {e}')
                    raise AssertionError(f'断言执行异常: {e}')
        logs.info('全部包含断言通过')

    def equals_assert(self):
        """"相等模式"""

    def not_equals_assert(self):
        """不相等模式"""

    def assert_result(self, expected, response, status_code):
        """
        断言模式，通过all_flag标记
        :param expected: 预期结果
        :param response: 实际返回结果,需要json格式
        :param status_code: 接口返回状态码
        :return:
        """
        try:
            for yq in expected:
                for key, value in yq.items():
                    if key == 'contains':
                        self.contains_assert(value, response, status_code)
                    elif key == 'eq':
                        self.equals_assert()
            logs.info('测试成功')
        except Exception as e:
            logs.error(f'测试失败！\n 异常信息：{e}')
            raise