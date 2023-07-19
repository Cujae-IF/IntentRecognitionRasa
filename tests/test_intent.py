import asynctest, asyncio
from main import app
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from src.core.intent_recognition import RasaAgentLoader, RasaIntentRecognizer


client = TestClient(app)

class TestIntentRoutes(asynctest.TestCase):
    @classmethod
    def setUpClass(cls):
        asyncio.run(cls.asyncSetUpClass())

    @classmethod
    async def asyncSetUpClass(cls):
        cls.agent = await RasaAgentLoader.load_nlu()
        cls.recognizer = RasaIntentRecognizer(cls.agent)
        await app.router.startup()

    async def test_predict_intent_greet(self):
        # Call the predict_intent route
        response = client.get(
            "/api/v1/intents",
            params={"text": "Hi there"},
            headers={"X-API-Key": "test_key"},
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"intent": "greet"})
        pure_nlu_response = await self.recognizer.parse_text("Hi")
        self.assertEqual(response.json(), pure_nlu_response)
