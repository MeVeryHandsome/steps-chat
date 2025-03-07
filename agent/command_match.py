from openai import OpenAI

client = OpenAI(api_key="sk-1c7148b9e750476a986b1fd33e261642", base_url="http://123.57.244.236:17300/v1")

def call_with_messages(messages):
    print("\n正在发起单次提问请求")
    response = client.chat.completions.create(
        model="/home/vllm_model_dir/qwen2.5-1.5b_command_model_250304_1-ckpt-116",
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


def call_with_stream(messages):
    responses = client.chat.completions.create(
        model="/home/vllm_model_dir/qwen2.5-1.5b_command_model_250304_1-ckpt-116",
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