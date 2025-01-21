from letta import create_client

client = create_client()


def generate_new_storyclip():
    """
    Ask the narrator agent to generate a new clip of the story.

    Args: 
        client: An instance of `letta.client.client.LocalClient`, used to communicate with agents.

    Returns:
        str: a new story fragment.
    """
    prompt = f"please generate the next story clip"
    response = client.send_message(
        agent_name="narrator",
        role="system",
        message=prompt
    )
    return response

# def let_observe_func(agent_name: str, story_fragment: str):
#     """
#     Sends a message to the specified agent, allowing them to observe a story fragment and reflect on it.

#     Args: 
#         agent_name (str): The name of the character(agent) to whom the story will be sent and present to.
#         story_fragment (str): The part of the story that is generated and is observed by the character (agent).

#     Returns:
#         str: The agent's thought to the story fragment.
#     """
#     prompt = f"You observe: {story_fragment}. Please reflect to it according to your personality and charcteristics, and also in relation to your personal goals. What are your thoughts?"
#     response = client.send_message(
#         agent_name=agent_name,
#         role="system",
#         message=prompt
#     )
#     return response


def let_observe_func():
    print("hi")

def test():
    print("hi")

def let_speak_func(agent_name: str, story_fragment: str):
    """
    Sends a message to the specified agent, asking them to react or respond to a story fragment.

    Args: 
        agent_name (str): The name of the character(agent) to whom the story will be sent and present to.
        story_fragment (str): The part of the story that is generated and is propting the character (agent) to react.

    Returns:
        str: The agent's response to the story fragment.
    """
    prompt = f"There happens: {story_fragment}. What would you like to say?"
    response = client.send_message(
        agent_name=agent_name,
        role="system",
        message=prompt
    )
    return response


