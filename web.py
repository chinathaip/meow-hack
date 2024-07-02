import os
import streamlit as st
import ollama
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector

load_dotenv()

search_endpoint = os.environ["AZURE_AI_SEARCH_ENDPOINT"]
search_key = os.environ["AZURE_AI_SEARCH_KEY"]
search_index = os.environ["AZURE_AI_SEARCH_INDEX"]
credentials = AzureKeyCredential(search_key)

st.title("💬 MeowHack Chatbot")


def generate_message():
    response = ollama.chat(
        model="phi3", stream=True, messages=st.session_state.messages
    )
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token


## the first message of the AI assisstant ##
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello there! How can I help you today?"}
    ]

### Message History ##
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_message)
    st.session_state.messages.append(
        {"role": "assistant", "content": st.session_state["full_message"]}
    )
