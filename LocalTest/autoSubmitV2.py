import json
import os.path
import pickle
import subprocess

import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
import time
import pyperclip


def getLastUrl(driver):
    time.sleep(1)
    # driver.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/nav/div[3]/div/div/span[1]/div/ol/li[1]')[-1].click()
    driver.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/nav/div[3]/div/div/span[1]/div[1]/ol/li[1]/a')[-1].click()
    time.sleep(15)
    currentUrl=driver.current_url
    return currentUrl


def startNewQuestion(driver,type=3):
    if type==3:
        driver.get('https://chat.openai.com/')
    else:
        driver.get('https://chat.openai.com/?model=gpt-4')
    time.sleep(30)


def clickButton(driver, str):
    #try 3 times
    for i in range(3):
        try:
            driver.find_elements(By.XPATH, str)[-1].click()
            break
        except WebDriverException:
            pass
        time.sleep(1)


def skipUselessButton(driver):
    # 跳过next按钮
    buttonList=driver.find_elements(By.TAG_NAME, 'button')
    for button in buttonList:
        # print(button.text)
        if button.text=="Next":
            button.click()
            break
    buttonList=driver.find_elements(By.TAG_NAME, 'button')
    for button in buttonList:
        # print(button.text)
        if button.text=="Next":
            button.click()
            break
    buttonList=driver.find_elements(By.TAG_NAME, 'button')
    for button in buttonList:
        # print(button.text)
        if button.text=="Done":
            button.click()
            break
    buttonList=driver.find_elements(By.TAG_NAME, 'button')
    for button in buttonList:
        # print(button.text)
        if "Okay" in button.text:
            button.click()
            break
    # clickButton(driver,'//button[contains(text(), "Next")]')
    # time.sleep(1)
    # clickButton(driver,'//button[contains(text(), "Next")]')
    # time.sleep(1)
    # clickButton(driver,'//button[contains(text(), "Done")]')



def loadCookie(path, driver):
    # 加载Cookie并刷新
    with open(path, "rb") as file:
        cookies = pickle.load(file)
    for cookieindex in range(len(cookies)):
        if cookieindex >= 8:
            continue
        driver.add_cookie(cookies[cookieindex])


def submitQuestion(question, driver):
    inp_search = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
    inp_search.clear()
    # inp_search.send_keys(question)
    currentPaste=pyperclip.paste()
    pyperclip.copy(question)
    # time.sleep(0.3)
    # inp_search.send_keys("\n")
    inp_search.send_keys(Keys.CONTROL,'v')
    pyperclip.copy(currentPaste)
    inp_search.send_keys("\n")
    pyperclip.copy(currentPaste)
    time.sleep(5)


def getLastAnswer(driver):
    html=driver.page_source
    # count = html.count("relative p-1 rounded-sm h-[30px] w-[30px] text-white flex items-center justify-center")
    count = html.count("relative p-1 rounded-sm h-9 w-9 text-white flex items-center justify-center")
    # inp_search = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/div/div/div/div['+str(count*2+1)+']/div/div[2]')
    # inp_search = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div[1]/div/div/div/div['+str(count*2)+']/div/div[2]/div[1]')
    # inp_search = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[1]/div/div/div/div['+str(count*2)+']/div/div[2]/div[1]')
    inp_search = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[1]/div/div/div/div['+str(count*2)+']/div/div/div[2]/div[1]')
    #//*[@id="__next"]/div[1]/div[2]/div/main/div/div[1]/div/div/div/div[2]/div/div[2]
    # //*[@id="__next"]/div[1]/div[2]/div/main/div/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div
    ans=inp_search.text

    return ans

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


def waitForAnswer(driver):
    for i in range(240):
        time.sleep(1)
        html = driver.page_source
        if "reached the current usage cap" in html:
            return None
        if html.count("h-4 w-4 m-1 md:m-0")>0:
            time.sleep(1)
            return True
    return False

def preDealStr(tempStr):
    tempList = tempStr.split("\n")
    result=""
    for index in range(len(tempList)):
        if tempList[index].strip().startswith("\"codeContent\""):
            continue
        if tempList[index].strip().startswith("\"reason\""):
            continue
        if tempList[index].strip().startswith("\"lineNumber\""):
            result+=tempList[index].strip().replace(",", "")
        else:
            result += tempList[index].strip()
    return result

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
        for i, char in enumerate(input_string[start + 1:], start=start + 1):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                # 如果大括号平衡了，则找到 JSON 字符串的结束位置
                if brace_count == 0:
                    return input_string[start: i + 1],i+1
    return None,None

def checkAnsAvailable(currentAns):
    maxTry=50
    currentTry=0
    temp = preDealStr(currentAns).replace("jsonCopy code", "")
    # print(temp)
    skipStrNum = 0
    while True:
        currentTry+=1
        if currentTry>maxTry:
            return False
        try:
            if not temp.startswith("{") or not temp.endswith("}"):
                thisTemp,tempSkipStrNum = extract_json(temp)
                if thisTemp==None and tempSkipStrNum==None:
                    return False
                skipStrNum+=tempSkipStrNum
            else:
                thisTemp=temp
            answers1Json = json.loads(thisTemp)
            break
        except:
            temp=temp[skipStrNum:]

    if "faultLocalization" not in answers1Json.keys():
        return False

    return True


def throwException(param):
    raise Exception(param)


def directlyAgain(driver):
    buttonList=driver.find_elements(By.TAG_NAME, 'button')
    for button in buttonList:
        # print(button.text)
        if button.text=="Dismiss" or button.text=="dismiss":
            # actions = ActionChains(driver)
            # actions.move_to_element(button).click()
            button.click()
            break
    # clickButton(driver, '//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div[1]/div/div[2]/div/button')
    clickButton(driver, '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[2]/form/div/div[1]/div/div[2]/div/button')
    # clickButton(driver, '//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div[1]/div/button')
    # clickButton(driver, '//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div[1]/div/div[2]/div/button/div')
    # buttonList=driver.find_elements(By.TAG_NAME, 'button')
    # for button in buttonList:
    #     # print(button.text)
    #     if button.text=="Regenerate":
    #         # actions = ActionChains(driver)
    #         # actions.move_to_element(button).click()
    #         button.click()
    #         break
    time.sleep(1)


def deal(driver,cookieName, type=3):
    # 启动浏览器并打开网站
    global retryTime
    global submitTime
    global limitTime
    startNewQuestion(driver)

    loadCookie(cookieName, driver)
    # loadCookie("cookies.pkl", driver)

    startNewQuestion(driver)

    skipUselessButton(driver)

    readFileRootPath = r"D:\Defects4JFile\NLInformationOrigin"
    outputFileRootPath = r"D:\Defects4JFile\ChatGPTAnswerOrigin - 测试用例修正"

    for repeatTime in [0, 1, 2, 3, 4]:

        for projectName in projectOrigin.keys():
            for versionInt in range(1, projectOrigin[projectName] + 1):
                versionStr = str(versionInt) + "b"

                if projectName == "Closure" and versionStr == "34b":
                    continue

                if projectName == "Closure" and versionStr == "68b":
                    continue

                if projectName == "Closure" and versionStr == "123b":
                    continue

                if projectName == "Closure" and versionStr == "132b":
                    continue

                if projectName == "Closure" and versionStr == "157b":
                    continue

                if projectName == "Closure" and versionStr == "173b":
                    continue

                readFilePath = os.path.join(readFileRootPath, projectName, versionStr, "NLInformation.in")
                if not os.path.exists(readFilePath):
                    continue
                with open(readFilePath, "rb") as file:
                    questions = pickle.load(file)

                outputDirPath = os.path.join(outputFileRootPath, projectName, versionStr)
                if not os.path.exists(outputDirPath):
                    os.makedirs(outputDirPath)

                if type == 3:
                    if repeatTime == 0:
                        outputFilePath = os.path.join(outputDirPath, "ChatGPTAnswer.out")
                        outputTxtPath = os.path.join(outputDirPath, "ChatGPTAnswer.txt")
                    else:
                        outputFilePath = os.path.join(outputDirPath, "ChatGPTAnswer_" + str(repeatTime) + ".out")
                        outputTxtPath = os.path.join(outputDirPath, "ChatGPTAnswer_" + str(repeatTime) + ".txt")
                else:
                    if repeatTime == 0:
                        outputFilePath = os.path.join(outputDirPath, "ChatGPTAnswer4.out")
                        outputTxtPath = os.path.join(outputDirPath, "ChatGPTAnswer4.txt")
                    else:
                        outputFilePath = os.path.join(outputDirPath, "ChatGPTAnswer4_" + str(repeatTime) + ".out")
                        outputTxtPath = os.path.join(outputDirPath, "ChatGPTAnswer4_" + str(repeatTime) + ".txt")
                # if os.path.exists(outputTxtPath):
                #     print(projectName, versionStr, "has been answered")
                #     continue

                answerList = []
                if os.path.exists(outputFilePath):
                    answerList= pickle.load(open(outputFilePath, "rb"))
                # for itemindex in range(len(questions)):
                itemindex=-1
                while itemindex<len(questions):
                    itemindex+=1
                    if itemindex>=len(questions):
                        break

                    # print(repeatTime,projectName, versionStr, itemindex, "start",end=" ")
                    if len(answerList) > itemindex:
                        # print("has been answered")
                        continue
                    item = questions[itemindex]

                    print(repeatTime, projectName, versionStr, itemindex, "start", end=" ")
                    if len(item["faultLineContent"])<2:
                        print("too short")
                        answerList.append({})
                        continue

                    singleAnswerResult = {}

                    print(submitTime)

                    startNewQuestion(driver, type)

                    # prompt1="Please analyze the following code snippet for potential bugs. Return the results strictly in JSON format with a single JSON object containing two fields: 'intentOfThisFunction' (to describe what the function aims to achieve), and 'faultLocalization' (a JSON array). The 'faultLocalization' array should contain five JSON objects, each with three  fields: 'lineNumber' (to indicate the line number of the suspicious code), 'codeContent' (to show the actual code) and 'reason' (to explain why this locations were identified as potentially buggy). Note: The response must be a JSON object, not a plain text description."
                    prompt1 = "Please analyze the following code snippet for potential bugs. Return the results in JSON format, consisting of a single JSON object with two fields: 'intentOfThisFunction' (describing the intended purpose of the function)," \
                              " and 'faultLocalization' (an array of JSON objects). The 'faultLocalization' array should contain up to five JSON objects, each with three fields: 'lineNumber' (indicating the line number of the suspicious code)," \
                              " 'codeContent' (showing the actual code), and 'reason' (explaining why this location is identified as potentially buggy). Note: The codes in the 'faultLocalization' array should be listed in descending order of suspicion."
                    for line in range(len(item["faultLineNumbers"])):
                        prompt1 += str(item["faultLineNumbers"][line]) + ":" + item["faultLineContent"][line].strip()+""

                    #put prompt1 into the text box
                    submitQuestion(prompt1, driver)
                    submitTime += 1
                    waitResult=waitForAnswer(driver)
                    if waitResult==None:
                        throwException("limitation error")
                    currentAns = getLastAnswer(driver)

                    while not checkAnsAvailable(currentAns):
                        # itemindex-=1
                        print("answer is not available")
                        directlyAgain(driver)
                        waitResult = waitForAnswer(driver)
                        if waitResult == None:
                            throwException("limitation error")
                        currentAns = getLastAnswer(driver)
                        # continue

                    singleAnswerResult["answer1"] = currentAns

                    if len(item["errorLogContent"]) > 0:
                        prompt2 = "I have received an error message and a unit test case related to the code snippet I provided in the first prompt. The error message is: \""

                        testCaseNum=-1
                        for testCaseIndex in range(len(item["testCaseLineNum"])):
                            if len(item["testCaseContent"][testCaseIndex])>0 and len(item["errorLogContent"][testCaseIndex])>0:
                                testCaseNum=testCaseIndex
                                print("testCaseNum",testCaseIndex)
                                break

                        # if testCaseNum==-1:
                        #     print("testCaseNum==-1")
                        if testCaseNum!=-1:
                            temp1 = ""
                            for line in range(len(item["errorLogContent"][testCaseNum])):
                                if line>0 and "---" in item["errorLogContent"][testCaseNum][line]:
                                    break
                                temp1 += item["errorLogContent"][testCaseNum][line].strip() + "\n"

                            prompt2 += temp1[:3000]
                            prompt2 += "\". Additionally, here is the unit test case: \""

                            testCases = ""
                            for line in range(len(item["testCaseLineNum"][testCaseNum])):
                                testCases += str(item["testCaseLineNum"][testCaseNum][line]) + ":" + item["testCaseContent"][testCaseNum][line].strip() + "\n"

                            prompt2 += testCases[:1000]
                            # prompt2+="\". Please analyze the code snippet along with this error message and unit test cases. Update the JSON result you provided earlier, taking into account the new information. Remember only include the top five locations in the fault localization array, ordered from the most to the least suspicious. Return only the updated JSON result without any additional content."
                            # prompt2+="\". Please analyze the given code snippet, error message, and unit test cases. Update the previously provided JSON to include 'intentOfThisFunction' describing the function's purpose, and a 'faultLocalization' array. The array should have five objects, each with 'lineNumber', 'codeContent', and 'reason' fields for the suspicious lines, in descending order of suspicion. Ensure the response is solely the updated JSON."
                            prompt2 += "\". Please analyze the code snippet from the first prompt, along with the provided error message and unit test case." \
                                       " Update and return the JSON object consisting of 'intentOfThisFunction' (describing the intended purpose of the function)," \
                                       " and 'faultLocalization' (an array of JSON objects). The 'faultLocalization' array should contain up to five JSON objects, each with three fields: 'lineNumber' (indicating the line number of the suspicious code)," \
                                       " 'codeContent' (showing the actual code), and 'reason' (explaining why this location is identified as potentially buggy)." \
                                       " Note: The codes in the 'faultLocalization' array should be listed in descending order of suspicion, and the analysis should focus exclusively on the code snippet from the first prompt and not the unit test case."
                            submitQuestion(prompt2, driver)
                            submitTime += 1

                            waitResult = waitForAnswer(driver)
                            if waitResult == None:
                                throwException("limitation error")
                            currentAns = getLastAnswer(driver)

                            retryTime = 0
                            retryMaxFlag=False
                            while not checkAnsAvailable(currentAns):
                                # itemindex-=1
                                print("answer is not available")
                                directlyAgain(driver)
                                retryTime += 1
                                if retryTime>5:
                                    print("retry time is too much")
                                    retryMaxFlag=True
                                    break
                                waitResult = waitForAnswer(driver)
                                if waitResult == None:
                                    throwException("limitation error")
                                currentAns = getLastAnswer(driver)
                                # continue

                            if retryMaxFlag==False:
                                singleAnswerResult["answer2"] = currentAns
                    # lastUrl = getLastUrl(driver)
                    # singleAnswerResult["url"]=lastUrl

                    retryTime = 0
                    answerList.append(singleAnswerResult)

                    with open(outputFilePath, "wb") as file:
                        pickle.dump(answerList, file)
                    with open(outputTxtPath, "w") as file:
                        file.write(str(answerList))

                    if type!=3:
                        if submitTime >= limitTime:
                            print(projectName, versionStr, "limited")
                            exit(0)

retryTime=0
submitTime=0
limitTime=18000
if __name__ == "__main__":

    # driver = uc.Chrome()
    #
    # driver.get('https://chat.openai.com/')
    #
    # print(driver.title)
    #
    # cookies = driver.get_cookies()
    # with open("cookies.pkl", "wb") as file:
    #     pickle.dump(cookies, file)
    # exit(0)

    type=3

    cookiesPath="D:\OneDrive\CODE\project\ChatGPTFL\cookies"
    cookiesFilesList=os.listdir(cookiesPath)
    # cookiesFilesList.sort(reverse=True)

    #choose Cookie In Turn

    index = 0  # 初始化索引

    while True:
        selected_element = cookiesFilesList[index]  # 选择当前索引处的元素
        # selected_element = cookiesFilesList[0]  # 选择当前索引处的元素
        index = (index + 1) % len(cookiesFilesList)  # 更新索引，实现循环选择
        print(selected_element)

        #get current hour
        currentHour=time.localtime(time.time()).tm_hour
        if currentHour>6:
            if "glw" in selected_element:
                print("glw is not available")
                continue

        try:

            driver = uc.Chrome()
                # position=driver.get_window_position()
                # print(position)
                # driver.set_window_position(x=1661, y=195)
                # driver.maximize_window()
            deal(driver,os.path.join(cookiesPath,selected_element),type)
            driver.close()

        except Exception as e:
            print("error",e)
            driver.close()
            if type==3:
                time.sleep(10+retryTime*10)
            else:
                time.sleep(60+retryTime*60)
            retryTime+=1
            if retryTime>10:
                time.sleep(30*60)
            continue