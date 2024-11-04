from letta import create_client 
client = create_client()

def print_agent(agent_name):
    agents = client.list_agents() 
    for agent in agents:
        if agent.name == agent_name:
            print(agent)
            return
    else:
        print("print", agent_name, "not find")

def get_agents():
    agents = client.list_agents() 
    for agent in agents:
        print("get", agent.name,":", agent.id)

def list_tools(agent_name):
    agents = client.list_agents() 
    for agent in agents:
        if agent.name == agent_name:
            print(agent.tools)
            return
    else:
        print("list tools", agent_name, "not find")


def get_mem(agent_name):
    agents = client.list_agents() 
    for agent in agents:
            # memory = client.get_recall_memory_summary(agent.id)
            # print(memory)
            # print("------------------------------------------------------")
            # print("Core Memory: ", client.get_core_memory(agent.id))
            # print(client.get_core_memory(agent.id).get_block("human"))
            # print("------------------------------------------------------")
            # memory = client.get_archival_memory(agent.id)
            # memory.compile()
            # memory.get_block('human')
            print("Archival Memory: ", client.get_archival_memory(agent.id))
            print("------------------------------------------------------")
            # print("archival_memory_summary", client.get_archival_memory_summary(agent.id))
            # print("------------------------------------------------------")
            # print("recall_memory_summary", client.get_recall_memory_summary(agent.id))
            
            return
    else:
        print("get mem", agent_name, "not find")


def get_system(agent_name):
    agents = client.list_agents() 
    for agent in agents:
        if agent.name == agent_name:
            print(agent.system)
            return
    else:
        print("get system", agent_name, "not find")

# def update_system(agent_name, systemInstruction):
#     agents = client.list_agents() 
#     for agent in agents:
#         if agent.name == agent_name:
#             agent.system = systemInstruction
#         return

# def update_system(agent_name, systemInstruction):
#     agents = client.list_agents() 
#     for agent in agents:
#         if agent.name == agent_name:
#             agent_to_find = agent
#             agent_to_find.system = systemInstruction
#             print(agent_to_find)


def test(agent_name):
    agents = client.list_agents() 
    for agent in agents:
        if agent.name == agent_name:
            atr = dir(agent.name)
            print(atr)
            print(agent.__getattribute__())


get_agents()
# list_tools("test")
# get_mem("Microwave")
# test("Microwave")

# get_system("test")
# new_systemInstruction = "you are a microwave, yeah!!"
# updated_agent = update_system("Microwave", new_systemInstruction)
# print_agent("test")
# print_agent("Microwave")