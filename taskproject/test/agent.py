import streamlit as st
import pandas as pd
import json
from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent

import environ

env = environ.Env()
environ.Env.read_env()

API_KEY = env("apikey")


def create_agent(filename: str):

    llmodel = OpenAI(openai_api_key=API_KEY)

    df = pd.read_csv(filename)

    return create_pandas_dataframe_agent(llmodel, df, verbose=False)


# Query Agent

def query_agent(agent, query):

    prompt = (
        """
            For the following query, if it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            There can only be two types of chart, "bar" and "line".

            If it is just asking a question that requires neither, reply as follows:
            {"answer": "answer"}
            Example:
            {"answer": "The title with the highest rating is 'Gilead'"}

            If you do not know the answer, reply as follows:
            {"answer": "I do not know."}

            Return all output as a string.

            All strings in "columns" list and data list, should be in double quotes,

            For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

            Lets think step by step.

            Below is the query.
            Query: 
            """
        + query
    )

    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    return response.__str__()


def decode_response(response: str) -> dict:

    return json.loads(response)


def write_response(response_dict: dict):

    if "answer" in response_dict:
        st.write(response_dict["answer"])

    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)


# Interface Code

st.title("📊 ChatCSV - Find Insights From Your CSV")
st.write("ChatCSV is a tool that allows you to query a large language model (LLM) to find insights from your CSV file. It is powered by the OpenAI API.")

data = st.file_uploader("Upload a CSV file", type=["csv"])

query = st.text_input("Ask a question")

if st.button("Submit", type="primary"):
    # Creating an agent
    agent = create_agent(data)

    # Querying the agent
    response = query_agent(agent=agent, query=query)

    # Decode the response

    decoded_response = decode_response(response)

    # Write the response
    write_response(decoded_response)
