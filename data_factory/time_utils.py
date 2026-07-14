"""当前时间工具类，支持两种输出格式"""

from datetime import datetime


class TimeUtils:
    """获取当前时间，按指定格式输出"""

    @staticmethod
    def get_current_time(fmt: str) -> str:
        """
        获取当前时间字符串
        :param fmt: "ydm" 返回 YYYY-MM-DD， "hms" 返回 YYYY-MM-DD HH:MM:SS
        :return: 格式化后的时间字符串
        """
        now = datetime.now()
        if fmt == "ydm":
            return now.strftime("%Y-%m-%d")
        elif fmt == "hms":
            return now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError(f"不支持的格式参数: {fmt}，仅支持 'ydm' 或 'hms'")
