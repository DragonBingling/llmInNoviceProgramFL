# Overall
This is all the experimental code for an empirical study on the performance of LLMs in assisting novice programmers with fault localization, along with specific steps for paper replication.



## 1. Requirements

找到根目录的 requirements.txt ，运行以下依赖命令。

```
pip install -r requirements.txt
```

若是还有缺少的依赖，可以根据信息依次使用pip导入。



## 2. LLMs

In this study, multiple different LLMs were used for experimentation, namely ChatGPT-4, ChatGPT-3.5, ChatGLM3, Llama2, and Code LLama.

Among these, ChatGLM3, Llama2, and Code LLama are open-source LLMs that can be deployed following their respective official documentation. The versions used and their corresponding official website links are provided below:

**ChatGLM3-6b:** https://github.com/THUDM/ChatGLM3

**Llama-2-7b-chat-hf:** https://huggingface.co/meta-llama/Llama-2-7b-chat-hf

**CodeLlama-7b-Instruct-hf :** https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf



对于商业大模型ChatGPT-4, ChatGPT-3.5，我们使用官方提供的API接口进行实验。

为了规范化实验，在所有开源大模型上，都使用商业大模型格式的接口来进行实验。如何部署商业大模型格式的api接口，可以参考 https://github.com/xusenlinzy/api-for-open-llm 。



## 3. Dataset



本实验的所有原始数据代码可以在（https://drive.google.com/file/d/19DZCtlhmq_7994gy6-0NwVRGRiUu04JE/view?usp=sharing）中下载。

其中，本实验在两个服务器上并行进行，data存放着ChatGPT-4与ChatGPT3.5的实验数据，data_openLLM存放着ChatGLM3, Llama2, and Code LLama 的实验数据。

data文件夹和data_openLLM文件夹中，都各自包含一个完整的codeflaws数据集和一个condefects数据集。

本实验的所有实验数据都直接存在codeflaws与condefects数据集的各个版本分支下，例如，ChatGPT-4 在 codeflaws-v1的实验结果存放在目录

```
raw_datas\data\codeflaws\version\v1\test_data\gpt-4 
```

下。









记得修改你的key。

记得修改prompt的地址。
