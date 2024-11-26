from letta import create_client

# Create the client instance
client = create_client()

def send_message_to(message, role, agent_id=None, agent_name=None, recipient=None, **kwargs):
    """
    Wrapper for send_message that includes the recipient in the message.
    
    Arguments:
        message (str): The content of the message.
        role (str): The role of the sender (e.g., 'user' or 'assistant').
        agent_id (str, optional): The ID of the agent receiving the message.
        agent_name (str, optional): The name of the agent receiving the message.
        recipient (str, optional): The name of the intended recipient.
        **kwargs: Additional arguments to pass to the original send_message.
    
    Returns:
        LettaResponse: The response from the agent.
    """
    if recipient:
        # Add recipient label to the message
        labeled_message = f"To: {recipient}\n{message}"
    else:
        labeled_message = message

    # Call the original send_message function
    return client.send_message(
        message=labeled_message,
        role=role,
        agent_id=agent_id,
        agent_name=agent_name,
        **kwargs
    )
