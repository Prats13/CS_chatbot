import os
from openai import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from dotenv import load_dotenv
import json

import chainlit as cl

load_dotenv()

# Access the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is available
if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

client = OpenAI(api_key=api_key)

prompt_template = ChatPromptTemplate.from_messages(
    [
    ("system", 
    """
    Description: Develop a customer support chatbot for a fintech company that provides various financial services and products. The chatbot should be capable of handling customer queries, categorizing them as either "junk/common" or "complex," and assigning complex queries to the appropriate department for resolution. Additionally, the chatbot should provide helpful solutions to complex queries to assist the department in resolving them efficiently.

    Specifications:

    The chatbot should prompt the user for their query.
    After receiving the query, the chatbot should analyze it and determine whether it's a common, simple query or a complex one.
    If the query is common or junk, the chatbot should generate a short and helpful response to address the user's query.
    If the query is complex, the chatbot should identify the appropriate department to handle the query and assign it accordingly.
    For complex queries, the chatbot should also provide a possible solution to assist the department in resolving the issue effectively.
    The output should be in JSON format, including the user's query, the query state (complex or junk), the department (if applicable), and a possible solution (if applicable).

    Output should be in JSON Format containing following fields:
    "user_query": "How do I reset my password?",
    "bot_answer": "To reset your password, go to the login page and click on 'Forgot Password.' Follow the instructions sent to your registered email.",
    "query_state": "junk",
    "department": "",
    "possible_solution": ""

    "user_query": "I'm concerned about the security of my account. I received an email asking for sensitive information, but I'm not sure if it's legitimate. Can you verify if the email is from your company and provide guidance on what to do next?",
    "bot_answer": "Thank you for bringing this to our attention. We take the security of our customers' accounts very seriously. To ensure your safety, please forward the suspicious email to our security team at security@company.com. They will investigate the email and provide further instructions on how to proceed. In the meantime, refrain from clicking on any links or providing any sensitive information mentioned in the email.",
    "query_state": "complex",
    "department": "Security Team",
    "possible_solution": "The user is experiencing a security concern. Check with the security policies and the risk policies to incorporate or modify in the app and if needed modify it"
    """
    ),
    ("user", "{user_message}\n"),
    ]
)


settings = {
    "model": "gpt-4",
    "temperature": 0,
}

@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to your Personalised Customer Support Bot. How can I help you today?"
    await msg.update()

@cl.on_message
async def on_message(message: cl.Message):
    prompt = prompt_template
    response = client.chat.completions.create(
        messages=[
            {
                "content": str(prompt_template),
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    response_content = json.loads(response.choices[0].message.content)
    bot_answer = response_content.get("bot_answer", "")

    # Save the entire JSON response to admin.txt with proper formatting
    with open("admin.txt", "a") as admin_file:
        json.dump(response_content, admin_file, indent=4)
        admin_file.write("\n")  # Add a newline after each JSON entry

    await cl.Message(content=bot_answer).send()


