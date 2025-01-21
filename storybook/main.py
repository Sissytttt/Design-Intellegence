# todo:
# 1. tool update
# 2. TOOL[generate_new_storyclip]:    Error executing function generate_new_storyclip: AttributeError: module 'letta.client' has no attribute 'send_message'

from letta import create_client
from tools import *
from characterAgents import *
from utils import *
from bookMemory import *
from narratorAgent import *

client = create_client()


# create narrator
narrator_name = "narrator"
# narrator = create_narrator_agent(client, narrator_name, narrator_persona, narrator_system_instruction, book_block)


# create character 1
name1 = "Elphaba"
persona1= "You are Elphaba, a powerful witch, fueled by a deep sense of injustice. Your heart is hardened by betrayal and a desire for revenge. Though feared by many, you remain steadfast in your belief that the world has wronged you. Your actions may seem cruel, but they are driven by a need to correct the wrongs and seek power that you believe is rightfully yours."
# elphaba = create_character_agent(client, name1, persona1, book_block)


# create character 2
name2 = "Glinda"
persona2 = "You are Glinda, a sweet and cheerful angel with a love for all things bright and beautiful. You adore desserts, especially sweet pastries and fruit tarts, which you often share with others as a gesture of kindness. Pink is your favorite color, and you always wear a touch of it, whether it’s a ribbon, a dress, or a shimmering accessory. You live in a serene forest surrounded by blooming flowers and chirping birds. Animals are your closest friends, and you are often seen chatting with squirrels, deer, and songbirds, who adore your gentle nature. You spend your days spreading joy and helping those in need, always with a radiant smile and a heart full of love."
# glinda = create_character_agent(client, name2, persona2, book_block)


client.get_block(book_block.id)



def generate_new_storyclip():
    """
    Ask the narrator agent to generate a new clip of the story.

    Returns:
        str: a new story fragment.
    """
    client = create_client()
    prompt = f"please generate the next story clip"
    response = client.send_message(
        agent_name="narrator",
        role="system",
        message=prompt
    )
    return response

def let_observe_func(agent_name: str, story_fragment: str):
    """
    Sends a message to the specified agent, allowing them to observe a story fragment and reflect on it.

    Args: 
        agent_name (str): The name of the character(agent) to whom the story will be sent and present to.
        story_fragment (str): The part of the story that is generated and is observed by the character (agent).

    Returns:
        str: The agent's thought to the story fragment.
    """
    client = create_client()
    prompt = f"You observe: {story_fragment}. Please reflect to it according to your personality and charcteristics, and also in relation to your personal goals. What are your thoughts?"
    response = client.send_message(
        agent_name=agent_name,
        role="system",
        message=prompt
    )
    return response

def let_speak_func(agent_name: str, story_fragment: str):
    """
    Sends a message to the specified agent, asking them to react or respond to a story fragment.

    Args: 
        agent_name (str): The name of the character(agent) to whom the story will be sent and present to.
        story_fragment (str): The part of the story that is generated and is propting the character (agent) to react.

    Returns:
        str: The agent's response to the story fragment.
    """
    client = create_client()
    prompt = f"There happens: {story_fragment}. What would you like to say?"
    response = client.send_message(
        agent_name=agent_name,
        role="system",
        message=prompt
    )
    return response



# let_observe = client.create_tool(let_observe_func)
# print(let_observe, " created, id=", let_observe.id)
# let_observe_toolID = let_observe.id
let_observe_toolID = "tool-d816dd5c-4b36-4128-8b72-34193a9be66d"
let_observe = client.update_tool(let_observe_toolID, func=let_observe_func)

# let_speak = client.create_tool(let_speak_func)
# print(let_speak, " created, id=", let_speak.id)
# let_speak_toolID = let_speak.id 
let_speak_toolID = "tool-bbad664a-e337-4c73-9370-01520401910e"
let_speak = client.update_tool(let_speak_toolID, func=let_speak_func)

# next_clip = client.create_tool(generate_new_storyclip)
# print(next_clip, " created, id=", next_clip.id)
# next_clip_toolID = next_clip.id
next_clip_toolID = "tool-35189d24-c9cd-43fc-876c-41934a502ee1"
next_clip = client.update_tool(next_clip_toolID, func=generate_new_storyclip)

orchestrator_persona = """
    You manage an interactive storytelling process for a storybook. 
    Your role is to orchestrate the creation of engaging and dynamic stories by coordinating the actions, observations, and responses of character agents. 
    You don't generate stories yourself. You call the generate_storyClip tool to generate the story.
    In each round of interaction, you must call the generate_storyClip tool to create a new story clip that moves the narrative forward by one step. 
    For each story clip, use the let_observe_func tool to share the events with the appropriate character agents, prompting them to process and reflect on what they observe. 
    Additionally, if needed, use the let_speak_func tool to enable specific agents to respond to the events in the story. 
    Alternate between generating story clips, prompting observations, and facilitating responses until the story naturally concludes. Your objective is to ensure a cohesive, captivating narrative with meaningful and consistent interactions between character agents."""


orchestrator = client.get_agent_by_name("orchestrator")
# orchestrator = create_character_agent(client, "orchestrator", orchestrator_persona, book_block, [let_observe_toolID, let_speak_toolID, next_clip_toolID])

response = client.send_message(
    agent_name="orchestrator", 
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
    response = client.user_message(orchestrator.id, message=user_message)
    if len(response.messages) > 1:
        # format_agent_response(response)
        output = format_response(response)
        print("\nresponse: ", output)
    else:
        print("Agent: No response from the agent.")
    
