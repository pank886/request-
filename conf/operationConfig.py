import configparser

from conf.setting import FILE_PATH

class OperationConfig:
    """封装读取ini配置文件"""


    def __init__(self, file_path = None):

        if file_path is None:
            self.__file_path = FILE_PATH['conf']
        else:
            self.__file_path = file_path
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__file_path, encoding='utf-8')
        except Exception as e:
            print(e)

    def get_section_for_data(self, section, option):
        """
        读取ini数据

        """
        try:
            return self.conf.get(section, option)
        except Exception as e:
            print(e)

    def get_envi(self, option):
        """获取接口服务器ip地址"""
        return self.conf.get_section_for_data('api_envi', option)

    def get_MySQL(self, option):
        """获取接口服务器ip地址"""
        return self.conf.get_section_for_data('MySQL', option)


if __name__ == '__main__':
    open = OperationConfig()
    print(open.get_section_for_data('api_envi', 'host'))