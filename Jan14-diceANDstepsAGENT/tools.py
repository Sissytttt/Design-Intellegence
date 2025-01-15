

# define a function with a docstring
def roll_dice() -> str:
    """
    Rolls a 20-sided dice and returns the result as a string.
    
    Returns:
        str: The result of the dice roll in the format "You rolled a X", where X is a number between 1 and 20.
    """
    import random
    dice_roll = random.randint(1, 20)
    return f"You rolled a {dice_roll}"


def get_direction() -> str:
    """
    Returns a random direction from the four cardinal directions: East, South, West, or North.
    
    Returns:
        str: A random direction, one of "East", "South", "West", or "North".
    """
    import random
    directions = ["East", "South", "West", "North"]
    return random.choice(directions)


def create_roll_dice_tool(client):
    tool = client.create_tool(
        func=roll_dice,           
        name="roll_dice",            
    )
    print(f"Created tool: {tool.name}, ID: {tool.id}")

def create_get_direction_tool(client):
    tool = client.create_tool(
        func=get_direction,           
        name="get_direction",            
    )
    print(f"Created tool: {tool.name}, ID: {tool.id}")

# create_get_direction_tool()
get_direction_tool_id = "tool-7cd4af71-e31c-403e-af45-8b0a860731f3"
# create_roll_dice_tool()
roll_dice_tool_id = "tool-5be1794c-9e43-43fb-b82b-22e58fdb5ac6"
