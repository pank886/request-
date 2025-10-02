from readyaml import ReadYamlData

import random

class DebugTalk:

    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self, data, randoms):
        if randoms not in [0, 1]:
            return data[randoms - 1]

    def get_extract_data(self, node_name, randoms = None):
        """
        读取extract.yaml的数据
        :param node_name: 读取extract.yaml文件中的key值
        :param random: None 数组顺序展示 0 随机读取 -1 字符串展示
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms : self.get_extract_order_data(data, randoms),
                0 : random.choice(data),
                -1 : ','.join(data)
            }
            data = data_value[randoms]
        return data



if __name__ == '__main__':
    debug = DebugTalk()
    print(debug.get_extract_data('rerev', 3))
