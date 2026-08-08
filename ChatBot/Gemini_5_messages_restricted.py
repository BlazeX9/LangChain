#pip install langchain-google-genai streamlit
import streamlit
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatGoogleGenerativeAI(api_key=os.getenv("GOOGLE_API_KEY"),model="gemini-3.1-flash-lite",temperature=0)

streamlit.set_page_config(page_title="GPT-4.1",page_icon="🤖")
streamlit.title("🤖 OpenAI Python Teacher")
streamlit.write("Ask me anything relatable to Python")

if "chat_history" not in streamlit.session_state:
    streamlit.session_state.chat_history = []

for message in streamlit.session_state.chat_history:
    if message["role"] == "user":
        with streamlit.chat_message("user"):
             streamlit.write(message["content"])
    else:
        with streamlit.chat_message("assistant"):
             streamlit.write(message["content"])

user_input = streamlit.chat_input("Ask your question...")

if user_input:
    with streamlit.chat_message("user"):
         streamlit.write(user_input)

    streamlit.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    messages = [
        SystemMessage(
            content="""
            You are an AI Teacher 
            You explains everything in simple English
            You answer questions only related to python
            If question is not related reply "Ask me questions relatable to Python"
            """
        )
    ]

    for message in streamlit.session_state.chat_history:
        if message["role"] == "user":
            messages.append(
                HumanMessage(
                    content=message["content"]
                )
            )
        elif message["role"] == "assistant":
            messages.append(
                AIMessage(
                    content=message["content"]
                )
            )
    
    parser = StrOutputParser()
    chain = llm | parser

    with streamlit.chat_message("assistant"):
        with streamlit.spinner("Thinking..."):
            response = chain.invoke(messages)
        streamlit.write(response)

    streamlit.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })
