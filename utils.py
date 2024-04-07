from http import HTTPStatus
import dashscope

def call_with_messages(prompt):
    messages = [{'role': 'system', 'content': '你是一名汽车车控系统专家'},
                {'role': 'user', 'content': prompt}]
    print("\n正在发起单次提问请求")
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
        api_key='sk-7336b609d03b4646acf0d874a6a95554',
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        raise Exception('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


def call_with_stream(prompt):
    messages = [{'role': 'user', 'content': prompt}]
    responses = dashscope.Generation.call("qwen-turbo",
                                          messages=messages,
                                          result_format='message',  # set the result to be "message" format.
                                          stream=True,  # set stream output.
                                          incremental_output=True,  # get streaming output incrementally.
                                          api_key='sk-7336b609d03b4646acf0d874a6a95554',
                                          )
    print("\n正在发起流式回答请求")
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            now_content = response.output.choices[0]['message']['content']
            yield now_content
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))