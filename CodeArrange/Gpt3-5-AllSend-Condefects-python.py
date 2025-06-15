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
    if tokens > 4096:
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
    # with open("evaluate/errlist.pkl", "rb") as f:
    #     errlist = pickle.load(f)
    Codeflaws_Filter_Data = []

    for versionInt in range(1, rangeIndex):
        # if versionInt in errlist:
        #     print("跳过:",versionInt)
        #     continue
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

        isok = send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index,experiment_model)

        if isok is True:
            Codeflaws_Filter_Data.append(versionStr)
        else:
            print(code_location + "不可用")
            continue

        print("这是第" + str(len(Codeflaws_Filter_Data)) + "个")
        with open('evaluate/Codeflaws_Filter_Data.pkl', 'wb') as file:
            pickle.dump(Codeflaws_Filter_Data, file)

        # if len(Codeflaws_Filter_Data) > 500:
        #     print("存了500个了，先退出")
        #     break_flag = True
        #     break

        # with open(code_location, 'r', encoding='utf-8') as file:
        #     # 读取文件内容并保存到字符串中
        #     code = file.read()
        # with open(test_outfile, 'w') as file:
        #     file.write(versionStr+"\n\n"+prompt)

def test_Condefects(prompt,experiment_index,experiment_model,rangeIndex):
    root_path = "/root/autodl-tmp/data/ConDefects-main/Code/"
    # with open("evaluate/errlist.pkl", "rb") as f:
    #     errlist = pickle.load(f)
    Condefects_Filter_Data = []
    break_flag = False
    jump_flag = True
    try:
        with open('evaluate/Condefects_Filter_Data.pkl', 'rb') as file:
            Condefects_Filter_Data = pickle.load(file)
    except:
        print("Condefects_Filter_Data读取失败")
        jump_flag = False

    jump_number = -1
    questions = os.listdir(root_path)



    # 遍历文件夹中的所有内容
    for question in questions:
        if break_flag:
            break
        question_path = os.path.join(root_path, question)

        # 检查是否为文件夹
        if os.path.isdir(question_path):
            # print(f'子文件夹: {contest_path}')
            try:
                java_path = os.path.join(question_path,"Java")
                questions = os.listdir(java_path)
                answers = os.listdir(java_path)
            except:
                print("列出JavaPath "+java_path+" 失败")
                continue
            for answer in answers:

                try:
                    if answer == Condefects_Filter_Data[-1]:
                        print("找到了最后一个元素，从这开始:"+str(len(Condefects_Filter_Data))+" :"+answer)
                        jump_flag = False
                        continue
                except:
                    print("Condefects_Filter_Data[-1]寻找失败")

                if jump_flag:
                    continue
                # 设置跳过数目，记得注释掉
                # if jump_number>0:
                #     jump_number-=1
                #     print("jump:",jump_number)
                #     continue
                # if answer in Condefects_Filter_Data:
                #     print(answer+" 已经在Condefects_Filter_Data中，筛选阶段先跳过他")
                #     continue

                # code_location = os.path.join(java_path, answer, "faultyVersion.java.java")

                #给代码增加行号
                AddLineNumber.process_code(os.path.join(java_path, answer), "faultyVersion.java")
                # code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c")
                # 增加行号的code_location
                # code_location = os.path.join(root_path, versionStr, "test_data/defect_root/source/tcas.c_indexed.txt")
                code_location = os.path.join(java_path, answer, "faultyVersion.java_indexed.txt")
                faulte_data_path = os.path.join(java_path, answer, "faultLocation.txt")
                ans_path = os.path.join(java_path, answer, experiment_model,str(experiment_index))
                with open(code_location, 'r', encoding='utf-8') as file:
                    # 读取文件内容并保存到字符串中
                    code = file.read()
                faulte_data_index = get_fault_data(faulte_data_path)

                isok = send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index, experiment_model)

                if isok is True:
                    Condefects_Filter_Data.append(answer)
                else:
                    print(code_location+ "不可用")
                    continue

                print("这是第"+str(len(Condefects_Filter_Data))+"个")
                with open('evaluate/Condefects_Filter_Data.pkl', 'wb') as file:
                    pickle.dump(Condefects_Filter_Data, file)

                if len(Condefects_Filter_Data) >511:
                    print("存了500个了，先退出")
                    break_flag=True
                    break
                    # with open('evaluate/Condefects_Filter_Data.pkl', 'wb') as file:
                    #     pickle.dump(Condefects_Filter_Data, file)

        # with open('evaluate/Condefects_Filter_Data.pkl', 'wb') as file:
        #     pickle.dump(Condefects_Filter_Data, file)

        # # 如果不是文件夹，则为文件
        # else:
        #     print(f'文件: {contest_path}')


    # for versionInt in range(1, rangeIndex):
    #     # if versionInt in errlist:
    #     #     print("跳过:",versionInt)
    #     #     continue
    #     versionStr = "v"+ str(versionInt);
    #     print("processing: "+versionStr)
    #     #数据目录
    #     # 给代码增加行号
    #     AddLineNumber.process_code(os.path.join(root_path,versionStr,"test_data/defect_root/source"),"tcas.c")
    #     # code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c")
    #     # 增加行号的code_location
    #     code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c_indexed.txt")
    #     faulte_data_path = os.path.join(root_path, versionStr, "test_data/defect_root/Fault_Record.txt")
    #     faulte_data_index = get_fault_data(faulte_data_path)
    #
    #     # 输出的目录
    #     ans_path = os.path.join(root_path,versionStr,"test_data",experiment_model)
    #     ans_path = os.path.join(ans_path,str(experiment_index))
    #     test_outfile = os.path.join(ans_path,"test_outfile.txt")
    #
    #     # 使用os.path.exists检查文件夹是否存在
    #     if not os.path.exists(ans_path):
    #         # 如果文件夹不存在，则创建它
    #         os.makedirs(ans_path)
    #         print(f"文件夹 '{ans_path}' 已创建")
    #
    #     #组合prompt
    #     with open(code_location, 'r', encoding='utf-8') as file:
    #         # 读取文件内容并保存到字符串中
    #         code = file.read()
    #     prompt_code = prompt + "\n\n" + code;
    #
    #     send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index,experiment_model)
    #
    #     with open(code_location, 'r', encoding='utf-8') as file:
    #         # 读取文件内容并保存到字符串中
    #         code = file.read()
    #     with open(test_outfile, 'w') as file:
    #         file.write(versionStr+"\n\n"+prompt)
def read_txt_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # 去除首尾空格和换行符，然后根据逗号拆分成列表
            line_data = line.strip().strip("[]").split(", ")
            # 将每个字符串转换为整数并加入到data列表中
            line_data = [int(num) for num in line_data]
            data.extend(line_data)
    return data

def run_Condefects(prompt,experiment_index,experiment_model,rangeIndex):
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/Code/"

    Condefects_Filter_Data = ['27941784', '27435812', '45556032', '45533632', '45705547', '45492377', '45517397', '28699500', '45484239', '45030219', '45814496', '45722066', '45783776', '45722260', '46056572', '46028780', '45783787', '43997330', '33055837', '42021171', '44101361', '40185010', '45767519', '44122587', '38915312', '38915061', '44930062', '45573210', '45777524', '45654990', '45332649', '44419168', '44646979', '45545460', '45003873', '45713633', '46026874', '45291809', '39123866', '45484479', '45803747', '44118621', '45317107', '32093401', '45275005', '45491531', '45279577', '31643804', '30923012', '45083106', '45754993', '45558657', '44668354', '44681618', '45471607', '45545981', '42082334', '33700497', '33700944', '46165545', '45750635', '45954819', '44094167', '46203182', '45935608', '36684114', '43020372', '45483518', '45054015', '41610915', '41651640', '45126109', '45974029', '37666166', '43954461', '45479683', '44381954', '43572863', '43559540', '45999150', '46206496', '45969465', '45574605', '45459245', '46183354', '44934690', '45461646', '45053294', '43012792', '46215877', '45520506', '44593613', '43463915', '43307420', '31727307', '31726462', '31731857', '38267983', '43287084', '38323705', '38323187', '38271304', '38556628', '38487427', '44987159', '45343856', '45523633', '34616740', '45277640', '45104462', '44441991', '45577481', '46153900', '44598432', '44415594', '46197892', '45488021', '45788276', '45028964', '44700899', '46009389', '45210558', '39201856', '42827862', '42886459', '43019650', '36403213', '37116120', '45284602', '45806316', '45777353', '45243368', '45038482', '45472060', '42888318', '45098095', '34289751', '40312293', '42233391', '35355978', '40932797', '39326078', '45683063', '45675161', '45791883', '45506869', '43716281', '40631011', '40304207', '42020807', '42743947', '45515530', '45522067', '42717104', '38524622', '38644891', '45218169', '45769357', '30239419', '36174552', '39679022', '45331235', '45897088', '45055612', '39687485', '45897602', '45469208', '45780372', '45753152', '45039073', '44882552', '45458203', '41639432', '43068920', '44404835', '39550972', '37080781', '45747617', '45725346', '46045444', '27582246', '27576444', '45502599', '45966660', '44864172', '44696240', '45992139', '40380616', '45533288', '45345625', '40407040', '44778158', '45256391', '46206336', '46129092', '45205318', '45989052', '46174870', '45084922', '37078962', '35227817', '36890038', '38471956', '38465931', '38467027', '45736394', '44672786', '46045921', '31269738', '44009597', '45812454', '44986856', '45710768', '45933759', '45053944', '40705107', '34807717', '44996552', '45811839', '45700046', '44163778', '43723091', '45802611', '43008956', '43399874', '44888915', '45664223', '45559213', '40787964', '43275130', '46196808', '37994644', '41927392', '46162583', '45814894', '45282104', '45522180', '45699667', '45303110', '45971969', '45489946', '34717448', '30827068', '34316813', '30830027', '30833301', '30896644', '31059522', '46033322', '45999253', '46151794', '45037018', '46188576', '45791112', '45999403', '45092436', '45343318', '45267327', '39202960', '39194356', '44652899', '38921956', '45090669', '45504321', '45665153', '32337261', '45949713', '46136201', '31137799', '45645329', '46194473', '45753057', '45752844', '46138292', '45948664', '45993248', '45783074', '45733476', '43029081', '40105806', '43234248', '45982558', '42742272', '27727642', '38955195', '27746730', '42090105', '45717410', '34720181', '34667900', '33636883', '43694743', '45944008', '39808227', '38864069', '45230444', '45802660', '27693193', '45107250', '44452913', '45539466', '40556226', '45736644', '46134579', '44929141', '45946021', '41328369', '45260317', '37028649', '45970897', '45268157', '45533123', '45313651', '29313863', '45761832', '46051370', '46217262', '31499069', '38643909', '39342455', '34054427', '40524794', '44926075', '41325604', '36899282', '45494468', '45803292', '45117916', '45948106', '44829145', '45785883', '32778317', '32782351', '32779304', '37620333', '40706832', '31744615', '45517172', '45289055', '46189922', '45710087', '46182298', '45788753', '45280139', '46179112', '44831745', '45723345', '45749744', '38744633', '45509155', '45756800', '44825978', '44613596', '44667415', '46182612', '45738993', '45118455', '45068144', '46165455', '45092563', '39932705', '46162555', '36162097', '45214207', '42875065', '45899321', '44408199', '40182881', '46008577', '42959730', '45445288', '41124657', '40431476', '38559514']

    # with open('evaluate/Condefects_Filter_Data.pkl', 'rb') as file:
    #         Condefects_Filter_Data = pickle.load(file)

    process_num = 0
    # 遍历文件夹中的所有内容
    questions = os.listdir(root_path)
    for question in questions:
        if process_num > rangeIndex:
            print("达到上线: " + str(rangeIndex))
            break
        question_path = os.path.join(root_path, question)

        # 检查是否为文件夹
        if os.path.isdir(question_path):
            try:
                java_path = os.path.join(question_path,"Python")
                questions = os.listdir(java_path)
                answers = os.listdir(java_path)
            except:
                print("列出JavaPath "+java_path+" 失败")
                continue
            for answer in answers:
                if str(answer) not in Condefects_Filter_Data:
                    continue
                process_num+=1
                if process_num > rangeIndex:
                    print("达到上线: "+str(rangeIndex))
                    break
                print("正在跑Condefects上的 "+experiment_model+" 实验： "+str(experiment_index)+" 的第 "+str(process_num)+" 个程序")

                #给代码增加行号
                AddLineNumber.process_code(os.path.join(java_path, answer), "faultyVersion.py")
                # code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c")
                # 增加行号的code_location
                # code_location = os.path.join(root_path, versionStr, "test_data/defect_root/source/tcas.c_indexed.txt")
                code_location = os.path.join(java_path, answer, "faultyVersion.py_indexed.txt")
                faulte_data_path = os.path.join(java_path, answer, "faultLocation.txt")
                ans_path = os.path.join(java_path, answer, experiment_model,str(experiment_index))
                faulte_data_index = get_fault_data(faulte_data_path)

                isok = send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index, experiment_model)
                i=0
                # if isok is True:
                #     Condefects_Filter_Data.append(answer)
                # else:
                #     print(code_location+ "不可用")
                #     continue



def run_Codeflaws(prompt,experiment_index,experiment_model,rangeIndex):
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/version/"
    Codeflaws_Filter_Data = []
    with open("evaluate/Codeflaws_Filter_Data.pkl", "rb") as f:
        Codeflaws_Filter_Data = pickle.load(f)

    process_num = 0

    for versionInt in range(1, 1544):
        # if versionInt in errlist:
        #     print("跳过:",versionInt)
        #     continue
        versionStr = "v" + str(versionInt);
        if versionStr not in Codeflaws_Filter_Data:
            print("跳过:"+versionStr)
            continue

        #在遍历达到一定个数后退出
        process_num +=1

        # print("processing: " + versionStr+" 第"+process_num+"个")
        if process_num>rangeIndex:
            break

        print("正在跑Codeflaws上的 " + experiment_model + " 实验： " + str(experiment_index) + " 的第 " + str(
            process_num) + " 个程序")

        # 数据目录
        # 给代码增加行号
        AddLineNumber.process_code(os.path.join(root_path, versionStr, "test_data/defect_root/source"), "tcas.c")
        # code_location = os.path.join(root_path,versionStr,"test_data/defect_root/source/tcas.c")
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

        isok = send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index, experiment_model)

def run_all(prompt):
    # 批量跑实验
    experiment_model = "gpt-3.5-turbo"
    for i in [1, 2, 3, 4, 5]:
        run_Condefects(prompt, i, experiment_model, 503)
    # for i in [1, 2, 3, 4, 5]:
    #     run_Codeflaws(prompt, i, experiment_model, 503)
    # # run_Condefects(prompt, "test", experiment_model, 503)

if __name__ == "__main__":
    prompt_location = "./prompts/prompt1-all.txt"
    with open(prompt_location, 'r', encoding='utf-8') as file:
        # 读取文件内容并保存到字符串中
        prompt = file.read()

    run_all(prompt)








