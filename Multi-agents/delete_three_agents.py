from letta import create_client 
client = create_client()


client.delete_agent(client.get_agent_id("Ducky"))
client.delete_agent(client.get_agent_id("Lulu"))
client.delete_agent(client.get_agent_id("Coco"))