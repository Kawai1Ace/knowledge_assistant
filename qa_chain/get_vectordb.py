import os
import sys

from langchain_openai import OpenAIEmbeddings
from database.create_db import create_db, load_knowledge_db

openai_embeddings = OpenAIEmbeddings(
    base_url="https://api.pumpkinaigc.online/v1",
    api_key="sk-8zrnDuUQreC9nX6l0399Ac9a85574e4d8243Ad7a62Ef1778"
)