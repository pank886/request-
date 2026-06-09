"""数据工厂：路径管理 + 统一对外接口"""

import os
from conf import setting

build_id = os.environ.get("BUILD_NUMBER",
                          os.environ.get("CI_JOB_ID", "local"))
workspace = os.environ.get("WORKSPACE",
                           os.environ.get("CI_PROJECT_DIR", setting.DIR_PATH))
DATA_DIR = os.path.join(workspace, "data")
os.makedirs(DATA_DIR, exist_ok=True)


def data_path(name):
    """生成带 CI 隔离的数据文件路径"""
    return os.path.join(DATA_DIR, f"{name}_{build_id}.txt")


from data_factory.plate_generator import PlateGenerator
