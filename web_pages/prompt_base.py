import streamlit as st
from streamlit.components.v1 import html


# 按钮点击事件
def increment_counter():
    st.session_state.counter += 1
    # 使用JavaScript保存状态到localStorage
    st.markdown(f"""
        <script>
        localStorage.setItem("counter", "{st.session_state.counter}");
        </script>
    """, unsafe_allow_html=True)


def prompt_base_page():
    # 初始化session_state
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    # JavaScript代码用于从localStorage读取状态并发送回Streamlit
    js = """
    <script>
        // 从localStorage获取计数器状态
        const counter = localStorage.getItem("counter") || "0";

        // 发送状态回Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: counter
        }, '*');
    </script>
    """

    # 用于接收从JavaScript发送回的值的函数
    def setComponentValue(value):
        st.session_state.counter = int(value)

    # 当页面加载时，执行JavaScript
    html(js, height=0, width=0)

    st.button("Increment", on_click=increment_counter)

    st.write(f"Counter: {st.session_state.counter}")
