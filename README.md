Understanding the Test : The initial step involved thoroughly understanding the provided test description, including mission, ground rules, and deployment options. We had to first go through openfabrics documentation (https://docs.openfabric.ai/developer-tools/index/) to understand the underlying data structures, classes and functions inside the project directory.
Framework Selection: The project utilizes the Openfabric PySDK for interacting with the Openfabric platform and handling execution context.
Preprocessing module, in which we pass the custom dataset consisting of Sample Questions and Answers that the customer may ask to the chatbot and their possible answers.
The dataset is in a pdf format that we load using PyPDFloader from langchain library
In this module firstly we load the pdf
 Then we create vector embeddings using sentence-transformers/all-MiniLM-L6-v2 from Huggingface Embeddings.
We then store these vector embeddings in a folder named vectorstore using FAISS Code snippet :
.
Secondly, we have the Chainlit (UI) and LLM processing module. In this module we set our custom prompt template as follows:

After setting the custom prompt template we setup our LLM. For our implementation we have used GPT 4:

After this we setup our UI interface using Chainlit. Chainlit is an open-source Python package to build production ready Conversational AI.
For this we define two functions - @on_messge function and the @on_chat_start function as follows -
The on_chat_start function initializes the UI interface with an opening message
The on_messsage function handles the input query by the user and performs the following the functionalities -
Decorator `@cl.on_message`:
- This decorator is used to register a function (`on_message`) as an event handler for incoming messages in the chat system.
Function `on_message(message: cl.Message)`:
-        This function is called whenever a new message is received in the chat system.
-        It takes a `cl.Message` object (`message`) as input, representing the incoming message.
3. Variable Initialization:
- The code initializes variables `prompt`, `response`, `response_content`, and `bot_answer`.
4. Prompt Construction:
- The variable `prompt` is assigned the value of `prompt_template`, which likely contains a template for generating prompts to the chatbot.
Generation of Response from OpenAI's GPT-4:
-        The `client.chat.completions.create()` function is called to generate a response from OpenAI's GPT-4 model.
-        The `messages` parameter contains a list of dictionaries representing the chat history, including both system and user messages.
-        The `settings` parameter likely contains configuration settings for the GPT-4 model.
Parsing of Response Content:
-        The content of the response received from the GPT-4 model is parsed and stored in the
`response_content` variable.
-        The JSON content of the response is accessed using `response.choices[0].message.content`.
-        The parsed JSON content likely contains fields such as `"bot_answer"`, `"query_state"`,
`"department"`, and `"possible_solution"`.
Saving Response to File:
 The entire JSON response content is saved to a file named "admin.txt" with proper formatting.
The `json.dump()` function is used to write the JSON content to the file with an indentation of 4 spaces for readability.
Saving Response to File:
 The entire JSON response content is saved to a file named "admin.txt" with proper formatting.
The `json.dump()` function is used to write the JSON content to the file with an indentation of 4 spaces for readability.
 A newline character (`\n`) is added after each JSON entry to separate them in the file.
Sending Bot's Response:
The bot's answer (`bot_answer`) extracted from the response content is sent as a message in the chat system.
The `await cl.Message(content=bot_answer).send()` statement sends the bot's response to the user.
