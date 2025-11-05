import logging
import os
import time

from logging.handlers import RotatingFileHandler #按文件大小滚动备份

from conf import setting

log_path = setting.FILE_PATH['LOG']
if not os.path.exists(log_path):
    os.makedirs(log_path, exist_ok=True)

logfile_name = log_path + r'\test.{}.log'.format(time.strftime("%Y%m%d%H%M%S"))

class RecordLog:
    """封装日志"""

    def output_logging(self):
        """获取logger对象"""
        logger = logging.getLogger(__name__)
        #防止打印重复日志
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVEL)
            log_format = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s')
            #日志输出到指定文件
            fh = RotatingFileHandler(filename= logfile_name, mode= 'a', maxBytes= 5242880, backupCount= 7, encoding= 'utf-8')
            #maxBytes：控制文件大小，单位是字节；backupCount：控制日志文件数量；mode：写入方式
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(log_format)

            #将相应的handler添加到logger
            logger.addHandler(fh)

            #将日志输出到控制台上
            sh = logging.StreamHandler()
            sh.setLevel(setting.STRNEM_LOG_LEVEL)
            sh.setFormatter(log_format)
            logger.addHandler(sh)

        return logger

apilog = RecordLog()
logs = apilog.output_logging()