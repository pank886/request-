# PyCharmMiscProject

基于 **pytest + Allure + YAML** 的接口自动化测试框架，用于大麦IoT停车管理系统（park-base）的 API 测试。

## 项目结构

```
PyCharmMiscProject/
├── base/                       # 核心引擎
│   └── apiutil.py              # 请求基类：YAML解析、${}占位符替换、数据提取、断言调度
├── common/                     # 公共模块
│   ├── assertions.py           # 断言引擎（contains / eq / ne / db 四种模式）
│   ├── sendrequests.py         # HTTP 请求封装（带超时重试）
│   ├── readyaml.py             # YAML 读写工具（提取变量持久化到 extract.yaml）
│   ├── debugtilk.py            # YAML 中调用的动态函数（车牌生成、时间获取等）
│   ├── connection.py           # MySQL 数据库连接与查询
│   └── recordlog.py            # 日志模块
├── conf/                       # 配置
│   ├── setting.py              # 路径常量、日志级别
│   └── operationConfig.py      # INI 配置文件读取（环境地址、数据库连接）
├── data_factory/               # 数据工厂
│   ├── plate_generator.py      # 随机车牌生成器（自动去重、持久化、上限2000）
│   └── time_utils.py           # 时间工具类
├── testcase/                   # 测试用例（YAML 数据驱动）
│   ├── VehicleAccess/          # 车辆进出场业务（包月/白名单/临停/多场地）
│   ├── SubConfiguration/       # 子配置管理
│   ├── ParkingBase/            # 停车基础
│   ├── VehicleAccess_001/      # 车辆进出场扩展用例
│   └── 园区基线/               # 园区基线测试
├── run.py                      # 测试执行入口（支持路径/marker筛选，自动生成Allure报告）
├── conftest.py                 # pytest fixtures（登录获取token、清理、前后置）
├── pytest.ini                  # pytest 配置
├── extract.yaml                # 运行时变量存储（自动生成，不入库）
└── data/                       # 数据文件（车牌记录持久化）
```

## 快速开始

### 环境要求

- Python 3.8+
- Allure 命令行工具（[下载地址](https://github.com/allure-framework/allure2/releases)）

### 安装

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置

1. 在 `conf/config.ini` 中配置环境地址和数据库连接：

```ini
[api_envi]
host = https://dev.damaiiot.com:40443

[MySQL]
host = your-mysql-host
port = 3306
user = your-user
password = your-password
database = your-database
```

2. 确保 `run.py` 中的 `ALLURE` 路径指向本机 Allure 安装目录：

```python
ALLURE = r"E:\pycharm-2025.1\allure\allure-2.21.0\bin\allure.bat"
```

### 运行测试

```bash
# 运行全部用例
python run.py

# 指定路径运行
python run.py -p testcase/SubConfiguration/

# 指定 marker 运行
python run.py -m danyuan       # 单元测试
python run.py -m mayan         # 冒烟测试
python run.py -m hg            # 回归测试

# 路径 + marker 组合
python run.py -p testcase/ -m danyuan
```

也可以直接用 pytest：

```bash
pytest -c pytest.ini --alluredir=./report/temp
```

### 查看报告

`run.py` 执行完毕后会自动打开浏览器展示 Allure HTML 报告（默认端口 63333）。

手动生成报告：

```bash
allure generate ./report/temp -o ./report/html --clean
allure open ./report/html
```

## YAML 测试用例编写

测试用例使用 YAML 文件定义，每个文件包含一个 `baseInfo` + `testCase` 列表：

```yaml
# 示例：车辆进场接口
- baseInfo:
    api_name: "车辆进场"
    url: /park-base-api/carIn
    method: POST
    header:
      Content-Type: "application/json;charset=UTF-8"

  testCase:
    - case_name: "临停车进场成功"
      json:
        carNumber: ${random_plates(1)}
        parkCode: "test"
        entryTime: ${get_current_time(hms)}
      validation:
        - contains:           # 包含断言
            $.code: "200"
        - eq:                 # 相等断言
            $.success: true
      extract:                # 从响应提取变量
        carCode: $.data.carCode
        plateNumber: '"plateNumber":"(.*?)"'
```

### 断言模式

| 模式 | 关键字 | 说明 |
|------|--------|------|
| 包含断言 | `contains` | 验证实际值**包含**预期字符串 |
| 相等断言 | `eq` | 验证实际值与预期值**完全相等** |
| 不相等断言 | `ne` | 验证实际值与预期值**不相等** |
| 数据库断言 | `db` | 验证数据库中**存在**对应记录 |

### 动态函数（`${}` 占位符）

YAML 中可通过 `${函数名(参数)}` 调用内置函数：

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_extract_data(key)` | 读取 extract.yaml 中的变量 | `${get_extract_data(carCode)}` |
| `random_plates(n)` | 生成 n 个不重复随机车牌 | `${random_plates(1)}` |
| `get_current_time(fmt)` | 获取当前时间，`ydm`=日期，`hms`=日期时间 | `${get_current_time(hms)}` |
| `split_extract_data(key, i)` | 拆分逗号拼接数据，取第 i 个 | `${split_extract_data(carCode, 0)}` |

### 数据提取

支持从响应中提取变量并存储到 `extract.yaml`，后续用例可直接引用：

- **JSONPath 提取**：`"carCode": "$.data.carCode"`
- **正则提取**：`"plateNumber": '"plateNumber":"(.*?)"'`
- **输入参数提取**：`input_extract` 支持从请求参数中提取数据

## Markers 说明

| Marker | 说明 |
|--------|------|
| `mayan` | 冒烟测试 |
| `danyuan` | 单元测试 |
| `hg` | 回归测试 |
| `functional` | 测试方法 |

## 核心特性

- **YAML 数据驱动**：测试用例与代码分离，数据变更无需改代码
- **自动化登录**：`conftest.py` 中 session 级别 fixture 自动登录并注入 token
- **请求重试**：遇到 5xx 状态码自动重试（最多 3 次，退避因子 2）
- **Allure 报告**：自动收集请求/响应详情、断言结果，生成可视化报告
- **车牌生成器**：自动去重持久化，支持跨用例全局唯一（上限 2000）
- **数据库断言**：支持直接查询 MySQL 验证数据落库
- **CI 友好**：通过环境变量 `BUILD_NUMBER` / `CI_JOB_ID` 实现 CI 环境数据隔离

## 分支说明

- `master` — 开发主分支
- `main` — 稳定发布分支

## License

Internal use only.
