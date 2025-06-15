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

def send_single_code_analyzer(mutiAgentPrompt, ans_path, code_location, experiment_model):
    global tokensum
    # response_txt_location = os.path.join(ans_path, "response.txt")
    response_topN_location = os.path.join(ans_path, "topN.txt")
    # res_json_location = os.path.join(ans_path, "response.pkl")
    analyzer_ans_location = os.path.join(ans_path, "analyzerAns.txt")

    if os.path.exists(response_topN_location):
        print("这个topN已经计算过了，跳过他")
        return True

    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        code = file.read()

    # 读取分析者prompt
    analyzePrompt = mutiAgentPrompt['analyzer'] + "\n" + code

    # 判断token是否超出限制
    tokens = getTokenNumbers.get_openai_token_len(analyzePrompt, model="text-davinci-001")
    tokensum += tokens
    if tokens > 8048:
        print("超出token限制跳过," + code_location)
        return False

    repeat_time = 5;

    repeat_time_this = repeat_time;
    while repeat_time_this > 0:
        repeat_time_this -= 1

        try:
            # 发送请求在这
            print(" 分析者，第 " + str(repeat_time - repeat_time_this) + " 次请求。" + code_location)
            response_txt = SendPromt.send_prompt_openai_gpt(analyzePrompt, experiment_model)
        except:
            print(" 请求发送异常" + code_location)
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_analyzer(response_txt)
        except:
            print(" Json读取异常" + code_location)
            continue

        if res_json_data is None:
            print(code_location + " json读取到空")
            continue
        else:
            if not os.path.exists(ans_path):
                # 如果文件夹不存在，则创建它
                os.makedirs(ans_path)
                print(f"文件夹 '{ans_path}' 已创建")

            with open(analyzer_ans_location, 'w', encoding='utf-8') as file:
                file.write(res_json_data['analyze'])

                # 跳出循环
            print("数据存储成功 " + code_location)
            return True
            break
    return False


def send_single_code_questioner(mutiAgentPrompt, ans_path, code_location, experiment_model):
    response_topN_location = os.path.join(ans_path, "topN.txt")
    analyzer_ans_location = os.path.join(ans_path, "analyzerAns.txt")
    questioner_ans_location = os.path.join(ans_path, "questionerAns.txt")

    # if os.path.exists(response_topN_location):
    #     print("这个topN已经计算过了，跳过他")
    #     return True

    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        code = file.read()
    with open(code_location, 'r', encoding='utf-8') as file:
        codelines = file.readlines()

    with open(analyzer_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        analyzerAns = file.read()

    suspiciousLines = []

    # 读取提问者prompt
    for i in range(len(codelines)):
        questionerPrompt = mutiAgentPrompt['questioner'] + "\n\n" + "purpose of the code for reference" + analyzerAns + '\n\n' + "Please determine whether line " + str(i+1) + " might be the buggy line. The code is as follows：\n\n" + code

        # 判断token是否超出限制
        tokens = getTokenNumbers.get_openai_token_len(questionerPrompt, model="text-davinci-001")
        if tokens > 8096:
            print("超出token限制跳过," + code_location)
            return False

        repeat_time = 5;

        repeat_time_this = repeat_time;
        while repeat_time_this > 0:
            repeat_time_this -= 1

            try:
                # 发送请求在这
                print(" 提问者，第 " + str(repeat_time - repeat_time_this) + " 次请求。第" + str(i+1) + "行" + code_location)
                response_txt = SendPromt.send_prompt_openai_gpt(questionerPrompt, experiment_model)
            except:
                print(" 提问者，请求发送异常" + code_location)
                continue

            if "TRUE" in response_txt:
                suspiciousLines.append(i+1)
            elif "FALSE" not in response_txt:
                print(" 提问者，返回数据异常，不包括TRUE和FALSE" + code_location)
                continue

            break
        if repeat_time_this == 0:
            return False
        # 如果重复总是出错，返回错误
        # return False

    with open(questioner_ans_location, 'w', encoding='utf-8') as file:
        # 使用 json.dump() 将列表写入文件
        json.dump(suspiciousLines, file)

    return True

def send_single_code_faultSeeker(mutiAgentPrompt, ans_path, code_location, experiment_model, faulte_data_index):
    global tokensum
    response_topN_location = os.path.join(ans_path, "topN.txt")
    analyzer_ans_location = os.path.join(ans_path, "analyzerAns.txt")
    faultSeeker_ans_location = os.path.join(ans_path, "faultSeekerAns.txt")

    if os.path.exists(response_topN_location):
        print("这个topN已经计算过了，跳过他")
        return True

    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        code = file.read()
    with open(code_location, 'r', encoding='utf-8') as file:
        codelines = file.readlines()

    with open(analyzer_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        analyzerAns = file.read()

    suspiciousLines = []

    # 读取提问者prompt

    faultSeekerPrompt = mutiAgentPrompt['faultSeeker'] + "\n\n" + "purpose of the code for reference：\n" + analyzerAns + "The code is as follows：\n\n" + code

    # 判断token是否超出限制
    tokens = getTokenNumbers.get_openai_token_len(faultSeekerPrompt, model="text-davinci-001")
    tokensum +=tokens
    if tokens > 8096:
        print("超出token限制跳过," + code_location)
        return False

    repeat_time = 5;

    repeat_time_this = repeat_time;
    while repeat_time_this > 0:
        repeat_time_this -= 1

        try:
            # 发送请求在这
            print(" faultSeeker第 " + str(repeat_time - repeat_time_this) + " 次请求" + code_location)
            response_txt = SendPromt.send_prompt_openai_gpt(faultSeekerPrompt, experiment_model)
        except:
            print(" faultSeeker，请求发送异常" + code_location)
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_sorter(response_txt)
        except:
            print(" faultSeekerJson读取异常" + code_location)
            continue

        if res_json_data is None:
            print(code_location + " json读取到空")
            continue
        else:
            topN = 100

            fault_lineNumbers = []

            faultlist = res_json_data['faultLocalization']
            for index in range(len(faultlist)):
                try:
                    fault_lineNumbers.append(faultlist[index]['lineNumber'])
                    if faultlist[index]['lineNumber'] == faulte_data_index:
                        topN = index + 1
                except:
                    print("读取lineNumber失败")
            print("faultSeeker_topN: ", topN)

            with open(faultSeeker_ans_location, 'w', encoding='utf-8') as file:
            # 使用 json.dump() 将列表写入文件
                json.dump(fault_lineNumbers, file)

        break
    if repeat_time_this == 0:
        return False
    # 如果重复总是出错，返回错误
    # return False


    print("faultSeeker数据存储成功")

    return True


def send_single_code_sorter(mutiAgentPrompt, ans_path, code_location, experiment_model, faulte_data_index):
    response_topN_location = os.path.join(ans_path, "topN.txt")
    analyzer_ans_location = os.path.join(ans_path, "analyzerAns.txt")
    questioner_ans_location = os.path.join(ans_path, "questionerAns.txt")
    sorter_ans_location = os.path.join(ans_path, "sorterAns.txt")


    # if os.path.exists(response_topN_location):
    #     print("这个topN已经计算过了，跳过他")
    #     return True

    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        code = file.read()

    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        analyzerAns = file.read()

    with open(questioner_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        questionerAns = file.read()

    # 读取分析者prompt
    sorterPrompt = (mutiAgentPrompt['sorter'] + "\nThe code is as follows：\n\n" + code
                    + "\n Possible purpose of the code：\n" + analyzerAns + "\n\n Pay more attention to the following lines: ") + questionerAns + ". These are for reference only. It may not be just these lines, and these lines may not be included either."

    # 判断token是否超出限制
    tokens = getTokenNumbers.get_openai_token_len(sorterPrompt, model="text-davinci-001")
    if tokens > 8096:
        print("超出token限制跳过," + code_location)
        return False

    repeat_time = 5;

    repeat_time_this = repeat_time;
    while repeat_time_this > 0:
        repeat_time_this -= 1

        try:
            # 发送请求在这
            print(" 排序者，第 " + str(repeat_time - repeat_time_this) + " 次请求。" + code_location)
            response_txt = SendPromt.send_prompt_openai_gpt(sorterPrompt, experiment_model)
        except:
            print(" 请求发送异常" + code_location)
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_sorter(response_txt)
        except:
            print(" Json读取异常" + code_location)
            continue

        if res_json_data is None:
            print(code_location + " json读取到空")
            continue
        else:
            topN = 100
            faultlist = res_json_data['faultLocalization']
            for index in range(len(faultlist)):
                try:
                    if faultlist[index]['lineNumber'] == faulte_data_index:
                        topN=index+1
                        break
                except:
                    print("读取lineNumber失败")
            print("topN: ", topN)

            with open(sorter_ans_location, 'w') as file:
                file.write(response_txt)
            with open(response_topN_location, 'w') as file:
                file.write(str(topN))

            return True
            break
    return False


def send_single_code_sorterAfterSeeker(mutiAgentPrompt, ans_path, code_location, experiment_model, faulte_data_index):
    global tokensum
    response_topN_location = os.path.join(ans_path, "topN.txt")
    analyzer_ans_location = os.path.join(ans_path, "analyzerAns.txt")
    faultSeeker_ans_location = os.path.join(ans_path, "faultSeekerAns.txt")
    sorterAfterSeeker_ans_location = os.path.join(ans_path, "sorterAfterSeekerAns.txt")


    if os.path.exists(response_topN_location):
        print("这个topN已经计算过了，跳过他")
        return True

    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        code = file.read()

    with open(analyzer_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        analyzerAns = file.read()

    with open(faultSeeker_ans_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        faultSeekerAns = file.read()

    # 读取分析者prompt
    sorterPrompt = (mutiAgentPrompt['sorter'] + "\nThe code is as follows：\n\n" + code
                    + "\n Possible purpose of the code：\n" + analyzerAns + " \n\n The Possible faultlines:\n" + faultSeekerAns)

    # 判断token是否超出限制
    tokens = getTokenNumbers.get_openai_token_len(sorterPrompt, model="text-davinci-001")
    tokensum += tokens
    if tokens > 8096:
        print("超出token限制跳过," + code_location)
        return False

    repeat_time = 5;

    repeat_time_this = repeat_time;
    while repeat_time_this > 0:
        repeat_time_this -= 1

        try:
            # 发送请求在这
            print(" sorterAfterSeeker，第 " + str(repeat_time - repeat_time_this) + " 次请求。" + code_location)
            response_txt = SendPromt.send_prompt_openai_gpt(sorterPrompt, experiment_model)
        except:
            print(" sorterAfterSeeker请求发送异常" + code_location)
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_sorter(response_txt)
        except:
            print(" Json读取异常" + code_location)
            continue

        if res_json_data is None:
            print(code_location + " json读取到空")
            continue
        else:
            topN = 100
            faultlist = res_json_data['faultLocalization']
            for index in range(len(faultlist)):
                try:
                    if faultlist[index]['lineNumber'] == faulte_data_index:
                        topN=index+1
                        break
                except:
                    print("读取lineNumber失败")
            print("topN: ", topN)

            with open(sorterAfterSeeker_ans_location, 'w') as file:
                file.write(response_txt)
            with open(response_topN_location, 'w') as file:
                file.write(str(topN))

            return True
            break
    return False


# CodeFlaws_读取并返回错误信息行号。
def get_fault_data(faulte_data_path):
    with open(faulte_data_path, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        faulte_data_str = file.read()
    faulte_data_index = re.search('\d+', faulte_data_str).group(0)
    faulte_data_index = int(faulte_data_index)
    return faulte_data_index

def run_codeflaws_muti(mutiAgentPrompt, experiment_index, experiment_model, rangeIndex):
    global tokensum
    root_path = "D:/私人资料2024/论文/大模型相关/多代理新手程序错误定位实验/data/codeflaws/version/"
    Codeflaws_Filter_Data = []
    with open("evaluate/Codeflaws_Filter_Data.pkl", "rb") as f:
        Codeflaws_Filter_Data = pickle.load(f)

    process_num = 0

    for versionInt in range(1, 1544):

        # 记录一下token消费
        tokensum=0

        versionStr = "v" + str(versionInt);
        if versionStr not in Codeflaws_Filter_Data:
            print("跳过:" + versionStr)
            continue

        # 在遍历达到一定个数后退出
        process_num += 1

        # print("processing: " + versionStr+" 第"+process_num+"个")
        if process_num > rangeIndex:
            break

        print("正在跑Codeflaws上的 " + experiment_model + " 实验： " + str(experiment_index) + " 的第 " + str(
            process_num) + " 个程序")

        start_time = time.time()

        # 数据目录
        # 给代码增加行号
        AddLineNumber.process_code(os.path.join(root_path, versionStr, "test_data/defect_root/source"), "tcas.c")

        # 增加行号的code_location
        code_location = os.path.join(root_path, versionStr, "test_data/defect_root/source/tcas.c_indexed.txt")
        faulte_data_path = os.path.join(root_path, versionStr, "test_data/defect_root/Fault_Record.txt")
        faulte_data_index = get_fault_data(faulte_data_path)

        # 输出的目录
        ans_path = os.path.join(root_path, versionStr, "test_data", experiment_model)
        ans_path = os.path.join(ans_path, str(experiment_index))
        test_outfile = os.path.join(ans_path, "test_outfile.txt")

        # 使用os.path.exists检查文件夹是否存在
        if not os.path.exists(ans_path):
            # 如果文件夹不存在，则创建它
            os.makedirs(ans_path)
            print(f"文件夹 '{ans_path}' 已创建")

        isok = send_single_code_analyzer(mutiAgentPrompt, ans_path, code_location, experiment_model)
        if not isok:
            print("analyzer发生异常，建议重试")
            return False

        isok = send_single_code_faultSeeker(mutiAgentPrompt, ans_path, code_location, experiment_model, faulte_data_index)
        if not isok:
            print("faultSeeker发生异常，建议重试")
            return False

        isok = send_single_code_sorterAfterSeeker(mutiAgentPrompt, ans_path, code_location, experiment_model, faulte_data_index)
        if not isok:
            print("sorterAfterSeeker发生异常，建议重试")
            return False

        # isok = send_single_code_questioner(mutiAgentPrompt, ans_path, code_location, experiment_model)
        # if not isok:
        #     print("questioner发生异常，建议重试")
        #     return False

        # isok = send_single_code_sorter(mutiAgentPrompt, ans_path, code_location, experiment_model, faulte_data_index)
        # if not isok:
        #     print("sorter发生异常，建议重试")
        #     return False

        # 记录运行时间
        end_time = time.time()
        time_location = os.path.join(ans_path, "time.txt")
        with open(time_location, 'w', encoding='utf-8') as file:
            # 将运行时间写入文件
            file.write(str(end_time - start_time))

        tokenCost_location = os.path.join(ans_path, "tokenCost.txt")
        with open(tokenCost_location, 'w', encoding='utf-8') as file:
            # 将运行时间写入文件
            file.write(str(tokensum))

    return True


if __name__ == "__main__":
    # prompt_location = "./prompts/prompt1-all.txt"
    # with open(prompt_location, 'r', encoding='utf-8') as file:
    #     # 读取文件内容并保存到字符串中
    #     prompt = file.read()
    #
    # run_all(prompt)

    with open('./prompts/mutiAgentPrompt.json', 'r', encoding='utf-8') as file:
        # 使用json.load()方法从文件中读取并解析JSON数据
        mutiAgentPrompt = json.load(file)

    isok = run_codeflaws_muti(mutiAgentPrompt, "muti_1", "gpt-4", 503)

    # print(mutiAgentPrompt['analyzer'])
