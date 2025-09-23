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

if __name__ == '__main__':
    res = get_testcase_yaml('logen.yaml')
    print(res)