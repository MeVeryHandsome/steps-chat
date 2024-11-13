from openai import OpenAI

client = OpenAI(api_key="sk-1c7148b9e750476a986b1fd33e261642", base_url="https://api.deepseek.com")

def call_with_messages(prompt):
    messages = [{'role': 'system', 'content': '你是行至智能公司的军事领域大模型'},
                {'role': 'user', 'content': prompt}]
    print("\n正在发起单次提问请求")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )
    if response:
        return response.choices[0].message.content
    else:
        raise Exception('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


def call_with_stream(prompt):
    messages = [{'role': 'system', 'content': '你是行至智能公司的军事领域大模型'},
                {'role': 'user', 'content': prompt}]
    responses = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
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