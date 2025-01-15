from letta import LLMConfig, EmbeddingConfig
from bookMemory import OrgMemory



def create_agent(client, org_block, name, persona, tool=None):
    agents = client.list_agents() 
    # tools = client.list_tools()
    # print(tools)

    client.set_default_embedding_config( 
    EmbeddingConfig(
        embedding_endpoint_type="openai",
        embedding_endpoint="https://api.openai.com/v1",
        embedding_model="text-embedding-ada-002",
        embedding_dim=1536,
        embedding_chunk_size=300
    )
)
    for agent in agents:
        if agent.name == name:
            client.delete_agent(client.get_agent_id(f"{name}"))
            print(f"delete {name}")
            print(f"recreating {name}")
    return client.create_agent(
        name=name,
        memory=OrgMemory(
            persona=persona,
            org_block=org_block
        ),
        llm_config=LLMConfig(
            model="gpt-4o-mini",
            model_endpoint_type="openai",
            model_endpoint="https://api.openai.com/v1",
            context_window=128000
        ),
        tool_ids=tool if tool else []
    )

