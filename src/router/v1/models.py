from src.router.core_routes import CoreRoutes
from fastapi import Query, Depends
from src.core.training import *
from pydantic import BaseModel

class Model(BaseModel):
    name: str

class ModelRoutes(CoreRoutes):
    def init_routes(self):
        @self.router.post("/models", dependencies=[Depends(self.api_key_dependency)])
        async def train_model_rasa_endpoint(model: Model):
            await train_model_rasa(model.name)
            return {"message": "Model trained successfully"}
