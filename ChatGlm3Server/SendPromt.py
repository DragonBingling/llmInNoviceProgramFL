import requests
import json
from openai import OpenAI

def send_request_and_save_to_file():
    url = "http://127.0.0.1:6006"
    headers = {'Content-Type': 'application/json'}
    prompt = ""
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        prompt = file.read()

    data = {"prompt": prompt, "history": []}

    response = requests.post(url, json=data, headers=headers)
    response_data = json.loads(response.text)
    print(response_data)
    print(response_data["history"][1]["content"])
    # Writing response to a file
    with open('response.txt', 'w') as file:
        file.write(response_data["history"][1]["content"])

    return "Response saved to response.txt"

def send_request_and_return(prompt):
    url = "http://127.0.0.1:8000"
    headers = {'Content-Type': 'application/json'}
    # prompt = ""
    # with open('prompt.txt', 'r', encoding='utf-8') as file:
    #     # 读取文件内容并保存到字符串中
    #     prompt = file.read()

    # data = {"你是谁"}
    data = {"prompt": prompt, "history": [],"max_tokens": 2048}

    response = requests.post(url, json=data, headers=headers)
    response_data = json.loads(response.text)
    # print(response_data)
    # print(response_data["history"][1]["content"])
    # Writing response to a file
    # with open('response.txt', 'w') as file:
    #     file.write(response_data["history"][1]["content"])

    return response_data["history"][1]["content"]

def send_prompt_openai_form(prompt,model):
    client = OpenAI(
        base_url="http://127.0.0.1:8000/v1",
        api_key="666"
    )
    # print(mykey)
    if model == "chatGlm3":
        model = "chatglm3"
    completion = client.chat.completions.create(
        model=model,  # 将模型更改
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # print(completion.choices[0].message.content)
    # 将结果保存在txt中
    response_txt = completion.choices[0].message.content
    # with open(savelocation, 'w') as file:
    #     file.write(response_txt)

    return response_txt

# Automatically call send_request_and_save_to_file() when the script is executed
if __name__ == "__main__":
    # send_request_and_save_to_file()
    # response = send_request_and_return("你是谁")
    # openbuddy-llama，chatGlm3，code-llama
    response = send_prompt_openai_form("你是谁开发的？","openbuddy-llama")
    i=0
# 要使用这个函数，只需要取消注释下面的代码并执行：
# send_request_and_save_to_file()
