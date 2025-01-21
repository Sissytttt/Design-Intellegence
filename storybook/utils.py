import json

def list_tools(client): 
    tools = client.list_tools()
    for tool in tools:
        print(f"{tool.name}:  , id: {tool.id}")

def print_tool_sourcecode(client, tool_name):
    tools = client.list_tools()
    for tool in tools:
        if tool.name == tool_name:
            print(tool.source_code)



def format_response(response):
    # print(response)
    if hasattr(response, "dict"):
        response = response.dict()
    if type(response) == str:
        response = json.loads(response)
    output = ""
    tool_called = None
    for message in response.get("messages", []):
        if message.get("message_type") == "reasoning_message":
            output += f"\n- Reasoning: {message.get('reasoning', 'No reasoning message replied')}"
        if message.get("message_type") == "tool_call_message":
            tool_call = message.get("tool_call", {})
            tool_called = tool_call.get('name')
            if tool_call["name"] == "send_message":
                output += f"\n{tool_call.get('name')}:  "
                arguments = tool_call.get("arguments", "{}")
                arguments_data = json.loads(arguments)
                output += f"  {arguments_data.get('message')}"
            else:
                output += "\n"
                output += f"\nTOOL[{tool_call.get('name')}]:  "
        if message.get("message_type") == "tool_return_message":
            tool_return = message.get("tool_return", "{}")
            tool_return_data = json.loads(tool_return)
            if tool_return_data.get('message') != "None":
                if tool_called == None or tool_called == "send_message":
                    print(f"  tool_return_data.get('message') is {tool_return_data.get('message')}")
                    output += f"  {tool_return_data.get('message')}"
                else:
                    tool_return = tool_return_data.get('message')
                    output += format_response(tool_return)
                    output += "\n"
    return output
