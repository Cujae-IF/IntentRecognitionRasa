from fastapi import APIRouter
from fastapi.security import APIKeyHeader
from src.router.v1.intent import IntentRoutes
from src.router.v1.models import ModelRoutes


router = APIRouter()
security = APIKeyHeader(name="X-Secret-Key", auto_error=False)

IntentRoutes(router, security).init_routes()
ModelRoutes(router, security).init_routes()
