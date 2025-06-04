import streamlit as st
import pandas as pd
import os
import time
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.memory.buffer import ConversationBufferMemory
from llm_model import ollama_response, get_table_info
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(
    page_title = "BI Agent",
)

DATA_DIR = "./data"

# file upload cleaner
# st.session_state.first_refresh = True # hard fixing
if 'first_refresh' not in st.session_state:
    st.session_state.first_refresh = True
    for f in os.listdir("data"):
        os.remove(os.path.join("./data", f))

# # message history
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

initial_message = """
You are a skilled data analyst and Python developer.\n
Write a complete and executable Streamlit Python program that loads real CSV files from a local `data/` directory and builds an interactive data dashboard.\n
\n

The following tables and their columns are the only data available:
    {table_info}

Instructions:\n
- Use `pandas` to load data from the `data/` directory\n
- Use only pandas and streamlit. Don't use deprecated modules.\n
- If relevant, **merge or join tables using appropriate keys** to consolidate the data\n
- Build an interactive Streamlit dashboard:\n
    - Add sidebar filters for relevant dimensions\n
    - Include data summaries and KPIs\n
    - Implement visualizations using Streamlit widgets\n
    - Ensure all output and analysis are based only on the provided tables and columns, do not create new column names\n
- Include all necessary import statements\n
- The code must be self-contained and runnable with: `streamlit run app.py`\n
- Output only the code inside a ```python code block\n
"""

if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )
    # Create the prompt object
    prompt = ChatPromptTemplate.from_template(initial_message)

    # Format the prompt with actual inputs
    formatted_prompt = prompt.format_messages(
        table_info=get_table_info(DATA_DIR)    
        )
    st.session_state.memory.chat_memory.add_message(SystemMessage(content=initial_message))


st.title("Build you BI Dashboard by chatting with me!")

if 'openai_api_key' in st.session_state and st.session_state.openai_api_key != "":
    st.sidebar.text_input(label="OpenAI API key", type="password", value=st.session_state.openai_api_key)
else:
    st.session_state.openai_api_key = st.sidebar.text_input(label="OpenAI API key", type="password")

# File upload form
with st.form("file upload form"):
    uploaded_files = st.file_uploader(label="File to analyze", type="csv", accept_multiple_files=True)

    submitted = st.form_submit_button("Submit")

    if uploaded_files is not None and submitted:
        for file in uploaded_files:
            dataframe = pd.read_csv(file)
            st.write(file.name)
            dataframe.to_csv(os.path.join("./data/", file.name))
    
st.header("Files in memory:")
for f in os.listdir("./data"):
    st.code(f)

if 'memory' in st.session_state:
    for message in st.session_state.memory.chat_memory.messages:
        role = message.type  # 'human' or 'ai'
        content = message.content

        with st.chat_message(role):
            if role in ["system", "human"]:
                st.markdown(content)
            else:
                st.code(content, language="python")


prompt = st.chat_input("Give me ideas to visualize!")
if prompt:
    if st.session_state.openai_api_key:
        with st.chat_message("user"):
            st.markdown(prompt)
        # st.session_state.memory.chat_memory.add_message(HumanMessage(content=prompt))
        with st.chat_message("assistant"):
            response = ollama_response(prompt, st.session_state.memory, st.session_state.openai_api_key)
            st.code(response, language="python")
            with open(os.path.join("./pages", "2_📊_Dashboard.py"), "w") as file:
                file.write(response)
        # st.session_state.memory.chat_memory.add_message(AIMessage(content=response))
    else:
        st.warning("Enter OPEN AI API key in the sidebar")
