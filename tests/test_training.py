from fastapi.testclient import TestClient
from main import app
from src.core.training import *
import asynctest
import os
import shutil

client = TestClient(app)

# TODO: Add a testcase where the trained model is used for intent recognition
class TestTrainingRoutes(asynctest.TestCase):
    def setUp(self):
        # Backup the original domain and NLU training data files
        shutil.copyfile(domain, f"{domain}.bak")
        shutil.copyfile(f"{training_files}nlu.yml", f"{training_files}nlu.yml.bak")

    def test_train_model_rasa_endpoint(self):
        # Train the model
        response = client.post("/api/v1/models", json={"name": "test_model"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Model trained successfully"})

        # Check if the model was created
        self.assertTrue(os.path.exists(f"{models}test_model.tar.gz"))

    def test_create_intent_endpoint(self):
        # Create the intent
        response = client.post("/api/v1/intents", json={"name": "test_intent", "examples": ["example1", "example2"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Intent created successfully"})

        # Load the domain file and check if the intent was added
        yaml = YAML(typ='safe')
        with open(domain, 'r') as f:
            domain_data = yaml.load(f)
        self.assertIn("test_intent", domain_data['intents'])

        # Load the NLU training data file and check if the examples were added
        with open(f'{training_files}nlu.yml', 'r') as f:
            nlu_data = f.read()
        self.assertIn("## intent:test_intent", nlu_data)
        self.assertIn("- example1", nlu_data)
        self.assertIn("- example2", nlu_data)

    def test_update_intent_endpoint(self):
        # Update the intent
        response = client.put("/api/v1/intents/test_intent", json={"examples": ["new_example1", "new_example2"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Intent updated successfully"})

        # Load the NLU training data file and check if the new examples were added
        with open(f'{training_files}nlu.yml', 'r') as f:
            nlu_data = f.read()
        self.assertIn("- new_example1", nlu_data)
        self.assertIn("- new_example2", nlu_data)

    def test_delete_intent_endpoint(self):
        # Delete the intent
        response = client.delete("/api/v1/intents/test_intent")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Intent deleted successfully"})

        # Load the domain file and check if the intent was removed
        yaml = YAML(typ='safe')
        with open(domain, 'r') as f:
            domain_data = yaml.load(f)
        self.assertNotIn("test_intent", domain_data['intents'])

    def test_delete_all_intents_endpoint(self):
        # Delete all intents
        response = client.delete("/api/v1/intents")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "All intents deleted successfully"})

        # Load the domain file and check if all intents were removed
        yaml = YAML(typ='safe')
        with open(domain, 'r') as f:
            domain_data = yaml.load(f)
        self.assertEqual(domain_data['intents'], [])

    def tearDown(self):
        # Delete the trained model
        if os.path.exists(f"{models}test_model.tar.gz"):
            shutil.rmtree(f"{models}test_model.tar.gz")

        # Restore the original domain and NLU training data files
        shutil.move(f"{domain}.bak", domain)
        shutil.move(f"{training_files}nlu.yml.bak", f"{training_files}nlu.yml")
