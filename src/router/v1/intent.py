from src.router.core_routes import CoreRoutes
from fastapi import Query, Depends
from src.core.training import *
from src.core.intent_recognition import IntentRecognizer, RasaAgentLoader, RasaIntentRecognizer
from pydantic import BaseModel
from typing import Optional


class Intent(BaseModel):
    name: str | None = None
    examples: List[str]


class IntentRoutes(CoreRoutes):
    def init_routes(self):
        @self.router.get("/intents", dependencies=[Depends(self.api_key_dependency)])
        async def predict_intent(
            text: str = Query(..., description="The text to predict the intent for"), 
            model: str | None = None,
            agent: IntentRecognizer = Depends()
        ):
            if model:
                agent = RasaIntentRecognizer(await RasaAgentLoader.load_nlu(model))
            # Run intent recognition
            return await agent.parse_text(text)
        
        @self.router.post("/intents", dependencies=[Depends(self.api_key_dependency)])
        async def create_intent_endpoint(intent: Intent):
            create_intent(intent.name, intent.examples)
            return {"message": "Intent created successfully"}

        @self.router.put("/intents/{intent_name}", dependencies=[Depends(self.api_key_dependency)])
        async def update_intent_endpoint(intent_name: str, intent: Intent):
            update_intent(intent_name, intent.examples)
            return {"message": "Intent updated successfully"}

        @self.router.delete("/intents/{intent_name}", dependencies=[Depends(self.api_key_dependency)])
        async def delete_intent_endpoint(intent_name: str):
            delete_intent(intent_name)
            return {"message": "Intent deleted successfully"}

        @self.router.delete("/intents", dependencies=[Depends(self.api_key_dependency)])
        async def delete_all_intents_endpoint():
            delete_all_intents()
            return {"message": "All intents deleted successfully"}
        