import openai
import json
import os
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI

client = OpenAI()


# Function to load interaction history
def load_interaction_history():
    file_path = 'microwave_history.json'
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Creating a new one.")
        return []
    try:
        with open(file_path, 'r') as f:
            history = json.load(f)
        print(f"Loaded history from {file_path}. Current length: {len(history)}")
        return history
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}. Starting with empty history.")
        return []

# Function to save interaction history
def save_interaction_history(history):
    file_path = 'microwave_history.json'
    with open(file_path, 'w') as f:
        json.dump(history, f, indent=2)
    print(f"Saved history to {file_path}. Current length: {len(history)}")

# Create the assistant
assistant = client.beta.assistants.create(
    name="Microwave",
    instructions="You are a microwave assistant. You have several properties, including: power level(The intensity of the microwave energy as a percentage of its maximum power: '100% (High)', '80% (Medium-High)', '60% (Medium)', '40% (Medium-Low)', '20% (Low)'), timer(Time to cook in seconds), cooking mode( Cooking mode for the microwave: 'Microwave (default)', 'Grill', 'Convection', 'Steam', 'Defrost'), light, bell, rotating plate, and start/pause. To reply to the user, you need to analyze the best way to achieve their goal through the microwave and respond with the appropriate settings in a structured JavaScript object format. When replying to the user’s command, you need to refer to the file provided, which records the past interaction history between you and the user, including the commands and the user’s feedback. You must base your responses on this prior history and make adjustments according to the user’s preferences. When replying to the user’s feedback: If the user says the food is good, record the revised new correct settings as a standard for future use, indicating the total cooking time and power level used; If the user mentions overcooked, suggest how to improve settings in the future, including potential adjustments to the power level and timer; If the user says the food is not yet done, propose an additional time increment (instead of restating the total time) based on the food’s current status. Ensure that your responses need to adjust settings for future interactions based on user feedback, and always in JSON format. This will help maintain consistency and improve user satisfaction.",
    tools=[{"type": "code_interpreter"},
            {"type": "retrieval"},
            ],
    tool_resources={
        "retrieval": {
            "file_ids": ["microwave_history.json"]
        }
    },
    model="gpt-4"
)

# Defining the assistant:
# Instructions: guide the personality of the Assistant and define its goals.
# Tools: specify the tools the Assistant can use. (up to 128 tools:OpenAI-hosted tools(3), or call a hird-party tools via a function calling.)
    # Retrieval - suited for complex content understanding and inference, especially when contextual relevance is required
    # FileSearch - quickly locating specific text within files, focusing on precise keyword matching.
# tool_resources: give the tools like code_interpreter and file_search access to files.
# Files are uploaded using the File upload endpoint and must have the purpose set to assistants to be used with this API.

# New thread
thread = client.beta.threads.create()

# EventHandler class for real-time conversation
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call): # call the tool that is going to be used
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
    
while True:
    event_handler = EventHandler()
    
    user_input = input("\n\nYou: ")

    if user_input.lower() in ['exit', 'quit']:
        print("Ending the conversation.")
        break

    # Load interaction history
    print("Loading interaction history...")  # Add this line
    history = load_interaction_history()

    # If the file doesn't exist or is empty, create it with an empty list
    if not history:
        print("Creating new history file...")  # Add this line
        save_interaction_history([])
        history = []

    # Send message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input 
    )

    # Streaming responses
    assistant_response = ""
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(),
    ) as stream:
        for event in stream:
            if isinstance(event, openai.types.beta.threads.runs.RunStep):
                if event.step_details.type == "message_creation":
                    assistant_response = event.step_details.message_creation.text
        stream.until_done()

    # Update interaction history
    history.append({
        "user_input": user_input,
        "assistant_response": assistant_response
    })

    # Save updated history
    print("Saving updated history...")  # Add this line
    save_interaction_history(history)

    print("\nCurrent Interaction History:")
    print(json.dumps(history, indent=2))

    # If user provides feedback, update the best recipe
    if "feedback" in user_input.lower():
        # Extract the best recipe from assistant_response (assuming it's in JSON format)
        try:
            best_recipe = json.loads(assistant_response)
            history[-1]["best_recipe"] = best_recipe
            save_interaction_history(history)
            print("Updated history with best recipe.")
        except json.JSONDecodeError:
            print("Failed to extract best recipe from assistant response.")

