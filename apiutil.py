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

        for i in range(str_data.count('${')):

            if '${' in str_data and '}' in str_data:
                #index检测字符串是否是子字符串，并找到字符串的索引位置
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                str_all_params = str_data[start_index:end_index + 1]
                #取出函数名
                func_name = str_all_params[2:str_all_params.index('(')]
                #取里面的函数值
                str
                print(ref_all_params)




if __name__ == '__main__':
    data = get_testcase_yaml('logen.yaml')

    print(data)
    base = BassRequests()
    base.replace_load(data)
