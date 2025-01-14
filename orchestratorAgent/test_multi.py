from letta import create_client
import json
from letta.schemas.memory import ChatMemory
from letta import client, LLMConfig, EmbeddingConfig
import inspect
from textwrap import dedent
from pprint import pprint
from letta.schemas.block import Block 
from letta.schemas.memory import BasicBlockMemory
from typing import Optional


client = create_client()

tools = client.list_tools()

org_description = "The system is a Game system for user to navigate a map " \
+ "and is building AI tools to make it easier to make random navigation " \
+ "and deploy LLM agents."

org_block = Block(label="company", value=org_description )


class OrgMemory(BasicBlockMemory): 

    def __init__(self, persona: str, org_block: Block): 
        persona_block = Block(label="persona", value=persona)
        super().__init__(blocks=[persona_block, org_block])


def list_tools(tools): 
    for tool in tools:
        print(f"{tool.name}:  , id: {tool.id}")
        # print(tool.tool_type)
        if tool.name == "get_step" or tool.name == "roll_dice":
            print(tool.source_code)

# print(list_tools(tools))

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


def get_direction() -> str:
    """
    Returns a random direction from the four cardinal directions: East, South, West, or North.
    
    Returns:
        str: A random direction, one of "East", "South", "West", or "North".
    """
    import random
    directions = ["East", "South", "West", "North"]
    return random.choice(directions)


def create_roll_dice_tool():
    tool = client.create_tool(
        func=roll_dice,           
        name="roll_dice",            
    )
    print(f"Created tool: {tool.name}, ID: {tool.id}")

def create_get_direction_tool():
    tool = client.create_tool(
        func=get_direction,           
        name="get_direction",            
    )
    print(f"Created tool: {tool.name}, ID: {tool.id}")

# create_get_direction_tool()
get_direction_tool_id = "tool-7cd4af71-e31c-403e-af45-8b0a860731f3"
# create_roll_dice_tool()
roll_dice_tool_id = "tool-5be1794c-9e43-43fb-b82b-22e58fdb5ac6"

def create_agent(name, persona, tool=None):
    agents = client.list_agents() 
    # tools = client.list_tools()
    # print(tools)

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
            print(f"recreating {name}")
    return client.create_agent(
        name=name,
        memory=OrgMemory(
            persona=persona,
            org_block=org_block
        ),
        llm_config=LLMConfig(
            model="gpt-4o-mini",
            model_endpoint_type="openai",
            model_endpoint="https://api.openai.com/v1",
            context_window=128000
        ),
        tool_ids=tool if tool else []
    )


# create roll_dice agent
agent1 = "roll_dice"

step_agent = create_agent(agent1, "you help with rolling a dice to decide the steps to go in the game", [roll_dice_tool_id])

agent_state1 = client.get_agent(client.get_agent_id(agent1))


# create find_direction agent
agent2 = "get_direction"

direction_agent = create_agent(agent2, "you help with deciding which direction to go in the game", [get_direction_tool_id])

agent_state = client.get_agent(client.get_agent_id(agent2))


def format_response(response):
    # print(response)
    if hasattr(response, "dict"):
        response = response.dict()
    output = ""
    for message in response.get("messages", []):
        if message.get("message_type") == "reasoning_message":
            output += f"\n- Reasoning: {message.get('reasoning', 'No reasoning message replied')}"
        if message.get("message_type") == "tool_call_message":
            tool_call = message.get("tool_call", {})
            output += f"\nTOOL[{tool_call.get('name')}]:  "
            if tool_call["name"] == "send_message":
                arguments = tool_call.get("arguments", "{}")
                arguments_data = json.loads(arguments)
                output += f"  {arguments_data.get('message')}"
        if message.get("message_type") == "tool_return_message":
            tool_return = message.get("tool_return", "{}")
            tool_return_data = json.loads(tool_return)
            if tool_return_data.get('message') != "None":
                output += f"  {tool_return_data.get('message')}"
    return output

# create orh agent

client.get_block(org_block.id)

def get_dir():
    """
    Get a random direction.

    Returns:
        direction (str): the direction to go
    """
    client = create_client()
    message = f"Generate a direction to go"
    print("Sending message to get_direction: ", message)
    response = client.send_message(
        agent_name="direction_agent",
        role="system",
        message=message
    )
    # print(format_response(response))
    return response

def get_step():
    """
    Get a random number of step to go.

    Returns:
        step_num (int): the number of steps to go
    """
    client = create_client()
    message = f"Roll me a dice"
    print("Sending message to roll_dice agent: ", message)
    response = client.send_message(
        agent_name="roll_dice",
        role="system",
        message=message
    )
    # print(format_response(response))
    return response


# client.delete_tool("get_step")
# get_direction_tool = client.create_tool(get_dir)
get_direction_tool_id = "tool-7cd4af71-e31c-403e-af45-8b0a860731f3"
# get_steps_tool = client.create_tool(get_step)

client.update_tool(id = "tool-24257f7c-bd17-43a1-9ab5-dc55192e63fa", func = get_step())
get_steps_tool_id = "tool-24257f7c-bd17-43a1-9ab5-dc55192e63fa"


# game_agent_persona="You are an orchestrator agent for a board game simulation. "\
#     + "Your job is to give the player a random direction from the 'get_dir' tool and a random number of steps  from the 'get_step' tool to let the player know where to go. "\
#     + "Each time when interact with the user, you need to execute a game move."\
#     + "To execute a game move, first you need to reply the user's question first, if they are not asking, just give it a reply."\
#     + "after that, you need to call the `get_direction` tool to determine the direction, "\
#     + "then call the `roll_dice` tool to determine the number of steps. "\
#     + "After obtaining both the direction and the number of steps, combine these into a game move "\
#     + "and relay the information to the user. "\
#     + "Repeat this process for every turn to provide continuous game updates."


# create_agent("game_agent", game_agent_persona, [get_direction_tool_id, get_steps_tool_id])

# client_state = client.get_agent(client.get_agent_id("game_agent"))

# response = client.send_message(
#     agent_name="game_agent", 
#     role="system", 
#     message="Run Game"
# )
# response=format_response(response)
# # print(response)


# while True:
#     # Get user input
#     user_message = input("\n\nYou: ")
    
#     # Exit condition
#     if user_message.lower() in ["exit", "quit"]:
#         print("Ending the conversation. Goodbye!")
#         break

#     # Interact with the agent
#     response = client.user_message(client_state.id, message=user_message)
#     if len(response.messages) > 1:
#         # format_agent_response(response)
#         output = format_response(response)
#         print("\nresponse: ", output)
#     else:
#         print("Agent: No response from the agent.")
    

