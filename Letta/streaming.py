# agent name to interact with:
agent_name = "Storyteller"
# agent_name = "test1"
# agent_name = "MIXI"
from letta import create_client
import json

client = create_client()

# Get an agent by Name
agent_state = client.get_agent(client.get_agent_id(agent_name))

# Start a streaming conversation
print("Start chatting with the agent! Type 'exit' to end the conversation.")

while True:
    # Get user input
    user_message = input("\n\nYou: ")
    
    # Exit condition
    if user_message.lower() in ["exit", "quit"]:
        print("Ending the conversation. Goodbye!")
        break

    # Interact with the agent
    response = client.user_message(agent_state.id, message=user_message)

    '''response:
        [
            InternalMonologue (...,internal_monologue="Updating user's name from Sissy to Julia for accurate interactions."))
            FunctionCallMessage (..., tool_call=FunctionCall(name='core_memory_replace', arguments='{\n  "name": "human",\n  "old_content": "Sissy",\n  "new_content": "Li Bo",\n  "request_heartbeat": true\n}')
            FunctionReturn (status='success')
            ...
        ]
    '''
    if len(response.messages) > 1:
        for i, message in enumerate(response.messages):
            class_name = type(message).__name__ 
            if class_name == "ReasoningMessage":
                print(f"\nReasoningMessage: {message.reasoning}")
            elif class_name == "ToolCallMessage":
                if message.tool_call.name == 'send_message':
                    arguments = message.tool_call.arguments
                    arguments_dict = json.loads(arguments)
                    print(f"\nSend_Message: {arguments_dict['message']}")
                else:
                    print(f"{message.tool_call.name}: {message.tool_call.arguments}")
            elif class_name == "ToolReturnMessage":
                    tool_return_dict = json.loads(message.tool_return)
                    print(f"\nFunctionReturn: {tool_return_dict['status']}, Status: {message.status}")
            else:
                print("UnknownClassType: ", message)
    else:
        print("Agent: No response from the agent.")