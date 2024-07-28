import streamlit as st
import os
import pandas as pd
import openai
from dotenv import load_dotenv


st.header('_:rainbow[Dynamic Checklist]_ ' , divider="grey")

def clear_text():
    st.session_state.new_item = ""

# This version clears the field but doesn't save the input.
new_item = st.text_input("Enter text here", on_change=clear_text, key='new_item')

# st.write(my_text)




def main():
    # st.title("Dynamic Checklist Example")

    # Initialize session state for storing checklist items
    if "checklist_items" not in st.session_state:
        st.session_state.checklist_items = []

    def clear_text():
        st.session_state.new_item = ""
    # Text input for adding new checklist items
    new_item = st.text_input("Enter text here")
    # Button to add the new item to the checklist
    if st.button("Add Item"):
        if new_item:
            st.session_state.checklist_items.append(new_item)
            st.experimental_rerun()  # Rerun the app to update the UI

    # Display checkboxes for each item in the checklist
    checked_items = {item: st.checkbox(item) for item in st.session_state.checklist_items}

    st.write("tasks you finished:")
    for item, checked in checked_items.items():
        if checked:
            st.write(f"- {item}")






if __name__ == "__main__":
    main()
