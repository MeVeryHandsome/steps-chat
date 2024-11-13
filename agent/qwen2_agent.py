# Copyright (c) Alibaba Cloud.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""A simple command-line interactive chat demo."""
from typing import List, Dict

import torch
import gc
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread


class QWEN2_5:
    DEFAULT_CKPT_PATH = "/model/Qwen/Qwen2___5-32B-Instruct"
    max_new_token = 4096
    normal_temperature = 0.15
    stream_temperature = 0.15
    cpu_only = False
    tokenizer = None
    model = None

    def __init__(self):
        self._load_model_tokenizer()

    def _load_model_tokenizer(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.DEFAULT_CKPT_PATH)

        if self.cpu_only:
            device_map = "cpu"
        else:
            device_map = "auto"

        model = AutoModelForCausalLM.from_pretrained(
            self.DEFAULT_CKPT_PATH,
            torch_dtype="auto",
            device_map=device_map
        ).eval()
        model.generation_config.max_new_tokens = self.max_new_token
        self.model = model

    def _gc(self):
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def chat_stream(self, messages: List[Dict]):
        input_text = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False,
        )
        inputs = self.tokenizer([input_text], return_tensors="pt").to(self.model.device)
        streamer = TextIteratorStreamer(
            tokenizer=self.tokenizer,
            skip_prompt=True,
            timeout=60.0,
            skip_special_tokens=True,
            # temperature=self.stream_temperature
        )
        generation_kwargs = {
            **inputs,
            "streamer": streamer,
        }
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        for new_text in streamer:
            yield new_text

    def normal_chat(self, messages: List[Dict]):
        input_text = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False
        )
        inputs = self.tokenizer([input_text], return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            # temperature = self.normal_temperature
        )
        response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response_text = response_text.split('assistant\n')[-1]
        self._gc()
        return response_text


Qwen2_5_model = QWEN2_5()


def call_with_stream(prompt):
    global Qwen2_5_model
    messages = [{'role': 'system', 'content': '你是行至智能公司的军事领域大模型，你的名字叫做行小至'},
                {'role': 'user', 'content': prompt}]
    responses = Qwen2_5_model.chat_stream(messages)
    print("\n正在发起流式回答请求")
    for response in responses:
        yield response


def call_with_messages(prompt):
    global Qwen2_5_model
    messages = [{'role': 'system', 'content': '你是行至智能公司的军事领域大模型，你的名字叫做行小至'},
                {'role': 'user', 'content': prompt}]
    print("\n正在发起单次提问请求")
    response = Qwen2_5_model.normal_chat(messages)
    return response


if __name__ == "__main__":
    result = call_with_messages("hello, 请问你是谁")
    print(result)
    result = call_with_stream("hello, 请问你是谁")
    for i in result:
        print(i)
