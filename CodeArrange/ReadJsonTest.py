import json
import re

def extract_json(input_string):
    """
    提取输入字符串中的JSON字符串。

    :param input_string: 输入字符串
    :return: 如果找到JSON字符串，则返回它。否则，返回None。
    """

    # 找到 JSON 字符串开始的位置
    start = input_string.find('{')
    if start == -1:
        return None,None
    else:
        # 初始化大括号计数器
        brace_count = 1
        # 从 JSON 字符串开始的位置之后开始循环
        jump_flag = False
        for i, char in enumerate(input_string[start + 1:], start=start + 1):
            if char == '"':
                jump_flag=not jump_flag
            if jump_flag:
                continue
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                # 如果大括号平衡了，则找到 JSON 字符串的结束位置
                if brace_count == 0:
                    return input_string[start: i + 1],i+1
    return None,None


def extract_json_regular(string):
    # 使用正则表达式查找包含整个 JSON 数据的部分
    pattern = r'\{.{0,4000}"faultLocalization".*\[.*\].{0,4000}\}'  # 匹配整个 JSON 数据，包括换行符和空格
    matches = re.findall(pattern, string, re.S)
    # xi
    for json_str in matches:
        try:
            data = json.loads(json_str)
            # 这里可以对提取出的 JSON 数据进行处理
            return data
            # print("从文本中提取的 JSON 数据:")
            # print("intentOfThisFunction:", data["intentOfThisFunction"])
            # print("faultLocalization:", data["faultLocalization"])
        except json.JSONDecodeError as e:
            print("无法解析 JSON 数据:", e)

if __name__ == "__main__":
    with open("./response.txt", 'r', encoding='utf-8') as file:
        # ��ȡ�ļ����ݲ����浽�ַ�����
        response = file.read()

    # res= extract_json(response)
    # print(res)
    data = extract_json_regular(response)
    print(data)
    # 使用正则表达式查找包含整个 JSON 数据的部分
    # pattern = r'\{.*\[.*\].*\}'  # 匹配整个 JSON 数据，包括换行符和空格
    # matches = re.findall(pattern, response,re.S)
    # # xi
    # for json_str in matches:
    #     try:
    #         data = json.loads(json_str)
    #         # 这里可以对提取出的 JSON 数据进行处理
    #         print("从文本中提取的 JSON 数据:")
    #         print("intentOfThisFunction:", data["intentOfThisFunction"])
    #         print("faultLocalization:", data["faultLocalization"])
    #     except json.JSONDecodeError as e:
    #         print("无法解析 JSON 数据:", e)