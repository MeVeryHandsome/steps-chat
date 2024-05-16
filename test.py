# # from agent.qwen_agent import call_with_messages, call_with_stream
# from agent.glm_agent import call_with_messages, call_with_stream
# from web_pages.dialogue import prompt_data
# prompt = "请问今天的天气怎么样？"
# result = call_with_messages(prompt)
# print(f"第一次结果:{result}")
# for r in call_with_stream(prompt):
#     print(r)
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from uvicorn.config import LOGGING_CONFIG

app = FastAPI()

# 允许任何域名跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许任何源
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许任何方法（GET, POST, PUT, DELETE, etc.）
    allow_headers=["*"],  # 允许任何头
)

function_list = {}

class Command(BaseModel):
    指令: str
    兵力名称: str
    巡逻方式: Optional[str] = None
    速度: Optional[float] = None
    航向: Optional[float] = None
    高度: Optional[float] = None
    载体名称: Optional[str] = None
@app.post("/api/apiCmd")
def execute_command(command: Command):
    print(command)
    if command.指令:
        re = command.指令
        return {"code": 200, "msg": "success", "data": f"{re}执行成功"}
    else:
        return {"code": 404, "msg": "failed", "data": f"{command}执行失败"}

def main():
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s " + LOGGING_CONFIG["formatters"]["access"]["fmt"]
    uvicorn.run(app, host="0.0.0.0", port=4321)

if __name__ == "__main__":
    main()
