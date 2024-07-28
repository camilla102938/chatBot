import streamlit as st
import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
# from pandasai.llm.openai import OpenAI
# from pandasai import PandasAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

message_history = [{"role": "user", "content": f"say OK."},
                   {"role": "assistant", "content": f"OK"}]


openai_api_key = os.getenv(
    "sk-AxwlgEAV2j6zWFVdhU8OT3BlbkFJHFveeaVJQJpy3hQyZUbYy")

st.set_page_config(page_title="📊 ChatCSV", page_icon="📊")
st.header("📊 ChatCSV")

input_csv = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])


def chat_with_csv(df, input):

    openai_api_key = os.getenv(
        "sk-AxwlgEAV2j6zWFVdhU8OT3BlbkFJHFveeaVJQJpy3hQyZUbYy")

    # llm = OpenAI(api_token=openai_api_key)

    llm = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=openai_api_key)

    # pandas_ai = PandasAI(llm)
    # result = pandas_ai.run(df, prompt=input)

    agent = create_pandas_dataframe_agent(
        llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)
    result = agent.run(df, input)

    print(result)
    return result


if input_csv:
    data = pd.read_csv(input_csv)
    st.dataframe(data)

    input_text = st.text_area("Enter your query")

    if input_text:
        if st.button("Chat with CSV"):
            st.info("Your Query: " + input_text)
            result = chat_with_csv(data, input_text)
            st.success(result)
