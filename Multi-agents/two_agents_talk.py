from letta import create_client
import json

client = create_client()

# Get agents by their names
storyteller_id = client.get_agent_id("Storyteller")
test_id = client.get_agent_id("test")

storyteller = client.get_agent(storyteller_id)
test = client.get_agent(test_id)

# Initial message from Storyteller
initial_message = "Hello! Let's start our conversation."

# Start the conversation
print("Starting the conversation between Storyteller and Test...")
print(f"Storyteller: {initial_message}")

current_message = initial_message

while True:
    # Send message from Storyteller to Test
    response_test = client.user_message(test.id, message=current_message)
    
    # Extract Test's reply
    if len(response_test.messages) > 1:
        for message in response_test.messages:
            if type(message).__name__ == "FunctionCallMessage" and message.function_call.name == "send_message":
                arguments = message.function_call.arguments
                arguments_dict = json.loads(arguments)
                current_message = arguments_dict["message"]
                print(f"\nTest: {current_message}")
                break
    else:
        print("Test: No response from Test.")
        break

    # Send Test's reply to Storyteller
    response_storyteller = client.user_message(storyteller.id, message=current_message)

    # Extract Storyteller's reply
    if len(response_storyteller.messages) > 1:
        for message in response_storyteller.messages:
            if type(message).__name__ == "FunctionCallMessage" and message.function_call.name == "send_message":
                arguments = message.function_call.arguments
                arguments_dict = json.loads(arguments)
                current_message = arguments_dict["message"]
                print(f"\nStoryteller: {current_message}")
                break
    else:
        print("Storyteller: No response from Storyteller.")
        break
