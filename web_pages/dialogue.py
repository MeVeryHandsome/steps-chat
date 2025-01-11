import os
from datetime import datetime

from utils.config_utils import header, prompt_data, call_with_messages, call_with_stream
from utils.exec_cmd import execute_command




# 分步回答
def answer_by_steps(user_input):
    #需要实现yield
    print("!!!!!!!!!!!!!")
    prompt_list = prompt_data.copy()
    length = len(prompt_list)
    if length == 0:
        message = "没有对应提示词，请确认后重试"
        print(message)
    elif length > 1:
        for result in chain_of_thought(prompt_list, user_input):
            yield result
    else:
        only_one = prompt_list.pop(-1)
        full_content = ''
        for r in call_with_stream(compose_prompt(only_one["prompt"], user_input, [])):
            full_content += r
            yield(r)
        


# 思维链
def chain_of_thought(prompt_list, user_input):
    first=prompt_list.pop(0)
    first_prompt = first["prompt"]
    first_title=first["title"]
    last=prompt_list.pop(-1)
    last_prompt = last["prompt"]
    last_title=last["title"]
    execution_failed = False
    results = []
    # 第一次调用
    yield first_title+'\n'
    for result in first_step(execution_failed, first_prompt, user_input, results):
        yield result
    yield '\n\n\n'

    yield prompt_list[0]["title"]+'\n'
    # 中间过程
    for result in intermediate_steps(execution_failed, prompt_list, user_input, results):
        yield result
    yield '\n\n\n'

    # 最后一次流式回答
    yield last_title+'\n'
    for result in final_step(execution_failed, last_prompt, user_input, results):
        yield result

def compose_prompt(origin_prompt, user_input, results):
    actual_prompt = origin_prompt
    if "{question}" in origin_prompt:
        actual_prompt = origin_prompt.replace("{question}", user_input)
    for index, result in enumerate(results):
        if f"{{result{index + 1}}}" in actual_prompt:
            actual_prompt = actual_prompt.replace(f"{{result{index + 1}}}", result)
    return actual_prompt


def first_step(execution_failed, first_prompt, user_input, results):
    try:
        full_result = ""
        for result in call_with_stream(compose_prompt(first_prompt, user_input, results)):
            full_result += result
            yield result
        print(f"-----------第1次结果:\n{full_result}")
        print("------------第一次结束\n")
        results.append(full_result)
    except Exception as e:
        print(e)
        print('<font color="red">网络异常，请重试</font>')
        execution_failed = True
    return execution_failed


def intermediate_steps(execution_failed, prompt_list, user_input, results):
    if execution_failed:
        for index in range(len(prompt_list)):
            print('<font color="red">前序步骤出错，暂停执行</font>')
    else:
        for index, content in enumerate(prompt_list):
            try:
                actual_prompt = compose_prompt(content["prompt"], user_input, results)
                full_result = ""
                for result in call_with_stream(actual_prompt):
                    full_result+=result
                    yield result

                # chat_box.update_msg(element_index=index, expanded=False)
                # chat_box.update_msg(result, element_index=index + 1, streaming=False, expanded=True, state="complete")
                # chat_box.update_msg("进行中...", element_index=index + 2, streaming=False, expanded=True)
                print(f"-----------第{index + 2}次结果:\n{full_result}")
                print(f"------------第{index + 2}次结束\n")
                results.append(full_result)
            except Exception as e:
                print(e)
                # chat_box.update_msg('<font color="red">网络异常，请重试</font>', element_index=index + 1,
                #                     streaming=False, state="error")
                execution_failed = True

    return execution_failed


def final_step(execution_failed, last_prompt, user_input, results):
    if execution_failed:
        pass
        # chat_box.update_msg('<font color="red">前序步骤出错，暂停执行</font>', element_index=-1, streaming=False,
        #                     expanded=True, state="error")
    else:
        full_result = "" # with incrementally we need to merge output.
        try:
            for r in call_with_stream(compose_prompt(last_prompt, user_input, results)):
                full_result+=r
                yield r
                # chat_box.update_msg(full_content, element_index=-1, streaming=True, expanded=True)
            # chat_box.update_msg(element_index=-2, expanded=False)
            # chat_box.update_msg(full_content, element_index=-1, streaming=False, state="complete")
            print(f"-----------最后一次结果:\n{full_result}")
            print("-----------最后一次结束\n")
            # if execute_command(full_content):
            #     st.toast("执行成功", icon='🎉')
            # else:
            #     st.toast("网络波动，请重试", icon='🛜')
        except Exception as e:
            print(e)
            # chat_box.update_msg(full_content + '<br/><br/><font color="red">网络异常，请重试</font>', element_index=-1,
            #                     streaming=False, state="error")


# def init_all_steps():
#     all_messages = [Markdown("进行中", in_expander=True, expanded=False, title=prompt_data[0]["title"])]
#     for i in range(1, len(prompt_data)):
#         all_messages.append(Markdown("等待中...", in_expander=True,
#                                      expanded=False, title=prompt_data[i]["title"]))
#     return all_messages
