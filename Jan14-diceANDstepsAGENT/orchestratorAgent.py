from letta import create_client




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

