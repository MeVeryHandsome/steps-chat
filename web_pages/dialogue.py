import os
from datetime import datetime

import streamlit as st
from streamlit_chatbox import *
from utils.config_utils import header, prompt_data, call_with_messages, call_with_stream, diagram_prompt
from utils.prompt_utils import compose_prompt

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


# 欢迎提示框
def greeting():
    if call_with_messages.__module__ == "agent.glm_agent":
        model_name = "行至军事大模型"
    elif call_with_messages.__module__ == "agent.qwen_agent":
        model_name = "行至军事大模型"
    else:
        model_name = "行至军事大模型"
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
    if length >= 1:
        chain_of_thought(prompt_list, user_input)


# 思维链
def chain_of_thought(prompt_data, user_input):
    all_messages = init_all_steps()
    chat_box.ai_say(all_messages)
    results, execution_failed = intermediate_steps(prompt_data, user_input)
    if not execution_failed:
        show_diagram(diagram_prompt, results)


def init_all_steps():
    all_messages = [Markdown("进行中", in_expander=True, expanded=False, title=prompt_data[0]["title"])]
    for i in range(1, len(prompt_data)):
        all_messages.append(Markdown("等待中...", in_expander=True,
                                     expanded=False, title=prompt_data[i]["title"]))
    return all_messages


def intermediate_steps(prompt_list, user_input):
    results = []
    execution_failed = False
    index = 0
    for content in prompt_list:
        try:
            actual_prompt = compose_prompt(content["prompt"], user_input, results)
            return_type = content["type"]

            if return_type == "stream":
                result = ''
                for r in call_with_stream(actual_prompt):
                    result += r
                    chat_box.update_msg(result, element_index=index, expanded=True, streaming=True)
                chat_box.update_msg(result, element_index=index, streaming=False, state="complete")
            elif return_type == "normal":
                result = call_with_messages(actual_prompt)
                chat_box.update_msg(result, element_index=index, streaming=False, expanded=True, state="complete")

            if index < len(prompt_list) - 1:
                chat_box.update_msg("进行中...", element_index=index + 1, streaming=False, expanded=True)

            print(f"-----------第{index + 1}次结果:\n{result}")
            print(f"------------第{index + 1}次结束\n")
            results.append(result)
            index += 1

        except Exception as e:
            print(e)
            chat_box.update_msg('<font color="red">网络异常，请重试</font>', element_index=index,
                                streaming=False, state="error")
            execution_failed = True
            break

    if execution_failed:
        for i in range(index + 1, len(prompt_list)):
            chat_box.update_msg('<font color="red">前序步骤出错，暂停执行</font>', element_index=i,
                                streaming=False, expanded=True, state="error")
    return results, execution_failed


def show_diagram(diagram_prompt, results):
    actual_prompt = compose_prompt(diagram_prompt, '', results)
    result = call_with_messages(actual_prompt)
    print(result)
 # 使用 expander 模拟弹窗显示
    try:
        with st.expander("点击查看流程图", expanded=False):
            st.graphviz_chart(result)
    except Exception as e:
        print(e)