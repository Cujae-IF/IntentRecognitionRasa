from fastapi import FastAPI, Depends
from src.router.v1.router import router as v1_router
from src.core.intent_recognition import RasaIntentRecognizer, RasaAgentLoader, IntentRecognizer

app = FastAPI()
app.include_router(v1_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    agent = await RasaAgentLoader.load_agent()
    intent_recognizer = RasaIntentRecognizer(agent)
    app.dependency_overrides[IntentRecognizer] = lambda: intent_recognizer