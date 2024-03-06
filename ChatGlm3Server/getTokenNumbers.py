import tiktoken # pip install tiktoken

def get_openai_token_len(text, model="text-davinci-001"):
    """
    获取 prompt 的 token 长度
    masscode://snippets/0i8a-yjF
    2023-04-25 13:37:12
    https://github.com/openai/tiktoken
    :return:
    """
    enc = tiktoken.get_encoding("cl100k_base")
    assert enc.decode(enc.encode("hello world")) == "hello world"

    # To get the tokeniser corresponding to a specific model in the OpenAI API:
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    # print(tokens)
    # print(enc.decode(tokens))
    return len(tokens)

if __name__ == "__main__":
    # send_request_and_save_to_file()
    # response = send_request_and_return("你是谁")
    response = get_openai_token_len("text", model="text-davinci-001")
    i=0