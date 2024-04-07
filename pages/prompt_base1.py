import streamlit as st


# 添加或更新提示
def update_prompts():
    # 将当前的提示框内容保存到缓存中
    prompts = [st.session_state[f'prompt_{i}'] for i in range(st.session_state['num_prompts'])]
    if prompts:
        st.session_state['cached_prompts'] = prompts


# 取消更新并恢复到之前的提示
def cancel_update():
    # 检查是否有缓存的提示，如果有，则恢复
    if 'cached_prompts' in st.session_state:
        for i, prompt in enumerate(st.session_state['cached_prompts']):
            st.session_state[f'prompt_{i}'] = prompt
        st.session_state['num_prompts'] = len(st.session_state['cached_prompts'])


def add_prompt():
    # 增加提示框数量的回调函数
    st.session_state['num_prompts'] += 1


def prompt_base_page():
    # 初始化
    if 'num_prompts' not in st.session_state:
        st.session_state['num_prompts'] = 1
    if 'cached_prompts' not in st.session_state:
        st.session_state['cached_prompts'] = []

    st.title('多轮对话提示设置')

    # 渲染提示输入框
    for i in range(st.session_state['num_prompts']):
        if i == 0:
            st.text_area(f"Prompt {i + 1}", key=f"prompt_{i}")
        else:
            st.text_area(f"Prompt {i + 1} (在此Prompt中使用{{{{result}}}}来引用上一个结果):",
                         key=f"prompt_{i}")

    # 使用 on_click 参数和回调函数来响应按钮点击
    st.button("添加更多Prompt", on_click=add_prompt)

    # 确定和取消按钮
    col1, col2 = st.columns(2)
    with col1:
        st.button("确定", on_click=update_prompts)
    with col2:
        st.button("取消", on_click=cancel_update)

    # （可选）显示当前缓存的提示，用于验证
    st.write("缓存的提示:")
    for prompt in st.session_state.get('cached_prompts', []):
        st.write(prompt)
