import json
import re

import requests

def execute_command(response):
    status = True
    schedule_code = parse_schedule_data(response)
    headers = {'Content-Type': 'application/json'}
    url = "http://127.0.0.1:4321/api/apiCmd"
    for each_code in schedule_code:
        try:
            print(each_code)
            response = requests.post(url, headers=headers, json=each_code, timeout=5)
            response.raise_for_status()  # 检查是否有HTTP错误
        except requests.exceptions.RequestException as e:
            print('请求失败:', e)
            status = False
    return status

def parse_schedule_data(data):
    """
    解析并打印给定 JSON 字符串中的调度数据。
    :param data: 包含 JSON 数据的字符串
    """
    result = []
    data = extract_instruction_sequence(data)
    for sequence in data:
        for schedule in sequence["调度数据"]:
            result.append(schedule)
    return result

def extract_instruction_sequence(json_str):
    """
    提取 JSON 数据中的 "指令序列" 部分并转换为列表。

    :param json_str: 包含 JSON 数据的字符串
    :return: "指令序列" 部分的列表
    """
    # 使用正则表达式匹配 "指令序列" 后的内容
    match = re.search(r'"指令序列":\s*(\[.*\])', json_str, re.DOTALL)
    if match:
        instruction_sequence_str = match.group(1)
        # 将匹配到的内容转换为列表
        instruction_sequence = json.loads(instruction_sequence_str)
        return instruction_sequence
    else:
        raise ValueError('"指令序列" 部分未找到')