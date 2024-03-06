import requests

def send_request_and_save_to_file():
    url = "http://127.0.0.1:6006"
    headers = {'Content-Type': 'application/json'}
    data = {"prompt": "你好", "history": []}

    response = requests.post(url, json=data, headers=headers)
    
    response_data = json.loads(response_text)
    # 提取 history 部分
    history = response_data.get("history", [])
    # 遍历 history 中的每个条目，并提取 content
    contents = [item["content"] for item in history if "content" in item]
    # 打印提取的内容
    for content in contents:
        print(content)
    # Writing response to a file
    with open('response.txt', 'w') as file:
        file.write(response.text)

    return "Response saved to response.txt"

# Automatically call send_request_and_save_to_file() when the script is executed
if __name__ == "__main__":
    send_request_and_save_to_file()
# 要使用这个函数，只需要取消注释下面的代码并执行：
# send_request_and_save_to_file()
