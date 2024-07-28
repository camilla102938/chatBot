import streamlit as st
import os
import pandas as pd
import openai
from dotenv import load_dotenv

st.set_page_config(page_title=" ChatCSV")
st.header("ChatCSV")


load_dotenv("openai.env")
openai.api_key = os.getenv(
    "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")


def predict(input):
    global message_history

    print(message_history)

    message_history.append({"role": "user", "content": input})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    print('???', input, '???')

    reply_content = completion.choices[0].message.content
    print('!!!', reply_content, '!!!')

    message_history.append({"role": "assistant", "content": reply_content})
    response = [(message_history[i]["content"],
                message_history[i+1]["content"])
                for i in range(2, len(message_history)-1, 2)]

    print('?!?!', response, '!?!?')
    return response


input_csv = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])

if input_csv:

    data = pd.read_csv(input_csv)
    # text = st.text(data)

    message_history = [{"role": "user", "content": f"{data} If you understand, say OK."},
                       {"role": "assistant", "content": f"OK"}]

    input_text = st.text_area("Enter your query")
    submit = st.button("Send with CSV")

    if input_text:
        if submit:
            print('send')
            st.info("Your Query: " + predict(input_text))
            print('sent')
