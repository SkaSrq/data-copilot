import chainlit as cl
import openai
import os
from langchain.agents import AgentExecutor, AgentType
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
from prefix import prefix
from table_info import custom_table_info
load_dotenv()
def agent_factory():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    # db_user = "admin"
    # db_password = "Admin123"
    # db_host = "unremot-db.ci4i0mtcvbbw.ap-southeast-2.rds.amazonaws.com"
    # db_name = "data_copilot"
    db = SQLDatabase.from_uri(os.getenv("DATABASE_URL"),
                              include_tables=['products'],
                              sample_rows_in_table_info=3,
                              custom_table_info=custom_table_info)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True,
                                      agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, prefix=prefix
                                      )
    return agent_executor


@cl.on_chat_start
def main():
    agent_executor = agent_factory()
    cl.user_session.set("agent", agent_executor)


@cl.on_message
async def main(message: str):
    agent_executor: AgentExecutor = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    resp = await cl.make_async(agent_executor.run)(message, callbacks=[cb])
    final_message = cl.Message(content=resp)
    await final_message.send()
