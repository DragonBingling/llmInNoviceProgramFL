import os.path
import pickle
import re
import requests
import json
from openai import OpenAI

import AddLineNumber
import ReadJsonTest
import SendPromt

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

# 发送请求，返回response_txt,res_json_data
def send_request_and_return(prompt):
    # with open('prompt.txt', 'r', encoding='utf-8') as file:
    #     # 读取文件内容并保存到字符串中
    #     prompt = file.read()
    with open('key.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        mykey = file.read()

    client = OpenAI(
        base_url="https://oneapi.xty.app/v1",
        api_key=mykey
    )
    # print(mykey)
    completion = client.chat.completions.create(
        model="gpt-4",  # 将模型更改为GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # print(completion.choices[0].message.content)
    # 将结果保存在txt中
    response_txt=completion.choices[0].message.content
    # with open(savelocation, 'w') as file:
    #     file.write(response_txt)

    return response_txt

    # try:
    #     # res_json_data = json.loads(completion.choices[0].message.content)
    #     res_json_data = ReadJsonTest.extract_json_regular(completion.choices[0].message.content)
    #     return response_txt,res_json_data
    #     # with open('response.pkl', 'wb') as file:
    #     #     pickle.dump(res_json_data, file)
    # except:
    #     # print(savelocation+" Json读取异常")
    #     return response_txt,False
    # data = {"prompt": prompt, "history": []}
    #
    # response = requests.post(url, json=data, headers=headers)
    # response_data = json.loads(response.text)
    # print(response_data)
    # print(response_data["history"][1]["content"])
    # # Writing response to a file
    # with open('response.txt', 'w') as file:
    #     file.write(response_data["history"][1]["content"])
    # print("Response saved to"+savelocation)
    # return response_txt,res_json_data

# def get_ReplaceIndex()
def send_single_code_faultlocalization(prompt, ans_path,code_location,faultdata,experiment_model):
    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        code = file.read()

    prompt_code=prompt+"\n\n"+code;
    # with open("response.txt", 'w') as file:
    #     file.write(prompt_code)

    repeat_time = 10;

    repeat_time_this = repeat_time;
    while repeat_time_this>0:
        repeat_time_this-=1


        try:
            # 发送请求在这
            print(" 第 " + str(repeat_time - repeat_time_this) + " 次请求。" + code_location)
            # response_txt = send_request_and_return(prompt_code)
            response_txt = SendPromt.send_request_and_return(prompt_code)
        except:
            print(" 请求发送异常"+code_location)
            continue

        try:
            res_json_data = ReadJsonTest.extract_json_regular(response_txt)
        except:
            print(" Json读取异常"+code_location)
            continue

        if res_json_data is None:
            print(code_location + " json读取到空")
            continue
            # if repeat_time_this == 1:
            #     print("请求次数达到最大，跳过")
            # return False
        else:
            if not os.path.exists(ans_path):
                # 如果文件夹不存在，则创建它
                os.makedirs(ans_path)
                print(f"文件夹 '{ans_path}' 已创建")

            # 读取json信息

            # 判断是否替换
            ReplaceIndex = True
            response_txt_location = os.path.join(ans_path,"response.txt")
            response_topN_location = os.path.join(ans_path,"topN.txt")
            res_json_location = os.path.join(ans_path,"response.pkl")

            topN = 100
            faultlist = res_json_data['faultLocalization']
            for index in range(len(faultlist)):
                # print(faultlist[index]['lineNumber'])
                if faultlist[index]['lineNumber']==faultdata:
                    topN=index+1
                    break
            print("topN: ",topN)

            if ReplaceIndex == True:
                with open(response_txt_location, 'w') as file:
                    file.write(response_txt)
                with open(res_json_location, 'wb') as file:
                    pickle.dump(res_json_data, file)
                with open(response_topN_location, 'w') as file:
                    file.write(str(topN))
                # 跳出循环
            print("数据存储成功 "+code_location)
            break


# CodeFlaws_读取并返回错误信息行号。
def get_fault_data(faulte_data_path):
    with open(faulte_data_path, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        faulte_data_str = file.read()
    faulte_data_index = re.search('\d+', faulte_data_str).group(0)
    faulte_data_index = int(faulte_data_index)
    return faulte_data_index


def test_Codeflaws(prompt,experiment_index,experiment_model,rangeIndex):
    root_path = "/root/autodl-tmp/data/codeflaws/version/"
    with open("evaluate/errlist.pkl", "rb") as f:
        errlist = pickle.load(f)
    for versionInt in range(1, rangeIndex):
        if versionInt in errlist:
            print("跳过:",versionInt)
            continue
        versionStr = "v"+ str(versionInt);
        print("processing: "+versionStr)
        #数据目录
        # 给代码增加行号
        AddLineNumber.process_code(os.path.join(root_path,versionStr,"test_data/defect_root/source"),"tcas.c")
        # code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c")
        # 增加行号的code_location
        code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c_indexed.txt")
        faulte_data_path = os.path.join(root_path, versionStr, "test_data/defect_root/Fault_Record.txt")
        faulte_data_index = get_fault_data(faulte_data_path)

        # 输出的目录
        ans_path = os.path.join(root_path,versionStr,"test_data",experiment_model)
        ans_path = os.path.join(ans_path,str(experiment_index))
        test_outfile = os.path.join(ans_path,"test_outfile.txt")

        # 使用os.path.exists检查文件夹是否存在
        if not os.path.exists(ans_path):
            # 如果文件夹不存在，则创建它
            os.makedirs(ans_path)
            print(f"文件夹 '{ans_path}' 已创建")

        #组合prompt
        with open(code_location, 'r', encoding='utf-8') as file:
            # 读取文件内容并保存到字符串中
            code = file.read()
        prompt_code = prompt + "\n\n" + code;

        send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index,experiment_model)

        with open(code_location, 'r', encoding='utf-8') as file:
            # 读取文件内容并保存到字符串中
            code = file.read()
        with open(test_outfile, 'w') as file:
            file.write(versionStr+"\n\n"+prompt)



# Automatically call send_request_and_save_to_file() when the script is executed
if __name__ == "__main__":
    prompt_location = "/root/autodl-tmp/My/main_code/prompt-要求输出为json-增加可解析描述.txt"
    with open(prompt_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        prompt = file.read()

    # 发送一次得到回答
    # send_single_code_faultlocalization(prompt,ans_path_v1,code_location_v1,6)

    # 遍历Codeflaws进行测试
    experiment_index = 2
    experiment_model="chatGlm3"
    # modelAns(gpt4),chatGlm3
    test_Codeflaws(prompt,experiment_index,experiment_model,1000)





