# agent name to interact with:
agent_name = "test"

from letta import create_client
import json
from letta.schemas.memory import ChatMemory
from letta import client, LLMConfig, EmbeddingConfig
import inspect
from textwrap import dedent
from pprint import pprint


# define a function with a docstring
def roll_dice() -> str:
    """
    Rolls a 20-sided dice and returns the result as a string.
    
    Returns:
        str: The result of the dice roll in the format "You rolled a X", where X is a number between 1 and 20.
    """
    import random
    dice_roll = random.randint(1, 20)
    return f"You rolled a {dice_roll}"


def parse_source_code(func) -> str:
    """Parse the source code of a function and remove indendation"""
    source_code = dedent(inspect.getsource(func))
    return source_code


def create_character_agent(name, persona_description):
    agents = client.list_agents() 

    # --------------------
    tool = client.create_tool(
        func=roll_dice,           
        name="Dice Roller test",            
    )
    print(f"Created tool: {tool.name}, ID: {tool.id}")
    # --------------------

    client.set_default_embedding_config( 
    EmbeddingConfig(
        embedding_endpoint_type="openai",
        embedding_endpoint="https://api.openai.com/v1",
        embedding_model="text-embedding-ada-002",
        embedding_dim=1536,
        embedding_chunk_size=300
    )
)
    for agent in agents:
        if agent.name == name:
            client.delete_agent(client.get_agent_id(f"{name}"))
            print(f"delete {name}")
    return client.create_agent(
        name=name,
        memory=ChatMemory(
            human="",
            persona=persona_description
        ),
        llm_config=LLMConfig(
            model="gpt-4o-mini",
            model_endpoint_type="openai",
            model_endpoint="https://api.openai.com/v1",
            context_window=128000
        ),
        tool_ids=[tool.id]
    )


client = create_client()

# Get an agent by Name
create_character_agent(agent_name, "you are a helpful agent")

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

    if len(response.messages) > 1:
        print(response)
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


