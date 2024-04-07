import os
import streamlit as st
from streamlit_option_menu import option_menu
from web_pages.dialogue import dialogue_page
# from web_pages.prompt_base2 import prompt_base_page

st.set_page_config(layout="wide")

all_pages = {
    "大模型对话": {
        "icon": "chat",
        "func": dialogue_page,
    },
    # "提示词管理": {
    #     "icon": "hdd-stack",
    #     "func": prompt_base_page,
    # }
}
icons = [x["icon"] for x in all_pages.values()]

VERSION = "0.1-beta"
with st.sidebar:
    col1, col_empty, col2 = st.columns([0.35, 0.05, 0.6])
    with col1:
        st.image(os.path.join("img", "logo-xchat.png"), width=50, use_column_width=True)
    with col2:
        st.write("")  # 这个空写操作是为了使按钮与文本区域垂直对齐
        st.caption("汽车任务规划", unsafe_allow_html=True)
    st.caption(f"""<p align="right">当前版本：{VERSION}</p>""", unsafe_allow_html=True)
    selected_page = option_menu("", options=list(all_pages), icons=icons, default_index=0)

if selected_page in all_pages:
    all_pages[selected_page]["func"]()
