from src.router.core_routes import CoreRoutes
from fastapi import Query, Depends
from src.core.intent_recognition import IntentRecognizer


class IntentRecognition(CoreRoutes):
    def init_routes(self):
        @self.router.get("/intent_recognition", dependencies=[Depends(self.api_key_dependency)])
        async def predict_intent(
            text: str = Query(..., description="The text to predict the intent for"), 
            agent: IntentRecognizer = Depends()
        ):
            # Run intent recognition
            return await agent.parse_text(text)