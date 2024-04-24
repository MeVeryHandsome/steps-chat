import yaml

# 打开并读取YAML文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    file_content = yaml.safe_load(file)
    logo = file_content['logo']
    version = file_content['version']
    main_screen_icon = file_content['main_screen_icon']
    header = file_content['header']
    model:str = file_content['model']
    prompt_data = list(file_content['prompts'].values())

if model.upper() == "GLM":
    from agent.glm_agent import call_with_stream, call_with_messages
elif model.upper() == "QWEN":
    from agent.qwen_agent import call_with_stream, call_with_messages
elif model.upper() == "FAKE":
    from agent.fake_llm import call_with_stream, call_with_messages
