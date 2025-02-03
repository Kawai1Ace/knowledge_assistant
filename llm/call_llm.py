import openai
import json
import requests
import _thread as thread
import base64
import datetime
from dotenv import load_dotenv, find_dotenv
import hashlib
import hmac
import os
import queue
from urllib.parse import urlparse
import ssl
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import zhipuai
from langchain.utils import get_from_dict_or_env
from typing import Optional, Dict

from openai import OpenAI

# 使用websocket_client
import websocket

def get_completion(prompt: str, model: str, temperature=0.1, api_key=None, secret_key=None, access_token=None, appid=None, api_secret=None, max_tokens=2048):
    """
    调用大模型获取回复，支持上述三种模型+gpt
    arguments:
    prompt: 输入提示
    model：模型名
    temperature: 温度系数
    api_key：如名
    secret_key, access_token：调用文心系列模型需要
    appid, api_secret: 调用星火系列模型需要
    max_tokens : 返回最长序列
    return: 模型返回，字符串
    """
    
    # 调用GPT
    if model in ['gpt-4o-mini']:
        return get_completion_gpt(prompt, model, temperature, api_key, max_tokens)

    else:
        return "Error Model"
    
def get_completion_gpt(prompt: str, model: str, temperature:float, api_key: str, max_tokens: int):
    # 原生OpenAI接口
    if api_key == None:
        api_key = parse_llm_api_key("openai")
    openai.api_key = api_key
    
    client = OpenAI(
        api_key=openai.api_key,
        base_url="https://api.pumpkinaigc.online/v1"
    )
    
    # 具体调用
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

def get_access_token(api_key, secret_key):
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    # 指定网址
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    # 设置 POST 访问
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # 通过 POST 访问获取账户对应的 access_token
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def parse_llm_api_key(model:str, env_file: Optional[Dict]=None):
    """
    通过 model 和 env_file 的来解析平台参数
    """   
    if env_file == None:
        _ = load_dotenv(find_dotenv())
        env_file = os.environ
    
    if model == "openai":
        return env_file["OPENAI_API_KEY"]
    elif model == "wenxin":
        return env_file["WENXIN_API_KEY"], env_file["WENXIN_SECRET_KEY"]
    elif model == "spark":
        return env_file["SPARK_API_KEY"], env_file["SPARK_APPID"], env_file["SPARK_API_SECRET"]
    elif model == "zhipu":
        # return env_file["ZHIPU_API_KEY"]
        return get_from_dict_or_env(env_file, "ZHIPU_API_KEY", "ZHIPU_API_KEY")
    else:
        raise ValueError(f"model{model} not support!!!")
    
    
# class Ws_param(object):
#     # 初始化
#     def __init__(self, APPID, APIKey, APISecret, Spark_url):
#         self.APPID = APPID
#         self.APIKey = APIKey
#         self.APISecret = APISecret
#         self.host = urlparse(Spark_url).netloc
#         self.path = urlparse(Spark_url).path
        