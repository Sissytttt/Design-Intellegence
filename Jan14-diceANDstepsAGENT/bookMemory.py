from letta.schemas.block import Block 
from letta.schemas.memory import BasicBlockMemory


class OrgMemory(BasicBlockMemory): 

    def __init__(self, persona: str, org_block: Block): 
        persona_block = Block(label="persona", value=persona)
        super().__init__(blocks=[persona_block, org_block])