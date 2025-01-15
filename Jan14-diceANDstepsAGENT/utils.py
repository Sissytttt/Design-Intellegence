import json

def list_tools(tools): 
    for tool in tools:
        print(f"{tool.name}:  , id: {tool.id}")
        # print(tool.tool_type)
        # if tool.name == "get_step" or tool.name == "roll_dice":
        #     print(tool.source_code)



def format_response(response):
    # print(response)
    if hasattr(response, "dict"):
        response = response.dict()
    output = ""
    for message in response.get("messages", []):
        if message.get("message_type") == "reasoning_message":
            output += f"\n- Reasoning: {message.get('reasoning', 'No reasoning message replied')}"
        if message.get("message_type") == "tool_call_message":
            tool_call = message.get("tool_call", {})
            output += f"\nTOOL[{tool_call.get('name')}]:  "
            if tool_call["name"] == "send_message":
                arguments = tool_call.get("arguments", "{}")
                arguments_data = json.loads(arguments)
                output += f"  {arguments_data.get('message')}"
        if message.get("message_type") == "tool_return_message":
            tool_return = message.get("tool_return", "{}")
            tool_return_data = json.loads(tool_return)
            if tool_return_data.get('message') != "None":
                output += f"  {tool_return_data.get('message')}"
    return output
