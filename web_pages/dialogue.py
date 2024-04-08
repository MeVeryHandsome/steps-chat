import os
from datetime import datetime
# from agent.qwen_agent import call_with_stream, call_with_messages
from agent.glm_agent import call_with_stream, call_with_messages
import streamlit as st
from streamlit_chatbox import *
import yaml

# 打开并读取YAML文件
with open('prompt.yaml', 'r', encoding='utf-8') as file:
    data: dict[str, str] = yaml.safe_load(file)['prompts']

chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatchat_icon_blue_square_v2.png"
    )
)


def dialogue_page():
    # 创建对话区域和输入区域
    st.title('大模型对话')

    greeting()

    chat_input_placeholder = "请输入对话内容，换行请使用Shift+Enter。输入/help查看自定义命令 "
    # 当用户提交问题时的逻辑
    if user_input := st.chat_input(chat_input_placeholder, key="prompt"):
        answer_by_steps(user_input)

    extra_btn()


def greeting():
    if call_with_messages.__module__ == "agent.glm_agent":
        model_name = "GLM-4"
    elif call_with_messages.__module__ == "agent.qwen_agent":
        model_name = "Qwen-turbo"
    else:
        model_name = "XChat"
    if not chat_box.chat_inited:
        st.toast(
            f"欢迎使用汽车任务规划系统! \n\n"
            f"当前运行的模型`{model_name}`, 您可以开始提问了."
        )
        chat_box.init_session()


def answer_by_steps(user_input):
    chat_box.reset_history()
    chat_box.user_say(user_input)
    chat_box.ai_say("正在思考...")
    prompt_list = list(data.values())
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
        for r in call_with_stream(only_one.format(question=user_input)):
            full_content += r
            chat_box.update_msg(full_content, streaming=True)
        chat_box.update_msg(full_content, streaming=False)
        return


def chain_of_thought(prompt_list, user_input):
    first = prompt_list.pop(0)
    last = prompt_list.pop(-1)
    result = call_with_messages(first.format(question=user_input))
    print(f"-----------第1次结果:\n{result}")
    for index, prompt in enumerate(prompt_list):
        final_prompt = prompt.format(question=result)
        result = call_with_messages(final_prompt)
        print(f"-----------第{index + 2}次结果:\n{result}")
    full_content = ''  # with incrementally we need to merge output.
    for r in call_with_stream(last.format(question=result)):
        full_content += r
        chat_box.update_msg(full_content, streaming=True)
    chat_box.update_msg(full_content, streaming=False)
    print(f"-----------最后一次结果:\n{full_content}")


def extra_btn():
    now = datetime.now()
    with st.sidebar:
        cols = st.columns(2)
        export_btn = cols[0]
        if cols[1].button(
                ":wastebasket: 清空",
                use_container_width=True,
        ):
            chat_box.reset_history()
            st.rerun()
    export_btn.download_button(
        ":file_folder: 导出",
        "".join(chat_box.export2md()),
        file_name=f"{now:%Y-%m-%d %H.%M}_对话记录.md",
        mime="text/markdown",
        use_container_width=True,
    )
