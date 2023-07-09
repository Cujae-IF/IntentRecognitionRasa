from src.router.core_routes import CoreRoutes
from fastapi import Query, Depends
from src.core.training import *

class TrainingRoutes(CoreRoutes):
    def init_routes(self):
        @self.router.post("/train_model_rasa", dependencies=[Depends(self.api_key_dependency)])
        async def train_model_rasa_endpoint(model_name: str = None):
            return await train_model_rasa(model_name)

        @self.router.post("/create_intent", dependencies=[Depends(self.api_key_dependency)])
        async def create_intent_endpoint(intent_name: str, examples: List[str]):
            create_intent(intent_name, examples)
            return {"message": "Intent created successfully"}

        @self.router.put("/update_intent", dependencies=[Depends(self.api_key_dependency)])
        async def update_intent_endpoint(intent_name: str, new_examples: List[str]):
            update_intent(intent_name, new_examples)
            return {"message": "Intent updated successfully"}

        @self.router.delete("/delete_intent", dependencies=[Depends(self.api_key_dependency)])
        async def delete_intent_endpoint(intent_name: str, domain_file: str, nlu_file: str):
            delete_intent(intent_name, domain_file, nlu_file)
            return {"message": "Intent deleted successfully"}

        @self.router.delete("/delete_all_intents", dependencies=[Depends(self.api_key_dependency)])
        async def delete_all_intents_endpoint(domain_file: str, nlu_file: str):
            delete_all_intents(domain_file, nlu_file)
            return {"message": "All intents deleted successfully"}
