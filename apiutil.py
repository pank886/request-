import json

import yaml
from readyaml import get_testcase_yaml, ReadYamlData



class BassRequests:

    def __init__(self):
        self.read = ReadYamlData()

    def replace_load(self, data):
        """
        yaml文件替换解析有${}格式的数据
        """
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)