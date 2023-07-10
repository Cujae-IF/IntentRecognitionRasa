from src.router.core_routes import CoreRoutes
from fastapi import Query, Depends
from src.core.training import *
from pydantic import BaseModel


class Intent(BaseModel):
    intent_name: str
    examples: List[str]


class TrainingRoutes(CoreRoutes):
    def init_routes(self):
        @self.router.post("/train_model_rasa", dependencies=[Depends(self.api_key_dependency)])
        async def train_model_rasa_endpoint(model_name: str = Query(..., description="Fixed model name to save in the directory")):
            await train_model_rasa(model_name)
            return {"message": "Model trained successfully"}

        @self.router.post("/create_intent", dependencies=[Depends(self.api_key_dependency)])
        async def create_intent_endpoint(intent: Intent):
            create_intent(intent.intent_name, intent.examples)
            return {"message": "Intent created successfully"}

        @self.router.put("/update_intent", dependencies=[Depends(self.api_key_dependency)])
        async def update_intent_endpoint(intent: Intent):
            update_intent(intent.intent_name, intent.examples)
            return {"message": "Intent updated successfully"}

        @self.router.delete("/delete_intent", dependencies=[Depends(self.api_key_dependency)])
        async def delete_intent_endpoint(intent_name: str = Query(..., description="The name of the intent to delete")):
            delete_intent(intent_name)
            return {"message": "Intent deleted successfully"}

        @self.router.delete("/delete_all_intents", dependencies=[Depends(self.api_key_dependency)])
        async def delete_all_intents_endpoint():
            delete_all_intents()
            return {"message": "All intents deleted successfully"}
