import re

node_pattern = re.compile(r'"id":\s*"(\w+)",\s*"type":\s*"(\w+)",\s*"description":\s*"([^"]+)"')
condition_pattern = re.compile(r'"id":\s*"(\w+)",.*?"next":\s*\[\s*(.*?)\s*\]', re.DOTALL)
direct_connection_pattern = re.compile(r'"id":\s*"(\w+)",.*?"next":\s*"(\w+)"')


def compose_prompt(origin_prompt, user_input, results):
    actual_prompt = origin_prompt
    if "{question}" in origin_prompt:
        actual_prompt = origin_prompt.replace("{question}", user_input)
    for index, result in enumerate(results):
        if f"{{result{index + 1}}}" in actual_prompt:
            actual_prompt = actual_prompt.replace(f"{{result{index + 1}}}", result)
    return actual_prompt


def get_dot_format_data(data):
    # 提取所有节点信息（id、type 和 description）
    nodes = node_pattern.findall(data)
    # 提取条件和连接关系（带条件的 next）
    condition_connections = condition_pattern.findall(data)
    # 提取直接连接关系（无条件的 next）
    direct_connections = direct_connection_pattern.findall(data)
    # 构建ID到Description的映射
    id_to_description = {node[0]: node[2] for node in nodes}
    # 构建DOT格式数据
    dot = 'digraph flowchart {\n'

    # 添加节点并设置不同形状
    for node_id, node_type, description in nodes:
        if node_type == 'decision':
            dot += f'    "{description}" [shape=diamond];\n'  # 判断节点为菱形
        else:
            dot += f'    "{description}" [shape=box];\n'  # 行动节点为长方形

    # 处理带条件的连接关系，将ID映射为Description
    for source_id, connections_str in condition_connections:
        source_description = id_to_description.get(source_id, "Unknown")
        # 解析所有条件连接
        connection_items = re.findall(r'"condition":\s*"([^"]+)",\s*"id":\s*"(\w+)"', connections_str)
        for condition, target_id in connection_items:
            target_description = id_to_description.get(target_id, "Unknown")
            dot += f'    "{source_description}" -> "{target_description}" [label="{condition}"];\n'

    # 处理无条件的连接
    for source_id, target_id in direct_connections:
        source_description = id_to_description.get(source_id, "Unknown")  # 获取来源描述
        target_description = id_to_description.get(target_id, "Unknown")  # 获取目标描述
        dot += f'    "{source_description}" -> "{target_description}";\n'

    dot += '}'
    return dot


# 正则表达式，提取有效的DOT内容
dot_pattern = re.compile(r'digraph\s+[a-zA-Z0-9_]+\s*\{[^}]+\}', re.DOTALL)


def prevent_non_sense(dot_string):
    # 使用正则表达式提取内容
    dot_content = dot_pattern.search(dot_string)

    # 输出匹配的内容
    if dot_content:
        return dot_content.group()
