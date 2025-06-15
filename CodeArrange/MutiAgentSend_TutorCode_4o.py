import os.path
import pickle
import re
import requests
import json
from openai import OpenAI

import AddLineNumber
import ReadJsonTest
import SendPromt
import getTokenNumbers
import time

# Defects4J 程序列表，就通过这个列表来遍历所有的程序
projectOrigin = {
    "Chart": 26,
    # "Lang": 65,
    # "Math": 106,
    # "Mockito": 38,
    # "Time": 27,
    # "Closure": 176,
    # "Cli": 39,
    # "Codec": 18,
    # "Collections": 4,
    # "Compress": 47,
    # "Csv": 16,
    # "Gson": 18,
    # "JacksonCore": 26,
    # "JacksonDatabind": 112,
    # "JacksonXml": 6,
    # "Jsoup": 93,
    # "JxPath": 22,
}

tokensum = 0


def send_single_code_problemAnalyzer(mutiAgentPrompt, ans_path, code_index, code_info, experiment_model):
    global tokensum
    # response_txt_location = os.path.join(ans_path, "response.txt")
    response_topN_location = os.path.join(ans_path, "topN.txt")
    # res_json_location = os.path.join(ans_path, "response.pkl")
    problemAnalyzer_ans_location = os.path.join(ans_path, "problemAnalyzerAns.txt")

    if os.path.exists(response_topN_location):
        print("这个topN已经计算过了，跳过他")
        return True

    # with open(code_location, 'r', encoding='utf-8') as file:
    #     # 读取文件内容并保存到字符串中
    #     code = file.read()

    # 读取problemAnalyzer promot
    problemAnalyzerPrompt = (mutiAgentPrompt['problemAnalyzer'] + "\n\n problemDescription：\n"
                             + code_info['problemDescription']
                             + '\n input： ' + code_info['input']
                             + '\n output ' + code_info['output'])

    # 判断token是否超出限制
    tokens = getTokenNumbers.get_openai_token_len(problemAnalyzerPrompt, model="text-davinci-001")
    tokensum += tokens
    if tokens > 8048:
        print("超出token限制跳过, " + str(code_index))
        return False

    repeat_time = 5;

    repeat_time_this = repeat_time;
    while repeat_time_this > 0:
        repeat_time_this -= 1

        try:
            # 发送请求在这
            print(" problemAnalyzer，第 " + str(repeat_time - repeat_time_this) + " 次请求。" + str(code_index))
            response_txt = SendPromt.send_prompt_openai_gpt(problemAnalyzerPrompt, experiment_model)
        except:
            print(" 请求发送异常" + str(code_index))
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_analyzer(response_txt)
        except:
            print(" Json读取异常" + str(code_index))
            continue

        if res_json_data is None:
            print(str(code_index) + " json读取到空")
            continue
        else:
            if not os.path.exists(ans_path):
                # 如果文件夹不存在，则创建它
                os.makedirs(ans_path)
                print(f"文件夹 '{ans_path}' 已创建")

            with open(problemAnalyzer_ans_location, 'w', encoding='utf-8') as file:
                file.write(res_json_data['analyze'])

                # 跳出循环
            print("数据存储成功 " + str(code_index))
            return True
            break
    return False


def send_single_code_codeAnalyzer(mutiAgentPrompt, ans_path, code_index, code_info, experiment_model):
    global tokensum
    response_topN_location = os.path.join(ans_path, "topN.txt")
    problemAnalyzer_ans_location = os.path.join(ans_path, "problemAnalyzerAns.txt")
    codeAnalyzer_ans_location = os.path.join(ans_path, "codeAnalyzerAns.txt")

    if os.path.exists(response_topN_location):
        print("这个topN已经计算过了，跳过他")
        return True

    with open(problemAnalyzer_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        problemAnalyzerAns = file.read()

    # 读取codeAnalyzer prompt

    codeAnalyzerrPrompt = (mutiAgentPrompt['codeAnalyzer']
                           + "\n\n problemDescription:\n" + code_info['problemDescription']
                           + '\n\n input： ' + code_info['input']
                           + '\n\n output ' + code_info['output']
                           + '\n\n reference problem-solving ideas: \n' + problemAnalyzerAns
                           + '\n\n incorrect_code:\n' + code_info['incorrect_code_indexed']
                           )

    # 判断token是否超出限制
    tokens = getTokenNumbers.get_openai_token_len(codeAnalyzerrPrompt, model="text-davinci-001")

    tokensum += tokens
    if tokens > 8096:
        print("超出token限制跳过," + str(code_index))
        return False

    repeat_time = 5;

    repeat_time_this = repeat_time;

    while repeat_time_this > 0:
        repeat_time_this -= 1

        try:
            # 发送请求在这
            print(" codeAnalyzer，第 " + str(repeat_time - repeat_time_this) + " 次请求。" + str(code_index))
            response_txt = SendPromt.send_prompt_openai_gpt(codeAnalyzerrPrompt, experiment_model)
        except:
            print("codeAnalyzer 请求发送异常" + str(code_index))
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_analyzer(response_txt)
        except:
            print("codeAnalyzer Json读取异常" + str(code_index))
            continue

        if res_json_data is None:
            print(str(code_index) + "codeAnalyzer json读取到空")
            continue
        else:

            with open(codeAnalyzer_ans_location, 'w', encoding='utf-8') as file:
                file.write(res_json_data['analyze'])

                # 跳出循环
            print("codeAnalyzer 数据存储成功 " + str(code_index))
            return True
            break
    return False


def send_single_code_faultSeeker(mutiAgentPrompt, ans_path, code_index, code_info, experiment_model):
    global tokensum
    response_topN_location = os.path.join(ans_path, "topN.txt")
    problemAnalyzer_ans_location = os.path.join(ans_path, "problemAnalyzerAns.txt")
    codeAnalyzer_ans_location = os.path.join(ans_path, "codeAnalyzerAns.txt")
    faultSeeker_ans_location = os.path.join(ans_path, "faultSeekerAns.txt")

    if os.path.exists(response_topN_location):
        print("这个topN已经计算过了，跳过他")
        return True

    with open(problemAnalyzer_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        problemAnalyzerAns = file.read()
    with open(codeAnalyzer_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        codeAnalyzerAns = file.read()

    # 读取提问者prompt

    faultSeekerPrompt = (mutiAgentPrompt['faultSeeker']
                         + "\n\n problemDescription:\n" + code_info['problemDescription']
                         + '\n\n input： ' + code_info['input']
                         + '\n\n output ' + code_info['output']
                         + '\n\n reference problem-solving ideas: \n' + problemAnalyzerAns
                         + '\n\n incorrect_code:\n' + code_info['incorrect_code_indexed']
                         + '\n\n reference ideas behind this incorrect code:\n' + codeAnalyzerAns
                         )

    # 判断token是否超出限制
    tokens = getTokenNumbers.get_openai_token_len(faultSeekerPrompt, model="text-davinci-001")
    tokensum += tokens
    if tokens > 8096:
        print("超出token限制跳过," + str(code_index))
        return False

    repeat_time = 5;

    repeat_time_this = repeat_time;
    while repeat_time_this > 0:
        repeat_time_this -= 1

        try:
            # 发送请求在这
            print(" faultSeeker第 " + str(repeat_time - repeat_time_this) + " 次请求" + str(code_index))
            response_txt = SendPromt.send_prompt_openai_gpt(faultSeekerPrompt, experiment_model)
        except:
            print(" faultSeeker，请求发送异常" + str(code_index))
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_sorter(response_txt)
        except:
            print(" faultSeekerJson读取异常" + str(code_index))
            continue

        if res_json_data is None:
            print(str(code_index) + " json读取到空")
            continue
        else:
            topN = 100

            fault_lineNumbers = []

            faultlist = res_json_data['faultLocalization']
            for index in range(len(faultlist)):
                try:
                    fault_lineNumbers.append(faultlist[index]['lineNumber'])
                    if faultlist[index]['lineNumber'] == code_info['faultLines'][0]:
                        topN = index + 1
                except:
                    print("读取lineNumber失败")
            print("faultSeeker_topN: ", topN)

            with open(faultSeeker_ans_location, 'w', encoding='utf-8') as file:
                # 使用 json.dump() 将列表写入文件
                file.write(response_txt)
            with open(response_topN_location, 'w') as file:
                file.write(str(topN))

        break
    if repeat_time_this == 0:
        return False
    # 如果重复总是出错，返回错误
    # return False

    print("faultSeeker数据存储成功")

    return True

# CodeFlaws_读取并返回错误信息行号。
def get_fault_data(faulte_data_path):
    with open(faulte_data_path, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        faulte_data_str = file.read()
    faulte_data_index = re.search('\d+', faulte_data_str).group(0)
    faulte_data_index = int(faulte_data_index)
    return faulte_data_index


def run_tutorcode_muti(mutiAgentPrompt, experiment_index, experiment_model, rangeIndex):
    global tokensum
    root_path = "D:/私人资料2024/论文/大模型相关/多代理新手程序错误定位实验/data/tutorcode/version/"
    json_data_path = "D:/私人资料2024/论文/大模型相关/多代理新手程序错误定位实验/DataSets/TutorCode_generateFaultLines_indexed.json"

    with open(json_data_path, 'r', encoding='utf-8') as file:
        # 使用json.load()方法从文件中读取并解析JSON数据
        tutor_data = json.load(file)

    process_num = 0

    for index, item in enumerate(tutor_data):
        process_num += 1
        if process_num > rangeIndex:
            break

        print("正在跑Tutorcode上的 " + experiment_model + " 实验： " + str(experiment_index)
              + " 的第 " + str(process_num) + " 个程序")

        faulte_data_index = item['faultLines'][0]

        ans_path = os.path.join(root_path, str(index), experiment_model, str(experiment_index))

        # 使用os.path.exists检查文件夹是否存在
        if not os.path.exists(ans_path):
            # 如果文件夹不存在，则创建它
            os.makedirs(ans_path)

        isok = send_single_code_problemAnalyzer(mutiAgentPrompt, ans_path, index, item, experiment_model)
        if not isok:
            print("problemAnalyzer发生异常，建议重试")
            return False

        isok = send_single_code_codeAnalyzer(mutiAgentPrompt, ans_path, index, item, experiment_model)
        if not isok:
            print("problemAnalyzer发生异常，建议重试")
            return False

        isok = send_single_code_faultSeeker(mutiAgentPrompt, ans_path, index, item, experiment_model)
        if not isok:
            print("problemAnalyzer发生异常，建议重试")
            return False

    return True


if __name__ == "__main__":
    # prompt_location = "./prompts/prompt1-all.txt"
    # with open(prompt_location, 'r', encoding='utf-8') as file:
    #     # 读取文件内容并保存到字符串中
    #     prompt = file.read()
    #
    # run_all(prompt)

    with open('./prompts/mutiAgentPrompt_TutorCode.json', 'r', encoding='utf-8') as file:
        # 使用json.load()方法从文件中读取并解析JSON数据
        mutiAgentPrompt = json.load(file)

    # isok = run_codeflaws_muti(mutiAgentPrompt, "muti_1", "gpt-4", 503)
    repeat = 10
    while repeat>0:
        isok = run_tutorcode_muti(mutiAgentPrompt, "muti_1", "gpt-4o", 200)
        print("结束一轮，休眠60s")
        time.sleep(60)
        repeat-=1

    # print(mutiAgentPrompt['analyzer'])
