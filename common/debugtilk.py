import random

from common.readyaml import ReadYamlData
from data_factory import PlateGenerator, TimeUtils


class DebugTalk:

    def __init__(self):
        self.read = ReadYamlData()

    def _resolve_extract_data(self, data, randoms):
        """共用提取逻辑"""
        if randoms is None:
            return data
        randoms = int(randoms)
        if randoms == 0:
            return random.choice(data)
        if randoms == -1:
            return ','.join(data)
        return data[randoms - 1]

    def get_extract_data(self, node_name, sec_node_name=None, randoms=None):
        """
        读取extract.yaml的数据
        :param node_name: 读取extract.yaml文件中的key值
        :param sec_node_name: 读取嵌套的key值
        :param randoms: None 数组顺序展示 0 随机读取 -1 字符串展示
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if sec_node_name is not None:
            data = data[sec_node_name]
        return self._resolve_extract_data(data, randoms)

    def get_extract_data_list(self, node_name, randoms=None):
        """
        读取extract.yaml的数据
        :param node_name: 读取extract.yaml文件中的key值
        :param randoms: None 数组顺序展示 0 随机读取 -1 字符串展示
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        return self._resolve_extract_data(data, randoms)

    def random_plates(self, count):
        """
        生成指定数量的不重复随机车牌，自动全局去重并持久化
        :param count: 车牌个数；传入 "clear" 清空所有已生成记录
        :return: 逗号分隔的车牌字符串
        """
        return PlateGenerator().generate(count)

    def get_current_time(self, fmt):
        """
        获取当前时间字符串
        :param fmt: "ydm" → "2026-05-27"， "hms" → "2026-05-27 14:33:00"
        :return: 格式化后的时间字符串
        """
        return TimeUtils.get_current_time(fmt)

    def get_offset_time(self, fmt, days=0, hours=0, minutes=0, seconds=0):
        """
        获取偏移后的时间字符串（可指定天/时/分/秒偏移，负数=过去）
        :param fmt:     "ydm" 仅日期， "hms" 日期+时间
        :param days:    偏移天数，默认 0，负数表示过去
        :param hours:   偏移小时，默认 0
        :param minutes: 偏移分钟，默认 0
        :param seconds: 偏移秒数，默认 0
        :return: 格式化后的时间字符串

        YAML 调用示例:
            ${get_offset_time(ydm, 1)}               → 明天日期
            ${get_offset_time(hms, -1)}              → 昨天此刻
            ${get_offset_time(ydm, 7)}               → 7天后日期
            ${get_offset_time(hms, 0, 2)}            → 2小时后
            ${get_offset_time(hms, 0, 0, 30)}        → 30分钟后
            ${get_offset_time(hms, 1, 10)}           → 明天上午10点
            ${get_offset_time(hms, -1, 0)}           → 昨天此刻
            ${get_offset_time(hms, 0, 0, -30)}       → 30分钟前
        """
        return TimeUtils.get_offset_time(
            fmt,
            days=int(days) if days else 0,
            hours=int(hours) if hours else 0,
            minutes=int(minutes) if minutes else 0,
            seconds=int(seconds) if seconds else 0,
        )

    def split_extract_data(self, node_name, index=0):
        """
        从extract.yaml中读取逗号拼接的数据，按索引拆分为单个
        :param node_name: extract.yaml中的key值
        :param index: 索引（0开始），取第N个元素
        :return: 拆分后的单个值
        """
        raw = str(self.read.get_extract_yaml(node_name))
        parts = [p.strip() for p in raw.split(',')]
        idx = int(index)
        return parts[idx] if idx < len(parts) else parts[0]
