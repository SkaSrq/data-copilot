import os

import chainlit as cl
from langchain.agents import AgentExecutor
from langchain.agents import Tool, load_tools, initialize_agent, AgentType
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from table_info import custom_table_info, table_info

from secret_key import openai_key, serp_api_key

template = """Question: {question}

Answer: Let's think step by step."""
os.environ["OPEN_API_KEY"] = openai_key
os.environ["SERPAPI_API_KEY"] = serp_api_key

_DEFAULT_TEMPLATE = """Given an input question, first understand the table structure.
These are the columns in products table use them accordingly:
acq_mrp_revenue: Revenue generated from new customer acquisitions (acq) based on the maximum retail price (MRP).
rep_mrp_revenue: Revenue generated from repeat customers (rep) based on the maximum retail price (MRP).
acq_item_discount: Discount provided to new customers (acq) on individual items.
rep_item_discount: Discount provided to repeat customers (rep) on individual items.
acq_listing_discount_uc: Listing discount for new customer acquisitions (acq) in unconverted currency.
rep_listing_discount_uc: Listing discount for repeat customers (rep) in unconverted currency.
acq_gross_revenue: Gross revenue from new customer acquisitions (acq).
rep_gross_revenue: Gross revenue from repeat customers (rep).
acq_net_revenue: Net revenue from new customer acquisitions (acq).
rep_net_revenue: Net revenue from repeat customers (rep).
acq_quantity: Quantity of products sold to new customers (acq).
rep_quantity: Quantity of products sold to repeat customers (rep).
acq_cogs: Cost of goods sold for new customer acquisitions (acq).
rep_cogs: Cost of goods sold for repeat customers (rep).
acq_logs: Logs related to new customer acquisitions (acq).
rep_logs: Logs related to repeat customers (rep).
hct_acq_final_spend: Final spend for new customer acquisitions (acq) related to hct (unclear abbreviation).
hct_repeat_final_spend: Final spend for repeat customers (rep) related to hct (unclear abbreviation).
doc_new_spend: New spend on doctor-related activities for new customers (acq).
doc_rep_spend: Spend on doctor-related activities for repeat customers (rep).
acq_influencer_spend: Spend on influencers for new customer acquisitions (acq).
repeat_influencer_spend: Spend on influencers for repeat customers (rep).
acq_content_marketing_spend: Spend on content marketing for new customer acquisitions (acq).
repeat_content_marketing_spend: Spend on content marketing for repeat customers (rep).
FB_Acq_Spend: Spend on Facebook advertising for new customer acquisitions (acq).
FB_Repeat_Spend: Spend on Facebook advertising for repeat customers (rep).
Aff_New_Spend: Spend on affiliate marketing for new customer acquisitions (acq).
Aff_Repeat_Spend: Spend on affiliate marketing for repeat customers (rep).
Partnership_New_spend: Spend on partnerships for new customer acquisitions (acq).
Partnership_Repeat_spend: Spend on partnerships for repeat customers (rep).
acq_non_working_spend: Non-working spend for new customer acquisitions (acq).
repeat_non_working_spend: Non-working spend for repeat customers (rep).
google_acq_spend: Spend on Google advertising for new customer acquisitions (acq).
google_repeat_spend: Spend on Google advertising for repeat customers (rep).
crm_new_spend: Spend on customer relationship management for new customer acquisitions (acq).
crm_repeat_spend: Spend on customer relationship management for repeat customers (rep).



1. Average order value or AoV is  the average value of an order, calculated as (Sum of all order value / Number of orders), Average product value is (Sum of all order value / Number of products sold)
 For order value we use Gross revenue (both repeat and acquisition) and quantity is the quantity of products.
2. Percentage of daily sales from a certain product is the proportion of sales (Net revenue in our table from both acquisition and repeat) contributed by a product across sales of all products
3. R/S or Revenue by spend is a metric used to understand the profitability of a particular product line, and is simply (Sum of net revenue / Sum of all marketing and branding spends) 
 
Question: {input}"""
# If someone asks for the table foobar, they really mean the employee table.

def agent_factory():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_key)
    llm_math_chain = LLMMathChain(llm=llm, verbose=True)
    # math_tool = Tool(
    #     name='Calculator',
    #     func=llm_math.run,
    #     description='Useful for when you need to answer questions about math.'
    # )

    db_user = "admin"
    db_password = "Admin123"
    db_host = "unremot-db.ci4i0mtcvbbw.ap-southeast-2.rds.amazonaws.com"
    db_name = "data_copilot"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              include_tables=["products"],
                              sample_rows_in_table_info=3,
                              custom_table_info=custom_table_info)
    sql_prompt = PromptTemplate(
        input_variables=["input"],
        template=_DEFAULT_TEMPLATE
    )
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=sql_prompt, use_query_checker=True)
    # sql_tool = Tool(
    #     name='SQL',
    #     func=db_chain.run,
    #     description='Useful for when you need to write sql query.'
    # )
    tools = []
    tools.append(Tool.from_function(func=llm_math_chain.run, name='Calculator',
                                    description='Useful for when you need to answer questions about math.'))
    tools.append(
        Tool.from_function(func=db_chain.run, name='SQL', description='Userful for when you need to write SQL query'))
    search_tools = load_tools(["serpapi"],llm=llm)
    final_tools = tools + search_tools
    agent = initialize_agent(final_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent


@cl.on_chat_start
def main():
    agent_executor = agent_factory()
    cl.user_session.set("agent", agent_executor)


@cl.on_message
async def main(message: str):
    prompt = '''''' + message
    agent_executor: AgentExecutor = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    resp = await cl.make_async(agent_executor.run)(prompt, callbacks=[cb])
    # resp = agent_executor.run(message)
    final_message = cl.Message(content=resp)
    await final_message.send()


# prompt = '''
#     Average order value or AoV is  the average value of an order, calculated as (Sum of all order value / Number of orders), Average product value is (Sum of all order value / Number of products sold)
#                 For order value we use Gross revenue (both repeat and acquisition) and quantity is the quantity of products.
#                 '''
#     acq='''acquisition is column name start with acq '''
#     RS='''R/S or Revenue by spend is a metric used to understand the profitability of a particular product line, and is simply (Sum of net revenue / Sum of all marketing and branding spends) .'''
#     cap='Whenever CAPSULES comes in product name then define this product is a capsule.'
#     channel="""In the products database table, marketing or expense channels are represented using two distinct columns for each channel. These columns differentiate between costs associated with acquiring new customers (often prefixed with "acq_" or ending in "new") and costs associated with retaining existing or old customers (often prefixed with "rep" or ending in "_repeat"). Columns associated with acquiring new customers typically have a name ending in "new_spend" or start with "acq".
# Columns associated with retaining old customers typically have a name ending in "repeat_spend" or start with "rep"""