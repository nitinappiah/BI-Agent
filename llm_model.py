from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama
import os
import pandas as pd
from langchain.agents import (
    AgentExecutor, create_react_agent, create_structured_chat_agent, create_tool_calling_agent
)
from langchain import hub

import re

def extract_python_code(text):
    # Regex to find code between ```python and ```
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def get_table_info(dir):
    result = ""
    for file in os.listdir(dir):
        result += f"{file} - columns: {list(pd.read_csv(os.path.join(dir, file)).columns)}\n"
    return result

def ollama_response(query, memory, openai_api_key):
    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = ChatOpenAI(model="o4-mini", openai_api_key=openai_api_key)
    agent = create_tool_calling_agent(llm=llm, tools=[], prompt=prompt)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=[],
        verbose=True,
        memory=memory,
        handle_parsing_errors=True
    )

    template = """
        Generate or modify python code to satisfy the request.

        {query}

        Here is the details about the data:

        {table_info}

    """
    prompt = ChatPromptTemplate.from_template(template)
    formatted_prompt = prompt.format_messages(
        query = query,
        table_info = get_table_info('./data')
        )
    response = agent_executor.invoke({"input": formatted_prompt[0].content})
    return extract_python_code(response['output'])

if __name__ == '__main__':
    print(ollama_response(dir="./data", query="create me a comprehensive dashboard with interesting plots"))