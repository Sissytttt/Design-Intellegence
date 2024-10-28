from letta import create_client 
client = create_client()

# Returns a list of `AgentState` objects
agents = client.list_agents() 
for agent in agents:
    print(agent.name,":", agent.id)