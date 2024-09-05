def compose_prompt(origin_prompt, user_input, results):
    actual_prompt = origin_prompt
    if "{question}" in origin_prompt:
        actual_prompt = origin_prompt.replace("{question}", user_input)
    for index, result in enumerate(results):
        if f"{{result{index + 1}}}" in actual_prompt:
            actual_prompt = actual_prompt.replace(f"{{result{index + 1}}}", result)
    return actual_prompt