import streamlit as st


# 添加或更新提示
def update_prompts():
    cprompts = {}
    for prompt_id in st.session_state['prompts'].keys():
        cprompts[prompt_id] = st.session_state[f'prompt_{prompt_id}']
    if cprompts:
        st.session_state['cached_prompts'] = cprompts


def add_prompt():
    # 为prompts字典添加一个新条目
    new_id = max(st.session_state.prompts.keys(), default=-1) + 1
    st.session_state.prompts[new_id] = ''


def delete_prompt(prompt_id):
    # 从prompts字典中删除指定的条目
    if prompt_id == 0:
        # 提示
        return
    else:
        del st.session_state.prompts[prompt_id]


def prompt_base_page():
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.title('提示词管理')
    # 添加提示词的按钮
    with col2:
        st.write("")  # 这个空写操作是为了使按钮与文本区域垂直对齐
        st.write("")  # 这个空写操作是为了使按钮与文本区域垂直对齐
        st.write("")  # 这个空写操作是为了使按钮与文本区域垂直对齐
        st.button("添加Prompt", on_click=add_prompt)
    if 'cached_prompts' not in st.session_state:
        st.session_state['cached_prompts'] = {0: ''}
    # 检查会话状态中的prompts字典是否存在，不存在则创建
    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = {0: ''}
    st.session_state['prompts'] = st.session_state['cached_prompts']
    # 渲染所有的prompts和它们旁边的删除按钮
    for prompt_id, prompt_text in list(st.session_state.prompts.items()):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            if prompt_id == 0:
                st.text_area(f"Prompt", key=f"prompt_{prompt_id}")
            else:
                st.text_area(f"Prompt (在此Prompt中使用{{{{result}}}}来引用上一个结果):",
                             key=f"prompt_{prompt_id}")
        with col2:
            # 在列布局中使用空间占位符来垂直对齐按钮
            st.write("")  # 这个空写操作是为了使按钮与文本区域垂直对齐
            st.write("")  # 这个空写操作是为了使按钮与文本区域垂直对齐
            st.button("✕", key=f"delete_{prompt_id}", on_click=delete_prompt, args=(prompt_id,))
    st.button("确定", on_click=update_prompts)
