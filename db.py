from langchain.agents import create_sql_agent, AgentType
from langchain.agents import load_tools
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.llms.openai import OpenAI
# from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents import load_tools
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.agents import initialize_agent

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
llm_math = LLMMathChain(llm=llm)
math_tool = Tool(
    name='Calculator',
    func=llm_math.run,
    description='Useful for when you need to answer questions about math.'
)
# when giving tools to LLM, we must pass as list of tools
tools = [math_tool]

zero_shot_agent = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3
)

db_user = "admin"
db_password = "Admin123"
db_host = "unremot-db.ci4i0mtcvbbw.ap-southeast-2.rds.amazonaws.com"
db_name = "data_copilot"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")


def get_agent():
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = load_tools(["llm-math"], llm=llm)
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
    return agent_executor
