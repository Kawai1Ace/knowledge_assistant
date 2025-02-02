import os
os.environ['http_proxy'] = "172.18.166.31:7899"
os.environ['https_proxy'] = "172.18.166.31:7899"

import sys
sys.path.append("../")

from langchain_openai import ChatOpenAI
from llm.call_llm import parse_llm_api_key

def model_to_llm(model: str=None, temperature: float=0.0, appid: str=None, api_key: str=None, Spark_api_secrte: str=None, Wenxin_secret_key:str=None):
    if model in ["gpt-4o-mini"]:
        if api_key == None:
            api_key = parse_llm_api_key("openai")
        llm = ChatOpenAI(model_name=model, temperature=temperature, openai_api_key=api_key, base_url="https://api.pumpkinaigc.online/v1")
    else:
        raise ValueError(f"model{model} not support!!!")
    return llm