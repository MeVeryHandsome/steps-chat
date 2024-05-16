from streamlit_chatbox import FakeLLM

llm = FakeLLM()


def call_with_messages(prompt):
    text, docs = llm.chat("测试")
    return text


def call_with_stream(prompt):
    yield """```json{
  "指令序列": [
    {
      "步骤": "起飞战斗机",
      "调度数据": [
        {
          "指令": "起飞",
          "兵力名称": "歼15机号008",
          "速度": 1500.0,
          "航向": 90.0,
          "高度": 10000.0,
          "载体名称": "福田机场"
        }
      ]
    },
    {
      "步骤": "执行S型侦察巡逻",
      "调度数据": [
        {
          "指令": "巡逻",
          "兵力名称": "歼15机号008",
          "巡逻方式": "S型"
        }
      ]
    }
  ]
}
```
"""
    # for x, docs in llm.chat_stream("测试"):
    #     yield x
