import requests

class SendRequests(object):
    def __init__(self):
        pass

    def get(self, url, data, header):
        """

        :param url:请求地址
        :param data: 请求参数
        :param header: 请求头
        :return:json格式返回值
        """
        if header is None:
            res = requests.get(url = url, params = data)
        else:
            res = requests.get(url = url, params = data, headers = header)
        return res.json()

    def post(self, url, data, header):
        """

        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :return:json格式返回值
        """
        if header is None:
            res = requests.post(url = url, data = data, verify = False)
        else:
            res = requests.post(url = url, data = data, headers = header, verify = False)
        return res.json()

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def run_main(self, url, data, header, method):
        """

        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :param method: 请求方法
        :return:
        """
        if method.upper() == "GET":
            return self.get(url, data, header)
        elif method.upper() == "POST":
            return self.post(url, data, header)
        else:
            return print('暂时仅支持get/post请求！')
