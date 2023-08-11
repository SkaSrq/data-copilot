import os

import chainlit as cl
from langchain.agents import AgentExecutor,AgentType
from langchain.agents import Tool
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.sql_database import SQLDatabase
from prompts import prefix
from dotenv import load_dotenv
load_dotenv()
from secret_key import openai_key

template = """Question: {question}

Answer: Let's think step by step."""


def agent_factory():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_key)
    llm_math = LLMMathChain(llm=llm)
    math_tool = Tool(
        name='Calculator',
        func=llm_math.run,
        description='Useful for when you need to answer questions about math.'
    )
    prompt = PromptTemplate(
        input_variables=["query"],
        template="If you generate any sql query do not add limit on that query. Here is a prompt - {query}"
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # initialize the LLM tool
    llm_tool = Tool(
        name='Language Model',
        func=llm_chain.run,
        description='use this tool for general purpose queries and logic'
    )
    db_user = "admin"
    db_password = "Admin123"
    db_host = "unremot-db.ci4i0mtcvbbw.ap-southeast-2.rds.amazonaws.com"
    db_name = "data_copilot"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    toolkit.get_tools().append(llm_tool)
    toolkit.get_tools().append(math_tool)
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, prefix=prefix)
    return agent_executor


@cl.on_chat_start
def main():
    agent_executor = agent_factory()
    cl.user_session.set("agent", agent_executor)


@cl.on_message
async def main(message: str):
    prompt = '''
    Average order value or AoV is  the average value of an order, calculated as (Sum of all order value / Number of orders), Average product value is (Sum of all order value / Number of products sold)
                For order value we use Gross revenue (both repeat and acquisition) and quantity is the quantity of products.
                '''
    acq='''acquisition is column name start with acq '''
    RS='''R/S or Revenue by spend is a metric used to understand the profitability of a particular product line, and is simply (Sum of net revenue / Sum of all marketing and branding spends) .'''
    cap='Whenever CAPSULES comes in product name then define this product is a capsule.'
    channel="""In the products database table, marketing or expense channels are represented using two distinct columns for each channel. These columns differentiate between costs associated with acquiring new customers (often prefixed with "acq_" or ending in "new") and costs associated with retaining existing or old customers (often prefixed with "rep" or ending in "_repeat"). Columns associated with acquiring new customers typically have a name ending in "new_spend" or start with "acq".
Columns associated with retaining old customers typically have a name ending in "repeat_spend" or start with "rep"""
    agent_executor: AgentExecutor = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    resp = await cl.make_async(agent_executor.run)(prompt+acq+RS+cap+channel+message, callbacks=[cb])
    final_message = cl.Message(content=resp)
    await final_message.send()
