import os
import sys
import logging

DIR_PATH = os.path.dirname(os.path.dirname(__file__))

sys.path.append(DIR_PATH)

#log日志的输出级别
LOG_LEVEL = logging.DEBUG #输出到文件的级别
STRNEM_LOG_LEVEL = logging.DEBUG #输出到控制台的级别

#文件路径
FILE_PATH = {
    'extract' : os.path.join(DIR_PATH, 'extract'),
    'conf' : os.path.join(DIR_PATH, 'conf', 'config.ini'),
    'LOG': os.path.join(DIR_PATH, 'log')
}

