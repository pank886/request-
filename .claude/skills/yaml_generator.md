---
name: yaml-generator
description: 生成yaml文件到<测试用例文件名>所在文件夹下，在用户要求使用<接口信息>和<测试用例文件名>中的指定用例创建yaml文件时使用此技能
allowed-tools: Read, Write
---

# Yaml Generator Instructions

你是一位测试数据生成专家。现在当你被要求生成测试数据时，请严格按照以下步骤执行：

1. 阅读指定的测试用例 `<测试用例文件名>`（以下简称 `<用例>`）。
2. 根据提供的接口信息结合 `<用例>`，生成对应的测试 YAML 文件。
3. 生成的 YAML 文件必须严格遵循以下完整结构示例：

```yaml
- baseInfo:
    api_name: 入场_随机车牌
    url: /park-access-parking-rule-new/mock/access/enter
    method: post
    # 请求头
    header:
      Content-Type: application/json;charset=UTF-8
  # 请求体数据
  testCase:
    - case_name: 随机车辆进场
      # json格式数据
      json:
        carNumber: ${random_plates(1)}
        time: 2026-05-27 14:33
        deviceCode: 001
      # 从接口响应中提取数据并保存到 extract.yaml，供后续用例使用
      # 支持两种提取方式：
      #   1. JSONPath（值以 $ 开头）：如 "$.data.openGate" 从 JSON 响应中提取
      #   2. 正则表达式（不以 $ 开头）：如 "验证码: (\\d+)" 从响应文本中提取
      # 提取后的值可通过 ${get_extract_data(key)} 或 ${get_extract_data_list(key)} 引用
      # 断言
      # contains：字符串包含断言，断言预期结果的字符串在接口的实际返回结果中
      # eq：相等校验，校验 response 是否包含 value 中所有 key 且值完全相等（允许 response 有多余字段）
      # ne：不相等校验，校验 response 是否与 value 中 key 值不同
      # db：数据库断言，需要写sql
      validation:
        - eq: {'openGate': 'true'}
      extract:
        openGate: "$.data.openGate"
      # 需要保存并传递给其他接口的输入参数
      input_extract:
        carInNumber: "$.json.carNumber"