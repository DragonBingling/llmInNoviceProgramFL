import json
import re
import pickle


def load_pkl_data(pkl_path):
    with open(pkl_path, 'rb') as file:
        loaded_data = pickle.load(file)

    faultlist = loaded_data['faultLocalization']
    for index in range(len(faultlist)):
        print(faultlist[index]['lineNumber'])
    i=0
        


if __name__ == "__main__":
    test_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/Codeflaws/version/v1/test_data/modelAns/response.pkl"
    load_pkl_data(test_path)