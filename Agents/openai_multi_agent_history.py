from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from agent_tools import *
import streamlit

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4.1-mini",temperature=0)
llm_tools = llm.bind_tools([
    AddTwoNumbers,
    MultiplyTwoNumbers,
    SaveToFile,
    ReadFromFile,
    DeleteFile,
    UpdateToFile,
    add_student,
    show_all_students,
    update_student,
    delete_student
])

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

streamlit.set_page_config(page_title="OpenAI Agent",page_icon="🤖")
streamlit.title("🤖 LangChain OpenAI Agent")

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

    response = llm_tools.invoke(user_input)

    if response.tool_calls:
        for tool in response.tool_calls:
            tool_name = tool["name"]
            tool_args = tool["args"]

            if tool_name in tool_map:
                result = tool_map[tool_name].invoke(tool_args)
                with streamlit.chat_message("assistant"):
                    streamlit.write(result)

                streamlit.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result
                })

            else:
                with streamlit.chat_message("assistant"):
                    streamlit.write("Unknown tool")

                streamlit.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Unknown tool"
                })

    else:
        with streamlit.chat_message("assistant"):
            streamlit.write(response.content)

        streamlit.session_state.chat_history.append({
            "role": "assistant",
            "content": response.content
        })