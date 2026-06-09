"""
读写yaml文件
"""

import os

import yaml
#from common.sendrequests import SendRequests
from conf.setting import FILE_PATH


class _StrSafeLoader(yaml.SafeLoader):
    """SafeLoader 子类，将日期时间解析为字符串而非 datetime 对象"""

    @staticmethod
    def _str_ts_constructor(loader, node):
        return loader.construct_scalar(node)

    @classmethod
    def load_yaml(cls, stream):
        """yaml.safe_load 的替代，自动将日期时间转为 ISO 字符串。"""
        return yaml.load(stream, Loader=cls)

    @classmethod
    def _register(cls):
        cls.add_constructor(
            'tag:yaml.org,2002:timestamp', cls._str_ts_constructor
        )


_StrSafeLoader._register()


def get_testcase_yaml(file):
    """
    获取yaml文件数据
    :param file: yaml文件路径
    :return: yaml文件内容
    """
    try:
        with open(file, 'r', encoding = 'utf-8') as f:
            return _StrSafeLoader.load_yaml(f)
    except Exception as e:
        print(e)

class ReadYamlData:
    """读取yaml数据，以及写入yaml数据到文件"""

    def write_yaml_data(self, value):
        """
        写入yaml文件数据
        :param value:（dict字典类型）写入的数据内容
        :return:
        """
        file_path = FILE_PATH['extract']
        if not isinstance(value, dict):
            print('写入文件的内容必须是字典类型')
            return

        # 读取已有数据
        existing = {}
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing = _StrSafeLoader.load_yaml(f) or {}

        # 合并后覆写
        existing.update(value)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(existing, f, allow_unicode=True, sort_keys=False)
        except Exception as e:
            print(e)

    def get_extract_yaml(self, node_name):
        """
        读取接口提取的变量值
        :param node_name:yaml文件key值
        :return:
        """
        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path):
            print('extract.yaml文件不存在')
            with open(file_path, 'w', encoding ='utf-8'):
                print('extract.yaml文件已创建')

        with open(file_path, 'r', encoding ='utf-8') as rf_e:
            extract_yaml = _StrSafeLoader.load_yaml(rf_e)
            return extract_yaml[node_name]

    def clear_yaml_data(self):
        """清空extrac.yaml文件的数据"""
        with open(FILE_PATH['extract'], 'r+') as f:
            f.truncate(0)