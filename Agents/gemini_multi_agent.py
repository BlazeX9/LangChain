from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from agent_tools import *
import streamlit
load_dotenv()

llm = ChatGoogleGenerativeAI(api_key=os.getenv("GOOGLE_API_KEY"),model="gemini-3.1-flash-lite",temperature=0)

llm_tools = llm.bind_tools([AddTwoNumbers,MultiplyTwoNumbers,SaveToFile,ReadFromFile,DeleteFile,UpdateToFile])

llm_tools = llm.bind_tools([AddTwoNumbers,MultiplyTwoNumbers,SaveToFile,ReadFromFile,DeleteFile,UpdateToFile,add_student,show_all_students,update_student,delete_student])

tool_map = {
    "AddTwoNumbers": AddTwoNumbers,
    "MultiplyTwoNumbers": MultiplyTwoNumbers,
    "SaveToFile": SaveToFile,
    "ReadFromFile": ReadFromFile,
    "DeleteFile": DeleteFile,
    "UpdateToFile": UpdateToFile,
    "add_student": add_student,
    "show_all_students": show_all_students,
    "update_student": update_student,
    "delete_student": delete_student
}

streamlit.title("LangChain Gemini-3.1 ChatBot")
user_input = streamlit.text_area("Ask your question: ")
user_submit = streamlit.button("Submit")

if user_submit and user_input:
    response = llm_tools.invoke(user_input)

    if response.tool_calls:
        for tool in response.tool_calls:
            tool_name = tool["name"]
            tool_args = tool["args"]
    
            if tool_name in tool_map:
                result = tool_map[tool_name].invoke(tool_args)
                streamlit.write("**Agent:**", result)
            else:
                streamlit.write("Unknown tool:", tool_name)
    else:
        streamlit.write("**Agent:**", response.content)