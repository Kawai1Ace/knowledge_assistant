import os
import sys

# 这段代码的功能是将当前文件的父目录路径添加到系统模块搜索路径中，使得可以从父目录导入模块。
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from langchain.embeddings.huggingface import HuggingFaceEmbeddings 
from langchain_openai import OpenAIEmbeddings
from llm.call_llm import parse_llm_api_key  

def get_embeddings(embedding: str, embedding_key: str=None, env_file: str=None):
    if embedding == "m3e":
        return HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
    if embedding == None:
        embedding_key = parse_llm_api_key(embedding)
    if embedding == "openai":
        return OpenAIEmbeddings(openai_api_key=embedding_key, base_url="https://api.pumpkinaigc.online/v1")
    else:
        raise ValueError("embedding not supported")