# Overall
This is all the experimental code for an empirical study on the performance of LLMs in assisting novice programmers with fault localization, along with specific steps for paper replication.



## 1. Requirements

Locate the **requirements.txt** file in the root directory and execute the following dependency command.

```
pip install -r requirements.txt
```

Should there be any additional dependencies missing, feel free to sequentially import them using pip based on the provided information.



## 2. LLMs

In this study, multiple different LLMs were used for experimentation, namely ChatGPT-4, ChatGPT-3.5, ChatGLM3, Llama2, and Code LLama.

Among these, ChatGLM3, Llama2, and Code LLama are open-source LLMs that can be deployed following their respective official documentation. The versions used and their corresponding official website links are provided below:

**ChatGLM3-6b:** https://github.com/THUDM/ChatGLM3

**Llama-2-7b-chat-hf:** https://huggingface.co/meta-llama/Llama-2-7b-chat-hf

**CodeLlama-7b-Instruct-hf :** https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf



For conducting experiments on commercial LLMs like ChatGPT-4 and ChatGPT-3.5, we utilize the official API interfaces provided.

To standardize our experiments, for all open-source LLMs, we employ the API interfaces in the format of commercial LLMs. Instructions on deploying a commercial LLM form API interface can be found at https://github.com/xusenlinzy/api-for-open-llm.



## 3. Dataset



The raw data and code for this experiment can be downloaded from https://drive.google.com/file/d/19DZCtlhmq_7994gy6-0NwVRGRiUu04JE/view?usp=sharing.

In this experiment, parallel processes are conducted on two servers. The 'data' directory contains experimental data for ChatGPT-4 and ChatGPT-3.5, while the 'data_openLLM' directory houses experimental data for ChatGLM3, Llama2, and Code LLama.

Within both the 'data' and 'data_openLLM' directories, there exists a complete CodeFlaws dataset and a ConDefects dataset.

All experimental data for this study is directly stored within various versions of the CodeFlaws and ConDefects datasets. For instance, the experimental results for ChatGPT-4 in CodeFlaws-v1 are stored in the directory blow.

```
raw_datas\data\codeflaws\version\v1\test_data\gpt-4 
```



## 4. Run

To facilitate experiment reproducibility, we have organized the main code into the **CodeArrange** directory. <u>Replicating the experiments only requires attention to this folder.</u>

The ChatGLM3Server and LocalTest folders contain the source code used during the actual experiment on two servers. ChatGLM3Server is tailored for open-source large models, while LocalTest is designed for commercial large models.



- Navigate to the **CodeArrange** directory:

  **Sendpromt** is used to send requests to LLMs and collect results.

  - Within it, the function *send_prompt_openai_gpt* is used for sending requests to GPT. In this function, the *base_url* and *api_key* need to be changed to correspond to the requested link address and key, which can be obtained by purchasing credits on the official website.
  - The *send_prompt_openai_form* function is used for requests to open-source LLMs. Simply modify the request address to the API address of the aforementioned LLM. The key can be filled in arbitrarily.
  - <u>It is advisable to test the Sendpromt requests for successful validation before proceeding to the next step.</u>

The *ReadJsonTest* function is utilized to extract the JSON fields from the results returned by the LLM.

The *getTokenNumbers* function is employed to extract the token count of the prompt.

*AddLineNumber* is responsible for processing the source code by adding line numbers to each line.

------

Gpt4-AllSend, Gpt3-5-AllSend, GLM3-AllSend, LLama2-AllSend, and codeLLama-AllSend are employed to dispatch requests for novice program fault localization in bulk to various LLMs, subsequently storing the resulting data in the 'data' repository.

Before execution, certain configurations pertaining to your setup necessitate adjustments. For illustrative purposes, let us consider the instance of *Gpt4-AllSend*:

- The *'prompt_location'* parameter serves to acquire prompts and can be altered to accommodate a custom prompt of your choice.
- Both *'run_Codeflaws'* function and *'run_Condefects'*  function involve traversing the respective datasets once for data retrieval, with the *<u>'root_path'</u>* requiring adjustment to reflect the location where the dataset is stored.
- *'Condefects_Filter_Data.pkl'* houses the program information filtered from our dataset.

------

The file *'Gpt4-prompt-various'* is utilized to conduct experiments with a variety of distinct prompts, all of which are housed within the 'prompts' directory.

## 5. Evaluate

Navigate to the *"Evaluate"* directory for the code responsible for evaluating the results of the data.

### Accuracy Count

Enter the "Evaluate" directory to calculate the accuracy of each LLM in the 'total_count' file and to assess the accuracy of SBFL and MBFL in the 'sbfl_mbfl_count' file. <u>*Remember to adjust the 'root_path' to the appropriate dataset location before executing*</u>. If utilizing the dataset sources from the previous sections, please be mindful that the dataset locations for open-source LLMs and GPT may differ, so ensure to modify the 'root_path' accordingly.



### Overlap 

Navigate to the *"Evaluate/venn"* directory. Utilize the *"Calc_venn_all_Codeflaws"* and *"Calc_venn_all_Condefects"* files for assessing, calculating statistics, and generating Venn diagrams. Similar to the previous step, ensure to adjust each *'root_path'* accordingly before execution.



### Prompt ablation

Enter the *"Evaluate"* directory. The *"prompt_various_count_Codeflaws"* file and the *"prompt_various_count_Condefects"* file are used for tallying diverse ablation outcomes.

