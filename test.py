from web_pages.dialogue import call_with_messages, data, call_with_stream
prompt_list = list(data.values())
length = len(prompt_list)
if length > 1:
    first = prompt_list.pop(0)
    last = prompt_list.pop(-1)
    result = call_with_messages(first)
    print(f"第一次结果:{result}")
    for index, prompt in enumerate(prompt_list):
        final_prompt = prompt.format(question=result)
        result = call_with_messages(final_prompt)
        print(f"第{index + 2}次结果:{result}")
    for r in call_with_stream(last.format(question=result)):
        print(r)



