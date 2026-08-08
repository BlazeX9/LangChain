#pip install langchain_openai streamlit
from dotenv import load_dotenv
import os
import streamlit
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4.1-mini",temperature=0)

streamlit.set_page_config(page_title="GPT-4.1",page_icon="🤖")
streamlit.title("🤖 OpenAI Teacher")
streamlit.write("Ask me anything and I will explain it in simple English")

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

    conversation = ""

    for message in streamlit.session_state.chat_history:
        conversation += f"{message['role']}: {message['content']}\n"

    prompt = PromptTemplate.from_template("""
    You are an AI Teacher who can explain things in simple English
    Conversation: {conversation}
    """)
    
    parser = StrOutputParser()
    chain = prompt | llm | parser

    with streamlit.chat_message("assistant"):
        with streamlit.spinner("Thinking..."):
            response = chain.invoke({
                "conversation": conversation
            })
        streamlit.write(response)

    streamlit.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })
