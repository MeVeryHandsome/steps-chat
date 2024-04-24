from zhipuai import ZhipuAI

client = ZhipuAI(api_key="24ff451cc3f957641db8b3485156156b.Xj7jZ0h9SHYu9Klg")


def call_with_messages(prompt):
    messages = [{'role': 'system', 'content': '你是一名汽车车控系统专家'},
                {'role': 'user', 'content': prompt}]
    print("\n正在发起单次提问请求")
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
        temperature=0.25,
        max_tokens=8192
    )
    if response:
        return response.choices[0].message.content
    else:
        raise Exception('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


def call_with_stream(prompt):
    messages = [{'role': 'user', 'content': prompt}]
    responses = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        stream=True,
        temperature=0.05,
        max_tokens=8192
    )
    print("\n正在发起流式回答请求")
    for response in responses:
        if response:
            now_content = response.choices[0].delta.content
            yield now_content
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return
