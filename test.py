import re
import streamlit as st
from utils.related_str_utils import prevent_non_sense

# 输入字符串
dot_string = '''
digraph flowchart {
    "启动无人机，接收侦察任务。" [shape=box];
    "是否在侦察范围内发现目标？" [shape=diamond];
    "目标是否构成威胁？" [shape=diamond];
    "准备攻击，锁定目标。" [shape=box];
    "发射导弹攻击目标。" [shape=box];
    "评估攻击结果，目标是否被摧毁？" [shape=diamond];
    "继续执行侦察巡逻任务。" [shape=box];
    "任务完成，返回基地。" [shape=box];

    "启动无人机，接收侦察任务。" -> "是否在侦察范围内发现目标？";
    "是否在侦察范围内发现目标？" -> "目标是否构成威胁？" [label="发现目标"];
    "是否在侦察范围内发现目标？" -> "继续执行侦察巡逻任务。" [label="未发现目标"];
    "目标是否构成威胁？" -> "准备攻击，锁定目标。" [label="威胁"];
    "目标是否构成威胁？" -> "继续执行侦察巡逻任务。" [label="无威胁"];
    "准备攻击，锁定目标。" -> "发射导弹攻击目标。";
    "发射导弹攻击目标。" -> "评估攻击结果，目标是否被摧毁？";
    "评估攻击结果，目标是否被摧毁？" -> "任务完成，返回基地。" [label="摧毁"];
    "评估攻击结果，目标是否被摧毁？" -> "准备攻击，锁定目标。" [label="未摧毁"];
    "继续执行侦察巡逻任务。" -> "是否在侦察范围内发现目标？";
}
'''
result = prevent_non_sense(dot_string)
st.graphviz_chart(result)

