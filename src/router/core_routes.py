from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from abc import ABC, abstractmethod


class CoreRoutes(ABC):
    router: APIRouter
    security: APIKeyHeader
    nextcloud_url: str

    def __init__(self, router: APIRouter, security: APIKeyHeader):
        self.router = router
        self.security = security

    def api_key_dependency(self):
        def authenticate(request: Request):
            api_key = request.headers.get(self.security.name)
            #TODO: move this key to an .env file
            if not api_key or api_key != "mysecretkey":
                raise HTTPException(status_code=401, detail="Unauthorized")
        return authenticate

    @abstractmethod
    def init_routes(self):
        pass