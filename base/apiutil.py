import json

from common.readyaml import get_testcase_yaml, ReadYamlData

from common.debugtilk import DebugTalk

from conf.operationConfig import OperationConfig

class BassRequests:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()

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

    def specifcation_yaml(self, case_info):
        """
        规范yaml测试用例写法
        case_info: list类型，调试取case_info[0]-->dict
        """
        pass

if __name__ == '__main__':
    data = get_testcase_yaml('../testcase/Login/logen.yaml')

    print(data)
    base = BassRequests()
    str_data = base.replace_load(data)
    print(str_data)