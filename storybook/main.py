from letta import create_client
from tools import *
from characterAgents import *
from utils import *
from bookMemory import *


client = create_client()

# create character 1
name1 = "Elphaba"
persona1= "You are Elphaba, a powerful witch, fueled by a deep sense of injustice. Your heart is hardened by betrayal and a desire for revenge. Though feared by many, you remain steadfast in your belief that the world has wronged you. Your actions may seem cruel, but they are driven by a need to correct the wrongs and seek power that you believe is rightfully yours."
elphaba = create_character_agent(client, name1, persona1, book_block)


# # create character 2
name2 = "Glinda"
persona2 = "You are Glinda, a sweet and cheerful angel with a love for all things bright and beautiful. You adore desserts, especially sweet pastries and fruit tarts, which you often share with others as a gesture of kindness. Pink is your favorite color, and you always wear a touch of it, whether it’s a ribbon, a dress, or a shimmering accessory. You live in a serene forest surrounded by blooming flowers and chirping birds. Animals are your closest friends, and you are often seen chatting with squirrels, deer, and songbirds, who adore your gentle nature. You spend your days spreading joy and helping those in need, always with a radiant smile and a heart full of love."
glinda = create_character_agent(client, name2, persona2, book_block)


# client.get_block(book_block.id)


# game_agent_persona="You are an orchestrator agent for a board game simulation. "\
#     + "Your job is to give the player a random direction from the 'get_dir' tool and a random number of steps  from the 'get_step' tool to let the player know where to go. "\
#     + "Each time when interact with the user, you need to execute a game move."\
#     + "To execute a game move, first you need to reply the user's question first, if they are not asking, just give it a reply."\
#     + "after that, you need to call the `get_direction` tool to determine the direction, "\
#     + "then call the `roll_dice` tool to determine the number of steps. "\
#     + "After obtaining both the direction and the number of steps, combine these into a game move "\
#     + "and relay the information to the user. "\
#     + "Repeat this process for every turn to provide continuous game updates."


# create_agent(client, book_block, "game_agent", game_agent_persona, [get_direction_tool_id, get_steps_tool_id])

# client_state = client.get_agent(client.get_agent_id("game_agent"))

response = client.send_message(
    agent_name="Elphaba", 
    role="system", 
    message="hi, nice to meet you"
)
response=format_response(response)
print(response)


while True:
    # Get user input
    user_message = input("\n\nYou: ")
    
    # Exit condition
    if user_message.lower() in ["exit", "quit"]:
        print("Ending the conversation. Goodbye!")
        break

    # Interact with the agent
    response = client.user_message(elphaba.id, message=user_message)
    if len(response.messages) > 1:
        # format_agent_response(response)
        output = format_response(response)
        print("\nresponse: ", output)
    else:
        print("Agent: No response from the agent.")
    
