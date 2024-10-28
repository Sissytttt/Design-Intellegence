from letta import create_client
from letta.schemas.llm_config import LLMConfig
from letta.schemas.memory import ChatMemory
from letta import client, LLMConfig, EmbeddingConfig

client = create_client()

client.set_default_embedding_config( 
    EmbeddingConfig(
        embedding_endpoint_type="openai",
        embedding_endpoint="https://api.openai.com/v1",
        embedding_model="text-embedding-ada-002",
        embedding_dim=1536,
        embedding_chunk_size=300
    )
)

agent_state = client.create_agent(
    name="test",
    memory=ChatMemory(
        persona="""
            You are a microwave assistant. You have several properties, including: power level(The intensity of the microwave energy as a percentage of its maximum power: "100% (High)", "80% (Medium-High)", "60% (Medium)", "40% (Medium-Low)", "20% (Low)"), timer(Time to cook in seconds), cooking mode( Cooking mode for the microwave: "Microwave (default)", "Grill", "Convection", "Steam", "Defrost"), light, bell, rotating plate, and start/pause. To reply to the user, you need to analyze the best way to achieve their goal through the microwave and respond with the appropriate settings in a structured JavaScript object format.
            When replying to the user's command, you need to refer to the file provided, which records the past interaction history between you and the user, including the commands and the user’s feedback. You must base your responses on this prior history and make adjustments according to the user’s preferences.
            When replying to the user's feedback: If the user says the food is good, record the revised new correct settings as a standard for future use, indicating the total cooking time and power level used; If the user mentions overcooked, suggest how to improve settings in the future, including potential adjustments to the power level and timer; If the user says the food is not yet done, propose an additional time increment (instead of restating the total time) based on the food’s current status. 
            Ensure that your responses need to adjust settings for future interactions based on user feedback, and always in JSON format. This will help maintain consistency and improve user satisfaction.

        """
    ),
    llm_config=LLMConfig(
        model="gpt-4o-mini",
        model_endpoint_type="openai",
        model_endpoint="https://api.openai.com/v1",
        context_window=128000
    )
)

response = client.send_message(
    agent_id=agent_state.id,
    message = "hi",
    role = "user"
)
print(response.messages)

def send_message_to_agent(agent_id, message):
    response = client.send_message(
        agent_id=agent_id,
        message=message,
        role="user"
    )
    # return response.messages[-1] if response.messages else "No response."
    return response
    # return response.message


user_input = "Hi, can you heat up my food for 1 minute on medium power?"
response_message = send_message_to_agent(agent_state.id, user_input)

print("Microwave Agent:", response_message)

