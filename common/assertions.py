import operator

import jsonpath_ng
import json

from common.recordlog import logs
from typing import Any, Optional
from common.connection import CommectMysql

def to_dict(obj: Any) -> Optional[dict]:
    """尝试将 obj 转换为 dict，若失败则返回 None"""
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        try:
            parsed = json.loads(obj)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
    # 其他情况无法安全转为 dict
    return None

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
        :param status_code:响应参数
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

    def equals_assert(self, value, response):
        """
        第二种模式，相等校验：校验 response 是否包含 value 中所有 key 且值完全相等（允许 response 有多余字段）
        :param value:预期结果，yaml文件当中validation关键字下的结果,必须为dict类型
        :param response:实际返回值,必须为dict类型
        :return:
        """
        value_dict = to_dict(value)
        response_dict = to_dict(response)
        #所有输入装换成字典类型，不能转换的抛出异常
        if value_dict is None:
            msg = f'用例参数无法转换为字典格式：“{value}”'
            logs.error(msg)
            raise AssertionError(msg)
        if response_dict is None:
            msg = f'返回值参数无法转换为字典格式：“{response}”'
            logs.error(msg)
            raise AssertionError(msg)
            # 检查 value 中的每个 key 是否都在 response 中
        res_list = [k for k in value_dict if k not in response_dict]
        if res_list:
            msg = f'返回值 “{response}” 中，没有预期结果 “{value}” 中的key值'
            logs.error(msg)
            raise AssertionError(msg)
        # 构建 response 的子集（只保留 value 中的 key）
        response_subset = {k: response_dict[k] for k in value_dict}
        if operator.eq(value_dict, response_subset):
            logs.info(f'相等断言成功，接口实际结果为 "{response}" ， 等于预期结果 “{value}”')
        else:
            msg = f'相等断言失败，接口实际结果为 "{response}" ， 不等于预期结果 “{value}”'
            logs.error(msg)
            raise AssertionError(msg)

    def not_equals_assert(self, value, response):
        """
        第三种模式，不相等校验：校验 response 是否与 value 中 key 值不同
        :param value:预期结果，yaml文件当中validation关键字下的结果,必须为dict类型
        :param response:实际返回值,必须为dict类型
        :return:
        """
        value_dict = to_dict(value)
        response_dict = to_dict(response)
        # 所有输入装换成字典类型，不能转换的抛出异常
        if value_dict is None:
            msg = f'用例参数无法转换为字典格式：“{value}”'
            logs.error(msg)
            raise AssertionError(msg)
        if response_dict is None:
            msg = f'返回值参数无法转换为字典格式：“{response}”'
            logs.error(msg)
            raise AssertionError(msg)
            # 检查 value 中的每个 key 是否都在 response 中
        res_list = [k for k in value_dict if k not in response_dict]
        if res_list:
            msg = f'返回值 “{response}” 中缺少预期 key “{value}”'
            logs.error(msg)
            raise AssertionError(msg)
        # 构建 response 的子集（只保留 value 中的 key）
        response_subset = {k: response_dict[k] for k in value_dict}
        if operator.eq(value_dict, response_subset):
            msg = f'不相等断言失败：实际值等于预期值。预期 "{value}"，实际 "{response_subset}"'
            logs.error(msg)
            raise AssertionError(msg)
        else:
            logs.info(f'不相等断言成功：实际值 "{response_subset}" 不等于预期值 "{value}"')

    def mysql_assert(self, expected_sql, data, one=False):
        """
        第四种模式，数据库断言校验，校验数据库中是否能查询到sql语句查询信息
        :param expected_sql: sql语句使用 %s 占位符
        :param data: 参数（元组/列表/字典），用于填充占位符
        :param one: 是否仅展示第一个结果
        :return:
        """
        conn = CommectMysql()
        db_value = conn.query(expected_sql, data, one=one)
        if db_value:
            logs.info(f'数据库断言成功, 查询结果为{db_value}')
        else:
            msg = f'数据库查询失败，检查查询语句 “{expected_sql}” ，查询条件 “{data}”'
            logs.error(msg)
            raise AssertionError(msg)

    def _handle_db_assert(self, value, global_one):
        """处理数据库断言"""
        if not isinstance(value, dict):
            raise AssertionError("'db' 断言值必须是一个字典，包含 'sql' 和 'data' 字段")

        expected_sql = value.get('sql')
        data = value.get('data')
        local_one = value.get('one', global_one)

        if expected_sql is None:
            raise AssertionError("'db' 断言缺少 'sql' 字段")
        if data is None:
            logs.info("'db' 断言缺少 'data' 字段或字段为空")

        self.mysql_assert(expected_sql=expected_sql, data=data, one=local_one)

    def assert_result(self, expected, response, status_code, one=False):
        """
        断言模式，通过all_flag标记
        :param expected: 预期结果
        :param response: 实际返回结果,需要json格式
        :param status_code: 接口返回状态码
        :param one: 数据库查询是否只取第一条
        :return:
        """
        if not isinstance(expected, list):
            raise AssertionError("'expected' 必须是一个列表")

            # 断言处理器映射
        handlers = {
            'contains': lambda v: self.contains_assert(v, response, status_code),
            'eq': lambda v: self.equals_assert(v, response),
            'ne': lambda v: self.not_equals_assert(v, response),
            'db': lambda v: self._handle_db_assert(v, one)
        }

        try:
            for idx, yq in enumerate(expected):
                if not isinstance(yq, dict):
                    raise AssertionError(f"第 {idx + 1} 个断言必须是字典，当前值: {yq}")

                if len(yq) != 1:
                    raise AssertionError(f"每个断言块只能包含一个断言类型，当前有 {len(yq)} 个: {list(yq.keys())}")

                key, value = next(iter(yq.items()))

                if key not in handlers:
                    raise AssertionError(
                        f"不支持的断言类型: '{key}'，"
                        f"当前支持: {', '.join(handlers.keys())}"
                    )

                handlers[key](value)

            logs.info('所有断言通过，测试成功')
        except AssertionError:
            raise
        except Exception as e:
            logs.error(f'测试失败！\n 异常信息：{e}')
            raise