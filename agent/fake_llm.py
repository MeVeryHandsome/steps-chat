from streamlit_chatbox import FakeLLM

llm = FakeLLM()


def call_with_messages(prompt):
    text, docs = llm.chat("测试")
    return text


def call_with_stream(prompt):
    for x, docs in llm.chat_stream("测试"):
        yield x
