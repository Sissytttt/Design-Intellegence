from letta.schemas.block import Block 
from letta.schemas.memory import BasicBlockMemory

book_description = "This is an interactive storytelling book designed for children to enjoy personalized, engaging stories."\
        + "It enables collective story-building with AI tools, featuring a variety of character agents, each with unique characteristics and roles, who collaboratively shape the story."\
        +"A narrator agent orchestrates the characters, facilitates their interactions, and weaves the narrative into a cohesive and captivating tale."

book_block = Block(label="storybook", value=book_description)

class BookMemory(BasicBlockMemory): 

    def __init__(self, persona: str, book_block: Block): 
        persona_block = Block(label="persona", value=persona)
        super().__init__(blocks=[persona_block, book_block])