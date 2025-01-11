'''
Author: yinyabo yinyabo@2802701695.com
Date: 2025-01-08 14:17:54
LastEditors: yinyabo yinyabo@2802701695.com
LastEditTime: 2025-01-08 16:06:26
FilePath: /steps-chat/routes/views.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from openai import OpenAI
from flask_cors import cross_origin
from web_pages.dialogue import answer_by_steps
from . import routes_bp  # 导入蓝图
from flask import Response, request, jsonify, app, stream_with_context
import os
from datetime import datetime

client = OpenAI(api_key="sk-f0977ac310804fc2a09dce4084bea9d3", base_url="https://api.deepseek.com")

# 健康检查接口
@routes_bp.route('/health', methods=['GET'])
def health_check():
    print("成功调用健康")
    def generate_numbers():
        import time
        for number in range(1, 100000):
            yield f"{number}\n"  # 每次生成一个数字就发送 \n 最好不要删除
            time.sleep(0.001)  # 为了演示，加入短暂延迟

    return Response(generate_numbers())


# 普通请求接口
@routes_bp.route('/chat', methods=['POST','GET'])
@cross_origin()
def chat():
    user_input=None
    if request.method == 'POST' and request.is_json:
        user_input = request.json.get('user_input', user_input)  # 获取 JSON 中的 'user_input'
    # 处理 GET 请求中的查询参数
    if request.method == 'GET':
        user_input = request.args.get('user_input', user_input)  # 获取 GET 请求中的 'user_input'
    return Response(stream_with_context(answer_by_steps(user_input)), content_type='text/plain; charset=utf-8')
