import asyncio, os
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
    # Get the list of all files in the models directory
    model_files = os.listdir("models")
    # Filter out files that are not .tar.gz files
    model_files = [f for f in model_files if f.endswith(".tar.gz")]
    # Sort the files by datetime in descending order
    model_files.sort(key=lambda f: f.split(".")[0], reverse=True)
    # Get the most recent model file
    most_recent_model_file = model_files[0]
    print(most_recent_model_file)
    # Load the most recent model
    agent = await load_agent(os.path.join("models", most_recent_model_file))

@app.get("/")
async def predict_intent(text: str = Query(..., description="The text to predict the intent for")):
    # Run intent recognition
    return await parse_text(agent, text)
