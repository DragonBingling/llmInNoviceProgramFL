import os
import pickle

from CodeArrange import AddLineNumber, getTokenNumbers


def send_single_code_faultlocalization(prompt, ans_path,code_location,faultdata,experiment_model):
    response_txt_location = os.path.join(ans_path, "response.txt")
    response_topN_location = os.path.join(ans_path, "topN.txt")
    res_json_location = os.path.join(ans_path, "response.pkl")

    if os.path.exists(response_topN_location):
        print("这个topN已经计算过了，跳过他")
        return True
    with open(code_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        code = file.read()

    prompt_code=prompt+"\n\n"+code;
    # with open("response.txt", 'w') as file:
    #     file.write(prompt_code)
    tokens = getTokenNumbers.get_openai_token_len(prompt_code, model="text-davinci-001")
    if tokens > 2048:
        print("超出token限制跳过,"+code_location)
        return False

    repeat_time = 10;

    repeat_time_this = repeat_time;
    while repeat_time_this>0:
        repeat_time_this-=1


        try:
            # 发送请求在这
            print(" 第 " + str(repeat_time - repeat_time_this) + " 次请求。" + code_location)
            # response_txt = send_request_and_return(prompt_code)
            response_txt = SendPromt.send_prompt_openai_gpt(prompt_code,experiment_model)
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


            topN = 100
            faultlist = res_json_data['faultLocalization']
            for index in range(len(faultlist)):
                # print(faultlist[index]['lineNumber'])
                try:
                    if faultlist[index]['lineNumber']==faultdata:
                        topN=index+1
                        break
                except:
                    print("读取lineNumber失败")
            print("topN: ",topN)
            # for index in range(len(faultlist)):
            #     # print(faultlist[index]['lineNumber'])
            #     lineNumber=-1
            #     try:
            #         lineNumber = int(faultlist[index]['lineNumber'])
            #     except:
            #         print("lineNumber转换失败: ")
            #         print(faultlist)
            #     if not lineNumber<0:
            #         continue
            #     if lineNumber==faultdata:
            #         topN=index+1
            #         break
            # print("topN: ",topN)

            if ReplaceIndex == True:
                with open(response_txt_location, 'w') as file:
                    file.write(response_txt)
                with open(res_json_location, 'wb') as file:
                    pickle.dump(res_json_data, file)
                with open(response_topN_location, 'w') as file:
                        file.write(str(topN))

                # 跳出循环
            print("数据存储成功 "+code_location)
            return True
            break
    return False

def arrange_Codeflaws(prompt,experiment_index,experiment_model,rangeIndex):
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/version/"
    Codeflaws_Filter_Data = []
    with open("Codeflaws_Filter_Data.pkl", "rb") as f:
        Codeflaws_Filter_Data = pickle.load(f)

    process_num = 0

    for versionInt in range(1544, 1762):
        # if versionInt in errlist:
        #     print("跳过:",versionInt)
        #     continue
        versionStr = "v" + str(versionInt);
        # if versionStr not in Codeflaws_Filter_Data:
        #     print("跳过:"+versionStr)
        #     continue

        #在遍历达到一定个数后退出
        process_num +=1

        # print("processing: " + versionStr+" 第"+process_num+"个")
        # if process_num>rangeIndex:
        #     break

        print("正在跑Codeflaws上的 " + experiment_model + " 实验： " + str(experiment_index) + " 的第 " + str(
            process_num) + " 个程序")

        # 数据目录
        # 给代码增加行号
        AddLineNumber.process_code(os.path.join(root_path, versionStr, "test_data/defect_root/source"), "tcas.c")
        # code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c")
        # 增加行号的code_location
        code_location = os.path.join(root_path, versionStr, "test_data/defect_root/source/tcas.c_indexed.txt")
        faulte_data_path = os.path.join(root_path, versionStr, "test_data/defect_root/Fault_Record.txt")

        with open(code_location, 'r', encoding='utf-8') as file:
            # 读取文件内容并保存到字符串中
            code = file.read()

        prompt_code = prompt + "\n\n" + code;
        # with open("response.txt", 'w') as file:
        #     file.write(prompt_code)
        tokens = getTokenNumbers.get_openai_token_len(prompt_code, model="text-davinci-001")

        if tokens > 2048:
            print("超出token限制跳过," + code_location)
            continue

        Codeflaws_Filter_Data.append(versionStr)


        # faulte_data_index = get_fault_data(faulte_data_path)
        #
        # # 输出的目录
        # ans_path = os.path.join(root_path, versionStr, "test_data", experiment_model)
        # ans_path = os.path.join(ans_path, str(experiment_index))
        # test_outfile = os.path.join(ans_path, "test_outfile.txt")

        # 使用os.path.exists检查文件夹是否存在
        # if not os.path.exists(ans_path):
        #     # 如果文件夹不存在，则创建它
        #     os.makedirs(ans_path)
        #     print(f"文件夹 '{ans_path}' 已创建")

        # isok = send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index, experiment_model)

    print(Codeflaws_Filter_Data)
    with open("Codeflaws_Filter_Data1.pkl", "wb") as f:
        pickle.dump(Codeflaws_Filter_Data, f)


if __name__ == "__main__":


    # prompt_location = "./prompts/prompt1-all.txt"
    # with open(prompt_location, 'r', encoding='utf-8') as file:
    #     # 读取文件内容并保存到字符串中
    #     prompt = file.read()
    #
    # arrange_Codeflaws(prompt,1,"gpt-4",1)

    Codeflaws_Filter_Data = []
    with open(
            "Codeflaws_Filter_Data.pkl",
            "rb") as f:
        Codeflaws_Filter_Data = pickle.load(f)

    i=0;