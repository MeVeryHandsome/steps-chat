import os
from datetime import datetime
import streamlit as st
from streamlit_chatbox import *
from utils.config_utils import header, prompt_data, call_with_messages, call_with_stream

chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatchat_icon_blue_square_v2.png"
    )
)


# 对话主界面逻辑
def dialogue_page():
    # 创建对话区域和输入区域
    st.title(header)

    greeting()

    chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter。"
    # 当用户提交问题时的逻辑
    if user_input := st.chat_input(chat_input_placeholder, key="prompt"):
        answer_by_steps(user_input)

    extra_btn()


# 欢迎提示框
def greeting():
    if call_with_messages.__module__ == "agent.glm_agent":
        model_name = "GLM-4"
    elif call_with_messages.__module__ == "agent.qwen_agent":
        model_name = "Qwen-Max"
    else:
        model_name = "XChat"
    if not chat_box.chat_inited:
        st.toast(
            f"欢迎使用{header}! \n\n"
            f"当前运行的模型`{model_name}`, 您可以开始使用了."
        )
        chat_box.init_session()
    chat_box.output_messages()


# 分步回答
def answer_by_steps(user_input):
    chat_box.reset_history()
    chat_box.user_say(user_input)
    prompt_list = prompt_data.copy()
    length = len(prompt_list)
    if length == 0:
        message = "没有对应提示词，请确认后重试"
        chat_box.update_msg(message, streaming=False)
        return
    if length > 1:
        chain_of_thought(prompt_list, user_input)
    else:
        only_one = prompt_list.pop(-1)
        full_content = ''
        for r in call_with_stream(only_one["prompt"].format(question=user_input)):
            full_content += r
            chat_box.update_msg(full_content, streaming=True)
        chat_box.update_msg(full_content, streaming=False)
        return


# 思维链
def chain_of_thought(prompt_list, user_input):
    first_prompt = prompt_list.pop(0)["prompt"]
    last_prompt = prompt_list.pop(-1)["prompt"]
    execution_failed = False
    all_messages = init_all_steps()
    chat_box.ai_say(all_messages)
    results = []
    # 第一次调用
    execution_failed = first_step(execution_failed, first_prompt, user_input, results)

    # 中间过程
    execution_failed = intermediate_steps(execution_failed, prompt_list, user_input, results)

    # 最后一次流式回答
    final_step(execution_failed, last_prompt, user_input, results)


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
        result = call_with_messages(first_prompt.format(question=user_input))

        chat_box.update_msg(result, expanded=True, element_index=0, streaming=False, state="complete")
        chat_box.update_msg("进行中...", element_index=1, streaming=False, expanded=True)
        print(f"-----------第1次结果:\n{result}")
        print("------------第一次结束\n")
        results.append(result)
    except Exception as e:
        print(e)
        chat_box.update_msg('<font color="red">网络异常，请重试</font>', element_index=0, streaming=False, state="error")
        execution_failed = True
    return execution_failed


def intermediate_steps(execution_failed, prompt_list, user_input, results):
    if execution_failed:
        for index in range(len(prompt_list)):
            chat_box.update_msg('<font color="red">前序步骤出错，暂停执行</font>', element_index=index + 1,
                                streaming=False, expanded=True, state="error")
    else:
        for index, content in enumerate(prompt_list):
            try:
                actual_prompt = compose_prompt(content["prompt"], user_input, results)

                result = call_with_messages(actual_prompt)

                chat_box.update_msg(element_index=index, expanded=False)
                chat_box.update_msg(result, element_index=index + 1, streaming=False, expanded=True, state="complete")
                chat_box.update_msg("进行中...", element_index=index + 2, streaming=False, expanded=True)
                print(f"-----------第{index + 2}次结果:\n{result}")
                print(f"------------第{index + 2}次结束\n")
                results.append(result)
            except Exception as e:
                print(e)
                chat_box.update_msg('<font color="red">网络异常，请重试</font>', element_index=index + 1,
                                    streaming=False, state="error")
                execution_failed = True

    return execution_failed


def final_step(execution_failed, last_prompt, user_input, results):
    if execution_failed:
        chat_box.update_msg('<font color="red">前序步骤出错，暂停执行</font>', element_index=-1, streaming=False,
                            expanded=True, state="error")
    else:
        full_content = ''  # with incrementally we need to merge output.
        try:
            for r in call_with_stream(compose_prompt(last_prompt, user_input, results)):
                full_content += r
                chat_box.update_msg(full_content, element_index=-1, streaming=True, expanded=True)
            chat_box.update_msg(element_index=-2, expanded=False)
            chat_box.update_msg(full_content, element_index=-1, streaming=False, state="complete")
            print(f"-----------最后一次结果:\n{full_content}")
            print("-----------最后一次结束\n")
        except Exception as e:
            print(e)
            chat_box.update_msg(full_content + '<br/><br/><font color="red">网络异常，请重试</font>', element_index=-1,
                                streaming=False, state="error")


def init_all_steps():
    all_messages = [Markdown("进行中", in_expander=True, expanded=False, title=prompt_data[0]["title"])]
    for i in range(1, len(prompt_data)):
        all_messages.append(Markdown("等待中...", in_expander=True,
                                     expanded=False, title=prompt_data[i]["title"]))
    return all_messages


# 额外按钮（包括新建对话与导出记录）
def extra_btn():
    now = datetime.now()
    with st.sidebar:
        new_btn = st.container()
        export_btn = st.container()
        # 新建对话（删除历史记录，刷新页面）
        if new_btn.button(
                ":speech_balloon: 新建对话",
                use_container_width=True,
        ):
            chat_box.reset_history()
            st.rerun()

    # 导出记录（下载chat_box导出的markdown内容）
    export_btn.download_button(
        ":file_folder: 导出记录",
        "".join(chat_box.export2md()),
        file_name=f"{now:%Y-%m-%d %H.%M}_对话记录.md",
        mime="text/markdown",
        use_container_width=True,
    )
