import os
import streamlit as st
from streamlit_option_menu import option_menu
from web_pages.dialogue import dialogue_page
# from web_pages.prompt_base2 import prompt_base_page

st.set_page_config(layout="wide")

all_pages = {
    "系统主界面": {
        "icon": "car-front-fill",
        "func": dialogue_page,
    },
    # "提示词管理": {
    #     "icon": "hdd-stack",
    #     "func": prompt_base_page,
    # }
}
icons = [x["icon"] for x in all_pages.values()]

VERSION = "Beta"
with st.sidebar:
    col1, col_center, col2 = st.columns([0.2, 0.6, 0.2])
    with col_center:
        st.image(os.path.join("img", "car-logo.png"), use_column_width=True)
    st.caption(f"""<p align="right">当前版本：{VERSION}</p>""", unsafe_allow_html=True)
    selected_page = option_menu("", options=list(all_pages), icons=icons, default_index=0)

if selected_page in all_pages:
    all_pages[selected_page]["func"]()
