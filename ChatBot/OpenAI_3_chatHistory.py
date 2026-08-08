#pip install langchain_openai
from dotenv import load_dotenv                              # Load variables from the .env file
import os                                                   # Access environment variables
from langchain_openai import ChatOpenAI                     # OpenAI LLM
from langchain_core.prompts import PromptTemplate           # Create AI prompts
from langchain_core.output_parsers import StrOutputParser   # Convert AI output to text
load_dotenv()                                               # Load the .env file

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4.1-mini",temperature=0.2)

chat_history = []
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input.strip():
        print("Please enter a question")
        continue

    chat_history.append(f"User: {user_input}")
    conversation = "\n".join(chat_history)

    prompt = PromptTemplate.from_template("""
    You are an AI Teacher who can explain things in simple English.
    Conversation: {conversation}
    """)

    parser = StrOutputParser()          # Parse AI response into plain text
    chain = prompt | llm | parser       # Build the LangChain pipeline
    response = chain.invoke({           # Execute the pipeline
        "conversation": conversation
        }
    )
    print("Agent:",response)
    chat_history.append(f"Agent: {response}")
