import asyncio
from pprint import pprint
from rasa.core.agent import load_agent, Agent

async def parse_text(agent: Agent, text):
    # Parse the text message
    response = await agent.parse_message(text)

    # Check if the response contains an intent
    if response and 'intent' in response:
        # Get the predicted intent
        intent = response['intent']['name']

        # Print the predicted intent
        print(f"Predicted intent: {intent}")
    else:
        # No intent was predicted
        print("No intent was predicted for this text.")

async def main():
    # Load the trained model
    agent = await load_agent("models/20230609-220103-parallel-opacity.tar.gz")

    # Define the text to predict the intent for
    text = "Hello"

    # Run intent recognition
    await parse_text(agent, text)

if __name__ == "__main__":
    asyncio.run(main())
