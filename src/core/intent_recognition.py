# utils.py
import os
from abc import ABC, abstractmethod
from rasa.core.agent import load_agent, Agent


class IntentRecognizer(ABC):
    @abstractmethod
    async def parse_text(self, text: str):
        pass


class RasaIntentRecognizer(IntentRecognizer):
    def __init__(self, agent: Agent):
        self.agent = agent

    async def parse_text(self, text: str):
        # Parse the text message
        response = await self.agent.parse_message(text)

        # Check if the response contains an intent
        if response and 'intent' in response:
            # Get the predicted intent
            intent = response['intent']['name']

            # Return the predicted intent
            return {"Predicted intent": intent}
        else:
            # No intent was predicted
            return {"Predicted intent": "No intent was predicted for this text."}


class NluLoader(ABC):
    @staticmethod
    @abstractmethod
    async def load_nlu():
        pass


class RasaAgentLoader(NluLoader):
    async def load_nlu():
        # Get the list of all files in the models directory
        model_files = os.listdir("nlu/models")
        # Filter out files that are not .tar.gz files
        model_files = [f for f in model_files if f.endswith(".tar.gz")]
        # Sort the files by datetime in descending order
        model_files.sort(key=lambda f: f.split(".")[0], reverse=True)
        # Get the most recent model file
        most_recent_model_file = model_files[0]
        print(most_recent_model_file)
        # Load the most recent model
        return await load_agent(os.path.join("nlu/models", most_recent_model_file))
