from fastapi import APIRouter
from fastapi.security import APIKeyHeader
from src.router.v1.intent_recognition import IntentRecognition
from src.router.v1.training import TrainingRoutes


router = APIRouter()
security = APIKeyHeader(name="X-Secret-Key", auto_error=False)

IntentRecognition(router, security).init_routes()
TrainingRoutes(router, security).init_routes()
