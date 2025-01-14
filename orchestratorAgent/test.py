from letta import create_client
import json

client = create_client()

# Get agents 
ducky_agent_id = client.get_agent_id("Ducky")
lulu_agent_id = client.get_agent_id("Lulu")
coco_agent_id = client.get_agent_id("Coco")

ducky_agent = client.get_agent(ducky_agent_id)
lulu_agent = client.get_agent(lulu_agent_id)
coco_agent = client.get_agent(lulu_agent_id)

agents = {
    "Ducky": ducky_agent,
    "Lulu": lulu_agent,
    "Coco": coco_agent
}

# analyze the recipient
def find_recipient(message):
    for name in agents.keys():
        if message.startswith(name + ","):
            return name
    return None

# send a message and route the conversation
def route_message(sender_name, initial_message):
    current_message = initial_message
    current_sender = sender_name

    while True:
        sender_agent = agents[current_sender]

        response = client.user_message(sender_agent.id, message=current_message)

        reply = None
        for message in response.messages:
            if message.message_type == "tool_call_message" and message.tool_call.name == "send_message":
                # Extract reply message from the function call arguments
                arguments = message.tool_call.arguments
                arguments_dict = json.loads(arguments)
                reply = arguments_dict.get("message")
                break

        if not reply:
            print(f"{current_sender}: No valid reply found.")
            break

        print(f"{current_sender}: {reply}")

        recipient = find_recipient(reply)

        if not recipient:
            print("Conversation ended. No valid recipient found.")
            break

        # Update the current sender and message
        current_message = reply
        current_sender = recipient

# Start the conversation
print("Starting the conversation...")
route_message("Lulu", "Coco, how is it going?")