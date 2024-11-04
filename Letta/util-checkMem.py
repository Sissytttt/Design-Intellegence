import requests

url = "https://app.letta.com/v1/agents/agent-2361a39c-4fd2-470b-9799-cf58fd8529ee/archival"

headers = {"Authorization": "Bearer "}

response = requests.request("GET", url, headers=headers)

print(response.text)