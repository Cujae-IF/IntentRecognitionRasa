import asyncio
from fastapi import FastAPI, Body
from rasa.core.agent import load_agent, Agent

app = FastAPI()

async def parse_text(agent: Agent, text):
    # Parse the text message
    response = await agent.parse_message(text)

    # Check if the response contains an intent
    if response and 'intent' in response:
        # Get the predicted intent
        intent = response['intent']['name']
        return intent
    else:
        # No intent was predicted
        return "No intent was predicted for this text."

@app.on_event("startup")
async def startup_event():
    global agent
    # Load the trained model
    agent = await load_agent("models/20230609-220103-parallel-opacity.tar.gz")

@app.post("/intent")
async def get_intent(text: str = Body(..., media_type="text/plain")):
    # Run intent recognition
    intent = await parse_text(agent, text)
    return {"intent": intent}
