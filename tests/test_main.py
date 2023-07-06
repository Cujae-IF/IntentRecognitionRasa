import asyncio
import asynctest
from src.core.intent_recognition import RasaAgentLoader, RasaIntentRecognizer

class TestIntentRecognition(asynctest.TestCase):
    @classmethod
    def setUpClass(cls):
        asyncio.run(cls.asyncSetUpClass())

    @classmethod
    async def asyncSetUpClass(cls):
        cls.agent = await RasaAgentLoader.load_nlu()
        cls.recognizer = RasaIntentRecognizer(cls.agent)

    async def test_greet(self):
        response = await self.recognizer.parse_text("Hi")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "greet")

    async def test_goodbye(self):
        response = await self.recognizer.parse_text("Goodbye")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "goodbye")

    async def test_affirm(self):
        response = await self.recognizer.parse_text("Yes")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "affirm")

    async def test_deny(self):
        response = await self.recognizer.parse_text("No")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "deny")

    async def test_thank_you(self):
        response = await self.recognizer.parse_text("Thank you")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "thank_you")

    async def test_apology(self):
        response = await self.recognizer.parse_text("Sorry")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "apology")

    async def test_request_help(self):
        response = await self.recognizer.parse_text("Can you help me?")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "request_help")

    async def test_inform_problem(self):
        response = await self.recognizer.parse_text("There's a problem")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "inform_problem")

    async def test_ask_question(self):
        response = await self.recognizer.parse_text("Can you tell me something?")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "ask_question")

    async def test_make_suggestion(self):
        response = await self.recognizer.parse_text("Maybe we could try this")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "make_suggestion")

    async def test_give_compliment(self):
        response = await self.recognizer.parse_text("You're doing great")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "give_compliment")

    async def test_express_concern(self):
        response = await self.recognizer.parse_text("I'm worried about this")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "express_concern")

    async def test_express_happiness(self):
        response = await self.recognizer.parse_text("I'm so happy")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "express_happiness")

    async def test_express_sadness(self):
        response = await self.recognizer.parse_text("I'm feeling sad")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "express_sadness")

    async def test_express_surprise(self):
        response = await self.recognizer.parse_text("Wow, I wasn't expecting that")
        predicted_intent = response["Predicted intent"]
        self.assertEqual(predicted_intent, "express_surprise")

if __name__ == '__main__':
    asynctest.main()
