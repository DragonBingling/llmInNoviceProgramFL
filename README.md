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



## 4. Run

为了方便实验的复现，我们将主要代码整理成**CodeArrange**文件夹中。复现实验仅需要关注这个文件夹。

ChatGlm3Server 与 LocalTest 文件夹是真实实验过程中在两个服务器上运行的源代码。其中ChatGlm3Server面向开源大模型，LocalTest面向商业大模型。



进入**CodeArrange**文件夹：

Sendpromt用于向大模型发送请求并收集结果。

- 其中，send_prompt_openai_gpt函数用于GPT的请求发送，在该函数中，需要将base_url与api_key改成请求对应的链接地址和key，可以在官网购买额度。
- send_prompt_openai_form用于开源大模型的请求，只需要修改对请求地址为上文LLM的api地址即可。key可随意填写。
- <u>可以先测试Sendpromt请求通过后，再进行下一步</u>。

ReadJsonTest用于提取LLM返回的结果中的json字段

getTokenNumbers用于提取prompt的token数量。

AddLineNumber用于处理源代码，将每一行加上行号。

------

Gpt4-AllSend，Gpt3-5-AllSend，GLM3-AllSend，LLama2-AllSend，codeLLama-AllSend 用于向各个大模型批量的发送新手程序错误定位的请求，并将结果数据存入data之中。

在运行前需要修改一些属于你的配置，这里我们以Gpt4-AllSend举例：

- prompt_location 用于获取prompt，可以修改成你自定义的prompt
- run_Codeflaws 与 run_Codeflaws 是向相应数据集整体遍历请求一次数据，其中 root_path 需要修改成数据集存放的地址。
- Condefects_Filter_Data.pkl 存放着我们在数据集中过滤出来的程序信息。

------

Gpt4-prompt-various 用于对多种不同的prompt进行实验，prompt都存放在prompts文件夹之中。



## 5. Evaluate

进入Evaluate文件夹，为对数据结果进行评估的代码

### Accuracy Count

进入Evaluate文件夹，在total_count文件中对各个LLM的精确性进行统计，在sbfl_mbfl_count中对sbfl与mbfl的精确性进行统计。<u>运行前注意修改root_path为相应的数据集地址。</u>若是用上文提供的数据集源数据，注意开源LLM与GPT的数据集地址不一样，root_path注意修改。



### Overlap 

进入 Evaluate/venn 目录下 Calc_venn_all_Codeflaws 与 Calc_venn_all_Condefects 文件用于评估统计并绘制venn图。与上一步类似，修改好每个root_path之后运行即可。



### Prompt ablation

进入Evaluate文件夹，prompt_various_count_Codeflaws文件与 prompt_various_count_Condefects 文件用于统计不同的消融结果。

