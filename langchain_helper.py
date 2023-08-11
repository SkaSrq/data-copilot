from secret_key import openai_key
import os
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY'] = openai_key
llm = OpenAI(temperature=0)
