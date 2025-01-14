# agent name to interact with:
agent_name = "test"

from letta import create_client
import json
from letta.schemas.memory import ChatMemory
from letta import client, LLMConfig, EmbeddingConfig


def create_character_agent(name, persona_description):
    agents = client.list_agents() 
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

    return client.create_agent(
        name=name,
        memory=ChatMemory(
            human="",
            persona=persona_description
        ),
        llm_config=LLMConfig(
            model="gpt-4o-mini",
            model_endpoint_type="openai",
            model_endpoint="https://api.openai.com/v1",
            context_window=128000
        ),
    )


client = create_client()

# Get an agent by Name
create_character_agent(agent_name, "you are a helpful agent")

agent_state = client.get_agent(client.get_agent_id(agent_name))

# Start a streaming conversation
print("Start chatting with the agent! Type 'exit' to end the conversation.")

while True:
    # Get user input
    user_message = input("\n\nYou: ")
    
    # Exit condition
    if user_message.lower() in ["exit", "quit"]:
        print("Ending the conversation. Goodbye!")
        break

    # Interact with the agent
    response = client.user_message(agent_state.id, message=user_message)

    if len(response.messages) > 1:
        for i, message in enumerate(response.messages):
            class_name = type(message).__name__ 
            if class_name == "ReasoningMessage":
                print(f"\nReasoningMessage: {message.reasoning}")
            elif class_name == "ToolCallMessage":
                if message.tool_call.name == 'send_message':
                    arguments = message.tool_call.arguments
                    arguments_dict = json.loads(arguments)
                    print(f"\nSend_Message: {arguments_dict['message']}")
                else:
                    print(f"{message.tool_call.name}: {message.tool_call.arguments}")
            elif class_name == "ToolReturnMessage":
                    tool_return_dict = json.loads(message.tool_return)
                    print(f"\nFunctionReturn: {tool_return_dict['status']}, Status: {message.status}")
            else:
                print("UnknownClassType: ", message)
    else:
        print("Agent: No response from the agent.")


