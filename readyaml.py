import os

import yaml

def get_testcase_yaml(file):
    """
    获取yaml文件数据
    :param file: yaml文件路径
    :return: yaml文件内容
    """
    try:
        with open(file, 'r', encoding = 'utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(e)

class ReadYamlData:
    """读取yaml数据，以及写入yaml数据到文件"""

    def __init__(self, yaml_file = None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = 'logen.yaml'

    def write_yaml_data(self, value):
        """
        写入yaml文件数据
        :param value:（dict字典类型）写入的数据内容
        :return:
        """
        file_path = 'extract.yaml'
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding = 'UTF-8'):
                pass
        try:
            file = open(file_path, 'a', encoding = 'utf-8')
            with file:
                if isinstance(value, dict):
                    write_data = yaml.dump(value, allow_unicode = True, sort_keys = False)
                    file.write(write_data)
                else:
                    print('写入文件的内容必须是字典类型')
        except Exception as e:
            print(e)

    def get_extract_yaml(self, node_name):
        """
        读取接口提取的变量值
        :param node_name:yaml文件key值
        :return:
        """
        if os.path.exists('extract.yaml'):
            pass
        else:
            print('extract.yaml文件不存在')
            with open('extract.yaml', 'w', encoding = 'utf-8'):
                print('extract.yaml文件已创建')

        with open('extract.yaml', 'r', encoding = 'utf-8') as rf_e:
            extract_yaml = yaml.safe_load(rf_e)
            return extract_yaml[node_name]


if __name__ == '__main__':
    res = get_testcase_yaml('logen.yaml')[0]
    url = res['baseInfo']['url']
    method = res['baseInfo']['method']
    header = res['baseInfo']['header']
    data = res['testCase'][0]['data']
    url_https = f"http://127.0.0.1:8787{url}"
    from requests_demo import RequestsDemo
    send = RequestsDemo()
    print(data)
    resd = send.run_main(url_https, data, header = None, method = method)
    print(resd)

    token = resd.get('token')
    print(token)

    write_date = {'token' : token}

    read = ReadYamlData()
    read.write_yaml_data(write_date)