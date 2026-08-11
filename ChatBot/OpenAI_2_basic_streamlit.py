# pip install streamlit langchain_openai
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4.1-mini",temperature=0.2)

st.title("AI Teacher")
user_input = st.chat_input("Ask your question:")

if user_input:
    if not user_input.strip():
        st.warning("Please ask a question")
    else:
        prompt = PromptTemplate.from_template("""
        You are an AI Teacher who can explain things in simple English.
        User Question: {question}
        """)

        parser = StrOutputParser()
        chain = prompt | llm | parser
        response = chain.invoke({
            "question": user_input
        })

        st.write("Agent:",response)
