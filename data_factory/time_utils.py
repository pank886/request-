"""当前时间工具类，支持多种输出格式和时间偏移"""

from datetime import datetime, timedelta


class TimeUtils:
    """获取当前时间或偏移时间，按指定格式输出"""

    # ===== 基础常量 =====
    FMT_DATE = "%Y-%m-%d"
    FMT_DATETIME = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def get_current_time(fmt: str) -> str:
        """
        获取当前时间字符串
        :param fmt: "ydm" → YYYY-MM-DD， "hms" → YYYY-MM-DD HH:MM:SS
        :return: 格式化后的时间字符串
        """
        now = datetime.now()
        if fmt == "ydm":
            return now.strftime(TimeUtils.FMT_DATE)
        elif fmt == "hms":
            return now.strftime(TimeUtils.FMT_DATETIME)
        else:
            raise ValueError(f"不支持的格式参数: {fmt}，仅支持 'ydm' 或 'hms'")

    @staticmethod
    def get_offset_time(fmt: str,
                        days: int = 0,
                        hours: int = 0,
                        minutes: int = 0,
                        seconds: int = 0) -> str:
        """
        获取当前时间偏移指定量后的时间字符串。
        所有偏移参数可为负数（表示过去）。

        :param fmt:     "ydm" → 日期， "hms" → 日期+时间
        :param days:    偏移天数（默认 0）
        :param hours:   偏移小时数（默认 0）
        :param minutes: 偏移分钟数（默认 0）
        :param seconds: 偏移秒数（默认 0）
        :return: 格式化后的时间字符串

        示例:
            TimeUtils.get_offset_time("ydm", days=1)          # 明天日期
            TimeUtils.get_offset_time("hms", days=-1)         # 昨天此时
            TimeUtils.get_offset_time("hms", hours=2)         # 2小时后
            TimeUtils.get_offset_time("hms", days=1, hours=10) # 明天上午10点
        """
        now = datetime.now()
        offset = now + timedelta(days=int(days),
                                 hours=int(hours),
                                 minutes=int(minutes),
                                 seconds=int(seconds))
        if fmt == "ydm":
            return offset.strftime(TimeUtils.FMT_DATE)
        elif fmt == "hms":
            return offset.strftime(TimeUtils.FMT_DATETIME)
        else:
            raise ValueError(f"不支持的格式参数: {fmt}，仅支持 'ydm' 或 'hms'")
