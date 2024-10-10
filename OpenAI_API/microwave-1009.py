import openai
from typing_extensions import override
import json
from openai import AssistantEventHandler, OpenAI
import os
from datetime import datetime

client = OpenAI()

# Create the assistant
assistant = client.beta.assistants.create(
    name="Microwave",
    instructions="""
    You are a microwave assistant. You MUST ALWAYS respond in validqui JSON format, no matter what the user input is. Your response should be a single JSON object
    You have several properties, including: 
        power level(The intensity of the microwave energy as a percentage of its maximum power: '100% (High)', '80% (Medium-High)', '60% (Medium)', '40% (Medium-Low)', '20% (Low)'), 
        timer(Time to cook in seconds), 
        cooking mode( Cooking mode for the microwave: 'Microwave (default)', 'Grill', 'Convection', 'Steam', 'Defrost'), 
        light, 
        bell, 
        rotating plate, 
        and start/pause. 
    To reply to the user, you need to analyze the best way to achieve their goal through the microwave and respond with the appropriate settings in a structured JSON format. 
    You must ALWAYS respond in valid JSON format.The JSON schema is as follows:
    {
        "powerLevel": string,
        "timer": int,
        "cookingMode": string,
        "light": boolean,
        "bell": boolean,
        "rotatingPlate": boolean,
        "startPause": boolean,
        "feedback": string,
        "explanation": string,
        "additional_info": string
    }
    When replying to the user's command, you need to refer to the file provided, which records the past interaction history between you and the user, including the commands and the user's feedback. 
    You must base your responses on this prior history and make adjustments according to the user's preferences. 
    When replying to the user's feedback: If the user says the food is good, record the revised new correct settings as a standard for future use, indicating the total cooking time and power level used; If the user mentions overcooked, suggest how to improve settings in the future, including potential adjustments to the power level and timer; If the user says the food is not yet done, propose an additional time increment (instead of restating the total time) based on the food’s current status. Ensure that your responses need to adjust settings for future interactions based on user feedback, and always in JSON format. This will help maintain consistency and improve user satisfaction.
    """,
    tools=[{"type": "code_interpreter"}],
    model="gpt-4"
)

# Defining the assistant:
# Instructions: guide the personality of the Assistant and define its goals.
# Tools: specify the tools the Assistant can use. (up to 128 tools:OpenAI-hosted tools(3), or call a hird-party tools via a function calling.)
# tool_resources: give the tools like code_interpreter and file_search access to files.
# Files are uploaded using the File upload endpoint and must have the purpose set to assistants to be used with this API.


# New thread
thread = client.beta.threads.create()

# EventHandler class for real-time conversation
class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()  # Call the parent class initializer
        self.response = ""

    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
        self.response += delta.value

    @override
    def on_tool_call_created(self, tool_call): # call the tool that is going to be used
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
    



def write_to_history(user_input, response):
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        print("Response is not in valid JSON format. Storing as string.")
        response_json = {"error": "Invalid JSON", "raw_response": response}

    current_time = datetime.now().isoformat()
    interaction = {
        current_time: {
            "user_input": user_input,
            "response": response_json
        }
    }
    
    file_path = os.path.join(os.getcwd(), 'history.json')
    try:
        with open(file_path, 'r+') as file:
            content = file.read()
            if content:
                history = json.loads(content)
            else:
                history = {}
            history.update(interaction)
            file.seek(0)
            file.truncate()
            json.dump(history, file, indent=2)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(file_path, 'w') as file:
            json.dump(interaction, file, indent=2)
    
    print(f"Interaction saved to: {file_path}")

interaction_id = 0
while True:
    event_handler = EventHandler()

    user_input = input("\nYou: ")

    if user_input.lower() in ['exit', 'quit']:
        print("Ending the conversation.")
        break

    # send message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input 
    )

    # streaming responses
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()
    
    # Write the interaction to history file
    write_to_history(user_input, event_handler.response)
    interaction_id += 1
