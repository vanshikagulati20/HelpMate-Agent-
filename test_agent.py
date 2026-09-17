from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

# Your Microsoft Foundry project endpoint
PROJECT_ENDPOINT = "https://sneha-agent-resource.services.ai.azure.com/api/projects/sneha-agent"

# Your existing Foundry agent
AGENT_NAME = "Sneha-agent"

# Authenticate using your Azure CLI login
credential = AzureCliCredential()

# Connect to your Foundry project
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential
)

# Connect to your existing agent
openai_client = project.get_openai_client(
    agent_name=AGENT_NAME
)

print("CampusIT Agent is ready!")
print("Type 'exit' to stop.\n")

# Store the previous response so the agent remembers the conversation
previous_response_id = None

while True:

    user_message = input("You: ")

    # Exit the chat
    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    # Continue the existing conversation
    if previous_response_id:
        response = openai_client.responses.create(
            input=user_message,
            previous_response_id=previous_response_id
        )
    else:
        # First message of the conversation
        response = openai_client.responses.create(
            input=user_message
        )

    # Save this response so the next message has context
    previous_response_id = response.id

    print("Agent:", response.output_text)
    print()