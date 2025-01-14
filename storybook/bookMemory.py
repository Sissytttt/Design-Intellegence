from letta.schemas.block import Block 
from letta.schemas.memory import BasicBlockMemory

book_description = "The system is a Game system for user to navigate a map " \
+ "and is building AI tools to make it easier to make random navigation " \
+ "and deploy LLM agents."

org_block = Block(label="company", value=book_description )


class OrgMemory(BasicBlockMemory): 

    def __init__(self, persona: str, org_block: Block): 
        persona_block = Block(label="persona", value=persona)
        super().__init__(blocks=[persona_block, org_block])