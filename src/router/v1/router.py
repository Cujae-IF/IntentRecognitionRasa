from fastapi import APIRouter
from fastapi.security import APIKeyHeader
from src.router.v1.intent_recognition import IntentRecognition


router = APIRouter()
security = APIKeyHeader(name="X-Secret-Key", auto_error=False)

IntentRecognition(router, security).init_routes()