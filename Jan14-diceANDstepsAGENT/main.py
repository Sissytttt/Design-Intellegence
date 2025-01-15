from letta import create_client
from tools import *
from characterAgents import *
from utils import *
from letta.schemas.block import Block 

book_description = "The system is a Game system for user to navigate a map " \
+ "and is building AI tools to make it easier to make random navigation " \
+ "and deploy LLM agents."

org_block = Block(label="company", value=book_description )


client = create_client()
# create_roll_dice_tool(client)


# create roll_dice agent
agent1 = "roll_dice"

step_agent = create_agent(client, org_block, agent1, "you help with rolling a dice to decide the steps to go in the game", [roll_dice_tool_id])

agent_state1 = client.get_agent(client.get_agent_id(agent1))


# create find_direction agent
agent2 = "get_direction"

direction_agent = create_agent(client, org_block, agent2, "you help with deciding which direction to go in the game", [get_direction_tool_id])

agent_state = client.get_agent(client.get_agent_id(agent2))

client.get_block(org_block.id)

# client.delete_tool("get_step")
# get_direction_tool = client.create_tool(get_dir)
get_direction_tool_id = "tool-7cd4af71-e31c-403e-af45-8b0a860731f3"
# get_steps_tool = client.create_tool(get_step)

# client.update_tool(id = "tool-24257f7c-bd17-43a1-9ab5-dc55192e63fa", func = get_step())
get_steps_tool_id = "tool-24257f7c-bd17-43a1-9ab5-dc55192e63fa"



game_agent_persona="You are an orchestrator agent for a board game simulation. "\
    + "Your job is to give the player a random direction from the 'get_dir' tool and a random number of steps  from the 'get_step' tool to let the player know where to go. "\
    + "Each time when interact with the user, you need to execute a game move."\
    + "To execute a game move, first you need to reply the user's question first, if they are not asking, just give it a reply."\
    + "after that, you need to call the `get_direction` tool to determine the direction, "\
    + "then call the `roll_dice` tool to determine the number of steps. "\
    + "After obtaining both the direction and the number of steps, combine these into a game move "\
    + "and relay the information to the user. "\
    + "Repeat this process for every turn to provide continuous game updates."


create_agent(client, org_block, "game_agent", game_agent_persona, [get_direction_tool_id, get_steps_tool_id])

client_state = client.get_agent(client.get_agent_id("game_agent"))

response = client.send_message(
    agent_name="game_agent", 
    role="system", 
    message="Run Game"
)
response=format_response(response)
# print(response)


while True:
    # Get user input
    user_message = input("\n\nYou: ")
    
    # Exit condition
    if user_message.lower() in ["exit", "quit"]:
        print("Ending the conversation. Goodbye!")
        break

    # Interact with the agent
    response = client.user_message(client_state.id, message=user_message)
    if len(response.messages) > 1:
        # format_agent_response(response)
        output = format_response(response)
        print("\nresponse: ", output)
    else:
        print("Agent: No response from the agent.")
    
