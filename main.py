import asyncio
from fastapi import FastAPI, Query
from rasa.core.agent import load_agent, Agent

app = FastAPI()

agent = None

async def parse_text(agent: Agent, text):
    # Parse the text message
    response = await agent.parse_message(text)

    # Check if the response contains an intent
    if response and 'intent' in response:
        # Get the predicted intent
        intent = response['intent']['name']

        # Return the predicted intent
        return {"Predicted intent": intent}
    else:
        # No intent was predicted
        return {"Predicted intent": "No intent was predicted for this text."}

@app.on_event("startup")
async def startup_event():
    global agent
    # Load the trained model
    agent = await load_agent("models/20230621-125102-quiet-phrase.tar.gz")

@app.get("/")
async def predict_intent(text: str = Query(..., description="The text to predict the intent for")):
    # Run intent recognition
    return await parse_text(agent, text)
